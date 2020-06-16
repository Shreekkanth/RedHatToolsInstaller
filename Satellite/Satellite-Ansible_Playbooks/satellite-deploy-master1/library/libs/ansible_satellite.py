#!/usr/bin/python
from satapi.satapi.satapi import SatAPI
from satapi.config.config import Config
import json
import zipfile
import os
import time

API=SatAPI(Config.APILocation,
           Config.APIUser,
           Config.APIPassword
          )

class Locations:

    def __init__(self):
        pass
    
    def location_exists(self, location):
        ''' Returns 0 if location already exists, 1 otherwise '''
        result = None
        try:
            location_exists = json.dumps(API.getLocationByName(location))
            location_exists = json.loads(location_exists)
        except:
            location_exists = { 'name': None }

        if location_exists["name"] == location:
            result = 0
        else:
            result = 1
        return result

    def create_location(self, location):
        ''' Returns 0 if location already exists, 1 if has been created, 2 if error happened '''
        result = None
        location_exists = self.location_exists(location)
        if location_exists == 0:
            result = 0
        else:
            try:
                location_created = json.dumps(API.createLocation(location))
                location_created = json.loads(location_created)
            except:
                location_created = { 'name': None }
            if location_created["name"] == location:
                result = 1
            else:
                result = 2
        return result

class Organizations:

    def __init__(self):
        pass

    def organization_exists(self, organization):
        ''' Returns 0 if organization already exists, 1 otherwise '''
        result = None
        try:
            organization_exists = json.dumps(API.getOrganizationByName(organization))
            organization_exists = json.loads(organization_exists)
        except:
            organization_exists = { 'name': None }

        if organization_exists["name"] == organization:
            result = 0
        else:
            result = 1
        return result

    def create_organization(self, organization):
        ''' Returns 0 if organization already exists, 1 if has been created, 2 if error happened '''
        result = None
        organization_exists = self.organization_exists(organization)
        if organization_exists == 0:
            result = 0
        else:
            try:
                organization_created = json.dumps(API.createOrganization(organization))
                organization_created = json.loads(organization_created)
            except:
                organization_created = { 'name': None }
            if organization_created["name"] == organization:
                result = 1
            else:
                result = 2
        return result

class HostCollections:
  
    def __init__(self):
        pass

    def hostcollection_exists(self, hostcollection, organization):
        ''' Returns 0 if host collection already exists, 1 otherwise '''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                hostcollection_exists = json.dumps(API.getHostcollectionByName(hostcollection, organization_results))
                hostcollection_exists = json.loads(hostcollection_exists)['results'][0]
            except:
                hostcollection_exists = { 'name': None }
            if hostcollection_exists["name"] == hostcollection:
                result = 0
            else:
                result = 1
        else:
            result = 1
        return result

    def create_hostcollection(self, hostcollection, organization):
        ''' Returns 0 if host collection already exists, 1 if has been created, 2 if error happened '''
        result = None
        hostcollection_exists = self.hostcollection_exists(hostcollection, organization)
        if hostcollection_exists == 0:
            result = 0
        else:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                hostcollection_created = json.dumps(API.createHostcollection(hostcollection, organization_results))
                hostcollection_created = json.loads(hostcollection_created)
            except:
                hostcollection_created = { 'name': None }
            if hostcollection_created["name"] == hostcollection:
                result = 1
            else:
                result = 2
        return result
                
