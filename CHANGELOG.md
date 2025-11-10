# Changelog

## [1.0.8] - 2025-11-10
- Fixed an error on the "Edit Generated Prompt" node  (invalid prompt: {'type': 'prompt_no_outputs', 'message': 'Prompt has no outputs', 'details': '', 'extra_info': {}} )
- Added a "Show Text" node, so folks don't have to install any other custom nodes to run the example workflow (Yeah ComfyUI does NOT have a simple show text node...)
- Updated the workflow example to use my own "Show Text" node

## [1.0.7] - 2025-11-05
- Changed Icon location to my own website as the ComfyUI Registry botched out on any GitHub URL I tried...

## [1.0.6] - 2025-10-30
- Minor changes for registry compliance

## [1.0.5] - 2025-10-30
### Changed
- Added screenshots
- Added workflow examples
- Updated README

## [1.0.4] - 2025-10-30
### Changed
- Save Prompt History now only saves, when the prompt changed, eliminating duplicate prompts in the archive.
- Added screenshots
- Added workflow examples
- Updated README

## [1.0.3] - 2025-10-29
### Changed
- Fixed links in nodes.py to git
- Added CHANGELOG.md
- Simplified __init__.py
- Added package.json for ComfyUI Manager compliance
- Added pyproject.toml for registry compliance

## [1.0.2] - 2025-10-29
### Changed
- Changed "project" to "filename" in load prompt node
- Changed display on info node  
- Changed console output to include ID number
- Updated README
- Fixed Versioning text
- Made print out in console less prominent

## [1.0.1] - 2025-10-22
### Added
- Added "project" back in as a tag that gets stored in the json

## [1.0.0] - 2025-10-20
### Major Changes
- Merged AF Edit Generated Prompt and AF Prompt History Nodes into single pack
- Complete overhauled Load Prompt node