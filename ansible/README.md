Notes while building, to be turned into file later:

* hosts file needs to be set up
* user needs to have sudo access
  - use --ask-become-pass if you don't want to make them sudoable without a password
* include section on dns / dnsmasq
  - make an optional ansible section

This was pulled from mediawiki setup:
# Notes before starting:
#
# Set up /etc/ansible/hosts to include any hosts for which you want to
# run this playbook, within a `[mediawiki]` group.  Test that you can
# ping these hosts with ansible and the desired user.  If they are not
# already in known_hosts, you may get an error.  Either add them to
# known_hosts or edit the configuration to ignore that check.  See
# https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html
# for general help with Ansible.