class HostGroups:
  
    def __init__(self):
        pass

    def hostgroup_exists(self, hostgroup):
        ''' Returns 0 if host group already exists, 1 otherwise '''
        result = None
        try:
            hostgroup_exists = json.dumps(API.getHostgroupByName(hostgroup))
            hostgroup_exists = json.loads(hostgroup_exists)
            hostgroup_name = hostgroup_exists["name"]
        except:
            hostgroup_name = None
        if hostgroup_name == hostgroup:
            result = 0
        else:
            result = 1
        return result

    def create_hostgroup(self, hostgroup):
        ''' Returns 0 if host group already exists, 1 if has been created, 2 if error happened '''
        result = None
        hostgroup_exists = self.hostgroup_exists(hostgroup)
        if hostgroup_exists == 0:
            result = 0
        else:
            try:
                hostgroup_created = json.dumps(API.createHostgroup(hostgroup))
                hostgroup_created = json.loads(hostgroup_created)
            except:
                hostgroup_created = { 'name': None }
            if hostgroup_created["name"] == hostgroup:
                result = 1
            else:
                result = 2
        return result

    def attach_location(self, hostgroup, location):
        ''' Returns 0 if location has been attached, 1 if error happened '''
        result = None
        hostgroup_exists = self.hostgroup_exists(hostgroup)
        if hostgroup_exists == 0:
            hostgroup_results = json.dumps(API.getHostgroupByName(hostgroup))
            hostgroup_results = json.loads(hostgroup_results) 
            locations = Locations()
            location_exists = locations.location_exists(location)
            if location_exists == 0:
                location_results = json.dumps(API.getLocationByName(location))
                location_results = json.loads(location_results)
                try:
                    hostgroup_attached = json.dumps(API.attachHostgroupToLocation(hostgroup_results, location_results))
                    hostgroup_attached = json.loads(hostgroup_attached)
                except:
                    hostgroup_attached = { 'name': None }
                if hostgroup_attached["name"] == hostgroup:
                    result = 0
                else:
                    result = 1
            else:
                result = 1
        else:
            result = 1
        return result

    def attach_organization(self, hostgroup, organization):
        ''' Returns 0 if organization has been attached, 1 if error happened '''
        result = None
        hostgroup_exists = self.hostgroup_exists(hostgroup)
        if hostgroup_exists == 0:
            hostgroup_results = json.dumps(API.getHostgroupByName(hostgroup))
            hostgroup_results = json.loads(hostgroup_results) 
            organizations = Organizations()
            organization_exists = organizations.organization_exists(organization)
            if organization_exists == 0:
                organization_results = json.dumps(API.getOrganizationByName(organization))
                organization_results = json.loads(organization_results)
                try:
                    hostgroup_attached = json.dumps(API.attachHostgroupToOrganization(hostgroup_results, organization_results))
                    hostgroup_attached = json.loads(hostgroup_attached)
                except:
                    hostgroup_attached = { 'name': None }
                if hostgroup_attached["name"] == hostgroup:
                    result = 0
                else:
                    result = 1
            else:
                result = 1
        else:
            result = 1
        return result

    def attach_content(self, hostgroup, contentview, lifecycle_env, organization):
        ''' Returns 0 if content has been attached, 1 if error happened '''
        result = None
        hostgroup_exists = self.hostgroup_exists(hostgroup)
        if hostgroup_exists == 0:
            hostgroup_results = json.dumps(API.getHostgroupByName(hostgroup))
            hostgroup_results = json.loads(hostgroup_results) 
            organizations = Organizations()
            organization_exists = organizations.organization_exists(organization)
            if organization_exists == 0:
                organization_results = json.dumps(API.getOrganizationByName(organization))
                organization_results = json.loads(organization_results)
                # Check if contentview and lfc_env exists --> contentview must be promoted to this environment, otherwise it will fail
                contentviews = ContentViews()
                contentview_exists = contentviews.contentview_exists(contentview, organization)
                lifecycle_envs = LifecycleEnvs()
                lfc_env_exists = lifecycle_envs.lifecycle_env_exists(lifecycle_env, organization)
                if contentview_exists == 0:
                    contentview_results = json.dumps(API.getContentViewByName(contentview, organization_results))
                    contentview_results = json.loads(contentview_results)
                else: 
                    contentview_results = {'id': None}
                if lfc_env_exists == 0:
                    lifecycle_env_results = json.dumps(API.getLifecycleEnvByName(lifecycle_env, organization_results))
                    lifecycle_env_results = json.loads(lifecycle_env_results)["results"][0]
                else:
                    lifecycle_env_results = {'id': None}
                try:
                    content_attached = json.dumps(API.setHostgroupContent(hostgroup_results, contentview_results, lifecycle_env_results))
                    content_attached = json.loads(content_attached)
                except:
                    content_attached = { 'name': None }
                if content_attached["name"] == hostgroup:
                    result = 0
                else:
                    result = 1
            else: 
                result = 1
        else:
            result = 1
        return result

    def attach_puppetenv(self,hostgroup, puppet_env):
        ''' Returns 0 if puppet env has been attached, 1 if error happened '''
        result = None
        hostgroup_exists = self.hostgroup_exists(hostgroup)
        if hostgroup_exists == 0:
            hostgroup_results = json.dumps(API.getHostgroupByName(hostgroup))
            hostgroup_results = json.loads(hostgroup_results) 
            # Check if puppet env exists (if not it will except)
            try:
                puppet_env_results = json.dumps(API.getPuppetEnvironmentByName(puppet_env))
                puppet_env_results = json.loads(puppet_env_results)
                try:
                    puppetenv_attached = json.dumps(API.setHostgroupPuppetEnvironment(hostgroup_results, puppet_env_results))
                    puppetenv_attached = json.loads(puppetenv_attached)
                except:
                    puppetenv_attached = {'name': None}
            except:
                result = 1 
            if puppetenv_attached["name"] == hostgroup:
                result = 0
            else: 
                result = 1
        else:
            result = 1
        return result

    def attach_puppetclass(self, hostgroup, puppetclasses):
        ''' Returns 0 if puppet class has been attached, 1 if error happened '''
        result = None
        classes_list = []
        hostgroup_exists = self.hostgroup_exists(hostgroup)
        if hostgroup_exists == 0:
            hostgroup_results = json.dumps(API.getHostgroupByName(hostgroup))
            hostgroup_results = json.loads(hostgroup_results)
            if puppetclasses != None:
                for puppetclass in puppetclasses.split(","):
                    try:
                        puppetclass_results = json.dumps(API.getPuppetClassByName(puppetclass.strip()))
                        puppetclass_results = json.loads(puppetclass_results)["results"]
                    except:
                        puppetclass_results = None
                    if puppetclass_results != None:
                        puppetclass_results = puppetclass_results[puppetclass.strip()][0]
                        classes_list.append(puppetclass_results["id"])
            try:
                puppetclass_attached = json.dumps(API.setHostgroupPuppetClassesIds(hostgroup_results, classes_list))
                puppetclass_attached = json.loads(puppetclass_attached)
            except:
                puppetclass_attached = {'name': None}
            if puppetclass_attached["name"] == hostgroup:
                result = 0
            else:
                result = 1
        else:
            result = 1
        return result


