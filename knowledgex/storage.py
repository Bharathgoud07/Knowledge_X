import os

from django.utils.deconstruct import deconstructible
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
import cloudinary.api


@deconstructible
class CloudinaryMediaStorage(MediaCloudinaryStorage):
    """
    Store images as image assets and documents as raw assets.
    """

    IMAGE_EXTENSIONS = {
        "jpg", "jpeg", "png", "gif",
        "bmp", "webp", "svg", "tif", "tiff",
    }

    RAW_EXTENSIONS = {
        "pdf", "doc", "docx",
        "ppt", "pptx",
        "xls", "xlsx",
        "txt", "zip", "rar",
    }

    def _get_resource_type(self, name):
        filename = os.path.basename(name).lower()

        for ext in self.IMAGE_EXTENSIONS:
            if f".{ext}" in filename:
                return "image"

        for ext in self.RAW_EXTENSIONS:
            if f".{ext}" in filename:
                return "raw"

        return "auto"

    def url(self, name):
        resource_type = self._get_resource_type(name)

        try:
            resource = cloudinary.api.resource(
                name,
                resource_type=resource_type,
            )
            return resource.get("secure_url")

        except Exception:
            url, _ = cloudinary_url(
                name,
                resource_type=resource_type,
            )
            return url