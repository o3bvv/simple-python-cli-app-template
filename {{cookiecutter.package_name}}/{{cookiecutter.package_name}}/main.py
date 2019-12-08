import logging
import sys

{% if cookiecutter.command_line_interface|lower == 'click' %}
from typing import Optional

import click
{%- endif %}

{% if cookiecutter.command_line_interface|lower == 'argparse' %}
from {{ cookiecutter.package_name }}.args import get_arguments_parser
{%- endif %}
from {{ cookiecutter.package_name }}.config import try_to_load_config
from {{ cookiecutter.package_name }}.logging import setup_logging
from {{ cookiecutter.package_name }}.logic import run

LOG = logging.getLogger(__name__)


{% if cookiecutter.command_line_interface|lower == 'click' %}
@click.command()
@click.option(
    '--config_path',
    type=click.Path(dir_okay=False, path_type=str),
    required=False,
    help="Path to config file",
)
@click.option(
    '--config_section_name',
    type=str,
    required=False,
    help="Name of config section to use",
)
def main(
    config_path: Optional[str]=None,
    config_section_name: Optional[str]=None,
) -> int:
{%- elif cookiecutter.command_line_interface|lower == 'argparse' %}
def main() -> int:
    parser = get_arguments_parser()
    args = parser.parse_args()
    {% if 'no' not in cookiecutter.config_file_format|lower -%}
    config_path = args.config_path
    config_section_name = args.config_section_name
    {%- endif %}
{%- endif %}
    {% if 'no' in cookiecutter.config_file_format|lower -%}
    config = try_to_load_config()
    {% else %}
    config = try_to_load_config(config_path, config_section_name)
    {%- endif %}

    setup_logging(config['logging'])

    try:
        LOG.info("{{ cookiecutter.executable_name }} started")
        run()
    except Exception:
        LOG.exception("{{ cookiecutter.executable_name }} failed")
        exit_code = -1
    else:
        LOG.info("{{ cookiecutter.executable_name }} ended")
        exit_code = 0
    finally:
        return exit_code


if __name__ == "__main__":
    sys.exit(main())
