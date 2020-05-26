DEV_SERVER=10.0.1.161

echo "Exporitng creds, inventory and org"
tower-cli receive \
--organization "SR Org" \
--credential_type "SR GitLab Credential Type" \
--credential "SR Dev Tower Credential" \
--credential "SR Prod Tower Credential" \
--credential "SR SCM Credential" \
--credential "SR Machine Credential" \
--credential "SR GitLab Credential" \
--inventory "SR Inventory" \
--tower-host $DEV_SERVER > server_assets.json

echo "Exporting project and jobs"
tower-cli receive \
--project "SR Project" \
--job_template "SR Export Assets" \
--job_template "SR Import Assets" \
--tower-host $DEV_SERVER > server_project.json
