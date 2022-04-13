#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
from enum import Enum
import re

PAGE_META_DEFAULT = ['title', 'alias']
PAGE_FILE_EXTENSION = '.' + 'md'  # this is the only format allowed so far


class Graph:
    def __init__(self):
        pass

    def read_folder_files(path: str) -> dict:
        # {fpath: content}
        fptoc = {}

        for file_ in listdir(path):
            fpath = join(path, file_)
            if isfile(fpath):
                fptoc[fpath] = Graph.read_file(fpath)

        return fptoc

    def read_file(fpath):
        with open(fpath, 'r') as f:
            text = f.read()

        return text

    def get_orphan_nodes(self):
        pass


class Page:
    """Page is a special form of blocks.
       It can contain multiple blocks at the upper level,
       and saved as a seperate file in the system.
    """
    def __init__(self, title, block_list, metadata={}, file_path=None):
        self.title = title
        self.block_list = block_list
        self.metadata = metadata
        self.file_path = file_path

    def __str__(self):
        return f'{self.title}, {self.metadata}: {self.block_list}'

    @classmethod
    def read_from(cls, file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()

        metadata = Page.retrieve_metadata(file_content)
        title = metadata.get(
            'title',
            file_path.rsplit('/', maxsplit=1)[-1].strip(PAGE_FILE_EXTENSION))

        return cls(title=title,
                   block_list=None,
                   metadata=metadata,
                   file_path=file_path)

    def reread(self):
        new_page = Page.read_from(self.file_path)
        self.title = new_page.title
        self.block_list = new_page.block_list
        self.metadata = new_page.metadata

    @staticmethod
    def retrieve_metadata(text: str) -> dict:
        parsed_properties = []

        # front matter: Start of the page, enclosed by two '---'s
        # syntax is 'property-name: abc'
        regex_front_matter = r'\A-{3}\n(.*\n)+-{3}'
        parsed_front_matter = re.match(regex_front_matter, text).group(0)
        if parsed_front_matter:
            regex_front_matter_syntax = r'(\w+): (.*)'
            parsed_properties += re.findall(regex_front_matter_syntax,
                                            parsed_front_matter)

        # inline: property-name followed by '""'.
        regex_inline_syntax = r'(\w*):: (.*)'
        parsed_inline = re.findall(regex_inline_syntax, text)
        if parsed_inline:
            parsed_properties += parsed_inline


        property_dict = {}
        if parsed_properties:
            # turn [(key, values)] into a dictionary
            for key, value in parsed_properties:
                # title should be unique
                if key == 'title':
                    property_dict[key] = property_dict.get(key, value)
                else:
                    value_list = [
                        one_of_the_value.strip()
                        for one_of_the_value in re.split(r', ?', value)
                    ]
                    property_dict[key] = property_dict.get(key,
                                                           []) + value_list

        return property_dict

    @staticmethod
    def tokenize(text):
        # TODO: improve above use tokenizer
        # remove front matter
        regex_front_matter = r'\A-{3}\n(.*\n)+-{3}\n+'
        text_main = re.sub(regex_front_matter, '', text)

        regex_block_specification = [
            ('LIST', r'- '),
            ('LINE_BREAK', r'\n'),
            ('INDENT', r'( {2}|\t)+'),
            ('CONTENT', r'.*'),
        ]
        regex_block = '|'.join('(?P<%s>%s)' % pair
                               for pair in regex_block_specification)

        tokenized = []
        for ind, matched in enumerate(re.finditer(regex_block, text_main)):
            last_kind = matched.lastgroup
            if last_kind == 'INDENT':
                tokenized.append()
            elif last_kind == 'LIST':
                print(last_kind)
            elif last_kind == 'LINE_BREAK':
                print('\n')
            elif last_kind == 'CONTENT':
                print(last_kind)
            else:
                pass



    @staticmethod
    def get_block_list(text: str) -> list:
        # remove front matter
        regex_front_matter = r'\A-{3}\n(.*\n)+-{3}\n+'
        text_main = re.sub(regex_front_matter, '', text)

        regex_list_syntax = r'([ \t]*)- '
        matched_all = re.finditer(regex_list_syntax, text_main)

        # last_matched = next(matched_all)
        # for matched in matched_all:
        #     matched_marker = text_main[matched.start():matched.end()]
        #     level = matched.end() - matched.start() - 1

        last_match = next(matched_all)
        while last_match is not None:
            print(last_match)
            matched_marker = text_main[last_match.start():last_match.end()]
            level = last_match.end() - last_match.start() - 1
            print(level); print(matched_marker)
            last_match = next(matched_all)


    def get_related_pages(self):
        pass

    def write_to(self, filepath):
        # translate / to -
        # raise NoPageFilePath Error
        pass

    def rename_as(self, filepath):
        pass

    def combine_page_files():
        pass


class Block:
    """Block is the smallest addressable (thus linkable) unit.
       It can contain a child block.
    """
    def __init__(self, content, metadata: {}):
        self.content = content

    @property
    def subblock(self):
        # iterative
        pass

    @staticmethod
    def convert_hanzi():
        pass

    # Use yield
    @staticmethod
    def convert_chinese_space():
        pass

    def get_linked_pages():
        pass
