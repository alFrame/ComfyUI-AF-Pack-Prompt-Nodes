"""
@author: Alex Furer
@title: AF Prompt Nodes Pack
@nickname: AF Prompt Nodes Pack
@description: A collection of prompt management nodes for ComfyUI including prompt editing, history saving, and loading functionality.
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# Tell ComfyUI about our web files
WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

__version__ = "1.0.1"
__author__ = "Alex Furer"
__title__ = "AF Prompt Nodes Pack"
__description__ = "A collection of prompt management nodes for ComfyUI"
__license__ = "MIT"
__changelog__ = [
    "v1.1.1 - Added \"project\" back in as a tag that get's stored in the json",
    "v1.0.0 - Merged AF Edit Generated Prompt and AF Prompt History into single pack",
    "v0.0.17 - Updated the init.py and modified the README (from Edit Generated Prompt)",
    "v0.0.16 - Reorganized metadata to follow ComfyUI standards",
    "v0.0.15 - Fixed an issue with LiteGraph throwing an error about the spacer widgets",
    "v0.0.14 - Initial Git Release (Edit Generated Prompt)",
    "v0.0.02 - Added 4 prompt inputs that save to one CSV line (Prompt History)",
    "v0.0.01 - Initial Version (Prompt History)"
]

print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *")
print(r"""
   ___   ____        _____           ___     __  ______  _  __       __      
  / _ | / __/ ____  / ___/__  __ _  / _/_ __/ / / /  _/ / |/ /__ ___/ /__ ___
 / __ |/ _/  /___/ / /__/ _ \/  ' \/ _/ // / /_/ // /  /    / _ Y _  / -_|_-<
/_/ |_/_/          \___/\___/_/_/_/_/ \_, /\____/___/ /_/|_/\___|_,_/\__/___/
                                     /___/
                                     
                🚀 AF - Prompt Nodes Pack Loaded!
                   
""")
print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *")