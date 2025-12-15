# Changelog

### 1.1.0
- Added the "Model Switch" node
- Updated README
- Cleaned up the CHANGELOG to meet standard

### v1.0.9
- Added "Show Text" node documentation
- Added a video about the "Edit Generated Prompt" node
- Updated the workflow example to use my own "Show Text" node

### v1.0.8
- Fixed an error on the "Edit Generated Prompt" node  ( invalid prompt: {'type': 'prompt_no_outputs', 'message': 'Prompt has no outputs', 'details': '', 'extra_info': {}} )
- Added a "Show Text" node, so folks don't have to install any other custom nodes to run the example workflow (Yeah ComfyUI does NOT have a simple show text node...)

### v1.0.7
- Changed Icon location to my own website as the ComfyUI Registry botched out on any GitHub URL I tried...

### v1.0.6
- Minor changes for registry compliance

### v1.0.5
- Added screenshots
- Added workflow examples
- Updated README

### v1.0.4
- Save Prompt History now only saves, when the prompt changed, eliminating duplicate prompts in the archive.
- Added screenshots
- Added workflow examples
- Updated README

### v1.0.3
- Fixed links in nodes.py to git
- Added CHANGELOG.md
- Simplified __init__.py
- Added package.json for ComfyUI Manager compliance
- Added pyproject.toml for registry compliance

### v1.0.2
- Changed "project" to "filename" in load prompt node
- Changed display on info node  
- Changed console output to include ID number
- Updated README
- Fixed Versioning text
- Made print out in console less prominent

### v1.0.1
- Added "project" back in as a tag that gets stored in the json

### v1.0.0
- Merged AF Edit Generated Prompt and AF Prompt History Nodes into single pack
- Complete overhauled Load Prompt node
