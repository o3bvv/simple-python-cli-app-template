#!/usr/bin/env python

import os


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if "{{ cookiecutter.create_author_file }}" != 'y':
        remove_file('AUTHORS.rst')

    if "{{ cookiecutter.command_line_interface|lower }}" != 'argparse':
        args_file = os.path.join('{{ cookiecutter.package_name }}', 'args.py')
        remove_file(args_file)

    if 'no' in "{{ cookiecutter.config_file_format|lower }}":
        utils_file = os.path.join('{{ cookiecutter.package_name }}', 'utils.py')
        remove_file(utils_file)
