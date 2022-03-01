import re
import subprocess
from logging import getLogger

LOG = getLogger(__name__)


def git_version() -> str:
    """Get the version using git describe"""

    # http://www.python.org/dev/peps/pep-0386/
    _PEP386_SHORT_VERSION_RE = r'\d+(?:\.\d+)+(?:(?:[abc]|rc)\d+(?:\.\d+)*)?'

    _GIT_DESCRIPTION_RE = r'^v(?P<ver>%s)-(?P<commits>\d+)-g(?P<sha>[\da-f]+)$' % (
        _PEP386_SHORT_VERSION_RE)

    # Try and determine the version from git
    cmd = 'git describe --tags --long --match v[0-9]*.*'.split()

    try:
        git_description = subprocess.check_output(cmd).decode().strip()
    except subprocess.CalledProcessError:
        LOG.exception('Unable to get version number from git tags')
        return '0.0'

    desc_match = re.search(_GIT_DESCRIPTION_RE, git_description)
    if not desc_match:
        LOG.exception('Git description (%s) is not a valid PEP386 version' %
                         (git_description,))

    commits = int(desc_match.group('commits'))
    if not commits:
        version = desc_match.group('ver')
    else:
        version = '%s.dev%d+git.%s' % (
            desc_match.group('ver'),
            commits,
            desc_match.group('sha')
        )

    return version


if __name__ == "__main__":
    print(git_version())