class LifecycleEnvs:

    def __init__(self):
        pass

    def lifecycle_env_exists(self, lifecycle_env, organization):
        ''' Returns 0 if lifecycle environment already exists, 1 if not exists, 2 if organization does not exists'''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                lifecycle_env_exists = json.dumps(API.getLifecycleEnvByName(lifecycle_env, organization_results))
                lifecycle_env_exists = json.loads(lifecycle_env_exists)['results'][0]
            except:
                lifecycle_env_exists = { 'name': None }
            if lifecycle_env_exists["name"] == lifecycle_env:
                result = 0
            else:
                result = 1
        else:
            result = 2
        return result

    def create_lifecycle_env(self, lifecycle_env, prior_lifecycle_env, organization):
        ''' Returns 0 if life cycle environment already exists, 1 if has been created, 2 if error happened '''
        result = None
        prior_lifecycle_env_exists = self.lifecycle_env_exists(prior_lifecycle_env, organization)
        if prior_lifecycle_env_exists == 0:
            lifecycle_env_exists = self.lifecycle_env_exists(lifecycle_env, organization)
            if lifecycle_env_exists == 0:
                result = 0
            else:
                organization_results = json.dumps(API.getOrganizationByName(organization))
                organization_results = json.loads(organization_results)
                # Get prior lifecycle environment id needed to create the new lce
                prior_lifecycle_env_results = json.dumps(API.getLifecycleEnvByName(prior_lifecycle_env, organization_results))
                prior_lifecycle_env_results = json.loads(prior_lifecycle_env_results)['results'][0]
                try:
                    lifecycle_env_created = json.dumps(API.createLifecycleEnv(lifecycle_env, organization_results, prior_lifecycle_env_results))
                    lifecycle_env_created = json.loads(lifecycle_env_created)
                except:
                    lifecycle_env_created = { 'name': None }
                if lifecycle_env_created["name"] == lifecycle_env:
                    result = 1
                else:
                    result = 2
        else:
            result = 2
        return result
   

class ContentViews:

    def __init__(self):
        pass

    def contentview_exists(self, contentview, organization):
        ''' Returns 0 if contentview already exists, 1 if not exists, 2 if organization does not exists'''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                contentview_exists = json.dumps(API.getContentViewByName(contentview, organization_results))
                contentview_exists = json.loads(contentview_exists)
            except:
                contentview_exists = { 'name': None }
            if contentview_exists["name"] == contentview:
                result = 0
            else:
                result = 1
        else:
            result = 2
        return result

    def create_contentview(self, contentview, organization, repositories=None):
        ''' Returns 0 if contentview already exists, 1 if has been created, 2 if error happened '''
        result = None
        repository_list = []
        contentview_exists = self.contentview_exists(contentview, organization)
        if contentview_exists == 0:
            result = 0
        else:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            # Get repo ids from repo list
            if repositories != None:
                for repo_name in repositories.split(","):
                    try:
                        repository_results = json.dumps(API.getRepositoryByName(organization_results, repo_name.strip()))
                        repository_results = json.loads(repository_results)
                    except:
                        repository_results = None
                    if repository_results != None:
                        if repository_results: # If repo is not enabled repository_results will be returned as boolean, and will fail when trying to append
                            repository_list.append(repository_results["id"])
            try:
                contentview_created = json.dumps(API.createContentView(contentview, organization_results["id"], repository_list))
                contentview_created = json.loads(contentview_created)
            except:
                contentview_created = { 'name': None }
            if contentview_created["name"] == contentview:
                result = 1
            else:
                result = 2
        return result

    def add_module(self, contentview, organization, module):
        ''' Returns 0 if module already exists, 1 if has been added, 2 if error happened '''
        result = None
        contentview_exists = self.contentview_exists(contentview, organization)
        if contentview_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            # Get content view modules
            contentview_results = json.dumps(API.getContentViewByName(contentview, organization_results))
            contentview_results = json.loads(contentview_results)
            contentview_modules = json.dumps(API.getContentViewPuppetModules(contentview_results))
            contentview_modules = json.loads(contentview_modules)
            # Check if module is already present in the contentview
            module_present = False
            for key in contentview_modules["results"]:
                if module == key["name"]:
                  module_present = True
                  break
            if module_present:
                result = 0     
            else:
                # Get module id
                try:
                    module_exists = False
                    module_results = json.dumps(API.searchModules(module))
                    module_results = json.loads(module_results)
                    for key in module_results["results"]:
                        if module == key["name"]:
                            module_exists = True
                            # get unique version id used to promote
                            module_data = { 'id': key["uuid"] }
                            break
                    if module_exists:
                        module_added = json.dumps(API.addModuleToContentView(module_data, contentview_results))
                        module_added = json.loads(module_added)
                        if module_added["name"] == module:
                            result = 1
                        else:
                            result = 2
                    else:
                        result = 2
                except: 
                    result = 2
        else:
            result = 2
        return result

    def publish_contentview(self, contentview, organization):
        ''' Returns 0 if contentview has been published, 1 if error happened '''
        result = None
        contentview_exists = self.contentview_exists(contentview, organization)
        if contentview_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                contentview_results = json.dumps(API.getContentViewByName(contentview, organization_results))
                contentview_results= json.loads(contentview_results)
                contentview_published = json.dumps(API.publishContentView(contentview_results))
                contentview_published = json.loads(contentview_published)
            except:
                contentview_published = { 'result': None, 'state': None }
            if contentview_published["result"] == "pending" and contentview_published["state"] == "planned":
                result = 0
            else:
                result = 1
        else:
            result = 1
        return result
        
    def promote_contentview(self, contentview, organization, lifecycle_environment, version="latest", lce_restrictions=False):
        ''' Return 0 if contentview has been promoted, 1 if error happened '''
        result = None
        contentview_exists = self.contentview_exists(contentview, organization)
        if contentview_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                contentview_results = json.dumps(API.getContentViewByName(contentview, organization_results))
                contentview_results = json.loads(contentview_results)
                version_exists = False
                if version.lower() == "latest":
                    # get latest cv version
                    latest_contentview_version = None
                    # order versions by version number reverse
                    contentview_results = sorted(contentview_results["versions"], key=lambda k: k['version'], reverse=True)
                    version_id = contentview_results[0]["id"]
                    if len(str(version_id)) > 0:
                        version_exists = True
                # check if cv version exists, if is latest it exists
                else:
                    for key in contentview_results["versions"]:
                        if version == key["version"]:
                            version_exists = True
                            # get unique version id used to promote
                            version_id = key["id"]
                            break
                if version_exists == True:
                    # check if lifecycle environment exists
                    lifecycle_environments = LifecycleEnvs()
                    lifecycle_exists = lifecycle_environments.lifecycle_env_exists(lifecycle_environment, organization)
                    if lifecycle_exists == 0:
                        lifecycle_env_results = json.dumps(API.getLifecycleEnvByName(lifecycle_environment, organization_results))
                        lifecycle_env_results = json.loads(lifecycle_env_results)['results'][0]
                        try:
                            contentview_promoted = json.dumps(API.promoteContentViewVersion(version_id, lifecycle_env_results, lce_restrictions))
                            contentview_promoted = json.loads(contentview_promoted)
                        except:
                            contentview_promoted = {'result': None, 'state': None}
                        if contentview_promoted["result"] == "pending" and contentview_promoted["state"] == "planned":
                            result = 0
                        else:
                            result = 1
                    else:
                        result = 1
                else:
                    result = 1
            except:
                result = 1
        else:
            result = 1
        return result

