#!/usr/bin/python3
import os
import re
import string
import sys


def user_interface():
    os_dict = {1: "ubuntu/precise64",
               2: "debian/jessie64",
               3: "fedora/25-cloud-base",
               4: "centos/7"}
    input_text_os = [
        "For the name of other OS see: https://atlas.hashicorp.com/boxes/search for OS.",
        os.linesep.join("(%s) %s" % (number, os_name) for number, os_name in os_dict.items()),
        "Enter number of choice for OS or the name of OS: > ", ]
    choice = input(os.linesep.join(input_text_os))
    chosen_os = os_dict[int(choice)] if choice.isdigit() else choice
    print("> Selected OS: %s" % chosen_os)
    vm_count = input("Enter the number of VMs to be created: > ")
    print("> Number of VMs: %s" % vm_count)
    create_vagrant_vms(int(vm_count), chosen_os)


def create_vagrant_vms(vm_count, chosen_os):
    current_dir = os.getcwd()
    ips = []
    for index in range(1, vm_count + 1):
        sub_dir = os.path.join(current_dir, "server%s" % index)
        os.system("mkdir -p %s" % sub_dir)
        template_file = open("Vagrantfile_template")
        write_vagrant_file(sub_dir, template_file, {"chosen_os": chosen_os})
        os.system("cd %s && vagrant up" % sub_dir)
        ips.append(get_vm_ip(sub_dir))
    ip_file = os.path.join(current_dir, "ips.txt")
    with open(ip_file, "w") as file:
        ips.append("")
        file.write(os.linesep.join(ips))


def write_vagrant_file(vagrant_dir, template_file, template_dict):
    template = string.Template(template_file.read())
    text = template.substitute(template_dict)
    vagrant_file = os.path.join(vagrant_dir, "Vagrantfile")
    with open(vagrant_file, "w") as file:
        file.write(text)


def get_vm_ip(vagrant_dir):
    output = os.popen("cd %s && vagrant ssh -c \"ip addr\"" % vagrant_dir).read()
    vm_ip, = re.findall(r"172\.\d{1,3}\.\d{1,3}\.(?!255)\d{1,3}", output)
    return vm_ip


def exec_vagrant_vms(command="destroy"):
    current_dir = os.getcwd()
    for sub_dir in os.listdir(current_dir):
        if os.path.isdir(sub_dir) and sub_dir.startswith("server"):
            sub_dir_abs = os.path.join(current_dir, sub_dir)
            os.system("cd %s && vagrant %s -f" % (sub_dir_abs, command))
            if command == "destroy":
                os.system("rm -rf %s" % sub_dir_abs)
                os.system("rm -f %s" % os.path.join(current_dir, "ips.txt"))


def info():
    info_dict = {
        "create": "Creating VMs",
        "destroy": "Deleting VMs",
        "suspend": "Suspending VMs",
        "resume": "Resuming VMs",
        "reload": "Reloading VMs"
    }
    lines = ["Command: python3 vms.py <argument>", "List of all Arguments:"]
    lines.extend(
        "* %s : %s" % (key, info_text) for key, info_text in info_dict.items())
    print((os.linesep + "  ").join(lines))


command_dict = {
    "create": user_interface,
    "destroy": lambda: exec_vagrant_vms("destroy"),
    "reload": lambda: exec_vagrant_vms("reload"),
    "suspend": lambda: exec_vagrant_vms("suspend"),
    "resume": lambda: exec_vagrant_vms("resume"),
    "info": info}

if len(sys.argv) == 2:
    command = sys.argv[1]
    command_dict.get(command, info)()
else:
    command_dict["info"]()
