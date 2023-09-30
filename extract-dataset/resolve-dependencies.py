#!/usr/bin/env python3

import git
import os
import subprocess

repo_root = git.Repo('.', search_parent_directories=True).working_tree_dir

process1 = subprocess.Popen(args="ls repos/*/*/pom.xml", cwd=repo_root, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process1.communicate()

pom_files = out.decode().split()

for pom_relative_address in pom_files:
    pom_address = os.path.join(repo_root, pom_relative_address)
    pom_directory = pom_address[0:-8]
    print(pom_directory)
    process = subprocess.Popen(args="mvn dependency:resolve", cwd=pom_directory, shell=True)
    process.wait()
    process = subprocess.Popen(args="mvn dependency:resolve-plugins", cwd=pom_directory, shell=True)
    process.wait()
