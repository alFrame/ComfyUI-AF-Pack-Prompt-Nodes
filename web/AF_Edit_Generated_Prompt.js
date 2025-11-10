import { app } from "/scripts/app.js";

app.registerExtension({
    name: "AF.PromptNodes",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "AF_Edit_Generated_Prompt") {
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                const r = onExecuted ? onExecuted.apply(this, arguments) : undefined;
                
                // Update generated prompt display
                let displayText = "";
                if (message.ui && message.ui.generated_prompt) {
                    displayText = message.ui.generated_prompt[0] || "";
                } else if (message.generated_prompt) {
                    displayText = message.generated_prompt[0] || "";
                }
                
                if (displayText) {
                    let displayWidget = this.widgets?.find(w => w.name === "generated_prompt");
                    if (displayWidget) {
                        displayWidget.value = displayText;
                        this.setDirtyCanvas(true, true);
                    }
                }
                
                return r;
            };
        }

		// Update the onExecuted handler for Show Text node
		if (nodeData.name === "AF_Show_Text") {
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				const r = onExecuted ? onExecuted.apply(this, arguments) : undefined;
				
				// Update text display
				let displayText = "";
				if (message.ui && message.ui.text) {
					displayText = message.ui.text[0] || "";
				} else if (message.text) {
					displayText = message.text[0] || "";
				}
				
				if (displayText) {
					let displayWidget = this.widgets?.find(w => w.name === "text");
					if (displayWidget) {
						displayWidget.value = displayText;
						this.setDirtyCanvas(true, true);
					}
				}
				
				return r;
			};
		}
	},
    
    async nodeCreated(node, app) {
        if (node.comfyClass === "AF_Edit_Generated_Prompt") {
            // Wait for widgets to be properly initialized
            setTimeout(() => {
                // Make generated_prompt readonly
                const displayWidget = node.widgets?.find(w => w.name === "generated_prompt");
                if (displayWidget) {
                    displayWidget.options = displayWidget.options || {};
                    displayWidget.options.readonly = true;
                    
                    if (displayWidget.inputEl) {
                        displayWidget.inputEl.readOnly = true;
                        displayWidget.inputEl.style.cursor = "text";
                        displayWidget.inputEl.style.color = "#888888"; // Gray text
                        displayWidget.inputEl.style.opacity = "0.7"; // Slightly transparent
                        
                        displayWidget.inputEl.addEventListener('keydown', function(e) {
                            const allowedKeys = [
                                'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
                                'Home', 'End', 'PageUp', 'PageDown'
                            ];
                            
                            const isCtrlKey = e.ctrlKey || e.metaKey;
                            const allowedCtrlKeys = ['a', 'c', 'x'];
                            
                            if (allowedKeys.includes(e.key) || 
                                (isCtrlKey && allowedCtrlKeys.includes(e.key.toLowerCase()))) {
                                return;
                            }
                            
                            e.preventDefault();
                            e.stopPropagation();
                        });
                    }
                }
                
                // Add some spacer widgets for padding - FIX: Add empty callback to prevent console warning
                const spacerTop = node.addWidget("text", "spacer_top", "", () => {});
                spacerTop.computeSize = () => [0, 10]; // Empty widget with 10px height
                spacerTop.draw = () => {}; // Don't draw anything
                
                // Add copy button and immediately set its properties
                const copyButton = node.addWidget("button", "copy_button", "", () => {
                    const sourceWidget = node.widgets?.find(w => w.name === "generated_prompt");
                    const targetWidget = node.widgets?.find(w => w.name === "manual_or_paste_generated");
                    
                    if (sourceWidget && targetWidget && sourceWidget.value) {
                        targetWidget.value = sourceWidget.value;
                        if (targetWidget.inputEl) {
                            targetWidget.inputEl.value = sourceWidget.value;
                        }
                        if (targetWidget.callback) {
                            targetWidget.callback(targetWidget.value, targetWidget, node);
                        }
                        node.setDirtyCanvas(true, true);
                    }
                });
                
                // Set the button label after creation
                copyButton.label = "  Copy Generated Prompt for Editing "; // Add spaces for padding
                copyButton.name = "copy_button";
                
                // Add bottom spacer - FIX: Add empty callback to prevent console warning
                const spacerBottom = node.addWidget("text", "spacer_bottom", "", () => {});
                spacerBottom.computeSize = () => [0, 10]; // Empty widget with 10px height
                spacerBottom.draw = () => {}; // Don't draw anything
                
            }, 50);
        }
		
		// Handle Show Text node creation
		if (node.comfyClass === "AF_Show_Text") {
			setTimeout(() => {
				const displayWidget = node.widgets?.find(w => w.name === "text");
				if (displayWidget?.inputEl) {
					displayWidget.inputEl.readOnly = true;
					displayWidget.inputEl.style.cursor = "text";
				}
				node.size = [500, 300]; // Just make node bigger
			}, 50);
		}
    }
});