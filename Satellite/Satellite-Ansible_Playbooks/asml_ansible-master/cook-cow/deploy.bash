# Bastion is satellite in my case
#
# Not syncing vars. Do manually if changed. 
# Could do .gitignore, but they wouldn't appear in the repo
#
# make a file called deploy.conf and gitignore it. Inside write BASTION="bastion_user@bastion_ip:/dest/folder/" (with the trailing slash)

. deploy.conf

rsync -avtr ./* ${BASTION} --exclude="group_vars/*" --exclude="deploy.*" --exclude="*.swp"
