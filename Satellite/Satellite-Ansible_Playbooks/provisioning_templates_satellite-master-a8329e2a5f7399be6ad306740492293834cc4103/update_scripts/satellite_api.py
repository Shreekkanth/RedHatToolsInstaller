#!/usr/bin/python
# Description: This script should be part of the
# templates git directory that would use the API scripts to push and modify
# kickstart templates in satellite using the Sat 6 api.
# jenkins user should have the .hammer/cli_config.yaml file in its
# home directory that would allow for sat6 authentication.
# Takes in account production branch and other dev branches
# When a non-production branch is changed, a sat6 api call is used to
# create a new file:  branchname_filename. This would allow the separation of
# the production templates with he Development ones.
# When changes are made to the production branch they WILL overwrite the
# production templates. Use with caution.
#
# Does not download or modify locked templates
import json
import sys
import yaml
import os
import sys
from optparse import OptionParser
from git import Repo

repo = Repo(".")
branch = repo.active_branch
SAT_6_DIR = "sat6"
NON_TEMPLATES = "update_scripts"
TEMPLATE_TYPES = ["finish", "iPXE", "kexec", "provision", "PXEGrub",
                  "PXELinux", "script", "user_data", "ZTP", "other"]
try:
    import requests
except ImportError:
    print "Please install the python-requests module."
    sys.exit(-1)

# try reading the information from the
# hammer cli .yaml file
hammer_file = os.path.expanduser('~/.hammer/cli_config.yaml')
try:
    f = open(hammer_file, 'r')
    data = yaml.load(f)
    f.close()
    USERNAME = data[':foreman'][':username']
    print "Acting as user %s \n" % USERNAME
    PASSWORD = data[':foreman'][':password']
    URL = data[':foreman'][':host']
    KATELLO_API = "%s/katello/api/" % URL
    SAT_API = "%s/api/v2/" % URL
    POST_HEADERS = {'content-type': 'application/json'}
    SSL_VERIFY = True
    ORG_NAME = data[':foreman'][':org_name']
    PRODUCTION_BRANCH = 'master'
except IOError, ioerror:
    print str(ioerror)
    print """ Please create a .hammer/cli_config.yaml
    file in your home directory with username/password/
    hostname/org_name variables"""
    sys.exit(-1)


def get_json(location):
    """
    Performs a GET using the passed URL location
    """
    r = requests.get(location, auth=(USERNAME, PASSWORD), verify=SSL_VERIFY)

    return r.json()


def post_json(location, json_data):
    """
    Performs a POST and passes the data to the URL location
    """
    result = requests.post(
        location,
        data=json_data,
        auth=(USERNAME, PASSWORD),
        verify=SSL_VERIFY,
        headers=POST_HEADERS)
    return result.json()


def put_json(location, json_data):
    """
    Performs a PUT and passes the data to the URL location
    """
    result = requests.put(
        location,
        data=json_data,
        auth=(USERNAME, PASSWORD),
        verify=SSL_VERIFY,
        headers=POST_HEADERS)
    return result.json()


def get_satellite_name(template_type, git_filename,
                       production_branch=PRODUCTION_BRANCH):
    """
    Gets a git filename from a satellite template name
    """
    prefix = ""
    satellite_name = ""
    if production_branch != branch.name:
        prefix = branch.name

    if (template_type != "other"):
        satellite_name = git_filename.replace("_", " ")
        if prefix != "":
            satellite_name = prefix + " " + satellite_name
    else:
        satellite_name = git_filename.replace(" ", "_")
        if prefix != "":
            satellite_name = prefix + "_" + satellite_name

    return satellite_name


def get_git_name(template_type,
                 satellite_filename, production_branch=PRODUCTION_BRANCH):
    """
    Gets the filename of a git file from a satellite template name
    """
    prefix = ""
    if production_branch != branch.name:
        if template_type != "other":
            prefix = branch.name + " "
        else:
            prefix = branch.name + "_"

    if prefix != "" and satellite_filename.startswith(prefix):
        git_filename = satellite_filename[len(prefix):]
    else:
        git_filename = satellite_filename

    git_filename = git_filename.replace(" ", "_")

    return git_filename


def get_config_template(template_type, template_name):
    """
    Gets the contents of the template from satellite
    """
    satellite_filename = get_satellite_name(template_type, template_name,
                                            PRODUCTION_BRANCH)
    config_templates = get_json(SAT_API +
                                'config_templates/' +
                                "?search=" + satellite_filename)['results']
    template_id = None
    for template in config_templates:
        if template['name'] == satellite_filename:
            template_id = template['id']

    if len(config_templates) == 0 or template_id is None:
        raise IOError
    else:
        current_template = get_json(SAT_API +
                                    'config_templates/' + str(template_id))
        return current_template


def get_template_kind_id(template_type):
    """
    Queries the Satellite 6 API on template type and returns ID
    """
    config_template_id = None
    if template_type != ("other" or "snippet" or None):
        template_types = get_json(SAT_API +
                                  'template_kinds/' +
                                  '?search=' +
                                  template_type)["results"]
        if len(template_types) != 1:
            return None
        else:
            return template_types[0]['id']


