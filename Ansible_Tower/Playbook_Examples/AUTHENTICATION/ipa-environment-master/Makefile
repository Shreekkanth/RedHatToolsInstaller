ENV := development
TF := .infra/tf
LOCATION := "Australia East"

_tf:
	@[ -d $(TF) ] \
	  || git clone -b master git@bitbucket.org:redhat-anzservices/ipa-devel-env.git $(TF) \
	  && cd $(TF) && git pull origin master

_ipa_deploy: _tf
	[ -e secrets.tf ] && cp secrets.tf $(TF)/secrets.tf || true
	[ -e $(TF)/secrets.tf ] || mv $(TF)/secrets.tf-example $(TF)/secrets.tf
		test -f ~/.ssh/id_rsa.pub || ssh-keygen -t rsa -N ''
	@cd $(TF); terraform get
	cd $(TF); terraform apply -var "location=${LOCATION}"
	cd $(ENV) ; ln -sf ../$(TF)/terraform_ansible_inventory inventory
	ln -sf $(TF)/ssh_config .

## requirements : Install ansible dependecies.
requirements:
	ansible-galaxy -r install requirements.yml

## spin : Deploy development infrastructure.
spin: _ipa_deploy

## test : Run automated tests.
test: requirements
	ansible-playbook --inventory-file tests/inventory --syntax-check tests/test.yml
	ansible-playbook --inventory-file tests/inventory --list-tasks tests/test.yml

## clean : Clean the project directory of build artefacts.
clean:
	[ -f $(TF)/terraform.tfstate ] && ( cd $(TF) && terraform destroy -force ) || true
	[ -L ssh_config ] && unlink ssh_config || true
	[ -d $(TF) ] && rm -rf $(shell dirname $(TF)) || true
	[ -L $(ENV)/inventory ] && ( unlink $(ENV)/inventory && git checkout HEAD -- inventory ) || true
	[ -d .roles_cache ] && rm -rf .roles_cache || true
	[ -d results ] && rm -rf results || true
	[ -d recovery ] && rm -rf recovery || true

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
