# vms

Required:
  - Vagrant
  - Linux
  - Python3
  - Public SSH-Key in ~/.ssh/id_rsa.pub
  
Purpose:
  Creating a cluster of Virtual Machines via Vagrant. You can ssh into each VM via the user: vagrant such as: `ssh vagrant@<ip-address of the VM>`
  
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
