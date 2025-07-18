from .caching_mask import caching_mask
from .caching_image import caching_image
from .caching_controlnet import caching_controlnet
from .caching_text import caching_text
from .caching_condition import caching_condition
from .caching_from_combined_images import caching_from_combined_images
from .caching_clear import caching_clear
from .caching_wildcard_list import caching_wildcard_list

NODE_CLASS_MAPPINGS = {
    "caching_controlnet":           caching_controlnet,
    "caching_image":                caching_image,
    "caching_mask":                 caching_mask,
    "caching_text":                 caching_text,
    "caching_condition":            caching_condition,
    "caching_from_combined_images": caching_from_combined_images,
    "caching_wildcard_list":        caching_wildcard_list,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "caching_controlnet":           "Caching Controlnet Image to not Waste",
    "caching_image":                "Caching Image to not Waste",
    "caching_mask":                 "Caching Mask to not Waste",
    "caching_text":                 "Caching Text to not Waste",
    "caching_condition":            "Caching Conditioning to not Waste",
    "caching_from_combined_images": "Caching Combined Image to not Waste",
    "caching_wildcard_list":        "Caching Wildcard List",
}

WEB_DIRECTORY = "."