class SubscriptionManifest:

    def __init__(self):
        pass

    def subscription_manifest_exists(self, organization):
        ''' Returns 0 if a manifest file has been already uploaded, 1 if not, 2 if error happened '''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                manifest_results = json.dumps(API.getSubscriptionManifestHistory(organization_results))
                manifest_results = json.loads(manifest_results)
                manifest_exists = False
                for key in manifest_results:
                    if key["status"] == "SUCCESS":
                        manifest_exists = True
                        break
                if manifest_exists == True:
                    result = 0
                else:
                    result = 1 
            except:
                result = 2
        else:
            result = 2
        return result

    def delete_subscription_manifest(self, organization):
        ''' Returns 0 if a manifest file has been deleted, 1 if error happened '''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                manifest_deleted = json.dumps(API.deleteSubscriptionManifest(organization_results))
                manifest_deleted = json.loads(manifest_deleted)
            except:
                manifest_deleted = { 'result': None, 'state': None }
            if manifest_deleted["state"] == "planned" and manifest_deleted["result"] == "pending":
                result = 0
            else:
                result = 1
        else:
            result = 1
        return result


    def upload_subscription_manifest(self, organization, manifest_zip, force=False):
        ''' Returns 0 if manifest file has been uploaded, 1 if a subscription manifest already exists, 2 if error happened '''
        result = None
        # Check if manifest file exists
        try:
            is_zip = zipfile.is_zipfile(manifest_zip)
            if is_zip:
                subscription_manifest_exists = self.subscription_manifest_exists(organization)
                if subscription_manifest_exists == 0 and force == False:
                    # Manifest is already installed or was installed at some point and won't be overwrited
                    result = 1
                elif subscription_manifest_exists == 0 and force == True:
                    # Manifest is already installed or was installed at some point but will be overwrited
                    subscription_manifest_deleted = self.delete_subscription_manifest(organization)
                    if subscription_manifest_deleted == 0:
                        time.sleep(15) # Deletion task must complete before continuing
                        organization_results = json.dumps(API.getOrganizationByName(organization))
                        organization_results = json.loads(organization_results) 
                        try:
                            manifest_uploaded = json.dumps(API.uploadSubscriptionManifest(organization_results, manifest_zip))
                            manifest_uploaded = json.loads(manifest_uploaded)
                        except:
                            manifest_uploaded = { 'result': None, 'state': None }  
                        if manifest_uploaded["state"] == "planned" and manifest_uploaded["result"] == "pending":
                            result = 0
                        else:
                            result = 2
                    else:
                        result = 2
                elif subscription_manifest_exists == 1:
                    # Manifest doesn't exists and will be uploaded
                    organization_results = json.dumps(API.getOrganizationByName(organization))
                    organization_results = json.loads(organization_results)
                    try:
                        manifest_uploaded = json.dumps(API.uploadSubscriptionManifest(organization_results, manifest_zip))
                        manifest_uploaded = json.loads(manifest_uploaded)
                    except:
                        manifest_uploaded = { 'result': None, 'state': None }
                    if manifest_uploaded["state"] == "planned" and manifest_uploaded["result"] == "pending":
                        result = 0
                    else:
                        result = 2
                else:
                    result = 2
            else:
                result = 2
        except:
            result = 2
        return result

