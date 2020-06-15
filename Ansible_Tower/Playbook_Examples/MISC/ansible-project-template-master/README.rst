About
=======

This is an experimental Ansible project template to setup build/test environment and provide
GPS RHUI v3 delivery documents and so on.

Prerequisites
================

- Environments:

  - Fedora 28+; other platform should be OK if requirements are satisfied but not tested at all.
  - Any KVM/libvirt host in which virt-install command is available, to build and test VMs

- RPMs to install:

  - python-docutils: python3-docutils or python2-docutils from Fedora's official repo
  - gimp: from Fedora's official repo
  - inkscape: from Fedora's official repo
  - optipng: from Fedora's official repo
  - miniascape:

    - from my github repo: https://github.com/ssato/miniascape (git checkout && build RPMs)
    - from my internal yum repo, http://file.nrt.redhat.com/ssato/yum/fedora/27/x86_64/ for example

  - python3-anyconfig: from Fedora's official repo (F28+) or my copr repo, https://copr.fedorainfracloud.org/coprs/ssato/python-anyconfig/
  - python3-anytemplate: from my copr repo, https://copr.fedorainfracloud.org/coprs/ssato/python-anyconfig/
  - python-docutils-exts: from my internal yum repo, http://file.nrt.redhat.com/ssato/yum/fedora/27/x86_64/ for example

.. note:: bootstrap/install.sh might help you to install required RPMs automatically.

Resources
==============

Automation Discovery Session
---------------------------------

- Value Stream Mapping:

  - https://en.wikipedia.org/wiki/Value_stream_mapping
  - https://dev.classmethod.jp/devops/value-stream-mapping/
  - https://www.slideshare.net/slideshow/embed_code/key/AkOtIzH8O2pOQW
  - https://www.lucidchart.com/pages/value-stream-mapping

Usage
===========

Preparation
------------

#. Checkout this git repo and make a branch or another git repo for your project like followings. Please note that you need \-\-recurse\-submodules option to checkout miniascape-templates git submodule also:

   ::

      $ git clone ssh://git@gitlab.consulting.redhat.com:2222/ssato/rhui-3-project-template.git acme-ccsp-rhui-v3-project.git --recurse-submodules

#. Prepare YAML configuration (ctx) files for your site in <site_name>/.
   Easiest way may be to rename exjp/ to <your_site_name>/ and customize
   20_guests.yml in it.

#. Modify Makefile in the top dir

- set SITE: s/exjp/<your_site_name>/g
- set PROJECT_DIR to dir path in google drive for backup

How it works
================

- miniascape loads site/host/guests configurations (top_dir/\*/\*.yml) and
  generate libvirt configuration and scripts to build VMs under out/.

- doc:

  - Jinja2 templates are compiled by anytemplate_cli automatically (see also Makefile.depends generated)
  - PNG images are converted from .xcf by gimp and/or .svg by inkscape and optimized by optipng automatically (do.)
  - PDF/Word files are converted from intermediate ODT file generated from reStructured Text files by rst2odt, by unoconv.

Author
=======

- Satoru SATOH <ssato@redhat.com>
