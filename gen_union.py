#GENERATES A MOD VERSION FOR UNION

import os
import shutil
import json
from datetime import datetime
import click
import copytree_edit


def gen_modinfo(buildtype, test):
    with open("modinfo.template.json") as infile:
        modinfo = json.load(infile)

    with open("edit.modinfo.json") as infile:
        extra_info = json.load(infile)

    modinfo["date"] = datetime.today().strftime('%Y-%m-%d')
    modinfo["build"] = extra_info["build"]
    version_data = (str(extra_info["version"]), str(extra_info["subversion"]), str(extra_info["increment"]))
    modinfo["version"] = '.'.join(version_data)
    modinfo["identifier"] += buildtype
    if test:
        modinfo["identifier"] += "_test"

    extra_info["increment"] += 1

    with open("edit.modinfo.json", 'w') as out:
        json.dump(extra_info, out)

    return modinfo

def build(buildtype, test):
    folder_names = ['union_license/', 
                    'vanilla_derivative/',
                    'legion_derivative/']
    for i in os.listdir('other_derivative'):
        if os.path.isdir('other_derivative/' + i):
            folder_names.append('other_derivative/' + i + '/')
    

    for i in [name + buildtype for name in folder_names]:
        copytree_edit.copytree(i, "gen/" + buildtype)

    with open("gen/" + buildtype + "/modinfo.json", 'w') as out:
        json.dump(gen_modinfo(buildtype, test), out)

@click.command()
@click.option('--client/--no-client', default=True)
@click.option('--server/--no-server', default=True)
@click.option('--test/--prod', default=True)
def main(client, server, test):
    if client:
        build("client", test)
    if server:
        build("server", test)


if __name__ == '__main__':
    main()
