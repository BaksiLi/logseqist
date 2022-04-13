#!/usr/bin/env python
# -*- coding: utf-8 -*-

# read/write config yaml file

from ruamel.yaml import YAML

class GraphDirectory(Enum):
    # GRAPH_ROOT = './'
    GRAPH_ROOT = '../example_graph/'
    JOURNALS_DIRECTORY = 'journal'
    PAGES_DIRECTORY = 'pages'
    ASSETS = 'assets'
    META = 'logseq'
    DELETED_FILES = '.trash'  # this is Obsidian style


def read_configuration_file(file_path: str):
    yaml = YAML(typ='safe')

    # accept only allowed keys
    with open(file_path, 'r') as f:
        configs = yaml.load(f)

    return configs

def write_config_file(file_path: str):
    pass
