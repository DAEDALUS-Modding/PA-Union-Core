#GENERATES A MOD VERSION FOR UNION

import os
import shutil
import json
import sys
from datetime import datetime

import click
#use pip to install this

import copytree_edit

def gen_folder_names():
    folder_names = ['union_license/', 
                        'vanilla_derivative/',
                        'legion_derivative/']
    for i in os.listdir('other_derivative'):
        if os.path.isdir('other_derivative/' + i):
            folder_names.append('other_derivative/' + i + '/')
    return folder_names

def call_paeiou(client, server, folder_names):
    paeiou_dir_in = "PAEIOU_directory.txt"
    if (os.path.isfile(paeiou_dir_in)):
        with open(paeiou_dir_in) as infile:
            paeiou_path = infile.readline()
    else:
        paeiou_path = input("PAEIOU path: ")
        with open(paeiou_dir_in, 'w+') as outfile:
            outfile.write(paeiou_path)
    sys.path.insert(1, paeiou_path)

    import paeiou

    paeiou_input_path = "gen/PAEIOU/in"
    
    for i in [name + "PAEIOU_build" for name in folder_names]:
        if os.path.isdir(i):
            copytree_edit.copytree(i, paeiou_input_path)

    paeiou.direct_function(client, 
                            server, 
                            0, 
                            0, 
                            "com.pa.union", 
                            paeiou_input_path + "/units/", 
                            paeiou_input_path + "/unit_add_list.txt", "gen/PAEIOU/out/", 
                            nmu_path = paeiou_input_path + "/non-managed_units_list.txt",
                            extra_si = paeiou_input_path + "/extra_si/")


def gen_modinfo(buildtype, test):
    with open("modinfo.template.json") as infile:
        modinfo = json.load(infile)

    with open("edit.modinfo.json") as infile:
        extra_info = json.load(infile)

    modinfo["context"] = buildtype
    modinfo["date"] = datetime.today().strftime('%Y-%m-%d')
    modinfo["build"] = extra_info["build"]
    version_data = (str(extra_info["version"]), str(extra_info["subversion"]), str(extra_info["increment"]))
    modinfo["version"] = '.'.join(version_data)
    modinfo["identifier"] += buildtype
    if test:
        modinfo["identifier"] += "_test"

    extra_info["increment"] += 1

    with open("edit.modinfo.json", 'w') as out:
        json.dump(extra_info, out, indent="\t")

    return modinfo

def build(buildtype, test, folder_names):
    for i in [name + buildtype for name in folder_names]:
        if os.path.isdir(i):
            copytree_edit.copytree(i, "gen/" + buildtype)

    with open("gen/" + buildtype + "/modinfo.json", 'w') as out:
        json.dump(gen_modinfo(buildtype, test), out, indent="\t")

@click.command()
@click.option('--client/--no-client', default=True)
@click.option('--server/--no-server', default=True)
@click.option('--test/--prod', default=True)
def main(client, server, test):
    shutil.rmtree("gen")

    folder_names = gen_folder_names()

    call_paeiou(client, server, folder_names)
    folder_names.append("gen/PAEIOU/out/")

    if client:
        build("client", test, folder_names)
    if server:
        build("server", test, folder_names)


if __name__ == '__main__':
    main()