def diff_files(template_type, git_template_name):
    """
    Checks if the current git template of this branch is different in satellite
    returns True if it's different, False if it's the same
    """
    satellite_template = get_config_template(template_type, git_template_name)
    filepath = SAT_6_DIR + "/" + template_type + "/" + git_template_name
    fo = open(filepath, 'r')
    contents = fo.read()
    fo.close()
    difference = True
    if contents != satellite_template['template']:
        difference = True
    else:
        difference = False
    return difference


def update_config_templates(option, opt, value, parser,
                            prod_branch=PRODUCTION_BRANCH):
    """
    Updates  a file if it exists if not it creates it
    """
    for template_type in TEMPLATE_TYPES:
        for filename in os.listdir(SAT_6_DIR + "/" + template_type):
            try:
                template = get_config_template(template_type, filename)
                # update organizations
                if ORG_NAME not in template['organizations']:
                    template["organizations"].append(ORG_NAME)
                # update if different
                if template_type == 'other':
                    is_snippet = True
                else:
                    is_snippet = False
                files_are_different = diff_files(template_type, filename)
                filehandle = open(SAT_6_DIR + "/" +
                                  template_type + "/" + filename, 'r')
                contents = filehandle.read()
                filehandle.close()
                result = {}

                if files_are_different and not is_snippet:
                    j_out = json.dumps({"id": str(template['id']),
                                        "config_template": {
                                        "name": template['name'],
                                        "snippet": False,
                                        "audit_comment": "automatic script",
                                        "template": contents,
                                        "template_kind_id":
                                        get_template_kind_id(template_type),
                                        "organizations":
                                        template['organizations']
                                        }})

                    result = put_json(SAT_API + "/config_templates/" +
                                      str(template['id']), j_out)

                elif files_are_different and is_snippet:
                    j_out = json.dumps({"id": template['id'],
                                        "template": contents,
                                        "snippet": is_snippet,
                                        "name": template['name'],
                                        "organizations":
                                        template['organizations']
                                        })
                    result = put_json(SAT_API + "/config_templates/" +
                                      str(template['id']),
                                      j_out)
                if 'template' in result and result['template'] == contents:
                    print "SUCCESS"
                elif result != {}:
                    print "FAIL"
                    print json.dumps(result)
                    sys.exit(-1)
            except IOError, e:
                # create if not exists
                filehandle = open(SAT_6_DIR + "/" + template_type +
                                  "/" + filename)
                contents = filehandle.read()
                filehandle.close()
                satellite_name = get_satellite_name(template_type, filename)
                if template_type == "other":
                    is_snippet = True
                    post_json(SAT_API + "/config_templates/",
                              json.dumps({"name": satellite_name,
                                          "template": contents,
                                          "snippet": is_snippet,
                                          "organizations":
                                          template['organizations']
                                          }))
                else:
                    post_json(SAT_API + "/config_templates/",
                              json.dumps({"name": satellite_name,
                                          "template": contents,
                                          "template_kind_id":
                                          get_template_kind_id(template_type),
                                          "organizations":
                                          template['organizations']
                                          }))


def get_all_not_locked_config_templates(option, opt, value, parser):
    """
    Download into files all the templates that aren't in state "locked"
    on the satellite server. THis is a first time operation.
    If the files exist, it won't overwrite them
    """
    config_templates = get_json(SAT_API +
                                'config_templates/' + "?per_page=500")
    for template in config_templates['results']:
        config_template_info = get_json(SAT_API +
                                        'config_templates/' +
                                        str(template['id']))
        if not config_template_info["locked"]:

            directory = config_template_info["template_kind_name"]
            if directory is not None and not os.path.exists(SAT_6_DIR +
                                                            "/" + directory):
                os.makedirs(SAT_6_DIR + "/" + directory)
            elif directory is None and not os.path.exists(SAT_6_DIR +
                                                          "/" + "other"):
                directory = "other"
                os.makedirs(SAT_6_DIR + "/" + directory)
            elif directory is None:
                directory = "other"
            git_name = get_git_name(directory,
                                    config_template_info["name"],
                                    PRODUCTION_BRANCH)
            filepath = SAT_6_DIR + "/" + directory + "/" + git_name
            if not os.path.exists(filepath):
                template_file = file(filepath, "w")
                template_file.write(config_template_info["template"])
                template_file.close()


def parse_commandline():
    global options
    global args
    global parser
    usage = """
    usage: %prog --download|--pull
    This program is used to interract with the satellite API about provisioning
    templates
    """
    download_help = """
    This program is used to download the most relevant branch
    artifacts from satellite to your local git repository
    """
    push_help = """
    This option is used to upload templates from your local git
    repository to satellite
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--download",
                      action="callback",
                      callback=get_all_not_locked_config_templates)
    # help=download_help)
    parser.add_option("-p", "--push",
                      action="callback",
                      callback=update_config_templates)
    # help=push_help)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    (options, args) = parser.parse_args()


def main():
    """
    Templates need to be updated when a user changes them.
    depending on the git branch.
    """
    parse_commandline()


if __name__ == "__main__":
    main()
