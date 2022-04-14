#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join
import re
from typing import NamedTuple, Tuple

LOGSEQ_FILE_FORMAT = 'md'  # this is the only format allowed so far
PAGE_FILE_EXTENSION = '.' + LOGSEQ_FILE_FORMAT


class Graph:
    """Graph is a collection of pages.

    It roughly corresponds to the Logseq database.
    """
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
    def __init__(self, title, children_blocks, properties={}, file_path=None):
        self.title = title
        self.children_blocks = children_blocks
        self.properties = properties
        self.file_path = file_path
        # metadata: create-time, create-email, edit-time, edit-email

    def __str__(self):
        return f'{self.title}, {self.properties}: {self.children_blocks}'

    @classmethod
    def read_from(cls, file_path):
        with open(file_path, 'r') as f:
            file_content = f.read()

        properties = Page.get_properties(file_content)
        title = properties.get(
            'title',
            file_path.rsplit('/', maxsplit=1)[-1].strip(PAGE_FILE_EXTENSION))

        return cls(title=title,
                   children_blocks=None,
                   properties=properties,
                   file_path=file_path)

    def reread(self):
        new_page = Page.read_from(self.file_path)
        self.title = new_page.title
        self.children_blocks = new_page.children_blocks
        self.properties = new_page.properties

    @staticmethod
    def parse_front_matter(text: str):
        regex_front_matter_syntax = r'(\w+): (.*)'
        return re.findall(regex_front_matter_syntax, text)

    @staticmethod
    def parse_properties(parsed_properties: [tuple]) -> dict:
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

    def get_properties(text):
        pass

    @staticmethod
    def tokenizer(text: str) -> Tuple[BlockToken]:
        regex_block_specification = [
            ('FRONT_MATTER', r'\A-{3}\n(?P<front_matter>(.*\n)+)-{3}\n+'),
            ('INDENT', r'\t'),
            ('LINE_BREAK', r'\n'),
            ('PROPERTY',
             r'(- |( {2})+)(?P<property_name>\w+):: (?P<property_value>.*)'),
            ('LIST', r'(- ?)(?P<list_line_value>.*)'),  # use (?:...)?
            ('CONTENT_LINE', r'[\t ]+(?P<content_line_value>.*)'),
        ]
        regex_block = '|'.join('(?P<%s>%s)' % pair
                               for pair in regex_block_specification)

        indent_buffer = 0
        for matched in re.finditer(regex_block, text):
            type_ = matched.lastgroup
            value = matched.group()
            # print(type_, indent_buffer)  # DEBUG

            indent_level = 0

            if type_ == 'FRONT_MATTER':
                value = Page.parse_front_matter(matched.group('front_matter'))

            # This part deal with indent and line breaks
            elif type_ == 'INDENT':
                indent_buffer += 1
                continue
            elif type_ == 'LINE_BREAK':
                indent_buffer = 0
                continue

            elif type_ == 'PROPERTY':
                indent_level = indent_buffer
                value = (matched.group('property_name'),
                         matched.group('property_value'))
            elif type_ == 'LIST':
                indent_level = indent_buffer
                value = matched.group('list_line_value')
            elif type_ == 'CONTENT_LINE':
                indent_level = indent_buffer
                value = matched.group('content_line_value')

            yield (BlockToken(type_, value, indent_level, matched.span()))

    @staticmethod
    def retrieve_children_blocks(text, with_confirm=False):
        """From tokenizer
        """
        # token_buffer = ''
        for token in Page.tokenizer(text):
            if with_confirm:
                print(token)
                input()

            # List block = List + Content_line

            # get block lineages by their levels

            # properties: level - applies to the page
            #             level >= 1 applies the their corresponding blocks

    def get_related_pages(self):
        pass

    def combine_page_files():
        pass

    def write_to(self, filepath):
        # translate / to -
        # raise NoPageFilePath Error
        pass

    def rename_as(self, filepath):
        pass


class BlockToken(NamedTuple):
    type_: str
    value: str or (str, str) or list[(str, str)]
    indent_level: int
    span: Tuple[int, int]
    # span: tuple[int, int]  # python 3.9


class Block:
    """Block is the smallest addressable (thus linkable) unit.
       Each block can contain a child block.
    """
    def __init__(self, type_, values, properties: {}):
        self.values = values
        # metadata: uid, edit-time, edit-mail

    @property
    def child_block(self):
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
