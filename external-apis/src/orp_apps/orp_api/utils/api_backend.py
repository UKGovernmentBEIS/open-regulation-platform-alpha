# Standard
import logging

# Third Party
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

LOG = logging.getLogger(__name__)


# A reasonable default retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 408, 502, 503, 504],
    method_whitelist=['HEAD', 'GET'],
)

# Instantiate an HTTPAdapter with sane defaults and include retries
adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=retry_strategy)


def create_session() -> Session:
    """Create a Session object."""
    session = Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