class Repositories:

    def __init__(self):
        pass

    def create_product(self, organization, product_name):
        ''' Returns 0 if repo already exists, 1 if has been created, 2 if error happened '''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                product_exists = json.dumps(API.getProductByName(product_name, organization_results))
                product_exists = json.loads(product_exists)
                product_id = product_exists["results"][0]["id"]
            except:
                product_exists = False
            if product_exists:
                result = 0
            else:
                try:
                    product_created = json.dumps(API.createProduct(product_name, organization_results))
                    product_created = json.loads(product_created)
                except:
                    product_created = { 'name': None }
                if product_created["name"] == product_name:
                    result = 1
                else:
                    result = 2
        else: 
            result = 2
        return result

    def create_repo(self, organization, product_name, repo_name, content_type):
        ''' Returns 0 if repo already exists, 1 if has been created, 2 if error happened '''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                product_exists = json.dumps(API.getProductByName(product_name, organization_results))
                product_exists = json.loads(product_exists)
                product_id = product_exists["results"][0]["id"]
                try:
                    repository_exists = json.dumps(API.getRepositorySetByName(product_id, repo_name))
                    repository_exists = json.loads(repository_exists)
                    repository_id = repository_exists["results"][0]["id"]
                except:
                    repository_exists = False
            except:
                product_exists = False
            if product_exists and repository_exists:
                result = 0
            elif product_exists and repository_exists == False:
                try:
                    repository_created = json.dumps(API.createRepository(repo_name, product_id, content_type))
                    repository_created = json.loads(repository_created)  
                except:
                    repository_created = { 'name': None }
                if repository_created["name"] == repo_name:
                    result = 1
                else:
                    result = 2
            else:
                result = 2
        else:
            result = 2
        return result

    def manage_repo(self, organization, product_name, repo_name, basearch, releasever, action):
        ''' Returns 0 if action has succeed, 1 if no action needed, 2 if error happened '''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                product_exists = json.dumps(API.getProductByName(product_name, organization_results))
                product_exists = json.loads(product_exists)
                product_id = product_exists["results"][0]["id"]
                try:
                    repository_exists = json.dumps(API.getRepositorySetByName(product_id, repo_name))
                    repository_exists = json.loads(repository_exists)
                    repository_id = repository_exists["results"][0]["id"]
                except:
                    repository_exists = False
            except:
                product_exists = False
            if product_exists and repository_exists:
                # Check if repo is already enabled
                repo_already_enabled = False
                # Get all repos enabled in the organization
                repositories_enabled = json.dumps(API.getRepositories(organization_results))
                repositories_enabled = json.loads(repositories_enabled)
                # Get the repo details for the product and repo name
                repository_set = json.dumps(API.getRepositorySetByName(product_id,repo_name))
                repository_set = json.loads(repository_set)
                # repo_name an repo_product_name slightly differs: example Red Hat Satellite Tools 6.2 (for RHEL 7 Server) (RPMs) vs. Red Hat Satellite Tools 6.2 for RHEL 7 Server RPMs x86_64
                if len(repository_set["results"][0]["repositories"]) > 0:
                    repo_product_name = repository_set["results"][0]["repositories"][0]["name"]
                else:
                    repo_product_name = None
                for key in repositories_enabled["results"]:
                    if repo_product_name == key["name"]:
                        repo_already_enabled = True
                        break
                if action.lower() == "enable":
                    if repo_already_enabled:
                        result = 1 
                    else:
                        try:
                            repo_result = json.dumps(API.enableRepositorySet(product_id, repository_id, basearch, releasever))
                            repo_result = json.loads(repo_result)
                        except:
                            repo_result = {'result': None}
                elif action.lower() == "disable":
                    if repo_already_enabled:
                        try:
                             repo_result = json.dumps(API.disableRepositorySet(product_id, repository_id, basearch, releasever))
                             repo_result = json.loads(repo_result)
                        except:
                             repo_result = {'result': None}
                    else:
                        result = 1
                else:
                    repo_result = {'result': None}
                if result != 1:
                    if repo_result["result"] == "success":
                        result = 0
                    else:
                        result = 2
            else:
                result = 2
        else:
            result = 2
        return result

    def synchronize_repo(self, organization, repo_name):
        ''' Returns 0 if action has succeed, 1 otherwise '''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                repository_results = json.dumps(API.getRepositoryByName(organization_results, repo_name))
                repository_results = json.loads(repository_results)
                repository_id = repository_results["id"]
                try:
                    repository_sync = json.dumps(API.syncRepository(repository_id))
                    repository_sync = json.loads(repository_sync)
                    if repository_sync["state"] == "planned" and repository_sync["result"] == "pending":
                        result = 0
                    else: 
                        result = 1
                except:
                    result = 1
            except:
                result = 1
        else:
            result = 1
        return result

    def upload_content(self, organization, content_file, repo_name):
        ''' Returns 0 if content file has been uploaded, 1 if error happened '''
        result = None
        # Check if file exists
        try:
            is_file = os.path.isfile(content_file)
            if is_file:
                organizations = Organizations()
                organization_exists = organizations.organization_exists(organization)
                if organization_exists == 0:
                    organization_results = json.dumps(API.getOrganizationByName(organization))
                    organization_results = json.loads(organization_results)
                    try:
                        repository_results = json.dumps(API.getRepositoryByName(organization_results, repo_name))
                        repository_results = json.loads(repository_results)
                        repository_id = repository_results["id"]
                        # It is not possible to check if file already exists in the repo because the filename and the name once uploaded are not the same
                        try:
                            file_uploaded = json.dumps(API.uploadContentToRepository(content_file, repository_id))
                            file_uploaded = json.loads(file_uploaded)
                        except:
                            file_uploaded = { 'status': None }
                        if file_uploaded["status"] == "success":
                            result = 0
                        else:
                            result = 1
                    except:
                        result = 1
                else:
                    result = 1
            else:
                result = 1
        except:
            result = 1
        return result


