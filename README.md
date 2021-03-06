# vms

Required:
  - Vagrant
  - Linux
  - Python3
  - Public SSH-Key in ~/.ssh/id_rsa.pub
  
Purpose:
  Creating a cluster of Virtual Machines via Vagrant and DHCP. Collects the IP-Address of each VM in a file. You can then ssh into each VM via the user: vagrant such as: `ssh vagrant@<ip-address of the VM>`
  
# HowTo
  - Info:
      ```
          python3 vms.py info
      ```
    Gives an overview of available commands.
  - Creating VMs:
      ```
          python3 vms.py create
      ```
    This will create server-subfolders for each VM in the current directory.
    Also a file ips.txt will be created containing the IP-addresses of all created VMs.
  - Destroy/Suspend/Resume/Reload VMs:
      ```
          python3 vms.py <command>
      ```
    with `<command> = destroy, suspend, resume, reload`: This will destroy, suspend, resume, reload all VMs

