# AWX settings file
# Ansible Managed File - DO NOT HAND EDIT

###############################################################################
# MISC PROJECT SETTINGS
###############################################################################

ADMINS = (
   #('Joe Admin', 'joeadmin@example.com'),
)

STATIC_ROOT = '/var/lib/awx/public/static'

PROJECTS_ROOT = '/var/lib/awx/projects'

JOBOUTPUT_ROOT = '/var/lib/awx/job_status'

SECRET_KEY = file('/etc/tower/SECRET_KEY', 'rb').read().strip()

ALLOWED_HOSTS = ['*']

INTERNAL_API_URL = 'http://127.0.0.1:80'

USE_X_FORWARDED_PORT = True
USE_X_FORWARDED_HOST = True

###############################################################################
# EMAIL SETTINGS
###############################################################################

SERVER_EMAIL = 'root@localhost'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
EMAIL_SUBJECT_PREFIX = '[AWX] '

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

###############################################################################
# LOGGING SETTINGS
###############################################################################

LOGGING['handlers']['tower_warnings']['level'] =  'INFO'

# Note: This setting may be overridden by database settings.
# This setting is now configured via the Tower API.
# PENDO_TRACKING_STATE = 'detailed'

