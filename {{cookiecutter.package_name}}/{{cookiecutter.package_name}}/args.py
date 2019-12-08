import argparse


def get_arguments_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="{{ cookiecutter.project_short_description }}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    {% if 'no' not in cookiecutter.config_file_format|lower -%}
    parser.add_argument(
        '--config_path',
        dest='config_path',
        type=str,
        help="path to config file",
    )

    parser.add_argument(
        '--config_section_name',
        dest='config_section_name',
        default=None,
        type=str,
        help="name of config section to use",
    )
    {%- endif %}

    return parser
