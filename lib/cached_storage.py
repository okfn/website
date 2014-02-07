from django.core.files.storage import get_storage_class
from s3_folder_storage.s3 import StaticStorage


class CachedStaticStorage(StaticStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedStaticStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedStaticStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
