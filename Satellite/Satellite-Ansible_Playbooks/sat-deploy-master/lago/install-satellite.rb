#!/usr/bin/env ruby

require 'English'
require 'open3'

HOST = "satellite.example.com"
CAPSULE = "capsule.example.com"

def syscall(cmd)
  puts Dir.pwd
  puts cmd

  output = ''
  exit_status = false

  Open3.popen3(cmd) do |stdin, stdout, stderr, wait_thr|
    while line = stdout.gets
      output += line
      puts line
    end

   exit_status = wait_thr.value
  end

  return output, exit_status.success?
end

def execute_host(cmd)
  host = 'satellite.example.com'
  output, status = syscall("lago shell #{host} \"#{cmd}\"")
  exit(1) if status == false
  output
end

def execute_capsule(cmd)
  host = 'capsule.example.com'
  output, status = syscall("lago shell #{host} \"#{cmd}\"")
  exit(1) if status == false
  output
end

def snapshot(snapshot)
  syscall("lago snapshot #{snapshot}").first
end

def revert(snapshot)
  return unless syscall("lago status | grep 'Snapshots:'").first.include?(snapshot)
  syscall("lago revert #{snapshot}").first
end

version = ARGV[0]

Dir.chdir("environment-#{version}") do
  host_ip_address = execute_host("ifconfig eth0 2>/dev/null|awk '/inet/ {print $2}'|sed 's/addr://'").split(" ")[1]
  capsule_ip_address = execute_capsule("ifconfig eth0 2>/dev/null|awk '/inet/ {print $2}'|sed 's/addr://'").split(" ")[1]

  execute_host("echo #{capsule_ip_address} capsule.example.com capsule >> /etc/hosts")
  execute_host("echo #{host_ip_address} satellite.example.com satellite >> /etc/hosts")

  execute_capsule("echo #{capsule_ip_address} capsule.example.com capsule >> /etc/hosts")
  execute_capsule("echo #{host_ip_address} satellite.example.com satellite >> /etc/hosts")

  revert('install')
  execute_host("yum -y localinstall http://sat-r220-02.lab.eng.rdu2.redhat.com/pub/katello-ca-consumer-latest.noarch.rpm")
  execute_host("subscription-manager register --org Sat6-CI --activationkey 'Satellite Library #{version.upcase}' --force")

  execute_host('yum -y update')
  execute_host('yum -y install satellite')
  snapshot('install')

  execute_host('satellite-installer -v --scenario satellite --foreman-admin-password changeme --foreman-oauth-consumer-secret foreman --foreman-oauth-consumer-key foreman --foreman-proxy-oauth-consumer-key foreman --foreman-proxy-oauth-consumer-secret foreman')

  execute_host("capsule-certs-generate --capsule-fqdn #{CAPSULE} --certs-tar ~/#{CAPSULE}.tar.gz")

  syscall("lago copy-from-vm #{HOST} '~/#{CAPSULE}.tar.gz' .").first
  syscall("lago copy-to-vm #{CAPSULE} '#{CAPSULE}.tar.gz' '~/'").first

  execute_capsule('subscription-manager clean')
  execute_capsule('yum remove -y katello-ca*')
  execute_capsule("yum -y localinstall http://sat-r220-02.lab.eng.rdu2.redhat.com/pub/katello-ca-consumer-latest.noarch.rpm")
  execute_capsule("subscription-manager register --org Sat6-CI --activationkey 'Capsule Library #{version.upcase}'")
  execute_capsule('yum -y update')
  execute_capsule('yum -y install satellite-capsule')

  execute_capsule('satellite-installer -v --scenario capsule\
                    --capsule-parent-fqdn "satellite.example.com"\
                    --foreman-proxy-foreman-base-url "https://satellite.example.com"\
                    --foreman-proxy-trusted-hosts "satellite.example.com"\
                    --foreman-proxy-register-in-foreman   "true"\
                    --foreman-proxy-oauth-consumer-key    "foreman"\
                    --foreman-proxy-oauth-consumer-secret "foreman"\
                    --capsule-pulp-oauth-secret     "foreman"\
                    --capsule-certs-tar             "/root/capsule.example.com.tar.gz"\
                    --capsule-puppet "true"')

  execute_capsule('subscription-manager unregister')
  execute_capsule('yum remove -y katello-ca*')
  execute_capsule('yum -y localinstall http://satellite/pub/katello-ca-consumer-latest.noarch.rpm')
  execute_capsule('subscription-manager register --org "Default_Organization" --username admin --password changeme')
end
