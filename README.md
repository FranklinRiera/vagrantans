# Hypervisor Type-2: deploying an HTTP App via Vagrant + Ansible

## Objectives

- Learn about **Vagrant**
- Learn about Deploying a virtualbox VM with Vagrant
- Learn about **Ansible**

## [Vagrant](https://www.vagrantup.com/)

Vagrant is a source-available software product for building and maintaining portable virtual software development environments, e.g., for VirtualBox, KVM, Hyper-V, Docker containers, VMware, Parallels, and AWS. It tries to simplify the software configuration management of virtualization in order to increase development productivity. Vagrant is written in the Ruby language, but its ecosystem supports development in a few other languages. Vagrant has a Business Source License 1.1, while there is a fork called Viagrunts with the original MIT license.


> Vagrant is a tool for building and managing virtual machine environments in a single workflow. With an easy-to-use workflow and focus on automation, Vagrant lowers development environment setup time, increases production parity, and makes the “works on my machine” excuse a relic of the past.

> Vagrant is an automation tool with a domain-specific language (DSL) that is used to automate the creation of VMs and VM environments.

- [Vagrant, What is that?](https://medium.com/@kamilmasyhur/vagrant-what-is-that-5ba440427098)

![](https://miro.medium.com/v2/format:webp/0*pV4407g7awNTh1QP.png)


## [Ansible](https://www.ansible.com/)

Ansible® is an open source, command-line IT automation software application written in Python. It can configure systems, deploy software, and orchestrate advanced workflows to support application deployment, system updates, and more.

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*8H4XYCNV-xamG0joz22apQ.png)

- [Ansible 101 Getting Started](https://medium.com/@wintonjkt/ansible-101-getting-started-1daaff872b64)
- [Ansible community documentation](https://docs.ansible.com/?extIdCarryOver=true&intcmp=7013a0000034dzKAAQ&percmp=7013a000002i5nEAAQ&sc_cid=701f2000001OH7EAAW)

## Deploying a VirtualBox VM debian-based
### 1. Install Vagrant

Based on your OS, follow the [Install Vagrant instructions](https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-install) and verify the installation.

```bash
vagrant --version
Vagrant 2.3.4
```


### 2. Create Vagrant project

Create a new directory and change into it:

 ```bash
 $ mkdir vagrant
 $ cd vagrant
 ```


#### Initialize the directory
Vagrant has a built-in command for initializing a project, `vagrant init`, which can take a box name and URL as arguments. Initialize the directory and specify the `hashicorp/bionic64` box.

```bash
$ vagrant init hashicorp/bionic64

A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.
```

You now have a Vagrantfile in your current directory. Open the Vagrantfile, which contains some pre-populated comments and examples. In following tutorials you will modify this file.

Expand the file below to view the entire contents of the example Vagrantfile.

<details>
  <summary><b>Show Vagrantfile</b></summary>

```bash
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "hashicorp/bionic64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
```

</details>


The Box configured for this example is: `hashicorp/bionic64`. You can find more boxes at [HashiCorp's Vagrant Cloud box catalog.](https://vagrantcloud.com/boxes/search)

### Bring up the VM

Now that you have initialized your project and configured a box for it to use, it is time to boot your first Vagrant environment.

```bash
vagrant up
```

### SSH into the machine
You will not actually see anything though, since Vagrant runs the virtual machine without a UI. To prove that it is running, you can SSH into the machine:

```bash
vagrant ssh
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-58-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue Jun 16 21:57:57 UTC 2020

  System load:  0.44              Processes:           91
  Usage of /:   2.5% of 61.80GB   Users logged in:     0
  Memory usage: 11%               IP address for eth0: 10.0.2.15
  Swap usage:   0%

 * MicroK8s gets a native Windows installer and command-line integration.

     https://ubuntu.com/blog/microk8s-installers-windows-and-macos

0 packages can be updated.
0 updates are security updates.


vagrant@vagrant:~$
```

This command will drop you into a full-fledged SSH session. Go ahead and interact with the machine and do whatever you want. Although it may be tempting, be careful about `rm -rf /`, since Vagrant shares a directory at `/vagrant` with the directory on the host containing your Vagrantfile, and this can delete all those files. More info about [Shared folders](https://developer.hashicorp.com/vagrant/tutorials/getting-started/getting-started-synced-folders).


Terminate the SSH session with `CTRL+D`, or by logging out.

```ssh
vagrant@vagrant:~$ logout
Connection to 127.0.0.1 closed.
```

### Destroy the VM

Once you're back on your host machine, stop the machine that Vagrant is managing and remove all the resources created during the machine-creation process. When prompted, confirm with a yes.

```bash
vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
```

### Remove the box

The `vagrant destroy` command does not remove the downloaded box file. List your box files.

```bash
vagrant box list
hashicorp/bionic64  (virtualbox, 1.0.282)
```

Remove the box file with the `remove` subcommand, providing the name of your box.

```bash
vagrant box remove hashicorp/bionic64
Removing box 'hashicorp/bionic64' (v1.0.282) with provider 'virtualbox'...
```

### Basic Vagrant commands

- `vagrant up` that will instruct Vagrant to create and run the virtual machine
- `vagrant halt` that will stop the virtual machine
- `vagrant destroy` that will destroy the virtual machine (useful when we change the VagrantFile and want to recreate it again)
- `vagrant ssh` that will connect to that machine and give us a remote command line session
- `vagrant ssh-config` that will display SSH connection information if we want to connect to the machine without Vagrant


## 3. Install Ansible

Based on your OS, follow the [Install Ansible instructions](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-and-upgrading-ansible). For Debian/Ubuntu:

```bash
apt update
apt install ansible
```

## 4. Ansible Playbook + Templates
On the path `vagrant`, create a playbook file named `playbook.yml`.

 ```bash
touch playbook.yml
```

Open `playbook.yml` in your text editor, and paste in the configuration below. 

```yaml
- name: nginx gunicorn flask
  hosts: all
    #  connection: local
  become: true

  vars:
    LOCAL_PROJECT_HOME: "./myproject"
    PROJECT_HOME: "/opt/myproject"
    PROJECT_VENV: "myprojectvenv"
    MAIN_PY: "myproject.py"
    MAIN_SOCK: "myproject.sock"
    NGINX_PORT: 80
    PORT: 5000

  tasks:
  - name: apt install required packages
    apt:
      update_cache: yes
      name:
        - wget
        - curl 
        - python3-pip
        - python3-dev
        - nginx
        - python3-venv        
      state: present

  - name: Create remote directory
    file: path={{PROJECT_HOME}} state=directory

  - name: Copy project code to website server
    copy: src={{item}} dest={{PROJECT_HOME}}
    with_fileglob:
     - "{{LOCAL_PROJECT_HOME}}/*"

  - name: Install reqs into the specified virtualenv using Python3
    ansible.builtin.pip:
      requirements: "{{ PROJECT_HOME }}/requirements.txt"
      virtualenv: "{{ PROJECT_HOME }}/{{ PROJECT_VENV }}"
      virtualenv_command: "python3 -m venv"

  - name: delete a file (or symlink) if it exists
    file:
      path: "/etc/nginx/sites-enabled/default"
      state: absent        

  - name: nginx.conf config file
    template:
      src: "nginx.conf.j2"
      dest: "/etc/nginx/sites-available/myproject"

  - name: create a symlink if it doesn't exist
    file:
      src: "/etc/nginx/sites-available/myproject"
      dest: "/etc/nginx/sites-enabled/myproject"
      state: link

  - name: Create myproject service
    template:
      src: "myproject.service.j2"
      dest: "/etc/systemd/system/myproject.service"

  - name: Reload the SystemD to re-read configurations
    systemd:
      daemon-reload: yes
  
  - name: Enable the myproject service and start
    systemd:
      name: '{{ item }}.service'
      enabled: yes
      state: started
    loop:
      - myproject

  - name: restart nginx service
    systemd:
      name: nginx
      state: restarted
```


Create a `templates` directory with the following files:

- `myproject.service.j2`

```bash
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory={{ PROJECT_HOME }}
Environment="PATH={{ PROJECT_HOME }}/{{ PROJECT_VENV }}/bin"
ExecStart={{ PROJECT_HOME }}/{{ PROJECT_VENV }}/bin/gunicorn --workers 3 --bind unix:{{ MAIN_SOCK }} -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

- `nginx.conf.j2`

```bash
server {
    listen {{ NGINX_PORT }};

    location / {
        include proxy_params;
        proxy_pass http://unix:{{PROJECT_HOME }}/myproject.sock;
    }
}
```

## 5. HTTP App: Flask

Create a `myproject` directory with the following files:
- `myproject.py`

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

- `wsgi.py`

```python
from myproject import app

if __name__ == "__main__":
    app.run()
```

- `requirements.txt`

```bash
wheel
gunicorn
flask
```

## 6. Enable IP access to the VM from the Host-only
In order to test the HTTP App from the host, add the following configurations to the Vagrantfile:

```bash
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64" 

  config.vm.network "private_network", ip: "192.168.56.10"
end
```

The IP `192.168.56.10` must be in the LAN of the **Host-only Networks** configuration of Virtualbox. To get this information:
1. Open Virtualbox
2. Go to File -> tools -> Network manager
3. On the tab **Host-only Networks** you will find the LAN configured
![](figs/networkmanager.png)
4. Select an IP in this LAN for the above configuration
5. Execute

```bash
vagrant reload
```

## 7. Provision the HTTP App with Vagrant + Ansible
When we can successfully start our Vagrant box, it is time to setup the provisioning via Ansible. We have two basic options how to use Ansible together with Vagrant:

- **Option 1**: Use Ansible integration with Vagrant. Vagrant will call our Ansible playbook on vagrant up or on vagrant provision automatically.
- **Option 2**: Point our Ansible playbook to the IP address of the running Vagrant box. In this case we will invoke our playbook when we need it (e.g. after vagrant up is finished).

### **Option 1**: Use Ansible integration with Vagrant

To tell Vagrant that we want to provision the machine with Ansible, we have to modify the **Vagrantfile**:

```bash
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  config.vm.network "private_network", ip: "192.168.56.10"
  
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end
end
```

The `playbook.yml` will then be automatically picked up by Vagrant (use `hosts: all` in the Ansible playbook).

```bash
vagrant up
```

> In case a message is presented which states the VM was already up and configured but not provisioned, execute:
>```bash
> vagrant provision
> ```

Once the VM is UP and provisioned:
- SSH into the VM

```bash
vagrant ssh
```

- Test the HTTP App

```bash
vagrant@vagrant:~$ curl localhost
<h1 style='color:blue'>Hello There!</h1>
```

- Logout

```bash
vagrant@vagrant:~$ logout
```

From the host, test the HTTP App:

```bash
curl 192.168.56.10                              
<h1 style='color:blue'>Hello There!</h1>%
```

### **Option 2**: Point our Ansible playbook to the IP address of the running Vagrant box

#### Get the ssh info from vagrant

To obtain the `IdentityFile` (i.e., the private key for ssh):

```bash
vagrant ssh-config
Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile /home/diego/vagrant/.vagrant/machines/default/virtualbox/private_key
  IdentitiesOnly yes
  LogLevel FATAL
```

#### Configure an inventory file for Ansible
Create an `inventory.yml` file with the following:

```bash
webservers:
  hosts:
    web1:
      ansible_port: 22
      ansible_host: 192.168.56.10
      ansible_user: "vagrant"
      ansible_ssh_private_key_file: "/home/diego/vagrant/.vagrant/machines/default/virtualbox/private_key"
```

Modify the file `playbook.yml`

```yml
  #  hosts: all
  hosts: webservers
```

Execute the playbook:

```bash
ansible-playbook playbook.yml -i inventory.yml
PLAY [nginx gunicorn flask] ***************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************
ok: [web1]

TASK [apt install required packages] ******************************************************************************************************************************************************************************
^[[Aok: [web1]

TASK [Create remote directory] ************************************************************************************************************************************************************************************
ok: [web1]
...
```

### Test the HTTP App
- SSH into the VM

```bash
vagrant ssh
```

- Test the HTTP App

```bash
vagrant@vagrant:~$ curl localhost
<h1 style='color:blue'>Hello There!</h1>
```

- Logout

```bash
vagrant@vagrant:~$ logout
```

From the host, test the HTTP App:

```bash
curl 192.168.56.10                              
<h1 style='color:blue'>Hello There!</h1>%
```

## 8. Destroy All the Virtualbox resources

To clean all:

```bash
vagrant destroy
```
