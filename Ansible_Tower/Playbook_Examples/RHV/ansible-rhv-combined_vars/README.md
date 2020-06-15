# ansible-rhv

Configuring your freeipa credential variables
https://www.ansible.com/blog/ansible-tower-feature-spotlight-custom-credentials

INPUT CONFIGURATION
```
fields:
  - type: string
    id: user
    label: freeipa upsername
  - secret: true
    type: string
    id: password
    label: freeipa password
  - type: string
    id: realm
    label: freeipa realm (ALL CAPS)
required:
  - user
  - password
  - realm
```

INJECTOR CONFIGURATION
```
extra_vars:
  ipa_password: '{{ password }}'
  ipa_realm: '{{ realm }}'
  ipa_user: '{{ user }}'
```
