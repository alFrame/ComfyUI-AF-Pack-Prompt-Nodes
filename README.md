# ComfyUI-AF-Pack-Prompt-Nodes
A collection of prompt management nodes for ComfyUI

---

# 🎉 AF - Load Prompt History - FINAL VERSION

## Clean, Simple, Rock Solid!

No widget update issues, no complexity - just pure functionality.

---

## Node Overview

```
┌─────────────────────────────────┐
│ AF - Load Prompt History        │
├─────────────────────────────────┤
│ directory: [AF-PromptHistory  ] │
│ project:   [Prompt-History   ▼] │
│ timestamp_index: [0           ] │
├─────────────────────────────────┤
│ Outputs (5):                    │
│ • global_positive (STRING)      │
│ • global_negative (STRING)      │
│ • local_positive  (STRING)      │
│ • local_negative  (STRING)      │
│ • info (STRING) - Connect to    │
│   Show Text to see details!     │
└─────────────────────────────────┘
```

---

## How to Use

### **1. Basic Setup**

```
[AF - Load Prompt History]
    ├─ global_positive ──> [AF - Edit Generated Prompt] ──> [CLIP Text Encode]
    ├─ global_negative ──> [AF - Edit Generated Prompt] ──> [CLIP Text Encode]
    ├─ local_positive  ──> [AF - Edit Generated Prompt] ──> [CLIP Text Encode]
    ├─ local_negative  ──> [AF - Edit Generated Prompt] ──> [CLIP Text Encode]
    └─ info ──> [Show Text]
```

### **2. Set Directory**
- Default: `AF-PromptHistory`
- Or use custom path: `/mnt/d/MyPrompts/ProjectA`
- Supports relative or absolute paths

### **3. Select Project**
- Dropdown auto-populates with available `.json` files
- On boot, scans directory and caches projects
- Change directory → cache refreshes automatically

### **4. Choose Timestamp via Index**
- `0` = Newest (most recent)
- `1` = Second newest
- `2` = Third newest
- etc.

### **5. Connect Info Output**
**IMPORTANT:** Connect the `info` output to a **Show Text** node to see:
- Selected timestamp
- List of all available timestamps with indices
- Range validation
- Quick reference guide

---

## Example Info Output

```
══════════════════════════════════════════════════
  AF - LOAD PROMPT HISTORY
══════════════════════════════════════════════════

📂 Project: Prompt-History
📊 Available Timestamps: 4
🔢 Current Index: 0

⏰ SELECTED: 2025-10-13 | 23:47:15

──────────────────────────────────────────────────
Available Timestamps (newest first):
──────────────────────────────────────────────────
► [ 0] 2025-10-13 | 23:47:15
  [ 1] 2025-10-10 | 19:32:32
  [ 2] 2025-10-10 | 19:29:56
  [ 3] 2025-10-10 | 19:29:22
──────────────────────────────────────────────────

💡 TIP: Connect 'info' output to Show Text node
        to see this selection guide!
```

---

## Workflow Patterns

### **Pattern 1: Time Machine Workflow**
Browse your prompt history step by step:
1. Load node with index = 0 (newest)
2. Review prompts in Edit nodes
3. Change index to 1, 2, 3... to go back in time
4. Find the perfect iteration!

### **Pattern 2: A/B Testing**
```
[Load A: index=0] ─┐
                   ├──> [Switch Node] ──> [CLIP Encode]
[Load B: index=5] ─┘
```

### **Pattern 3: Multi-Project Comparison**
```
[Load: ProjectA] ──> [Edit Pos] ──> [Encode]
[Load: ProjectB] ──> [Edit Pos] ──> [Encode]
[Load: ProjectC] ──> [Edit Pos] ──> [Encode]
```

### **Pattern 4: Recommended Setup (Your Workflow)**
```
[Ollama LLM] ──> [AF - Edit Generated Prompt - Pos G] ─┐
                                                        │
[AF - Load Prompt History] ─────────────────────────────┤
    ├──> [AF - Edit Generated Prompt - Pos L] ─────────┤
    ├──> [AF - Edit Generated Prompt - Neg G] ─────────┤
    └──> info ──> [Show Text]                          │
                                                        ▼
                                                  [CLIP Encode]
```

---

## Directory Priority

The node checks paths in this order:

1. **`{ComfyUI}/output/{directory}/`** (user's working files) ← **PRIORITY**
2. **`{node_pack}/{directory}/`** (bundled defaults)

Files in `output/` override defaults with same name.

---

## Features

✅ **Auto-caching** - Scans directory on ComfyUI boot
✅ **Smart refresh** - Rebuilds cache when directory changes
✅ **Index-based** - Simple 0, 1, 2... selection (no dropdown issues!)
✅ **Detailed info** - Connect to Show Text for full details
✅ **Visual feedback** - Node border turns green when prompts loaded
✅ **Persistent state** - Workflow remembers your selections
✅ **Console logging** - Detailed messages for debugging

---

## Console Output

**On Boot:**
```
AF Load - Scanning directory: AF-PromptHistory
AF Load - Found project: Prompt-History
AF Load - Found project: Testing_v53
AF Load - Total projects found: 2
```

**On Execution:**
```
AF Load - Executing: dir=AF-PromptHistory, project=Prompt-History, index=0
AF Load - Loading timestamps from: .../Prompt-History.json
AF Load - Loaded 4 timestamps
AF Load - ✓ Successfully loaded: 2025-10-13 | 23:47:15
```

---

## Troubleshooting

### **Projects not showing in dropdown**
- Check ComfyUI console for cache messages
- Verify `.json` files exist in directory
- Try changing directory text to force refresh
- Restart ComfyUI

### **Index out of range**
- Check `info` output to see valid range
- Example: 4 timestamps = valid indices are 0-3
- Adjust `timestamp_index` accordingly

### **No prompts loading**
- Ensure project is selected (not "none")
- Verify timestamp_index is within range
- Check JSON file format (must be array of objects)
- Look for error messages in console

### **Directory not found**
- Use relative path from ComfyUI root
- Or use absolute path: `/full/path/to/directory`
- Check folder permissions
- Verify folder exists

---

## File Format

Your JSON files should look like this:

```json
[
  {
    "timestamp": "2025-10-13 23:47:15",
    "global_positive": "your prompt here",
    "global_negative": "your negative here",
    "local_positive": "your local prompt",
    "local_negative": "your local negative"
  },
  {
    "timestamp": "2025-10-13 17:05:47",
    "global_positive": "another prompt",
    ...
  }
]
```

The **AF - Save Prompt History** node creates this format automatically! ✨

---

## Pro Tips

💡 **Use Index 0 for Latest** - Always start with 0 to get the newest prompt

💡 **Info Output is Your Friend** - Always connect it to Show Text during setup

💡 **Shameless Plug** - Use with **AF - Edit Generated Prompt** nodes for best results! 😉

💡 **Multiple Load Nodes** - Each can point to different projects/indices

💡 **Save Workflow** - Your selections persist when workflow is saved/loaded

💡 **Console is Helpful** - Check it for detailed loading information

---

## What We Removed (And Why)

❌ **Preview Widgets in Node** - Caused update issues, unreliable
✅ **Clean 5-Output Design** - Connect to what you need, rock solid

This is the **Unix Philosophy**: Do one thing, do it well.

---

**Made with 🔥 by Alex Furer & Claude AI**

*Simple. Clean. Works every time.* ✨

---
