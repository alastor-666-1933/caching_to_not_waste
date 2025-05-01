from .caching_mask import caching_mask
from .caching_image import caching_image
from .caching_controlnet import caching_controlnet
from .caching_text import caching_text


NODE_CLASS_MAPPINGS = {
    "caching_controlnet": caching_controlnet,
    "caching_image":      caching_image,
    "caching_mask":       caching_mask,
    "caching_text":       caching_text,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "caching_controlnet": "Caching Controlnet Image to not Waste",
    "caching_image":      "Caching Image to not Waste",
    "caching_mask":       "Caching Mask to not Waste",
    "caching_text":       "Caching Text to not Waste",
}

WEB_DIRECTORY = "."