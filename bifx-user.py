#!/usr/bin/python3

# Simple script to read a CSV of one user per line
# In the format:
# Username, user id, group id, sudo access, home directory with trailing slash
# Where sudo access is either Y or N
#
# Version 1
# <john.dow@ed.ac.uk>

import csv

# Filename is expected to be accounts.txt living in CWD
filename = 'accounts.txt'

# Read file into a list of dictionaries
with open('accounts.txt', 'rt') as fin:
    cin = csv.DictReader(fin, fieldnames=['uname', 'uid', 'gid', 'sudo', 'homedir'])
    accounts = [row for row in cin]

# Iterate through the list, outputting syntax for each line
for user in accounts:
    # Output user details
    print("/* Add local user for " + user.get('uname') + " */")
    print("!auth.extrapasswd\t mADD(" + user.get('uname') + ")")
    print("auth.pw_uid_" + user.get('uname') + " \t" + user.get('uid'))
    print("auth.pw_gid_" + user.get('uname') + " \t" + user.get('gid'))
    print("auth.pw_dir_" + user.get('uname') + " \t" + user.get('homedir') + user.get('uname'))
    print("auth.pw_shell_" + user.get('uname') + " \t" + "/bin/bash")
    print("/* Store local account passwords in /etc/shadow */")
    print("!auth.pw_passwd_" + user.get('uname') + "\t" + "mSET(x)")
    print("!auth.extragroup\t mADD(" + user.get('uname') + ")")
    print("auth.gr_gid_" + user.get('uname') + "\t " + user.get('gid'))
    print("auth.gr_mem_" + user.get('uname') + "\t " + user.get('uname') + "\n")
    # Check if the user should have su and sudo access
    if user.get('sudo') == "Y":
        print("/* Add su access for " + user.get('uname') + "*/")
        print("!nsu.access\t mADD(" + user.get('uname') + ")")
        print("nsu.access_" + user.get('uname') + "\t allow <" + user.get('uname'))
        print("/* Add sudo access for " + user.get('uname') + "*/")
        print("!sudo.entries\t mADD(" + user.get('uname') + ")")
        print("sudo.entry_" + user.get('uname') + "\t " + user.get('uname') + " ALL=NOPASSWD: ALL\n")

