# automate-tower-ldap-config

## Usage

```bash
ansible-playbook -i inventory configure-ldap.yml \
  -e tower_host="http://localhost:80" \
  -e tower_username="admin" \
  -e tower_password="password" \
  -e tower_lane="dev"
```