class ActivationKeys:

    def __init__(self):
        pass

    def activationkey_exists(self, activation_key, organization):
        ''' Returns 0 if contentview already exists, 1 if not exists, 2 if organization does not exists'''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                activation_key_exists = json.dumps(API.getActivationKeyByName(activation_key, organization_results))
                activation_key_exists = json.loads(activation_key_exists)["results"][0]
            except:
                activation_key_exists = { 'name': None }
            if activation_key_exists["name"] == activation_key:
                result = 0
            else:
                result = 1
        else:
            result = 2
        return result

    def create_activationkey(self, activation_key, contentview, organization):
        ''' Returns 0 if contentview already exists, 1 if has been created, 2 if error happened '''
        result = None
        activation_key_exists = self.activationkey_exists(activation_key, organization)
        if activation_key_exists == 0:
            result = 0
        else:
            contentviews = ContentViews()
            contentview_exists = contentviews.contentview_exists(contentview, organization)
            if contentview_exists == 0:
                organization_results = json.dumps(API.getOrganizationByName(organization))
                organization_results = json.loads(organization_results)
                contentview_results = json.dumps(API.getContentViewByName(contentview, organization_results))
                contentview_results = json.loads(contentview_results)
                # get current cv environment id (it assummes that is are consecutive from earlier stages to later stages)
                environment_results = sorted(contentview_results["environments"], key=lambda k: k['id'], reverse=True)
                environment_results = environment_results[0]
                try:
                    activation_key_created = json.dumps(API.createActivationKey(activation_key, organization_results, environment_results, contentview_results))
                    activation_key_created = json.loads(activation_key_created)
                except:
                    activation_key_created = { 'name': None }
                if activation_key_created["name"] == activation_key:
                    result = 1
                else:
                    result = 2
            else:
                result = 2
        return result

    def add_subscription(self, activation_key, subscription_name, organization):
        ''' Returns 0 if subscription has been assigned, 1 if it is already assigned, 2 if error happened '''
        result = None
        activation_key_exists = self.activationkey_exists(activation_key, organization)
        if activation_key_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                subscription_results = json.dumps(API.searchSubscriptions(organization_results, subscription_name, 99))
                subscription_results = json.loads(subscription_results)
                subscription_id = None
                for key in subscription_results["results"]:
                    if key["name"] == subscription_name:
                        subscription_id = key["id"]
                        break
                if len(str(subscription_id)) > 0:
                    activation_key_results = json.dumps(API.getActivationKeyByName(activation_key, organization_results))
                    activation_key_results = json.loads(activation_key_results)["results"][0]
                    subscriptions = [{ 'id': subscription_id, 'quantity': 1 }]
                    try:
                        # Check if subscription is already assigned in the activation key
                        existing_subscriptions = json.dumps(API.getSubscriptionsByAK(activation_key_results["id"]))
                        existing_subscriptions = json.loads(existing_subscriptions)
                        version_exists = False
                        for key in existing_subscriptions["results"]:
                            if subscription_id == key["id"]:
                                version_exists = True
                                break

                        if version_exists:
                            result = 1
                        else:
                            try:
                                subscription_added = json.dumps(API.setActivationKeySubscriptions(activation_key_results,subscriptions))
                                subscription_added = json.loads(subscription_added)
                                if subscription_added["results"][0]["id"] == subscription_id:
                                    result = 0
                                else:
                                    result = 2
                            except:
                                result = 2
                    except:
                        result = 2
                else:
                    result = 2
            except: 
                result = 2
        else:
            result = 2
        return result
        
    def add_hostcollection(self, activation_key, hostcollection, organization):
        ''' Returns 0 if hostcollection has been assigned, 1 otherwise '''
        result = None 
        activation_key_exists = self.activationkey_exists(activation_key, organization)
        if activation_key_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                # Check if hostcollection exists
                hostcollections = HostCollections()
                hostcollection_exists = hostcollections.hostcollection_exists(hostcollection, organization)
                if hostcollection_exists == 0:
                    # Get hostcollection id
                    hostcollection_results = json.dumps(API.getHostcollectionByName(hostcollection, organization_results))
                    hostcollection_results = json.loads(hostcollection_results)['results'][0] 
                    hostcollections = [ hostcollection_results["id"] ]
                    # Get activation key id
                    activationkey_results = json.dumps(API.getActivationKeyByName(activation_key, organization_results))
                    activationkey_results = json.loads(activationkey_results)["results"][0]
                    try:
                        hostcollection_added = json.dumps(API.setActivationKeyHostCollections(activationkey_results, hostcollections))
                        hostcollection_added = json.loads(hostcollection_added)
                        if hostcollection_added["name"] == activation_key:
                            result = 0
                        else:
                            result = 1
                    except:
                        result = 1
                else:
                    result = 1 
            except:
               result = 1
        else:
            result = 1
        return result        

    def content_override(self, activation_key, content_name, status, organization):
        ''' Returns 0 if content has been override, 1 otherwise '''
        result = None
        activation_key_exists = self.activationkey_exists(activation_key, organization)
        if activation_key_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            # Get activation key id
            activationkey_results = json.dumps(API.getActivationKeyByName(activation_key, organization_results))
            activationkey_results = json.loads(activationkey_results)["results"][0]
            if status.lower() == "enable" or status.lower() == "disable" or status.lower() == "default":
                if status.lower() == "enable":
                    status = 1
                elif status.lower() == "disable":
                    status = 0
                else: 
                    status = "default"
                try:
                    content_overrided = json.dumps(API.overrideActivationKeyProduct(activationkey_results, content_name, status))
                    content_overrided = json.loads(content_overrided)
                    if status == 1 or status == 0:
                        result = 1
                        for key in content_overrided["content_overrides"]:
                            if key["contentLabel"] == content_name and int(key["value"]) == status:
                                 result = 0
                                 break
                    else:
                        if content_overrided["name"] == activation_key:
                            result = 0
                        else:
                            result = 1
                except:
                    result = 1
            else:
                result = 1 
        else:
            result = 1
        return result
 
