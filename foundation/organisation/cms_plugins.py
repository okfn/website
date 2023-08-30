from cms.extensions.extension_pool import extension_pool

from .models import SideBarExtension


extension_pool.register(SideBarExtension)
