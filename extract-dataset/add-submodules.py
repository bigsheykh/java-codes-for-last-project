#!/usr/bin/env python3

import json
import git
import os
import subprocess
import multiprocessing

list_of_all = []
list_of_unpassed = []
counter = 0
repo_root = git.Repo('.', search_parent_directories=True).working_tree_dir
data_set_path = os.path.join(repo_root, "extract-dataset/dataset-info.json")
repo_root_path = os.path.join(repo_root,"repos")

with open(data_set_path) as json_file:
    data_set = json.load(json_file)
    for x in data_set:
        y = data_set[x]
        z = "test_results"
        results = y[z]
        # print(results)
        for version in results:
            if len(results[version]) > 2:
                if results[version][1]:
                    if results[version][0]["passing"] + results[version][1]["passing"] + results[version][2]["passing"] > 1050:
                        list_of_all.append((x, version, results[version], data_set[x]["repo_name"]))
                    if results[version][0]["error"] != 0 or results[version][0]["failing"] != 0:
                        list_of_unpassed.append((x, version, results[version], data_set[x]["repo_name"]))
        counter = counter + 1

set_of_testing =  set([(x[3], x[1]) for x in list_of_all] + [(x[3], x[1]) for x in list_of_unpassed])
data_set_path = "/home/amirreza/Downloads/Duets/dataset"
list_of_testing = list(set_of_testing)
list_of_testing.reverse()
set_of_repos = set([x[0] for x in list_of_testing])
        

def add_submodule(repo):
    path_of_repo_info = os.path.join(data_set_path, repo[0],"project-info.json")
    repo_owner_and_name = str(repo[0]).split("/")
    repo_owner = repo_owner_and_name[0]
    repo_name = repo_owner_and_name[1]
    if os.path.exists(path_of_repo_info):
        with open(path_of_repo_info) as json_file:
            repo_info = json.load(json_file)
            repo_url:str = repo_info["url"]
            repo_url = repo_url.replace("api.github.com/repos", "github.com")
            repo_father_address = os.path.join(repo_root_path, repo_owner, repo_name)
            repo_relative_address = os.path.join(repo_father_address, repo[1])
            print(repo_owner, repo_name, repo_url, repo_relative_address)

            os.makedirs(os.path.join(repo_root_path, repo_owner), exist_ok=True)
            os.makedirs(repo_father_address, exist_ok=True)

            process1 = subprocess.Popen(args=f"git submodule add --name {repo_owner}-{repo_name}-{repo[1]} {repo_url}.git {repo[1]}", cwd=repo_father_address, shell=True)
            process1.wait()
            process2 = subprocess.Popen(args=f"git checkout {repo[1]}", cwd=repo_relative_address, shell=True)
            process2.wait()
            process3 = subprocess.Popen(args=f"git add {repo[1]}", cwd=repo_father_address, shell=True)
            process3.wait()
            process4 = subprocess.Popen(args=f"git commit -m \"add {repo[0]} with commit {repo[1]}\"", cwd=repo_father_address, shell=True)
            process4.wait()
    else:
        print(path_of_repo_info, "doesn't exist")


for repo in list_of_testing:
    add_submodule(repo)
    # print(repo, path_of_repo)
# print(len(set([x[0] for x in list_of_all])))
# print(len(set([x[0] for x in list_of_unpassed])))
# print(len(list_of_unpassed))