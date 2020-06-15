#!/usr/bin/env python3

import http.client
import json
import os
import sys
import re
import yaml


def parse_config_file():
    config = {}
    scriptbasename = __file__
    scriptbasename = os.path.basename(scriptbasename)
    scriptbasename = scriptbasename.replace('.py', '')
    config_file = os.path.join(os.path.dirname(
        __file__), '%s.yml' % scriptbasename)

    if os.path.isfile(config_file):
        with open(config_file) as f:
            try:
                config = yaml.safe_load(f.read())
            except Exception as exc:
                sys.exit("Error: parsing %s - %s" % (config_file, str(exc)))
    else:
        sys.exit("Error: config file does not exist - " + config_file)
    return config


def get_token_from_api(config):
    conn = http.client.HTTPSConnection("iam.cloud.ibm.com")
    payload = 'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=' + \
        config['ibm_cloud_api_key']
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'Cache-Control': 'no-cache'
    }

    try:
        conn.request("POST", "/identity/token", payload, headers)
        res = conn.getresponse().read()
        data = res.decode("utf-8")
        json_res = json.loads(data)
        return json_res['token_type'] + ' ' + json_res['access_token']
    except Exception as error:
        print(f"Error getting token. {error}")
        raise


def get_instances(config):
    conn = http.client.HTTPSConnection(
        config['ibm_cloud_region'] + ".iaas.cloud.ibm.com")
    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Authorization': config['token'],
        'cache-control': 'no-cache'
    }
    version = "2019-05-31"
    payload = ""
    try:
        instances = []
        page_url = "/v1/instances?generation=1&limit=1&version=" + version
        while True:
            conn.request("GET", page_url, payload, headers)
            res = conn.getresponse()
            data = res.read()
            page_data = json.loads(data.decode("utf-8"))
            instances = instances + page_data['instances']
            print(json.dumps(page_data, indent=2, sort_keys=True))
            if page_data.get('next'):
                page_url = page_data['next']['href']
            else:
                break

        print(json.dumps(instances, indent=2, sort_keys=True))
        return instances
    except Exception as error:
        print(f"Error fetching VPCs. {error}")
        raise


def build_inventory(instances):
    inventory = {}
    inventory['_meta'] = {}
    inventory['_meta']['hostvars'] = {}
    inventory['all'] = {}
    inventory['all']['hosts'] = []

    for d in instances:
        inventory['_meta']['hostvars'][d['name']] = {}
        inventory['_meta']['hostvars'][d['name']
                                       ]['ansible_host'] = d['primary_network_interface']['primary_ipv4_address']
        inventory['all']['hosts'].append(d['name'])

    return inventory


if len(sys.argv) == 2 and sys.argv[1] == '--list':
    config = parse_config_file()
    config['token'] = get_token_from_api(config)
    instances = get_instances(config)
    inventory = build_inventory(instances)
    print(json.dumps(inventory, indent=2, sort_keys=True))
elif len(sys.argv) == 3 and sys.argv[1] == '--host':
    print(json.dumps({'ansible_connection': 'ssh'}))
else:
    sys.stderr.write("Need an argument, either --list or --host <host>\n")

exit()
