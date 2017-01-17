# Make sure ansible is installed and setup and configure the hosts file correctly
# To initialize kubernetes use
ansible-playbook -i hosts kube-init.yaml

# To reset kubernetes use
ansible-playbook -i hosts kube-reset.yaml
