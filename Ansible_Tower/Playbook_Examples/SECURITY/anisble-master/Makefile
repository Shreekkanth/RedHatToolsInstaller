.PHONY: build
build:
	@docker build -t deloitte-ansible .

.PHONY: run
run:
	@docker run \
		-it \
		-e AZURE_SUBSCRIPTION_ID=`cat ~/.azure/credentials | grep subscription_id | cut -d '=' -f2` \
		-e AZURE_CLIENT_ID=`cat ~/.azure/credentials | grep client_id | cut -d '=' -f2` \
		-e AZURE_OBJECT_ID=`cat ~/.azure/credentials | grep object_id | cut -d '=' -f2` \
		-e AZURE_SECRET=`cat ~/.azure/credentials | grep secret | cut -d '=' -f2` \
		-e AZURE_TENANT=`cat ~/.azure/credentials | grep tenant | cut -d '=' -f2` \
		-e SNP_RESOURCE=${SNAPI_RESOURCE} \
		-e SNP_CLIENT_ID=${SNAPI_CLIENT_ID} \
		-e SNP_CLIENT_SECRET=${SNAPI_CLIENT_SECRET} \
		deloitte-ansible
