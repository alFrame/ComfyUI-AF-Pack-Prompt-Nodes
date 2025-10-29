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

print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *")
print(r"""
      ＡＦ  －  ＣｏｍｆｙＵＩ  Ｎｏｄｅｓ
                                     
       🚀 AF - Prompt Nodes Pack Loaded!
""")
print("*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * ")