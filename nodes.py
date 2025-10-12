# AF Prompt Nodes Pack - Combined Nodes
#
# Creator: Alex Furer - Co-Creator(s): Qwen3, Claude AI, DeepSeek
#
# Description: A collection of prompt management nodes for ComfyUI
#
# Repo: https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes
#
# LICENSE: MIT License
#
# v1.0.0

import csv
import os
from datetime import datetime
import folder_paths

# =============================================================================
# AF Edit Generated Prompt Node
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
    OUTPUT_NODE = False
    
    def process(self, generated_prompt="", manual_or_paste_generated="", input_text=""):
        # Handle None values by converting to empty strings
        generated_prompt = generated_prompt or ""
        manual_or_paste_generated = manual_or_paste_generated or ""
        input_text = input_text or ""
        
        # Determine output - NO ERROR THROWING, just return the manual text or input
        if manual_or_paste_generated.strip():
            output = manual_or_paste_generated
        elif input_text.strip():
            output = input_text
        else:
            # No prompt provided - return empty string to allow continuation
            output = ""
        
        # Send data to JavaScript extension
        display_text = input_text if input_text else "No input connected"
        
        return {
            "ui": {"generated_prompt": [str(display_text)]},
            "result": (output,)
        }

# =============================================================================
# AF Save Prompt History Node
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
                "directory": ("STRING", {"default": "AF-PromptHistory", "multiline": False}),
                "filename": ("STRING", {"default": "prompt_history_4", "multiline": False}),
                "project": ("STRING", {"default": "default", "multiline": False}),
            },
            "optional": {
                "global_positive": ("STRING", {"forceInput": True}),
                "global_negative": ("STRING", {"forceInput": True}),
                "local_positive": ("STRING", {"forceInput": True}),
                # Removed local_negative as requested
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("global_positive", "global_negative", "local_positive")

    FUNCTION = "save_prompts"
    OUTPUT_NODE = True
    CATEGORY = "AF - Nodes/AF - Prompt Pack"

    def save_prompts(self, directory, filename, project, global_positive="", global_negative="", local_positive=""):      
        csv_filename = filename.strip() + ".csv"
        
        try:
            output_dir = folder_paths.get_output_directory()
        except Exception as e:
            my_dir = os.path.dirname(os.path.abspath(__file__))
            comfyui_root = os.path.dirname(os.path.dirname(my_dir))
            output_dir = os.path.join(comfyui_root, "output")
        
        library_path = os.path.join(output_dir, directory.strip())
        
        try:
            os.makedirs(library_path, exist_ok=True)
        except Exception as e:
            return (global_positive, global_negative, local_positive)
            
        csv_file_path = os.path.join(library_path, csv_filename)
        file_exists = os.path.exists(csv_file_path)
        
        try:
            with open(csv_file_path, "a", newline='', encoding='utf-8') as csvfile:
                # Updated fieldnames - removed local_negative
                fieldnames = ['timestamp', 'project', 'global_positive', 'global_negative', 'local_positive']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'project': project.strip(),
                    'global_positive': global_positive.replace('\n', '\\n') if global_positive else '',
                    'global_negative': global_negative.replace('\n', '\\n') if global_negative else '',
                    'local_positive': local_positive.replace('\n', '\\n') if local_positive else '',
                })
                
        except Exception as e:
            pass
            
        return (global_positive, global_negative, local_positive)

# =============================================================================
# AF Load Prompt History Node (Enhanced with dropdowns)
# =============================================================================

