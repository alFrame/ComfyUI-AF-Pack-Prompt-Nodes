# ****** ComfyUI - AF Prompt Nodes Pack - Combined Nodes
#
# Creator: Alex Furer - Co-Creator(s): Qwen3, Claude AI, DeepSeek
#
# Description: A lightweight suite of ComfyUI custom nodes for AI prompt management and history tracking.
#
# Repo: https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes
#
# Issues, praise, comment, bugs, improvements: https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/issues
#
# LICENSE: MIT License
#
# Usage: https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/README.md
#
# Feature Requests / Wet Dreams
# -

import json
import os
from datetime import datetime
import folder_paths

# =============================================================================
# AF - Edit Generated Prompt Node
# =============================================================================

class AF_Edit_Generated_Prompt:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "generated_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "readonly": True
                }),
                "manual_or_paste_generated": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
            "optional": {
                "input_text": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "forceInput": True
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "AF - Nodes/AF - Prompt Pack"
    OUTPUT_NODE = True
    
    def process(self, generated_prompt="", manual_or_paste_generated="", input_text=""):
        generated_prompt = generated_prompt or ""
        manual_or_paste_generated = manual_or_paste_generated or ""
        input_text = input_text or ""
        
        if manual_or_paste_generated.strip():
            output = manual_or_paste_generated
        elif input_text.strip():
            output = input_text
        else:
            output = ""
        
        display_text = input_text if input_text else "No input connected"
        
        return {
            "ui": {"generated_prompt": [str(display_text)]},
            "result": (output,)
        }

# =============================================================================
# AF - Save Prompt History Node
# =============================================================================

class AF_Save_Prompt_History:
    def __init__(self):
        self.type = "AF Save Prompt History"
        self.aux_id = "AF-SPH-001"
        self.cnr_id = "prompt-save-history"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": "Prompt-History", "multiline": False}),
                "filename": ("STRING", {"default": "default", "multiline": False}),
                "project": ("STRING", {"default": "default", "multiline": False}),
            },
            "optional": {
                "global_positive": ("STRING", {"forceInput": True}),
                "global_negative": ("STRING", {"forceInput": True}),
                "local_positive": ("STRING", {"forceInput": True}),
                "local_negative": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("global_positive", "global_negative", "local_positive", "local_negative")
    FUNCTION = "save_prompts"
    OUTPUT_NODE = True
    CATEGORY = "AF - Nodes/AF - Prompt Pack"

    def save_prompts(self, directory, filename, project, global_positive="", global_negative="", local_positive="", local_negative=""):      
        json_filename = f"{filename.strip()}.json"
        
        # Get the node pack folder first
        node_dir = os.path.dirname(os.path.abspath(__file__))
        pack_dir = os.path.join(node_dir, directory.strip())
        
        # Try output directory as fallback
        try:
            output_dir = folder_paths.get_output_directory()
            output_path = os.path.join(output_dir, directory.strip())
        except:
            output_path = None
        
        # Prefer node pack directory, fallback to output
        library_path = pack_dir
        if output_path and os.path.exists(output_path):
            library_path = output_path
        
        try:
            os.makedirs(library_path, exist_ok=True)
        except Exception as e:
            print(f"AF Save Prompt History - Error creating directory: {e}")
            return (global_positive, global_negative, local_positive, local_negative)
            
        json_file_path = os.path.join(library_path, json_filename)
        
        existing_data = []
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
                    existing_data = json.load(jsonfile)
                    if not isinstance(existing_data, list):
                        existing_data = []
            except Exception as e:
                existing_data = []
        
        # Clean up prompts: remove trailing newlines but preserve internal ones
        def clean_prompt(prompt):
            if not prompt:
                return ""
            # Remove trailing whitespace and newlines, but preserve internal formatting
            return prompt.rstrip()
        
        # Clean the new prompts
        cleaned_gp = clean_prompt(global_positive)
        cleaned_gn = clean_prompt(global_negative)
        cleaned_lp = clean_prompt(local_positive)
        cleaned_ln = clean_prompt(local_negative)
        
        # Check if prompts are identical to the last entry
        if existing_data:
            last_entry = existing_data[-1]
            if (last_entry.get('global_positive', '') == cleaned_gp and
                last_entry.get('global_negative', '') == cleaned_gn and
                last_entry.get('local_positive', '') == cleaned_lp and
                last_entry.get('local_negative', '') == cleaned_ln):
                # Prompts haven't changed - skip saving
                print(f"AF Save Prompt History - Skipped (no changes detected)")
                return (global_positive, global_negative, local_positive, local_negative)
        
        new_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'project': project.strip(),
            'global_positive': cleaned_gp,
            'global_negative': cleaned_gn,
            'local_positive': cleaned_lp,
            'local_negative': cleaned_ln,
        }
        
        existing_data.append(new_entry)
        
        try:
            with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
                # Pretty formatting with indentation for human readability
                json.dump(existing_data, jsonfile, indent=2, ensure_ascii=False)
            print(f"AF Save Prompt History - Saved to {json_file_path}")
        except Exception as e:
            print(f"AF Save Prompt History - Error writing file: {e}")
            
        return (global_positive, global_negative, local_positive, local_negative)

