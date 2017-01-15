import os, string, re, sys


def create_vagrant_vms(vm_count):
    current_dir = os.getcwd()
    ips = []
    for index in range(1, vm_count + 1):
        sub_dir = os.path.join(current_dir, "server%s" % index)
        os.system("mkdir -p %s" % sub_dir)
        template_file = open("Vagrantfile_template")
        write_vagrant_file(sub_dir, template_file, dict())
        os.system("cd %s && vagrant up" % sub_dir)
        ips.append(get_vm_ip(sub_dir))
    ip_file = os.path.join(current_dir, "ips.txt")
    with open(ip_file, "w") as file:
        file.write(os.linesep.join(ips))


def write_vagrant_file(vagrant_dir, template_file, template_dict):
    template = string.Template(template_file.read())
    text = template.substitute(template_dict)
    vagrant_file = os.path.join(vagrant_dir, "Vagrantfile")
    with open(vagrant_file, "w") as file:
        file.write(text)


def get_vm_ip(vagrant_dir):
    print("get_vm_ip : %s" % vagrant_dir)
    output = os.popen("cd %s && vagrant ssh -c \"ifconfig\"" % vagrant_dir).read()
    print("outtput : %s" % output)
    vm_ip, = re.findall(r"172\.\d{1,3}\.\d{1,3}\.(?!255)\d{1,3}", output)
    return vm_ip


def exec_vagrant_vms(command):
    print("exec_vagrnat_vms : %s" % command)
    current_dir = os.getcwd()
    print("exec_vagrant: currentdir %s" % current_dir)
    for sub_dir in os.listdir(current_dir):
        if os.path.isdir(sub_dir) and sub_dir.startswith("server"):
            sub_dir_abs = os.path.join(current_dir, sub_dir)
            print("subdir : %s" % sub_dir_abs)
            os.system("cd %s && vagrant %s -f" % (sub_dir_abs, command))
            if command == "destroy":
                os.system("rm -rf %s" % sub_dir_abs)
                print("ips : %s" % os.path.join(current_dir, "ips.txt"))
                os.system("rm -f %s" % os.path.join(current_dir, "ips.txt"))


command_dict = {
    "create": lambda x, y: create_vagrant_vms(int(y)),
    "destroy": exec_vagrant_vms}

if len(sys.argv) > 1:
    command = sys.argv[1]
    print("command : %s" % command)
    command_dict[command](*sys.argv[1:])
