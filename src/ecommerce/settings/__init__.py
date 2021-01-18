from .base import *

# ordering is important - conf override.
from .production import *

try:
    from .local import *
except:
    pass


