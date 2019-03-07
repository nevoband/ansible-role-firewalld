import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_firewalld_is_installed(host):
    firewalld = host.package("firewalld")
    assert firewalld.is_installed
    assert firewalld.version.startswith("0.5")


def test_firewalld_is_running(host):
    firewalld = host.service("firewalld")
    assert firewalld.is_running
    assert firewalld.is_enabled


def test_firewall_rules(host):
    content = [
        "<service name=\"http\"/>",
        "<port protocol=\"tcp\" port=\"4444\"/>",
        "<port protocol=\"tcp\" port=\"80\"/>",
        "<source address=\"127.0.0.1\"/>"
    ]
    file = host.file("/etc/firewalld/zones/public.xml")
    assert file.exists
    for line in content:
        assert file.contains(line)
