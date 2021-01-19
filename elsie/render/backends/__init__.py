from .backend import Backend  # noqa
from .svg.backend import InkscapeBackend  # noqa

try:
    from .cairo.backend import CairoBackend  # noqa
except ImportError:
    pass
