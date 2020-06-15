This project focuses on using Ansible to interact with ServiceNow.  Because there is not currently an official Ansible module to interact with ServiceNow, I utilize direct REST API calls using the uri ansible module.

Current Roles:

create_snow_incident.yml
:: this role creates a ServiceNow incident ticket and automatically populates the ticket with important machine related data

wake_snow_demo_instance.yml
:: IN PROGRESS :: this ticket logs into service now developer portal and resets the 10 day timer.  If you don't login every 10 days the instance will automatically be deleted.

Please use freely and give any feedback should you find issues, have questions or want to just give a high five.
