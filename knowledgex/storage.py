from django.utils.deconstruct import deconstructible
from cloudinary_storage.storage import MediaCloudinaryStorage


@deconstructible
class CloudinaryMediaStorage(MediaCloudinaryStorage):
    """Store images as images and documents as raw Cloudinary assets."""

    def _get_resource_type(self, name):
        ext = (name or "").split(".")[-1].lower()
        image_exts = {"jpg", "jpeg", "png", "gif", "webp", "bmp", "svg", "tif", "tiff"}
        if ext in image_exts:
            return "image"
        if ext in {"pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "txt", "zip", "rar"}:
            return "raw"
        return "auto"