# =============================================================================
# AF - Load Prompt History Node
# =============================================================================

class AF_Load_Prompt_History:
    """
    Load prompt history from JSON files using an index-based selection.
    
    Usage:
    - Select filename from dropdown
    - Set timestamp_index (0 = newest, 1 = second newest, etc.)
    - Connect outputs to Edit Generated Prompt nodes or CLIP encoders
    - Connect 'info' output to Show Text node to see selection details
    """
    
    _filename_cache = {}
    _timestamp_cache = {}
    _last_directory = "AF-PromptHistory"
    
    def __init__(self):
        self.type = "AF Load Prompt History"
    
    @classmethod
    def get_directory_paths(cls, directory):
        """Get both possible directory paths (output folder takes priority)"""
        paths = []
        
        # Check output folder first (user's working files)
        try:
            output_dir = folder_paths.get_output_directory()
            output_path = os.path.join(output_dir, directory.strip())
            if os.path.exists(output_path):
                paths.append(output_path)
        except:
            pass
        
        # Check node pack folder (bundled defaults)
        node_dir = os.path.dirname(os.path.abspath(__file__))
        pack_path = os.path.join(node_dir, directory.strip())
        if os.path.exists(pack_path):
            paths.append(pack_path)
        
        return paths
    
    @classmethod
    def scan_filenames(cls, directory):
        """Scan directory and cache all available JSON files"""
        print(f"AF Load - Scanning directory: {directory}")
        paths = cls.get_directory_paths(directory)
        found = {}
        
        for path in paths:
            try:
                files = [f for f in os.listdir(path) if f.endswith('.json')]
                for f in files:
                    name = f[:-5]  # Remove .json extension
                    if name not in found:
                        found[name] = {"path": path, "filename": f}
                        print(f"AF Load - Found file: {name}")
            except Exception as e:
                print(f"AF Load - Error scanning {path}: {e}")
        
        print(f"AF Load - Total files found: {len(found)}")
        return found
    
    @classmethod
    def load_timestamps(cls, directory, filename):
        """Load and cache timestamps for a specific file"""
        cache_key = f"{directory}::{filename}"
        
        # Return cached if available
        if cache_key in cls._timestamp_cache:
            return cls._timestamp_cache[cache_key]
        
        # Rebuild filename cache if directory changed
        if directory != cls._last_directory:
            cls._filename_cache = cls.scan_filenames(directory)
            cls._last_directory = directory
        
        if filename not in cls._filename_cache:
            return []
        
        info = cls._filename_cache[filename]
        json_path = os.path.join(info["path"], info["filename"])
        
        print(f"AF Load - Loading timestamps from: {json_path}")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list) or not data:
                return []
            
            # Sort by timestamp (newest first)
            data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # Format: "2025-10-10 | 19:29:22"
            timestamps = [e['timestamp'].replace(' ', ' | ') for e in data if 'timestamp' in e]
            
            # Cache the result
            cls._timestamp_cache[cache_key] = timestamps
            print(f"AF Load - Loaded {len(timestamps)} timestamps")
            return timestamps
            
        except Exception as e:
            print(f"AF Load - Error loading timestamps: {e}")
            return []
    
    @classmethod
    def load_prompt(cls, directory, filename, timestamp):
        """Load prompt data for a specific timestamp"""
        if filename not in cls._filename_cache:
            return None
        
        info = cls._filename_cache[filename]
        json_path = os.path.join(info["path"], info["filename"])
        
        # Convert formatted timestamp back to original format
        orig_ts = timestamp.replace(' | ', ' ')
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Find matching entry
            for entry in data:
                if entry.get('timestamp') == orig_ts:
                    return {
                        "global_positive": entry.get('global_positive', ''),
                        "global_negative": entry.get('global_negative', ''),
                        "local_positive": entry.get('local_positive', ''),
                        "local_negative": entry.get('local_negative', '')
                    }
            return None
            
        except Exception as e:
            print(f"AF Load - Error loading prompt: {e}")
            return None
    
    @classmethod
    def INPUT_TYPES(cls):
        # Initialize cache on first call
        if not cls._filename_cache:
            cls._filename_cache = cls.scan_filenames(cls._last_directory)
        
        filenames = sorted(cls._filename_cache.keys()) if cls._filename_cache else ["none"]
        
        return {
            "required": {
                "directory": ("STRING", {"default": "AF-PromptHistory"}),
                "filename": (filenames,),
                "timestamp_index": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 999, 
                    "step": 1,
                    "display": "number"
                }),
                "tip": ("STRING", {
                    "default": "💡 TIP: Connect 'info' output to Show Text node to see this selection guide!",
                    "multiline": True
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("global_positive", "global_negative", "local_positive", "local_negative", "info")
    FUNCTION = "load_prompts"
    CATEGORY = "AF - Nodes/AF - Prompt Pack"

    def load_prompts(self, directory, filename, timestamp_index, tip=""):
        """
        Main execution function - loads prompts based on index selection
        
        Returns:
            Tuple of (global_positive, global_negative, local_positive, local_negative, info)
            - First 4 outputs: The actual prompts (connect to Edit Generated Prompt or CLIP)
            - Last output 'info': Selection details and timestamp list (connect to Show Text)
        """
        
        print(f"\nAF Load - Executing: dir={directory}, filename={filename}, index={timestamp_index}")
        
        # Update cache if directory changed
        if directory != self._last_directory:
            self._filename_cache = self.scan_filenames(directory)
            self._last_directory = directory
        
        # Load timestamps for selected file
        timestamps = []
        if filename and filename != "none" and filename in self._filename_cache:
            timestamps = self.load_timestamps(directory, filename)
        
        # Get timestamp by index
        selected_timestamp = ""
        if timestamps and 0 <= timestamp_index < len(timestamps):
            selected_timestamp = timestamps[timestamp_index]
        
        # Load actual prompt data
        gp = gn = lp = ln = ""
        
        if selected_timestamp:
            data = self.load_prompt(directory, filename, selected_timestamp)
            if data:
                gp = data["global_positive"]
                gn = data["global_negative"]
                lp = data["local_positive"]
                ln = data["local_negative"]
                print(f"AF Load - ✓ Successfully loaded: ID: {timestamp_index} | {selected_timestamp.replace(' | ', ' ')}")
            else:
                print(f"AF Load - ✗ Failed to load prompt data")
        
        # Build info display text
        info_lines = [
            "═" * 50,
            "  AF - LOAD PROMPT HISTORY",
            "═" * 50,
            f"📄 Filename: {filename}",
            f"📊 Available Timestamps: {len(timestamps)}",
            ""
        ]
        
        if selected_timestamp:
            info_lines.append(f"🔢 SELECTED: [{timestamp_index}] | {selected_timestamp}")
            info_lines.append("")
            info_lines.append("Global Positive:")
            info_lines.append(gp if gp else "(empty)")
            info_lines.append("")
            info_lines.append("Global Negative:")
            info_lines.append(gn if gn else "(empty)")
            info_lines.append("")
            info_lines.append("Local Positive:")
            info_lines.append(lp if lp else "(empty)")
            info_lines.append("")
            info_lines.append("Local Negative:")
            info_lines.append(ln if ln else "(empty)")
        elif timestamps:
            info_lines.append(f"⚠️  Index {timestamp_index} out of range!")
            info_lines.append(f"   Valid range: 0 to {len(timestamps)-1}")
        else:
            info_lines.append("⚠️  No timestamps found in this file")
        
        info_text = "\n".join(info_lines)
        
        return (gp, gn, lp, ln, info_text)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """Force re-evaluation on any input change"""
        import time
        return time.time()

# =============================================================================
# AF - Show Text Node
# =============================================================================

class AF_Show_Text:
    """
    Simple text display node - shows text in a large multiline read-only display.
    Perfect for showing prompt history, info text, or any multiline content.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "No input connected",
                    "readonly": True
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "display_text"
    CATEGORY = "AF - Nodes/AF - Prompt Pack"
    OUTPUT_NODE = True
    
    def display_text(self, text, unique_id=None, extra_pnginfo=None):
        # Return both UI update and pass-through output
        return {
            "ui": {"text": [str(text)]},
            "result": (text,)
        }

# =============================================================================
# AF - Model Switch Node (1-based Rails, 0=AUTO)
# =============================================================================

class AF_Model_Switch:
    """
    Switch between model configurations with dynamic input visibility.
    Uses 1-based indexing: Rail 1, Rail 2, Rail 3, etc.
    Rails 1 and 2 are permanent (connections never lost).
    Rails 3-10 are dynamically added/removed.

    Selected rail: 0 = AUTO (first connected), 1-10 = manual selection
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number_of_rails": ("INT", {
                    "default": 2,
                    "min": 2,
                    "max": 10,
                    "step": 1,
                    "display": "number",
                    "tooltip": "Number of visible rails (2-10)"
                }),
                "selected_rail": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10,
                    "step": 1,
                    "display": "number",
                    "tooltip": "Active rail: 0=AUTO (first connected), 1-10=manual selection"
                }),
                "status": ("STRING", {
                    "default": "💡 Active Rail: auto",
                    "multiline": True,
                    "dynamicPrompts": False
                }),
            },
            "optional": {
                # Rail 1 and Rail 2 are PERMANENT - never removed
                "model_1": ("MODEL",),
                "clip_1": ("CLIP",),
                "vae_1": ("VAE",),
                "model_2": ("MODEL",),
                "clip_2": ("CLIP",),
                "vae_2": ("VAE",),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    RETURN_NAMES = ("model", "clip", "vae")
    FUNCTION = "switch_model"
    CATEGORY = "AF - Nodes/AF - Prompt Pack"
    OUTPUT_NODE = True

    def switch_model(self, number_of_rails, selected_rail, status="", unique_id=None, extra_pnginfo=None, **kwargs):
        # Clamp values to valid ranges
        number_of_rails = max(2, min(10, number_of_rails))
        selected_rail = max(0, min(number_of_rails, selected_rail))

        # Determine actual active rail (1-based throughout!)
        actual_rail = None
        is_auto_mode = (selected_rail == 0)

        if is_auto_mode:
            # AUTO mode - find first rail with data
            for i in range(1, number_of_rails + 1):  # Rails 1 to number_of_rails
                test_model = kwargs.get(f"model_{i}", None)
                if test_model is not None:
                    actual_rail = i
                    print(f"AF Model Switch - AUTO → Rail {actual_rail}")
                    break

            if actual_rail is None:
                # No rails have data, default to rail 1
                actual_rail = 1
                print(f"AF Model Switch - AUTO → No data found, defaulting to Rail 1")

            status_text = f"💡 Active Rail: auto → {actual_rail}"
        else:
            # Manual mode - user selected specific rail (1-based)
            actual_rail = selected_rail
            status_text = f"🎯 Active Rail: {actual_rail}"
            print(f"AF Model Switch - Manual → Rail {actual_rail}")

        # Get selected components using 1-based rail number directly
        model = kwargs.get(f"model_{actual_rail}", None)
        clip = kwargs.get(f"clip_{actual_rail}", None)
        vae = kwargs.get(f"vae_{actual_rail}", None)

        # Final fallback if still no model
        if model is None:
            for i in range(1, number_of_rails + 1):
                test_model = kwargs.get(f"model_{i}", None)
                if test_model is not None:
                    model = test_model
                    clip = kwargs.get(f"clip_{i}", None)
                    vae = kwargs.get(f"vae_{i}", None)
                    print(f"AF Model Switch - Fallback to rail {i}")
                    break

        if model is not None:
            print(f"AF Model Switch - ✓ Outputting Rail {actual_rail} (of 1-{number_of_rails})")
        else:
            print(f"AF Model Switch - ⚠️  No models connected")
            status_text = "⚠️ Active Rail: none (no connections)"

        return {
            "ui": {"status": [status_text]},
            "result": (model, clip, vae)
        }

    @classmethod
    def IS_CHANGED(cls, number_of_rails, selected_rail, **kwargs):
        # Force re-evaluation when inputs change
        return f"{number_of_rails}-{selected_rail}"

# Update NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "AF_Edit_Generated_Prompt": AF_Edit_Generated_Prompt,
    "AF_Save_Prompt_History": AF_Save_Prompt_History,
    "AF_Load_Prompt_History": AF_Load_Prompt_History,
    "AF_Show_Text": AF_Show_Text,
    "AF_Model_Switch": AF_Model_Switch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AF_Edit_Generated_Prompt": "AF - Edit Generated Prompt",
    "AF_Save_Prompt_History": "AF - Save Prompt History",
    "AF_Load_Prompt_History": "AF - Load Prompt History",
    "AF_Show_Text": "AF - Show Text",
    "AF_Model_Switch": "AF - Model Switch",
}
