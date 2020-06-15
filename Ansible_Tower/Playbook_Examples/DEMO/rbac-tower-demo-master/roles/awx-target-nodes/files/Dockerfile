# centos.Dockerfile
# 
# A baseline CentOS 7 container with OpenSSH installed.
#
# @author Anthony Loukinas <anthony.loukinas@redhat.com>

FROM centos:7

# Dependencies
RUN yum install -y openssh-server

# Generate SSH key, and create default openssh config
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' && \ 
ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''
ADD src/sshd/sshd_config /etc/ssh/sshd_config 

# Set initial root password
RUN echo root:password | chpasswd

# Start with container with OpenSSHd
CMD ["/usr/sbin/sshd -D"]