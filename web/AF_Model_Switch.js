import { app } from "/scripts/app.js";

app.registerExtension({
    name: "AF.ModelSwitch",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "AF_Model_Switch") {

            // Hook into onExecuted to update status after workflow runs
            const originalOnExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function(message) {
                const r = originalOnExecuted?.apply(this, arguments);

                if (message?.status && Array.isArray(message.status) && message.status.length > 0) {
                    const statusText = message.status[0];

                    const statusWidget = this.widgets?.find(w => w.name === "status");
                    if (statusWidget) {
                        statusWidget.value = statusText;

                        if (statusWidget.inputEl) {
                            statusWidget.inputEl.value = statusText;

                            if (statusText.includes("auto")) {
                                statusWidget.inputEl.style.backgroundColor = "#2a2a1a";
                                statusWidget.inputEl.style.color = "#ffaa44";
                                statusWidget.inputEl.style.borderColor = "#cc8833";
                            } else if (statusText.includes("none")) {
                                statusWidget.inputEl.style.backgroundColor = "#2a1a1a";
                                statusWidget.inputEl.style.color = "#ff6666";
                                statusWidget.inputEl.style.borderColor = "#cc4444";
                            } else {
                                statusWidget.inputEl.style.backgroundColor = "#1a2a3a";
                                statusWidget.inputEl.style.color = "#88ccff";
                                statusWidget.inputEl.style.borderColor = "#4488cc";
                            }
                        }

                        this.setDirtyCanvas(true, false);
                    }
                }

                return r;
            };

            // Store original onNodeCreated
            const originalOnNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function() {
                const result = originalOnNodeCreated?.apply(this, arguments);

                // Rails 1 and 2 are PERMANENT (defined in Python INPUT_TYPES)
                // So we start counting from rail 2 as the baseline
                // _currentRailCount represents the TOTAL number of rails visible

                // Detect existing rail count from loaded inputs
                // Check for the highest rail number present (rails 3-10 are dynamic)
                let detectedRailCount = 2; // Always have at least rails 1 and 2
                if (this.inputs) {
                    for (let i = 10; i >= 3; i--) {
                        if (this.inputs.find(inp => inp.name === `model_${i}`)) {
                            detectedRailCount = i;
                            break;
                        }
                    }
                }

                // Initialize tracking
                this._currentRailCount = detectedRailCount;
                this._userResized = false;
                this._isInitializing = true; // Flag to prevent duplicate initialization

                // Setup callbacks with delay to ensure widgets exist
                setTimeout(() => {
                    const railCountWidget = this.widgets?.find(w => w.name === "number_of_rails");
                    const selectWidget = this.widgets?.find(w => w.name === "selected_rail");

                    // Rail count callback
                    if (railCountWidget) {
                        railCountWidget.callback = (value) => {
                            const count = Math.max(2, Math.min(10, parseInt(value) || 2));
                            this.updateRailInputs(count);
                        };
                    }

                    // Selected rail callback
                    if (selectWidget) {
                        selectWidget.callback = (value) => {
                            this.updateStatusDisplay(parseInt(value));
                        };
                    }

                    this.updateStatusDisplay(0);
                    this._isInitializing = false;
                }, 100);

                return result;
            };

            // Update status display (UI only, no execution)
            nodeType.prototype.updateStatusDisplay = function(selectedRail) {
                const statusWidget = this.widgets?.find(w => w.name === "status");
                if (!statusWidget) return;

                let statusText, bgColor, textColor, borderColor;

                // 0 = AUTO, 1-10 = manual rail selection
                if (selectedRail === 0 || isNaN(selectedRail)) {
                    statusText = "💡 Active Rail: auto";
                    bgColor = "#2a2a1a";
                    textColor = "#ffaa44";
                    borderColor = "#cc8833";
                } else {
                    // Display 1-based rail number
                    statusText = `🎯 Active Rail: ${selectedRail}`;
                    bgColor = "#1a2a3a";
                    textColor = "#88ccff";
                    borderColor = "#4488cc";
                }

                statusWidget.value = statusText;

                if (statusWidget.inputEl) {
                    statusWidget.inputEl.value = statusText;
                    statusWidget.inputEl.style.backgroundColor = bgColor;
                    statusWidget.inputEl.style.color = textColor;
                    statusWidget.inputEl.style.borderColor = borderColor;
                }

                this.setDirtyCanvas(true, false);
            };

            // Update rail inputs dynamically
            nodeType.prototype.updateRailInputs = function(railCount) {
                railCount = Math.max(2, Math.min(10, railCount));

                if (this._currentRailCount === railCount) return;

                const oldCount = this._currentRailCount;
                const newCount = railCount;

                console.log(`AF Model Switch - Updating rails from ${oldCount} to ${newCount}`);

                if (newCount > oldCount) {
                    // Adding rails: model_3, model_4, etc. (1-based!)
                    // Rails 1 and 2 are permanent, so we only add 3+
                    for (let i = oldCount + 1; i <= newCount; i++) {
                        // Check if this input already exists before adding
                        const modelExists = this.inputs.find(inp => inp.name === `model_${i}`);
                        const clipExists = this.inputs.find(inp => inp.name === `clip_${i}`);
                        const vaeExists = this.inputs.find(inp => inp.name === `vae_${i}`);

                        if (!modelExists) {
                            console.log(`AF Model Switch - Adding model_${i}`);
                            this.addInput(`model_${i}`, "MODEL");
                        }
                        if (!clipExists) {
                            console.log(`AF Model Switch - Adding clip_${i}`);
                            this.addInput(`clip_${i}`, "CLIP");
                        }
                        if (!vaeExists) {
                            console.log(`AF Model Switch - Adding vae_${i}`);
                            this.addInput(`vae_${i}`, "VAE");
                        }
                    }
                } else {
                    // Removing rails from the end
                    // NEVER remove rails 1 or 2 (they're permanent)
                    for (let i = oldCount; i > newCount && i > 2; i--) {
                        console.log(`AF Model Switch - Removing rail ${i}`);
                        for (let j = this.inputs.length - 1; j >= 0; j--) {
                            const input = this.inputs[j];
                            if (input.name === `vae_${i}` ||
                                input.name === `clip_${i}` ||
                                input.name === `model_${i}`) {
                                this.removeInput(j);
                            }
                        }
                    }
                }

                this._currentRailCount = newCount;

                // Update select widget: 0=AUTO, 1 to newCount for rails
                const selectWidget = this.widgets?.find(w => w.name === "selected_rail");
                if (selectWidget) {
                    const maxRail = newCount;
                    selectWidget.options = selectWidget.options || {};
                    selectWidget.options.min = 0;
                    selectWidget.options.max = maxRail;

                    // Clamp current selection to valid range
                    const currentValue = parseInt(selectWidget.value);
                    if (currentValue > maxRail) {
                        selectWidget.value = maxRail;
                        this.updateStatusDisplay(maxRail);
                    }

                    // Update the input element's attributes
                    if (selectWidget.inputEl) {
                        selectWidget.inputEl.max = maxRail;
                        selectWidget.inputEl.min = 0;
                    }
                }

                // Only adjust height, preserve width
                const widgetHeight = 100;
                const inputHeight = 20;
                const totalInputs = this._currentRailCount * 3;
                const newHeight = widgetHeight + (totalInputs * inputHeight);

                // Preserve current width, only update height
                if (this.size) {
                    this.size[1] = newHeight;
                } else {
                    this.size = [160, newHeight];
                }

                this.setDirtyCanvas(true, true);
            };

            // Override computeSize - minimal intervention, let LiteGraph work
            const originalComputeSize = nodeType.prototype.computeSize;
            nodeType.prototype.computeSize = function(out) {
                // If user hasn't resized, calculate proper height
                if (!this._userResized) {
                    let height = 200;

                    if (this._currentRailCount) {
                        const widgetHeight = 100;
                        const inputHeight = 20;
                        const totalInputs = this._currentRailCount * 3;
                        height = widgetHeight + (totalInputs * inputHeight);
                    }

                    const size = [160, height];

                    if (out) {
                        out[0] = size[0];
                        out[1] = size[1];
                        return out;
                    }

                    return size;
                }

                // User has resized - let LiteGraph handle it normally
                return originalComputeSize?.apply(this, arguments);
            };

            // Track when user manually resizes
            const originalOnResize = nodeType.prototype.onResize;
            nodeType.prototype.onResize = function(size) {
                this._userResized = true;
                return originalOnResize?.apply(this, arguments);
            };
        }
    },

    async nodeCreated(node) {
        if (node.comfyClass === "AF_Model_Switch") {
            setTimeout(() => {
                // Style rail count widget
                const railCountWidget = node.widgets?.find(w => w.name === "number_of_rails");
                if (railCountWidget?.inputEl) {
                    railCountWidget.inputEl.style.border = "1px solid #4488cc";
                    railCountWidget.inputEl.style.backgroundColor = "#1a2a3a";
                    railCountWidget.inputEl.style.padding = "4px";
                    railCountWidget.inputEl.style.borderRadius = "3px";
                }

                // Style selected rail widget
                const selectWidget = node.widgets?.find(w => w.name === "selected_rail");
                if (selectWidget?.inputEl) {
                    selectWidget.inputEl.style.border = "1px solid #88cc44";
                    selectWidget.inputEl.style.backgroundColor = "#1a3a2a";
                    selectWidget.inputEl.style.padding = "4px";
                    selectWidget.inputEl.style.borderRadius = "3px";
                    selectWidget.inputEl.style.fontWeight = "bold";
                }

                // Style status widget
                const statusWidget = node.widgets?.find(w => w.name === "status");
                if (statusWidget?.inputEl) {
                    statusWidget.inputEl.readOnly = true;
                    statusWidget.inputEl.style.fontFamily = "monospace";
                    statusWidget.inputEl.style.fontSize = "13px";
                    statusWidget.inputEl.style.fontWeight = "bold";
                    statusWidget.inputEl.style.cursor = "default";
                    statusWidget.inputEl.style.padding = "6px 8px";
                    statusWidget.inputEl.style.textAlign = "center";
                    statusWidget.inputEl.style.userSelect = "none";
                    statusWidget.inputEl.style.resize = "none";
                    statusWidget.inputEl.style.minHeight = "32px";
                    statusWidget.inputEl.style.maxHeight = "32px";
                    statusWidget.inputEl.style.height = "32px";
                    statusWidget.inputEl.style.overflow = "hidden";
                    statusWidget.inputEl.style.width = "100%";
                    statusWidget.inputEl.style.boxSizing = "border-box";

                    // Set initial AUTO color (orange)
                    statusWidget.inputEl.style.backgroundColor = "#2a2a1a";
                    statusWidget.inputEl.style.color = "#ffaa44";
                    statusWidget.inputEl.style.border = "1px solid #cc8833";
                }
            }, 200);
        }
    },

    async loadedGraphNode(node) {
        if (node.comfyClass === "AF_Model_Switch") {
            setTimeout(() => {
                // Mark as user-resized if node has custom size stored
                if (node.size && node.size[0] !== 160) {
                    node._userResized = true;
                }

                // Detect current rail count from actual inputs
                let actualRailCount = 2; // Minimum (rails 1 and 2 are permanent)
                if (node.inputs) {
                    for (let i = 10; i >= 3; i--) {
                        if (node.inputs.find(inp => inp.name === `model_${i}`)) {
                            actualRailCount = i;
                            break;
                        }
                    }
                }

                // Update _currentRailCount to match actual state
                node._currentRailCount = actualRailCount;

                const railCountWidget = node.widgets?.find(w => w.name === "number_of_rails");
                if (railCountWidget) {
                    const widgetValue = parseInt(railCountWidget.value) || 2;

                    console.log(`AF Model Switch - Loaded: widget=${widgetValue}, actual inputs=${actualRailCount}`);

                    // Sync: if widget and actual don't match, update to match widget
                    if (widgetValue !== actualRailCount && node.updateRailInputs) {
                        console.log(`AF Model Switch - Syncing rails to ${widgetValue}`);
                        node.updateRailInputs(widgetValue);
                    }
                }
            }, 100);
        }
    }
});
