#!/usr/bin/env python3

import json
import os
import subprocess
import multiprocessing

list_of_all = []
list_of_unpassed = []
counter = 0
with open("extract-dataset/dataset-info.json") as json_file:
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

print([(x[0], x[1]) for x in list_of_all])

print([(x[0], x[1]) for x in list_of_unpassed])


# print(counter)
# print(len(list_of_all))
set_of_testing =  set([(x[3], x[1]) for x in list_of_all] + [(x[3], x[1]) for x in list_of_unpassed])
# print(len(list_of_testing))
# print(list_of_testing)

data_set_path = "/home/amirreza/Downloads/Duets/dataset"
list_of_testing = list(set_of_testing)
list_of_testing.reverse()
# for repo in list_of_testing:
    
#     path_of_repo = os.path.join(data_set_path, repo[0], "commits", repo[1])
#     path_of_pom = os.path.join(data_set_path, repo[0], "commits", repo[1], "pom.xml")
#     path_of_infos = os.path.join(data_set_path, repo[0], "commits", repo[1], "pom.xml")
#     if os.path.exists(path_of_pom) and not "alibaba" in repo[0]:
#         process = subprocess.Popen(args="mvn dependency:resolve", cwd=path_of_repo, shell=True)
#         a = process.wait()
        


# set_of_repos = set([x[0] for x in list_of_testing])
# print(set_of_repos)

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
            os.makedirs(os.path.join("repos", repo_owner), exist_ok=True)
            os.makedirs(os.path.join("repos", repo_owner, repo_name), exist_ok=True)
            repo_relative_address = os.path.join("repos", repo_owner, repo_name, repo[1])
            os.makedirs(repo_relative_address, exist_ok=True)
            print(repo_owner, repo_name, repo_url, repo_relative_address)
            process = subprocess.Popen(args="git submodule add " + repo_url + ".git", cwd=repo_relative_address, shell=True)
            process.wait()
    else:
        print(path_of_repo_info, "doesn't exist")


with multiprocessing.Pool() as pool:
    pool.map(add_submodule, list_of_testing)

# for repo in list_of_testing:

    # print(repo, path_of_repo)
# print(len(set([x[0] for x in list_of_all])))
# print(len(set([x[0] for x in list_of_unpassed])))
# print(len(list_of_unpassed))