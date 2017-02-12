# Make sure ansible is installed and setup and configure the hosts file correctly
# To initialize kubernetes use
ansible-playbook -i hosts init-main.yaml

# To reset kubernetes use
ansible-playbook -i hosts stop-main.yaml