class Settings:

    def __init__(self):
        pass

    def update_setting(self, setting_name, setting_value):
        ''' Returns 0 if setting has been updated, 1 otherwise '''
        result = None
        try:
            setting_results = json.dumps(API.getSettingByName(setting_name))
            setting_results = json.loads(setting_results)['results'][0]
        except:
            setting_results = { 'name': None }
        if setting_results['name'] == setting_name:
            try:
                setting_updated = json.dumps(API.updateSetting(setting_results['id'], setting_value))
                setting_updated = json.loads(setting_updated)
                if setting_updated['name'] == setting_name and setting_updated['value'] == setting_value:
                    result = 0
                else:
                    result = 1
            except:
                result = 1
        else:
           result = 1
        return result

    def ldap_auth(self, name, ldap_host, ldap_port, ldap_account, account_password, base_dn, attr_login,
                  attr_name, attr_lastname, attr_mail, attr_photo, auto_register, group_sync, tls, 
                  group_base, server_type, ldap_filter, locations, organizations):
        ''' Returns 0 if auth has been setup, 1 if already exists, 2 otherwise '''
        result = None
        ldap_auth_exists = json.dumps(API.getLdapAuthSources())
        ldap_auth_exists = json.loads(ldap_auth_exists)['results']
        ldap_already_created = False
        for ldap_auth in ldap_auth_exists:
            ldap_auth_host = ldap_auth['host']
            ldap_server_type = ldap_auth['server_type']
            if ldap_auth_host == ldap_host and ldap_server_type == server_type:
                ldap_already_created = True
                break
        if ldap_already_created:
            result = 1
        else:
            organization_list = []
            for organization in organizations.split(","):
                try:
                    organization_exists = json.dumps(API.getOrganizationByName(organization.strip()))
                    organization_exists = json.loads(organization_exists)
                    organization_id = organization_exists["id"]
                except:
                    organization_exists = False
                if organization_exists != False:
                    organization_list.append(organization_id)
            location_list = []
            for location in locations.split(","):        
                try:
                    location_exists = json.dumps(API.getLocationByName(location.strip()))
                    location_exists = json.loads(location_exists)
                    location_id = location_exists["id"]
                except:
                    location_exists = False
                if location_exists != False:
                    location_list.append(location_id) 
            try:
                ldap_created = json.dumps(API.createLdapAuthSource(name, ldap_host, ldap_port, ldap_account, base_dn, account_password, attr_login,
                                                                   attr_name, attr_lastname, attr_mail, attr_photo, auto_register, group_sync, tls,
                                                                   group_base, server_type, ldap_filter, location_list, organization_list))
                ldap_created = json.loads(ldap_created)
                if ldap_created['host'] == ldap_host:
                    result = 0
                else:
                    result = 2 
            except:
                result = 2            
        return result      

class SyncPlans:
   
    def __init__(self):
        pass

    def syncplan_exists(self, sync_plan_name, organization):
        ''' Returns 0 if sync plan already exists, 1 if not exists, 2 if organization does not exists'''
        result = None
        organizations = Organizations()
        organization_exists = organizations.organization_exists(organization)
        if organization_exists == 0:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            try:
                sync_plan_exists = json.dumps(API.getSyncPlanByName(sync_plan_name, organization_results))
                sync_plan_exists = json.loads(sync_plan_exists)['results'][0]
            except:
                sync_plan_exists = { 'name': None }
            if sync_plan_exists['name'] == sync_plan_name:
                result = 0
            else:
                result = 1
        else:
            result = 2
        return result

    def create_syncplan(self, sync_plan_name, organization, interval, sync_date, description=None, products=None, enabled=False):
        ''' Returns 0 if sync plan already exists, 1 if has been created, 2 if error happened '''
        result = None
        product_list = []
        syncplan_exists = self.syncplan_exists(sync_plan_name, organization)
        if syncplan_exists == 0:
            result = 0
        else:
            organization_results = json.dumps(API.getOrganizationByName(organization))
            organization_results = json.loads(organization_results)
            # Get product ids
            if products != None:
                for product_name in products.split(","):
                    try:
                        product_exists = json.dumps(API.getProductByName(product_name.strip(), organization_results))
                        product_exists = json.loads(product_exists)
                        product_id = product_exists["results"][0]["id"]
                    except:
                        product_exists = False
                    if product_exists != False:
                        product_list.append(product_id)
            try:
                # Create content view and then add products
                syncplan_created = json.dumps(API.createSyncPlan(sync_plan_name, organization_results, interval, sync_date , description, enabled))
                syncplan_created = json.loads(syncplan_created)
                # Add products
                if len(product_list) > 0:
                    try:
                        product_added = json.dumps(API.addProductToSyncPlan(organization_results, syncplan_created, product_list))
                        product_added = json.loads(product_added)
                    except:
                        product_added = None
            except:
                syncplan_created = { 'name': None }
            if syncplan_created["name"] == sync_plan_name:
                result = 1
            else:
                result = 2
        return result

