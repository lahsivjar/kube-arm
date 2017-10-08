# kube-arm

Provides easy deployment for kubernetes cluster on ARM architecture (example Raspberry Pi). The setup is streamlined and automated for the most part and provides developers with hassle free management of the cluser.

## How it works

kube-arm uses [Ansible](http://docs.ansible.com/ansible/latest/index.html) for automating all setup tasks required to get the kubernetes cluster up and running. The core requirements for setting up and managing the cluster are provided by the ansible playbooks.

## Getting Started

### Hardware stuff

* It is recommended to have atleast two nodes for your cluster.
* We recommend installing [HypriotOS](https://blog.hypriot.com/faq/) on each node as it comes pre installed with [Docker](https://www.docker.com/what-docker) and is optimized to run it very well.

### Installing

* Clone kube-arm into a control PC (we will be executing ansible playbooks on this PC)
* Install ansible on the control PC. For installation steps check [ansible docs](http://docs.ansible.com/ansible/latest/intro_installation.html)
* Prepare the hosts file. You can refer to sample [hosts.sample](hosts.sample) for help.
* Run the playbook cluster-start.yaml
```
ansible-playbook -i hosts cluster-start.yaml
```

## Built With

* [kubernetes](https://kubernetes.io) - System for automating deployment, scaling and management of containerized applications
* [kubeadm](https://kubernetes.io/docs/admin/kubeadm/) - Tool for kubernetes administration
* [Ansible](http://docs.ansible.com/ansible/latest/intro.html) - IT automation system

## Tested With

* [Raspberry Pi 3 Model B](https://www.raspberrypi.org) - Single board ARM based computer
* [HypriotOS 4.4.39-hypriotos-v7](https://blog.hypriot.com) - Docker Pirates with ARMed explosives
* [kubernetes client-version 1.8.0, server-version 1.8.0](https://kubernetes.io) - System for automating deployment, scaling and management of containerized applications
* [kubeadm v1.8.0](https://kubernetes.io/docs/admin/kubeadm/) - Tool for kubernetes administration
* [Ansible 2.2.0.0](http://docs.ansible.com/ansible/latest/intro.html) - IT automation system

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

