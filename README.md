# AF - Pack Prompt Nodes

A lightweight suite of ComfyUI custom nodes for AI prompt management and history tracking.

## 📦 What's Included

**[AF - Edit Generated Prompt](#af---edit-generated-prompt)** - Receive LLM-generated prompts and optionally edit them manually  
**[AF - Save Prompt History](#af---save-prompt-history)** - Archive prompts to JSON files with timestamps  
**[AF - Load Prompt History](#af---load-prompt-history)** - Browse and load previous prompts by index

---

## 🚀 Installation

### Via ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "AF - Pack Prompt Nodes"
3. Install

### Manual Installation
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes.git
```

---

## AF - Edit Generated Prompt

**Purpose:** Pipe LLM output through your workflow with optional manual editing.

### How It Works
- **Upper field** (read-only, grayed): Displays incoming prompt from LLM
- **Lower field** (editable): Manual input or edited version
- **Output priority**: Lower field → Upper field → Empty string

- <img width="1890" height="919" alt="image" src="https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/screenshots/AF-Edit_Generated_Prompt_Node.png" />

### Typical Usage
```
[Ollama/LLM Node] → [AF - Edit Generated Prompt] → [CLIP Text Encode]
```

<img width="2095" height="521" alt="image" src="https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/screenshots/AF-Edit_Generated_Prompt_Workflow_Example.png" />

[Download example workflow](https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/example_workflows/AF-Edit_Generated_Prompt.json) (right click -> save as...)

**Key Feature:** Click "Copy Generated Prompt for Editing" to move prompt from upper to lower field for modifications.

---

## AF - Save Prompt History

**Purpose:** Save up to 4 prompts per entry with automatic timestamps.

<img width="1877" height="609" alt="image" src="https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/screenshots/AF-Save_Prompt_History_Node.png" />

### Inputs
- `directory` - Folder name (default: "Prompt-History")
- `filename` - JSON file name (default: "default")
- `project` - Project identifier (stored as metadata in JSON for reference)
- `global_positive/negative` - Main prompts (optional)
- `local_positive/negative` - Secondary prompts (optional)

<img width="1726" height="679" alt="image" src="https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/screenshots/AF-Save_Prompt_History_Workflow_Example.png" />

[Download example workflow](https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/example_workflows/AF-Save_and_Load_Prompt_History.json) (right click -> save as...)

### Where Files Are Saved
1. **Primary:** `ComfyUI/output/{directory}/` (user working files)
2. **Fallback:** `{node_pack_folder}/{directory}/` (bundled defaults)

### Output Format
```json
[
  {
    "timestamp": "2025-10-29 14:32:15",
    "project": "MyProject",
    "global_positive": "your prompt",
    "global_negative": "negative prompt",
    "local_positive": "local detail",
    "local_negative": "local negative"
  }
]
```

**Note:** All prompts are automatically cleaned (trailing whitespace removed, internal formatting preserved). The `project` field is stored for your reference but not used for filtering.

---

## 🔗 Common Workflow Patterns

### AI-Assisted with History Backup with the "AF - Save Prompt History" Node
```
[LLM] → [Edit Prompt] ┬ → [CLIP Encode] → [KSampler]
                      └ → [Save History]
```

## AF - Load Prompt History

**Purpose:** Load saved prompts using index-based time-travel through your history.

<img width="1095" height="945" alt="image" src="https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/screenshots/AF-Load_Prompt_History_Node.png" />

### Quick Reference
```
┌─────────────────────────────────┐
│ AF - Load Prompt History        │
├─────────────────────────────────┤
│ directory: [AF-PromptHistory  ] │
│ filename:  [MyProject        ▼] │
│ timestamp_index: [0           ] │
├─────────────────────────────────┤
│ Outputs:                        │
│ • global_positive               │
│ • global_negative               │
│ • local_positive                │
│ • local_negative                │
│ • info (connect to Show Text!)  │
└─────────────────────────────────┘
```

### How It Works
- **Filename dropdown** - Lists all `.json` files in the directory (without .json extension)
- **Index selection** - Choose which timestamp to load (0 = newest)
- **Info output** - Shows selected prompt content and metadata

<img width="1564" height="935" alt="image" src="https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/screenshots/AF-Load_Prompt_History_Workflow_Example.png" />

[Download example workflow](https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/blob/main/Docs/example_workflows/AF-Save_and_Load_Prompt_History.json) (right click -> save as...)

### Index System
- `0` = Most recent prompt
- `1` = Second most recent
- `2` = Third most recent
- etc.

### Directory Priority
Files in `output/{directory}/` override files in `{node_pack}/{directory}/` with the same name.

### Critical: Connect the Info Output!
Always connect `info` → `Show Text` node to see:
- Currently selected filename and timestamp
- Full content of all 4 prompts being loaded
- Total available timestamps count
- Error messages if index is out of range

### Example Info Display
```
══════════════════════════════════════════════════
  AF - LOAD PROMPT HISTORY
══════════════════════════════════════════════════
📄 Filename: MyProject
📊 Available Timestamps: 205

🔢 SELECTED: [126] | 2025-10-29 | 14:32:15

Global Positive:
A serene mountain landscape at sunset, golden hour lighting...

Global Negative:
ugly, deformed, low quality, blurry

Local Positive:
detailed foreground rocks, wildflowers

Local Negative:
(empty)
```

**Console Output:**
```
AF Load - ✓ Successfully loaded: ID: 126 | 2025-10-29 14:32:15
```

---

## 🔗 Common Workflow Patterns (suggestions)

### "AF - Load Prompt History" Node, Compare Previous Prompts
```
[Load History: index=0] → [Edit] → [CLIP] ┐
[Load History: index=5] → [Edit] → [CLIP] ├→ [KSampler]
[Load History: index=10]→ [Edit] → [CLIP] ┘
```

### Pattern 3: Multi-File Workflow
```
[Load: FileA.json] → [Edit Global+] → ┐
[Load: FileB.json] → [Edit Local+]  → ├→ [CLIP Encode]
[Load: FileC.json] → [Edit Global-] → ┘
```

---

## 🔧 Troubleshooting

### Files not appearing in dropdown
- Check ComfyUI console for cache messages
- Verify `.json` files exist in `output/{directory}/`
- Restart ComfyUI to rebuild cache
- Ensure files end with `.json` extension

### Index out of range
- Connect `info` output to Show Text to see available count
- Example: 205 timestamps = valid indices are 0-204
- The info display shows total count at the top

### Prompts not loading
- Ensure filename is selected (not "none")
- Check timestamp_index is within range (see info output)
- Verify JSON file format matches example above
- Look for error messages in console

### Directory not found
- Use relative path from ComfyUI root e.g.: `AF-PromptHistory`
- Or absolute path: `/full/path/to/directory`
- Check folder exists and has read/write permissions

---

## 💡 Pro Tips

- **Index 0 is your friend** - Always points to newest prompt
- **Info output shows everything** - See exactly what you loaded
- **Console logging** - Check ID and timestamp confirmation
- **Multiple load nodes** - Each can access different files/indices
- **Workflows persist** - Your selections save with the workflow
- **Project field** - Use it as a mental note when saving, great for manual inspection

---

## 📋 Requirements

- ComfyUI (recent version recommended)
- No external dependencies required
- Works with any LLM/text generation nodes, or your manual prompting text nodes

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🐛 Issues & Contributions

Found a bug? Have a feature request?  
→ [GitHub Issues](https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/issues)

---

## ⚠️ Disclaimer

This ComfyUI custom node is developed through AI-assisted coding. While carefully tested, it is provided **"as is" without warranty**. 

**By using this node pack:**
- You install and run at your own risk
- The creator is not liable for damages or data loss
- Compatibility with your setup is not guaranteed
- Test in a safe environment before production use

Report issues on GitHub - we appreciate your feedback!

---

## 📚 Additional Resources

- **[Changelog](CHANGELOG.md)** - Version history and updates
- [GitHub Issues](https://github.com/alFrame/ComfyUI-AF-Pack-Prompt-Nodes/issues) - Report bugs & request features
- [License](LICENSE) - MIT License details

---

**Made with ❤️ by Alex Furer & Qwen3, Claude AI, DeepSeek**
