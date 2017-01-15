# vms

Required:
  - Vagrant
  - Linux
  - Python3
  
Purpose:
  Creating a cluster of Virtual Machines via Vagrant.
  
# HowTo
  - Creating <n> VMs: 
      ```
          python3 vms.py create <n>
      ```
    This will create server-subfolders for each VM in the current directory.
    Also a file ips.txt will be created with the IP-addresses of all VMs.
  - Deleting/Stopping VMs: 
      ```
          python3 vms.py <command>
      ```
    with `<command> = destroy`: This will destroy & delete all VMs
