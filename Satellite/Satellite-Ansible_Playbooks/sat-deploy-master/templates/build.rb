#!/usr/bin/env ruby

require 'yaml'
require 'digest'
require 'erb'
require 'fileutils'


def validate_argv
  return ARGV[0] if ARGV.length == 1

  puts "Please provide the name of the box you wish to build."
  exit 1
end

def make_build_directory
  unless File.exist?('boxes')
    FileUtils.mkdir('boxes')
  end
end

def build_base(base, base_config)
  md5 = ''

  if Dir.glob("boxes/#{base}/*.box").empty?
    puts "No base image found for #{base}, building now..."
    build(base_config)
  end

  if !File.exists?("boxes/#{base}/box.img")
    Dir.chdir("boxes/#{base}/") do
      puts "Untarring base box to extract image..."
      system('tar -zxvf *.box')
    end
  end

  Dir.chdir("boxes/#{base}/") do
    puts "Calculating md5 of base box..."
    md5 = Digest::MD5.hexdigest(File.read('box.img'))
    puts "Calculated md5 of base box to be: #{md5}"
  end

  md5
end

def build(box_config, base = nil, md5 = nil)
  base_path = "#{Dir.pwd}/boxes/#{base}" if base
  minor_version = box_config['minor_version'] || Time.now.strftime("%Y%m%d%H%M%S")
  major_version = box_config['major_version']
  build_dir = "#{Dir.pwd}/boxes/#{box_config['config']}-#{minor_version}/"
  success = false

  Dir.chdir(box_config['config']) do
    puts "Beginning build of #{box_config['config']}..."
    hostname = "sat-#{minor_version.gsub('.', '')}-#{base}.example.com"
    activation_key = box_config['activation_key']

    command = [
      "packer",
      "build",
      "-var activation_key='#{activation_key}'",
      "-var checksum=#{md5}",
      "-var minor_version=#{minor_version}",
      "-var major_version=#{major_version}",
      "-var base_dir=#{base_path}",
      "-var hostname=#{hostname}",
      "-var build_dir=#{build_dir}",
      "*.json"
    ]

    puts command.join(' ')
    system(command.join(' '))
  end
end

box_name = validate_argv

config = YAML.load_file('build_config.yaml')
box_config = config['boxes'][box_name]

unless box_config
  puts "No box config found for #{box_name}"
  exit 1
end

base = box_config['base']
base_config = config['boxes'][base]

make_build_directory
base_md5 = build_base(base, base_config) if base
build(box_config, base, base_md5)
