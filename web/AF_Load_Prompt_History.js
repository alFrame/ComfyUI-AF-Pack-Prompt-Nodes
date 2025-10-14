import { app } from "/scripts/app.js";

app.registerExtension({
    name: "AF.PromptHistoryLoader",
    
    async nodeCreated(node) {
        if (node.comfyClass === "AF_Load_Prompt_History") {
            setTimeout(() => {
                // Style the tip widget
                const tipWidget = node.widgets?.find(w => w.name === "tip");
                if (tipWidget?.inputEl) {
                    tipWidget.inputEl.readOnly = true;
                    tipWidget.inputEl.style.backgroundColor = "#1a2a3a";
                    tipWidget.inputEl.style.color = "#88ccff";
                    tipWidget.inputEl.style.fontFamily = "monospace";
                    tipWidget.inputEl.style.fontSize = "16px";
                    tipWidget.inputEl.style.cursor = "default";
                    tipWidget.inputEl.style.border = "1px solid #4488cc";
                    tipWidget.inputEl.style.padding = "8px";
                    tipWidget.inputEl.style.resize = "none";
                    tipWidget.inputEl.style.textAlign = "center";
                }
            }, 200);
        }
    },
    
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "AF_Load_Prompt_History") {
            // Add visual feedback when node executes
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                const r = onExecuted?.apply(this, arguments);
                
                // Visual feedback: check if prompts were loaded
                if (message?.result) {
                    const [gp, gn, lp, ln, info] = message.result;
                    
                    // Green tint if prompts loaded, default gray if empty
                    if (gp || gn || lp || ln) {
                        this.boxcolor = "#2a5a2a";
                        console.log("AF Load - ✓ Prompts loaded successfully");
                    } else {
                        this.boxcolor = "#666";
                        console.log("AF Load - ○ No prompts loaded (empty or invalid selection)");
                    }
                    
                    this.setDirtyCanvas(true, true);
                }
                
                return r;
            };
        }
    }
});