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

## Examples
Most of the playbooks are self explanatory. In this section examples are presented for playbooks which requires some additional steps or parameters to be executed successfully.

1. Install ingress controller (traefik): If `ingress_controller_node` variable is defined in `hosts.ini` when `cluster-init` playbook is run then ingress controller is installed as part of that playbook. It can also be installed separately by:
    1. Define the variable `ingress_controller_node` in `hosts.ini` with the node name on which ingress controller will be installed under `kube:vars` section

        ```
        [kube:vars]
        ingress_controller_node=kube-02
        ```
    2. Run the playbook

        ```
        ansible-playbook -i hosts.ini install-ingress-controller.yaml
        ```
2. Add a new worker node to the cluster
    1. Define the new node in `hosts.ini` under `kube-workers`

        ```
        kube-05 ansible_host=192.168.1.19 ansible_user=pirate
        ```
    2. Run the playbook with the newly added node as target node

        ```
        ansible-playbook -i hosts.ini cluster-scaleup.yaml --extra-vars "TARGET_NODE=kube-05"
        ```
3. Remove a node from the cluster
    1. Run playbook with the name of the node that is to be removed

        ```
        ansible-playbook -i hosts.ini cluster-scaledown.yaml --extra-vars "TARGET_NODE=kube-05"
        ```
    2. Remove the entry for the `TARGET_NODE` from `hosts.ini`
4. `master` or `worker` specfic tasks can be run from a particular playbook using tags `master` and `workers` respectively

    ```
    # Will only reset worker nodes
    ansible-playbook -i hosts_sample.ini cluster-reset.yaml --tags=workers
    ```
    ```
    # Initialize only master node
    ansible-playbook -i hosts.ini cluster-init.yaml --tags=master
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

