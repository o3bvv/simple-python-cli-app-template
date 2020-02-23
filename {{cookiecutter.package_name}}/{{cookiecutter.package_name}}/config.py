import copy
import os

from typing import Dict
from typing import Optional

{% if cookiecutter.config_file_format|lower == 'yaml' -%}
import yaml
{%- elif cookiecutter.config_file_format|lower == 'json' -%}
import json
{%- endif %}

from jsonschema import validate

from {{ cookiecutter.package_name }}.exceptions import {{ cookiecutter.class_name_prefix }}Exception
{% if 'no' not in cookiecutter.config_file_format|lower -%}
from {{ cookiecutter.package_name }}.utils import update_nested_dict
{%- endif %}


class ConfigLoadingException({{ cookiecutter.class_name_prefix }}Exception):
    pass


{% if 'no' not in cookiecutter.config_file_format|lower -%}
class InvalidConfigFilePathError(ConfigLoadingException, ValueError):
    pass
{%- endif %}


_CONFIG_SCHEMA = {
    'type': 'object',
    'required': [
        'logging',
    ],
    'properties': {
        'logging': {
            'type': 'object',
        },
    },
}


_CONFIG_DEFAULTS = {
    'logging': {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'generic': {
                '()': "{{ cookiecutter.package_name }}.logging.LogRecordFormatter",
                'format': "%(asctime)s [%(levelname).1s] [{% if cookiecutter.logging_include_hostname|lower == 'y' %}%(hostname)s {% endif %}%(process)s %(threadName)s] %(message)s",
                'datefmt': "%Y-%m-%d %H:%M:%S.%f %z",
            },
            {% if cookiecutter.logging_format_json|lower == 'y' -%}
            'json': {
                '()': "{{ cookiecutter.package_name }}.logging.JsonLogRecordFormatter",
                'format': "(asctime) (levelname) {% if cookiecutter.logging_include_hostname|lower == 'y' %}(hostname) {% endif %}(process) (threadName) (message)",
                'datefmt': "%Y-%m-%d %H:%M:%S.%f %z",
            },
            {%- endif %}
        },
        {% if cookiecutter.logging_include_hostname|lower == 'y' -%}
        'filters': {
            'hostname_injector': {
                '()': "{{ cookiecutter.package_name }}.logging.LogRecordHostnameInjector",
            },
        },
        {%- endif %}
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': '{%- if cookiecutter.logging_format_json|lower == 'y' %}json{% else %}generic{% endif %}',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                {% if cookiecutter.logging_include_hostname|lower == 'y' -%}
                'filters': [
                    'hostname_injector',
                ],
                {%- endif %}
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    },
}


_CONFIG_ENV_VARS_MAP = {
    'logging': {
        'formatters': {
            'generic': {
                'format': "{{ cookiecutter.env_var_name_prefix }}_GENERIC_LOG_RECORD_FMT",
                'datefmt': "{{ cookiecutter.env_var_name_prefix }}_GENERIC_LOG_DATE_FMT",
            },
            {% if cookiecutter.logging_format_json|lower == 'y' -%}
            'json': {
                'format': "{{ cookiecutter.env_var_name_prefix }}_JSON_LOG_RECORD_FMT",
                'datefmt': "{{ cookiecutter.env_var_name_prefix }}_JSON_LOG_DATE_FMT",
            },
            {%- endif %}
        },
    },
}

{% if 'no' not in cookiecutter.config_file_format|lower -%}
def _maybe_override_from_file(
    config: Dict,
    file_path: Optional[str]=None,
    section_name: Optional[str]=None,
) -> None:

    if not file_path:
        return

    if not os.path.isfile(file_path):
        raise InvalidConfigFilePathError("config path must point to a file")

    with open(file_path, 'rt') as f:
        {% if cookiecutter.config_file_format|lower == 'yaml' -%}
        overrides = yaml.safe_load(f)
        {%- elif cookiecutter.config_file_format|lower == 'json' -%}
        overrides = json.load(f)
        {%- endif %}

    if overrides and section_name:
        overrides = overrides[section_name]

    if overrides:
        update_nested_dict(config, overrides)
{%- endif %}


def _maybe_override_log_record_format_from_env(config: Dict, formatter_name: str) -> None:
    value = os.environ.get(_CONFIG_ENV_VARS_MAP['logging']['formatters'][formatter_name]['format'])
    if value:
        config['logging']['formatters'][formatter_name]['format'] = value


def _maybe_override_log_date_format_from_env(config: Dict, formatter_name: str) -> None:
    value = os.environ.get(_CONFIG_ENV_VARS_MAP['logging']['formatters'][formatter_name]['datefmt'])
    if value:
        config['logging']['formatters'][formatter_name]['datefmt'] = value


def _maybe_override_logging(config: Dict) -> None:
    _maybe_override_log_record_format_from_env(config, 'generic')
    _maybe_override_log_date_format_from_env(config, 'generic')
    {% if cookiecutter.logging_format_json|lower == 'y' -%}
    _maybe_override_log_record_format_from_env(config, 'json')
    _maybe_override_log_date_format_from_env(config, 'json')
    {%- endif %}


def _maybe_override_from_env(config: Dict) -> None:
    _maybe_override_logging(config)

{% if 'no' in cookiecutter.config_file_format|lower -%}
def try_to_load_config(
    # extra params passed from CLI args
) -> Dict:
{% else %}
def try_to_load_config(
    file_path: Optional[str]=None,
    section_name: Optional[str]=None,
    # extra params passed from CLI args
) -> Dict:
{%- endif %}
    config = copy.deepcopy(_CONFIG_DEFAULTS)
    {% if 'no' not in cookiecutter.config_file_format|lower -%}
    _maybe_override_from_file(config, file_path, section_name)
    {%- endif %}
    # override from CLI args if passed as extra params
    _maybe_override_from_env(config)
    validate(config, _CONFIG_SCHEMA)
    return config
