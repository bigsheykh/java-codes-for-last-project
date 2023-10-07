#!/usr/bin/env python3

import json
import git
import os
import subprocess
import csv

from get_set_of_testings import get_set_of_testing

def add_submodule(repo):
    repo_root = git.Repo('.', search_parent_directories=True).working_tree_dir
    repo_root_path = os.path.join(repo_root,"repos")
    data_set_path = "/home/amirreza/Downloads/Duets/dataset"
    path_of_repo_info = os.path.join(data_set_path, repo,"project-info.json")
    repo_owner_and_name = str(repo).split("/")
    repo_owner = repo_owner_and_name[0]
    repo_name = repo_owner_and_name[1]
    if os.path.exists(path_of_repo_info):
        with open(path_of_repo_info) as json_file:
            repo_info = json.load(json_file)
            repo_url:str = repo_info["url"]
            repo_url = repo_url.replace("api.github.com/repos", "github.com")
            repo_father_address = os.path.join(repo_root_path, repo_owner)
            repo_complete_address = os.path.join(repo_father_address, repo_name)
            git_directory = os.path.join(repo_complete_address, ".git")
            if not os.path.exists(git_directory):

                os.makedirs(os.path.join(repo_root_path, repo_owner), exist_ok=True)
                os.makedirs(repo_father_address, exist_ok=True)

                process1 = subprocess.Popen(args=f"git submodule add --name {repo_owner}-{repo_name} {repo_url}.git {repo_name}", cwd=repo_father_address, shell=True)
                process1.wait()
                process3 = subprocess.Popen(args=f"git add {repo_name}", cwd=repo_father_address, shell=True)
                process3.wait()
                process4 = subprocess.Popen(args=f"git commit -m \"add {repo}\"", cwd=repo_father_address, shell=True)
                process4.wait()
            return (repo_owner, repo_name, repo_url, repo_complete_address, path_of_repo_info)
    else:
        print(path_of_repo_info, "doesn't exist")

def add_submodules():
    list_of_testing = list(get_set_of_testing())
    list_of_testing.reverse()
    set_of_repos = set([x[0] for x in list_of_testing])
    repos_info = []
    for repo in set_of_repos:
        repo_info = add_submodule(repo)
        for version in [x[1] for x in list_of_testing if repo == x[0]]:
            repos_info.append({
            "repo":repo, "repo_owner":repo_info[0],
            "repo_name":repo_info[1], "repo_url":repo_info[2],
            "version":version, "repo_complete_address":repo_info[3],
            "path_of_repo_info":repo_info[4]})

    return repos_info

if __name__ == '__main__':
    to_csv = add_submodules()
    keys = to_csv[0].keys()

    with open('people.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)
