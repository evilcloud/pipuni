#!/usr/local/bin/python3

import os
from pick import pick
import pkg_resources
import subprocess

quit = "...quit"
individual = "Individual packages"
# multiple = "Muli-selection"
m_seen = "Seen buffer"
# deleted = "Deleted packages"
main = "... main menu"
option = main


def get_pip():
    """returns list of installed pip packages"""
    packages = [p.project_name for p in pkg_resources.working_set]
    return packages


def pip_uninstall(pack_list):
    """picker for package. runs system processes for pip show and pip uninstall. returns picked option"""
    pack_list.insert(0, main)
    option, _ = pick(pack_list, "Pick a package to unstall")
    if option == main:
        return
    subprocess.call(["pip", "show", option])
    subprocess.call(["pip", "uninstall", option])
    return option


def seen_not_deleted(seen_packages):
    """returns pip packages that are installed and are part of seen_packages list"""
    packages = get_pip()
    return [package for package in packages if package in seen_packages]


def indi(seen_packages):
    """lists with individual packages, only first seeing"""
    while True:
        packages = get_pip()
        unseen_packages = [
            package for package in packages if package not in seen_packages
        ]
        package = pip_uninstall(unseen_packages)
        seen_packages.append(package)
        if not package:
            return seen_not_deleted(seen_packages)


def multi():
    pass


def seen(seen_packages):
    """lists and lets manage packages from seen_packages list"""
    while True:
        package = pip_uninstall(seen_not_deleted(seen_packages))
        if not package:
            return


seen_packages = []
while True:
    if option == main:
        menu_items = [quit, individual, m_seen]
        title = "Main menu:"
    if option == quit:
        print("Bye...")
        break
    if option == individual:
        seen_packages = indi(seen_packages)
        option = main
    if option == m_seen:
        seen(seen_packages)
    option, _ = pick(menu_items, title)
