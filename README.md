# kube-arm

Provides easy deployment for kubernetes cluster on ARM architecture (example Raspberry Pi). The setup is streamlined and automated for the most part and provides developers with hassle free management of the cluster.

## How it works

kube-arm uses [Ansible](http://docs.ansible.com/ansible/latest/index.html) for automating all setup tasks required to get the kubernetes cluster up and running. The core requirements for setting up and managing the cluster are provided by the ansible playbooks.

## Getting Started

### Setting up hardware

* It is recommended to have atleast two nodes for your cluster.
* We recommend installing [HypriotOS](https://blog.hypriot.com/getting-started-with-docker-on-your-arm-device/) on each node as it comes pre installed with [Docker](https://www.docker.com/what-docker) and is optimized to run it very well.
* If you are using something other than HypriotOS then you must setup docker-engine for each node.
* [Optional] After OS has been flashed configure the host name on each node.
* Setup ssh keys for all nodes:
  * Generate public/private rsa key pair for each node.
  * Copy control PC public ssh key to each node.
```
# Copy for all nodes
ssh-copy-id pirate@<node-ip>
```

### Initialising kubernetes cluster using kube-arm 

* Clone kube-arm into a control PC (we will be executing ansible playbooks on this PC).
* Install ansible on the control PC. For installation steps check [ansible docs](http://docs.ansible.com/ansible/latest/intro_installation.html).
* Prepare the hosts.ini file. You can refer to sample [hosts](hosts_sample.ini) for help.
* Run the playbook cluster-init.yaml:
```
ansible-playbook -i hosts.ini cluster-init.yaml
```

## Built With

* [kubernetes](https://kubernetes.io) - System for automating deployment, scaling and management of containerized applications
* [kubeadm](https://kubernetes.io/docs/admin/kubeadm/) - Tool for kubernetes administration
* [Ansible](http://docs.ansible.com/ansible/latest/intro.html) - IT automation system

## Tested With

* [Raspberry Pi 3 Model B](https://www.raspberrypi.org) - Single board ARM based computer
* [HypriotOS v1.5.0](https://blog.hypriot.com) - Docker Pirates with ARMed explosives
* [kubernetes client-version 1.8.0, server-version 1.8.0](https://kubernetes.io) - System for automating deployment, scaling and management of containerized applications
* [kubeadm v1.8.0](https://kubernetes.io/docs/admin/kubeadm/) - Tool for kubernetes administration
* [Ansible 2.4.0.0](http://docs.ansible.com/ansible/latest/intro.html) - IT automation system

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