class Capsule:
  
    def __init__(self):
        pass

    def capsule_exists(self, capsule):
        ''' Returns 0 if capsule exists and is a pulp node, 1 capsule exists but is not a pulp node, 2 capsule does not exists '''
        result = None
        try:
            capsule_exists = json.dumps(API.getCapsuleByName(capsule))
            capsule_exists = json.loads(capsule_exists)
            capsule_name = capsule_exists["name"]
        except:
            capsule_name = None
        if capsule_name == capsule:
            if capsule_exists["features"][0]["name"] != "Pulp Node":
                result = 1
            else:
                result = 0
        else:
            result = 2
        return result

    def set_locations(self, capsule, capsule_locations):
        ''' Return 0 if location has been assigned, 1 if error happened '''
        result = None
        location_list = []
        capsule_exists = self.capsule_exists(capsule)
        if capsule_exists == 0 or capsule_exists == 1:
            capsule_results = json.dumps(API.getCapsuleByName(capsule))
            capsule_results = json.loads(capsule_results)
            locations = Locations()
            for location in capsule_locations.split(","):
                try:
                    location_exists = json.dumps(API.getLocationByName(location.strip()))
                    location_exists = json.loads(location_exists)
                    location_id = location_exists["id"]
                except:
                    location_exists = False
                if location_exists != False:
                    location_list.append(location_id)
            if len(location_list) > 0:
                try:
                    capsule_locations_results = json.dumps(API.setCapsuleLocations(capsule_results["id"], location_list))
                    capsule_locations_results = json.loads(capsule_locations_results)
                    if len(location_list) == len(capsule_locations_results["locations"]):
                        result = 0
                    else:
                        result = 1
                except:
                    result = 1
            else:
                # no valid locations were processed
                result = 1
        else:
            result = 1
        return result 

    def set_organizations(self, capsule, capsule_organizations):
        ''' Return 0 if organization has been assigned, 1 if error happened '''
        result = None
        organization_list = []
        capsule_exists = self.capsule_exists(capsule)
        if capsule_exists == 0 or capsule_exists == 1:
            capsule_results = json.dumps(API.getCapsuleByName(capsule))
            capsule_results = json.loads(capsule_results)
            organizations = Organizations()
            for organization in capsule_organizations.split(","):
                try:
                    organization_exists = json.dumps(API.getOrganizationByName(organization.strip()))
                    organization_exists = json.loads(organization_exists)
                    organization_id = organization_exists["id"]
                except:
                    organization_exists = False
                if organization_exists != False:
                    organization_list.append(organization_id)
            if len(organization_list) > 0:
                try:
                    capsule_organizations_results = json.dumps(API.setCapsuleOrganizations(capsule_results["id"], organization_list))
                    capsule_organizations_results = json.loads(capsule_organizations_results)
                    if len(organization_list) == len(capsule_organizations_results["organizations"]):
                        result = 0
                    else:
                        result = 1
                except:
                    result = 1
            else:
                # no valid locations were processed
                result = 1
        else:
            result = 1
        return result 

    def set_lifecycle_env(self, capsule, organization, lifecycle_environment):
        ''' Return 0 if env is already set, 1 if env is set, 2 if capsule is not a pulp node, 3 if error happened '''
        result = None
        capsule_exists = self.capsule_exists(capsule)
        if capsule_exists == 0:
            capsule_results = json.dumps(API.getCapsuleByName(capsule))
            capsule_results = json.loads(capsule_results)
            organizations = Organizations()
            organization_exists = organizations.organization_exists(organization)
            if organization_exists == 0:
                organization_results = json.dumps(API.getOrganizationByName(organization))
                organization_results = json.loads(organization_results)
                lifecycle_environments = LifecycleEnvs()
                lifecycle_exists = lifecycle_environments.lifecycle_env_exists(lifecycle_environment, organization)
                if lifecycle_exists == 0:
                    lifecycle_env_results = json.dumps(API.getLifecycleEnvByName(lifecycle_environment, organization_results))
                    lifecycle_env_results = json.loads(lifecycle_env_results)['results'][0]
                    capsule_envs = json.dumps(API.getCapsuleLifecycleEnv(capsule_results["id"]))
                    capsule_envs = json.loads(capsule_envs)['results']
                    env_already_set = False 
                    for env in capsule_envs:
                        if env["id"] == lifecycle_env_results["id"]:
                            env_already_set = True
                            break
                    if env_already_set == False:
                        try:
                            capsule_environment = json.dumps(API.setCapsuleLifecycleEnv(capsule_results["id"], lifecycle_env_results["id"]))
                            capsule_environment = json.loads(capsule_environment)['results']
                            env_set = False
                            for env in capsule_environment:
                                if env["id"] == lifecycle_env_results["id"]:
                                    env_set = True
                                    break
                            if env_set == True:
                                result = 1
                            else:
                                result = 3
                        except:
                            result = 3 
                    else:
                        result = 0
                else:
                    result = 3
            else:
                result = 3
        elif capsule_exist == 1:
            result = 2
        else:
            result = 3
        return result

    def sync_content(self, capsule):
        ''' Return 0 if sync has started, 1 if capsule is not a pulp node, 2 if error happened '''
        result = None
        capsule_exists = self.capsule_exists(capsule)
        if capsule_exists == 0:
            capsule_results = json.dumps(API.getCapsuleByName(capsule))
            capsule_results = json.loads(capsule_results)
            try:
                capsule_sync = json.dumps(API.syncCapsule(capsule_results["id"]))
                capsule_sync = json.loads(capsule_sync)
                if capsule_sync["state"] == "planned" and capsule_sync["result"] == "pending":
                    result = 0
                else:
                    result = 2 
            except:
                result = 2
        elif capsule_exists == 1:
            result = 1
        else:
            result = 2
        return result

class Tasks:
  
    def __init__(self):
        pass

    def task_running(self, action):
        ''' Returns 1 if a task of this type of action is running, 0 if no task of this type is running, 2 if error happened '''
        result = None
        if action == "repository_sync":
            label = "Actions::Katello::Repository::Sync"
        elif action == "contentview_publish":
            label = "Actions::Katello::ContentView::Publish"
        elif action == "activationkey_create":
            label = "Actions::Katello::ActivationKey::Create"
        elif action == "manifest_import":
            label = "Actions::Katello::Provider::ManifestImport"
        elif action == "enable_repository":
            label = "Actions::Katello::RepositorySet::EnableRepository"
        elif action == "capsule_sync":
            label = "Actions::Katello::CapsuleContent::Sync"
        else:
            label = None
        try: 
            tasks = json.dumps(API.searchTask(None))
            tasks = json.loads(tasks)['results']
            task_running = True
            running_tasks = []
            for task in tasks:
                task_label = task['label']
                task_status = task['state']
                task_result = task['result']
                task_id = task['id']
                if task_label == label and task_status == "running":
                    running_tasks.append(task_id)
            if len(running_tasks) > 0:
                result = 1
            else:
                result = 0
        except:
            result = 2
        return result

    def wait_for_task(self, action, check_every, timeout):
        ''' Waits until no tasks of this type are running, 0 if no task is running, 1 if timeout'''
        result = None
        tasks_running = True
        running_time = 0
        while(tasks_running):
            tasks_active = self.task_running(action)
            if tasks_active == 0:
                tasks_running = False
                result = 0
            else:
                time.sleep(check_every)
                running_time = running_time + check_every
                if running_time > timeout:
                    tasks_running = False
                    result = 1
        return result



  


