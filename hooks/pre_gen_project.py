import re
import sys


PACKAGE_NAME_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

package_name = '{{ cookiecutter.package_name }}'

if not re.match(PACKAGE_NAME_REGEX, package_name):
    print((
        "ERROR: The package name '%s' is not a valid Python package name. "
        "Please do not use a - and use _ instead"
    ) % package_name)
    sys.exit(1)
