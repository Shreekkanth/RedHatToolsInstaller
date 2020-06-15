ROLE Name    : install_gitlab                                                 
ROLE Author  : Ken Hitchcock                                                   
ROLE Purpose : Automate GitLab installation                          


Requirements
Variables required to be set before running the role.
 - None required for the role


Note
Role only does the installation of packages. 
The recofiguration of gitlab using the gitlab-crl still needs to be run. 


Tasks to complete
 - Work out the configuration part to automate.
 - Write playbook to download repository files for disconnected environments.
 - Update yum repo with disconnected repository.
