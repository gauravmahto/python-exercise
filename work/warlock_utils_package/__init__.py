# This signals to python that this directory is package
# This file can be empty

# But below simplifies the imports and makes the package more user-friendly.

from .decorators import Decorator, decorator
from .timing_decorator import timing_decorator
