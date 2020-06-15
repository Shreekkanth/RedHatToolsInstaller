# Sample makefile to sync this dir to google drive.
#
# Requirements: rclone, https://rclone.org
#
GOOGLE_DRIVE ?= gdrive
PROJECTS_TOPDIR ?= projects
PROJECT_DIR ?=

REMOTE = $(GOOGLE_DRIVE):/$(PROJECTS_TOPDIR)/$(PROJECT_DIR)
PASS ?= redhat


backup:
ifeq ($(PROJECT_DIR),)
	@echo "You must set PROJECT_DIR in google drive"
	@echo "   example. make PROJECT_DIR=exjp-ccsp-rhui-v3-201803"
else
	@which rclone 2>/dev/null || { echo "[Error] You need to install rclone first."; exit 1; }
	time rclone sync received/ $(REMOTE)/received/
	(proj=$${PWD##*/}; arcname=$${proj}-`date +%F_%H%M`; \
	 cd .. && zip -q -e -r -P '$(PASS)' $${arcname}.zip $${proj}/ && \
	 time rclone copy $${arcname}.zip $(REMOTE)/)
	time rclone ls $(REMOTE)/
endif

.PHONY: backup
