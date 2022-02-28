from setuptools import setup, find_packages  # type: ignore
import os
import re

CACHED_VERSION_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "src", "orp_apps", "_version.py"
)


def get_version() -> str:
    if not os.path.exists(CACHED_VERSION_FILE):
        from git_version import git_version

        return git_version()
    else:
        with open(CACHED_VERSION_FILE) as f:
            match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
            if match:
                return match.group(1)
            else:
                raise ValueError("Invalid version file!")

INSTALL_REQUIRES = [
    'Django<3.3',
    'setuptools>=12',
    'djangorestframework-simplejwt',
    'djangorestframework',
    'django-rest-swagger',
    'django-cors-headers',
    'diskcache',
    'requests',
    'lxml==4.6.3',
    'pyyaml',
    'uritemplate',
    'psycopg2_binary',
    'drf-yasg'
]

TESTS_REQUIRES = [
    'flake8',
    'herodotus',
    'isort',
    'pycodestyle',
    'pydocstyle',
    'pytest-cov',
    'pytest-django',
    'pytest-mock',
    'pytest-pythonpath',
    'pytest-xdist',
    'pytest',
    'unify',
]

setup(
    name='orp_apps',
    # version=get_version(),
    version="0.1.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'testing': TESTS_REQUIRES
    },
)
