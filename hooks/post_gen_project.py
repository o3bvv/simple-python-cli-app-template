#!/usr/bin/env python

import os
import shutil


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(file_path):
    os.remove(os.path.join(PROJECT_DIRECTORY, file_path))


def remove_dir(dir_path):
    shutil.rmtree(dir_path)


SUPPORTED_CONFIG_FORMATS = {'yaml', 'json', }
CONFIG_EXAMPLES_DIR_NAME = "examples"


if __name__ == '__main__':

    if "{{ cookiecutter.create_author_file }}" != 'y':
        remove_file('AUTHORS.rst')

    if "{{ cookiecutter.command_line_interface|lower }}" != 'argparse':
        args_file = os.path.join('{{ cookiecutter.package_name }}', 'args.py')
        remove_file(args_file)

    config_file_format = "{{ cookiecutter.config_file_format|lower }}"
    if 'no' in config_file_format:
        utils_file = os.path.join('{{ cookiecutter.package_name }}', 'utils.py')
        remove_file(utils_file)

        config_examples_dir = os.path.join(CONFIG_EXAMPLES_DIR_NAME)
        remove_dir(config_examples_dir)
    else:
        for item in (SUPPORTED_CONFIG_FORMATS - {config_file_format, }):
            example_config_file = os.path.join(
                CONFIG_EXAMPLES_DIR_NAME,
                f'config.{item}',
            )
            remove_file(example_config_file)
