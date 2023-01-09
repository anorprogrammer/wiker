import sys
if sys.version_info < (3, 7):
    raise ImportError('Your Python version {0} is not supported by wiker, please install '
                      'Python 3.7+'.format('.'.join(map(str, sys.version_info[:3]))))

from .main import Wiker

__all__ = (
    'Wiker',
    '__version__'
)

__version__ = '0.0.1'
