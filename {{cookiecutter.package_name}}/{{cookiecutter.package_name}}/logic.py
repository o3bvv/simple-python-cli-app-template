import logging

from {{ cookiecutter.package_name }}.version import __version__

LOG = logging.getLogger(__name__)


def run() -> None:
    LOG.info(
        "hello from {{ cookiecutter.executable_name }} v%s",
        __version__,
    )
