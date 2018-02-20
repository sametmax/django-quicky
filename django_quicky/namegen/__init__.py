import pkg_resources
pkg_resources.declare_namespace(__name__)

from .namegen import NameGenerator
namegen = NameGenerator()