class AF_Load_Prompt_History:
    def __init__(self):
        self.type = "AF Load Prompt History"
        self.aux_id = "AF-LPH-001"
        self.cnr_id = "prompt-load-history"
    
    @classmethod
    def INPUT_TYPES(s):
        # Get initial data for dropdowns
        projects = s.get_available_projects()
        
        return {
            "required": {
                "directory": ("STRING", {"default": "AF-PromptHistory", "multiline": False}),
                "filename": ("STRING", {"default": "prompt_history_4", "multiline": False}),
                "project": (projects, {"default": projects[0] if projects else ""}),
                "global_positive": (["Loading..."], {"default": "Loading..."}),
                "global_negative": (["Loading..."], {"default": "Loading..."}),
                "local_positive": (["Loading..."], {"default": "Loading..."}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("global_positive", "global_negative", "local_positive")
    FUNCTION = "load_prompts"
    CATEGORY = "AF - Nodes/AF - Prompt Pack"
    OUTPUT_NODE = True

    @classmethod
    def get_available_projects(cls, directory="AF-PromptHistory", filename="prompt_history_4"):
        """Get list of unique projects from CSV file"""
        try:
            output_dir = folder_paths.get_output_directory()
        except:
            my_dir = os.path.dirname(os.path.abspath(__file__))
            comfyui_root = os.path.dirname(os.path.dirname(my_dir))
            output_dir = os.path.join(comfyui_root, "output")
        
        library_path = os.path.join(output_dir, directory.strip())
        csv_file_path = os.path.join(library_path, filename.strip() + ".csv")
        
        if not os.path.exists(csv_file_path):
            return ["No projects found"]
        
        projects = set()
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    project = row.get('project', '').strip()
                    if project:
                        projects.add(project)
        except Exception as e:
            return [f"Error: {str(e)}"]
        
        project_list = sorted(list(projects))
        return project_list if project_list else ["No projects found"]

    @classmethod
    def get_prompts_by_type(cls, prompt_type, directory="AF-PromptHistory", filename="prompt_history_4", project_filter=""):
        """Get prompts of specific type, optionally filtered by project"""
        try:
            output_dir = folder_paths.get_output_directory()
        except:
            my_dir = os.path.dirname(os.path.abspath(__file__))
            comfyui_root = os.path.dirname(os.path.dirname(my_dir))
            output_dir = os.path.join(comfyui_root, "output")
        
        library_path = os.path.join(output_dir, directory.strip())
        csv_file_path = os.path.join(library_path, filename.strip() + ".csv")
        
        if not os.path.exists(csv_file_path):
            return ["No prompts found"]
        
        prompts = set()
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Filter by project if specified
                    if project_filter and row.get('project', '').strip() != project_filter:
                        continue
                    
                    prompt = row.get(prompt_type, '').strip()
                    if prompt:
                        # Restore newlines from CSV storage
                        prompt = prompt.replace('\\n', '\n')
                        # Truncate very long prompts for dropdown display
                        if len(prompt) > 100:
                            display_prompt = prompt[:97] + "..."
                        else:
                            display_prompt = prompt
                        prompts.add((prompt, display_prompt))
        except Exception as e:
            return [f"Error: {str(e)}"]
        
        # Convert to list and sort by display text
        prompt_list = sorted(list(prompts), key=lambda x: x[1])
        # Return as simple list of display texts for dropdown
        return [display for _, display in prompt_list] if prompt_list else ["No prompts found"]

    def load_prompts(self, directory, filename, project, global_positive, global_negative, local_positive):
        """
        Return the selected prompts
        """
        # For now, just return the selected values
        # The actual prompt text is what was selected in the dropdown
        return (global_positive, global_negative, local_positive)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
        
# =============================================================================
# Node Mappings
# =============================================================================

NODE_CLASS_MAPPINGS = {
    "AF_Edit_Generated_Prompt": AF_Edit_Generated_Prompt,
    "AF_Save_Prompt_History": AF_Save_Prompt_History,
    "AF_Load_Prompt_History": AF_Load_Prompt_History,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AF_Edit_Generated_Prompt": "AF - Edit Generated Prompt",
    "AF_Save_Prompt_History": "AF - Save Prompt History", 
    "AF_Load_Prompt_History": "AF - Load Prompt History",
}