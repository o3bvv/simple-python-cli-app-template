import logging
import logging.config
import socket

from datetime import datetime
from typing import Dict

{% if cookiecutter.logging_time_zone|lower == 'utc' -%}
import pytz
{%- endif %}

{% if cookiecutter.logging_format_json|lower == 'y' -%}
from pythonjsonlogger.jsonlogger import JsonFormatter
{%- endif %}
{% if cookiecutter.logging_time_zone|lower == 'local' -%}
from tzlocal import get_localzone
{%- endif %}

{% if cookiecutter.logging_include_hostname|lower == 'y' -%}
class LogRecordHostnameInjector(logging.Filter):
    _hostname = socket.gethostname()

    def filter(self, record: logging.LogRecord) -> bool:
        record.hostname = self._hostname
        return True
{%- endif %}


class LogRecordFormatter(logging.Formatter):
    """
    Override standard implementation to support both microseconds and TZ.

    See also:
        https://github.com/python/cpython/blob/v3.7.3/Lib/logging/__init__.py#L539-L563
        https://github.com/python/cpython/blob/v3.7.3/Lib/logging/__init__.py#L298
        https://github.com/python/cpython/blob/v3.7.3/Lib/_strptime.py#L457-L494

    """
    converter = datetime.fromtimestamp
    {% if cookiecutter.logging_time_zone|lower == 'local' -%}
    _tz = get_localzone()
    {%- elif cookiecutter.logging_time_zone|lower == 'utc' -%}
    _tz = pytz.UTC
    {%- endif %}

    def formatTime(self, record: logging.LogRecord, datefmt: str=None) -> str:
        ct = self.converter(record.created, self._tz)

        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)

        return s


{% if cookiecutter.logging_format_json|lower == 'y' -%}
class JsonLogRecordFormatter(LogRecordFormatter, JsonFormatter):
    pass
{%- endif %}


def setup_logging(config: Dict) -> None:
    logging.config.dictConfig(config)
