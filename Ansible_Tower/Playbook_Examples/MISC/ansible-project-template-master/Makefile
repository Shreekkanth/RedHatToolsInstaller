# Please define this to specify your customer, site name and so on first!
SITE ?= exjp
TOPDIR = .

miniascape_OPTIONS = -t $(TOPDIR)/templates

ifeq ($(strip $(SITE)),)
$(error Variable SITE must be set!)
endif

all: backup

build:
	miniascape b $(miniascape_OPTIONS) -C $(TOPDIR)/$(SITE) -w $(TOPDIR)/out

floppy:
	for d in $(wildcard $(TOPDIR)/out/guests.d/*); do test -d $$d && make -C $$d floppy || :; done

setup:
	for d in $(wildcard $(TOPDIR)/out/guests.d/*); do test -d $$d && make -C $$d setup || :; done 

doc: $(TOPDIR)/doc/Makefile
	make -C doc

$(TOPDIR)/doc/Makefile:
	echo "NAME ?= $(SITE)-rhui-3-impl-doc" > $@; \
	echo 'REVISION ?= $$(shell date +%Y-%m-%d.1)' >> $@; \
	echo "include /usr/share/rst2odt/aux/Makefile" >> $@

include backup.mk

GIT_SUBMODULE_SUBDIRS = templates
update-submodules:
	for smd in $(GIT_SUBMODULE_SUBDIRS); do (cd $$smd && git pull origin master); done
	git commit -m "change: update submodules to follow changes in them" $(GIT_SUBMODULE_SUBDIRS)

.PHONY: build floppy setup doc
