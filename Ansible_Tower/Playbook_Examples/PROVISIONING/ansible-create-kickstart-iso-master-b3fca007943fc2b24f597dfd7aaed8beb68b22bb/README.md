# create-kickstart-iso

An Ansible Role to build custom kickstart ISOs from a source installation media ISO.

## Role Variables

### Defaults `defaults/main.yml`:
| Variable Name | Required | Description | Default Value | Type |
| --- | :---: | --- | :---:| :---: |
| ks_iso_install_media_path | Yes | Path to the source installation media iso file on the remote system | "" | string |
| ks_iso_kickstart_file | Yes | Filename of the kickstart file to add to the new bootable ISO contained within the role's "files" directory, or a fully-qualified path to a kickstart file on the Ansible Control system. | "" | string |
| ks_iso_built_path | Yes | Directory to store build ISO files | "" | string |
| ks_iso_built_filename | Yes | Filename to create the new ISO file as | "" | string |
| ks_iso_volume_id | Yes | Volume label of the ISO to create | "My Kickstart ISO" | string |
| ks_iso_boot_timeout | Yes | Time in 1/10 seconds to wait to boot the menu or `ontimeout` command in the isolinux.cfg file if user has not interacted with the menu | "150" | integer |
| ks_iso_boot_total_timeout | Yes | Time in 1/10 seconds to wait (even if the user moved the menu cursor) before performing the `ontimeout` or menu default command set in the isolinux.cfg file | "900" | integer |
| ks_iso_cleanup_build | Yes | Whether or not to cleanup the ks_iso_build_dir.path and unmount the source ISO | True | boolean |
| ks_iso_build_dir | No | To override the creation of a temporary build directory with a specified one if desired | `undefined` Can be set as `{ path: "/path/to/my/desired/build/directory"}` | dictionary |

### Defaults `vars/main.yml` - Not intended to be overridden
| Variable Name | Required | Description | Default Value | Type |
| --- | :---: | --- | :---:| :---: |
| ks_iso_pkgs | Yes | List of packages required for this role to function | ["createrepo", "genisoimage"] | list |
| ks_iso_paths | List of paths relative to the `ks_iso_build_dir.path` required to build the ISO | ["isolinux/images", "isolinux/ks", "isolinux/LiveOS", "isolinux/Packages", "isolinux/Packages", "isolinux/postinstall", "mnt"] | list |
| ks_iso_source_paths | Source and destination pairs of required files from the source installation media to the `ks_iso_build_dir.path` | [{src: "{{ ks_iso_build_dir.path }}/mnt/.discinfo", dest: "/isolinux/.discinfo"}, {src: "{{ ks_iso_build_dir.path }}/mnt/isolinux", dest: ""}, {src: "{{ ks_iso_build_dir.path }}/mnt/images", dest: "/isolinux/"}, {src: "{{ ks_iso_build_dir.path }}/mnt/LiveOS", dest: "/isolinux/"}, {src: "{{ ks_iso_build_dir.path }}/mnt/Packages", dest: "/isolinux/"}] | list of dictionaries |
| ks_iso_isolinux_boot_line | Yes | Command to run from the isolinux.cfg file's `ontimeout` parameter | "ontimeout vmlinuz initrd=initrd.img ks=cdrom:/ks/ks.cfg" | string |

## Example Playbook
```yaml
---
- name: "Build a new auto kickstart ISO from a RHEL7 ISO"
  hosts: "localhost"
  tasks:
    - name: "Build the kickstart ISO"
      include_role:
        name: "create-kickstart-iso"
      vars:
        ks_iso_install_media_path: "/root/isos/rhel-server-7.5-x86_64-dvd.iso"
        ks_iso_kickstart_file: "my_custom_kickstart.cfg"
        ks_iso_built_path: "/root/built_isos"
        ks_iso_built_filename: "my_new_auto_kickstart.iso"
        ks_iso_volume_id: "kool kickstart"
        ks_iso_boot_timeout: "50" # 5 secs
        ks_iso_boot_total_timeout: "300" # 30 secs
```

## License
[MIT](LICENSE)

## Author
[Andrew J. Huffman](mailto: ahuffman@redhat.com)
