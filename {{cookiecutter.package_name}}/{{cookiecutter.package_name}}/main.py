from {{ cookiecutter.package_name }}.version import __version__


def run() -> None:
    print("Hello from {{ cookiecutter.executable_name }} v%s" % __version__)


if __name__ == "__main__":
    run()
