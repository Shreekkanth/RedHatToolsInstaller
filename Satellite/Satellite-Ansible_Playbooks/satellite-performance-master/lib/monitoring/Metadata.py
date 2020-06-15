import json
import re
import logging
import sys
import os

class Metadata:

    def __init__(self):
        pass

    def load_file(self, filename):
        json_str = None
        try :
            with open(filename) as data:
                json_str = data.read()
        except IOError:
            print("Machine facts json is missing")
            exit(1)
        regex = re.compile(r"}\n{")
        new_json = re.sub(r"}\n{",r"},\n{",json_str,re.M)
        convert = "{ \"machines\": [" + new_json + "] }"
        sys_data = {}
        sys_data['system_data'] = json.loads(convert)
        return sys_data

    def get_hardware_metadata(self, sys_data):
        hard_dict = {}
        for item in sys_data['system_data']['machines']:
            if 'hardware_details' not in hard_dict:
                hard_dict['hardware_details'] = []
            hardware_dict = {}
            hardware_dict['label'] = item['inventory_hostname']
            hardware_dict['kernel'] = item['ansible_kernel']
            hardware_dict['total_mem'] = item['ansible_memory_mb']['real']['total']
            hardware_dict['total_logical_cores'] = item['facter_processorcount']
            hardware_dict['os_name'] = item['ansible_distribution'] + \
                item['ansible_distribution_version']
            hardware_dict['ip'] = item['ansible_default_ipv4']['address']
            hardware_dict['num_interface'] = len(item['ansible_interfaces'])
            hardware_dict['machine_make'] = item['ansible_product_name']
            hard_dict['hardware_details'].append(hardware_dict)
        return hard_dict

    def get_environment_metadata(self, sys_data):
        env_dict = {}
        for item in sys_data['system_data']['machines']:
            if 'environment_setup' not in env_dict:
                env_dict['environment_setup'] = {}
            for key,value in item.items():
                if 'osp' in key:
                    env_dict['environment_setup'][key] = value
        return env_dict

    def get_software_metadata(self, sys_data):
        soft_all_dict = {}
        for item in sys_data['system_data']['machines']:
            if 'software_details' not in soft_all_dict:
                soft_all_dict['software_details'] = {}
            nodes = ['controller', 'undercloud', 'compute']
            if any(node in item['inventory_hostname'] for node in nodes):
                if 'satellite' not in soft_all_dict['software_details']:
                    soft_all_dict['software_details']['satellite'] = {}
                if 'config' not in soft_all_dict['software_details']['satellite']:
                    soft_all_dict['software_details']['satellite']['config'] = []
                software_dict = {}
                software_dict['node_name'] = item['inventory_hostname']
                for soft in item:
                    if 'satellite' in soft:
                        service = soft.split('_')
                        service_name = service[1]
                        if service_name not in software_dict:
                            software_dict[service_name] = {}
                        if service_name in soft:
                            software_dict[service_name][soft] = item[soft]
                soft_all_dict['software_details']['satellite']['config'].append(software_dict)
        return soft_all_dict

    def write_metadata_file(self, data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file)


def main():
    _filename = os.path.join(sys.argv[1], 'machine_facts.json')
    metadata = Metadata()
    sysdata = metadata.load_file(_filename)
    env_data = metadata.get_environment_metadata(sysdata)
    metadata.write_metadata_file(env_data, os.path.join(sys.argv[1], 'environment-metadata.json'))
    hardware_data = metadata.get_hardware_metadata(sysdata)
    metadata.write_metadata_file(hardware_data, os.path.join(sys.argv[1], 'hardware-metadata.json'))
    software_data = metadata.get_software_metadata(sysdata)
    metadata.write_metadata_file(software_data, os.path.join(sys.argv[1], 'software-metadata.json'))

if __name__ == '__main__':
    sys.exit(main())
