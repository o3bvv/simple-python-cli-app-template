import itertools
import shlex
import os
import sys

from pathlib import Path

from setuptools import find_packages
from setuptools import setup

from subprocess import check_output
from typing import List, Optional, Tuple

from {{ cookiecutter.package_name }}.version import __version__


__here__ = Path(__file__).parent.absolute()


def maybe_get_shell_output(command: str) -> str:
    try:
        args = shlex.split(command)
        with open(os.devnull, 'w') as devnull:
            return check_output(args, stderr=devnull).strip().decode()
    except Exception:
        pass


def maybe_get_current_branch_name() -> Optional[str]:
    return maybe_get_shell_output("git rev-parse --abbrev-ref HEAD")


def maybe_get_current_commit_hash() -> Optional[str]:
    return maybe_get_shell_output("git rev-parse --short HEAD")


def parse_requirements(file_path: Path) -> Tuple[List[str], List[str]]:
    requirements, dependencies = list(), list()

    with file_path.open('rt') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith("-e"):
                line = line.split(' ', 1)[1]
                dependencies.append(line)
                line = line.split("#egg=", 1)[1]
                requirements.append(line)
            elif line.startswith("-r"):
                name = Path(line.split(' ', 1)[1])
                path = file_path.parent / name
                subrequirements, subdependencies = parse_requirements(path)
                requirements.extend(subrequirements)
                dependencies.extend(subdependencies)
            else:
                requirements.append(line)

    return requirements, dependencies


README = (__here__ / "README.rst" ).read_text()
CHANGELOG = (__here__ / "CHANGELOG.rst").read_text()

STABLE_BRANCH_NAME = "master"
CURRENT_COMMIT_HASH = maybe_get_current_commit_hash()
CURRENT_BRANCH_NAME = maybe_get_current_branch_name()
IS_CURRENT_BRANCH_STABLE = (CURRENT_BRANCH_NAME == STABLE_BRANCH_NAME)
BUILD_TAG = (
    f".{CURRENT_BRANCH_NAME}.{CURRENT_COMMIT_HASH}"
    if not IS_CURRENT_BRANCH_STABLE and CURRENT_COMMIT_HASH
    else ""
)

REQUIREMENTS_DIR_PATH = __here__ / "requirements"

INSTALL_REQUIREMENTS, INSTALL_DEPENDENCIES = parse_requirements(
    file_path=(REQUIREMENTS_DIR_PATH / "dist.txt"),
)
SETUP_REQUIREMENTS, SETUP_DEPENDENCIES = parse_requirements(
    file_path=(REQUIREMENTS_DIR_PATH / "setup.txt"),
)
TEST_REQUIREMENTS, TEST_DEPENDENCIES = parse_requirements(
    file_path=(REQUIREMENTS_DIR_PATH / "test.txt"),
)

setup(
    name="{{ cookiecutter.package_name }}",
    version=__version__,
    description="{{ cookiecutter.project_short_description }}",
    long_description=README + "\n\n" + CHANGELOG,
    long_description_content_type="text/x-rst",
    keywords="{{ cookiecutter.package_name }}",
{%- if cookiecutter.project_url %}
    url="{{ project_url }}",
{%- endif %}

    namespace_packages=[],
    packages=find_packages(
        include=[
            "{{ cookiecutter.package_name }}",
            "{{ cookiecutter.package_name }}.*",
        ],
    ),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.executable_name }}={{ cookiecutter.package_name }}.main:main',
        ],
    },

    python_requires=">=3.6",
    dependency_links=list(set(itertools.chain(
        INSTALL_DEPENDENCIES,
        SETUP_DEPENDENCIES,
        TEST_DEPENDENCIES,
    ))),
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite="tests",

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    author="{{ cookiecutter.author_name|replace('\"', '\\\"') }}",
    author_email="{{ cookiecutter.author_email }}",

    options={
        'egg_info': {
            'tag_build': BUILD_TAG,
            'tag_date': False,
        },
    },
    zip_safe=False,
)
