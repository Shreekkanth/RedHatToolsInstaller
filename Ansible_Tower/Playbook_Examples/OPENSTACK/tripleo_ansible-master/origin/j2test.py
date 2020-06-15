#!/usr/bin/python

from jinja2 import Template, Environment, FileSystemLoader

file="roles/ansible_installer/templates/hosts.multi.j2"

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(file)

data = {'origin':
        {'distribution': 'origin',
         'prefix': 'origin'},
        }
text = template.render(data)
print(text)

