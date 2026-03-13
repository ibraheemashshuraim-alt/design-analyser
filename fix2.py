import re

def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix AI Tips and Data Value Typography
    content = content.replace(
        ".data-block label { display: block; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px; font-family: 'Outfit'; }",
        ".data-block label { display: block; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px; font-family: 'Outfit', sans-serif; }"
    )
    content = content.replace(
        ".data-value { font-size: 0.9rem; color: #fff; word-break: break-word; }",
        ".data-value { font-size: 0.95rem; color: #fff; word-break: break-word; font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaliq', 'Outfit', sans-serif; line-height: 1.8; }"
    )
    content = content.replace(
        ".ltr-text { direction: ltr; }",
        ".ltr-text { direction: ltr; font-family: 'Outfit', sans-serif; }"
    )
    content = content.replace(
        ".ai-tip-box { background: rgba(181, 0, 255, 0.05); border-left: 3px solid var(--neon-purple); padding: 10px; border-radius: 0 8px 8px 0; font-family: 'Noto Nastaliq Urdu', serif; }",
        ".ai-tip-box { background: rgba(181, 0, 255, 0.05); border-left: 3px solid var(--neon-purple); padding: 12px; border-radius: 0 8px 8px 0; }"
    )
    content = content.replace(
        ".ai-tip-box p { font-size: 0.8rem; color: #eaeaec; margin: 0; line-height: 1.5; }",
        ".ai-tip-box p { font-size: 0.9rem; color: #eaeaec; margin: 0; line-height: 1.8; font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaliq', 'Outfit', sans-serif; }"
    )

    # 2. Add Reset Font Size text and adjust its parent
    reset_font_html = """
            <div style="margin-bottom: 20px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <label style="color:var(--text-muted);">Text Size (<span id="fontSizeDisplay">100%</span>)</label>
                    <button style="background:none; border:none; color:var(--neon-cyan); cursor:pointer; font-size:0.8rem; font-family:'Outfit';" onclick="resetFontSize()">Reset to Default</button>
                </div>
                <input type="range" id="fontSizeSlider" min="80" max="150" value="100" style="width:100%;">
                <div style="display:flex; justify-content:space-between; color:var(--text-muted); font-size:0.8rem; direction:ltr;">
                    <span>Small</span><span>Default</span><span>Large</span>
                </div>
            </div>"""
            
    old_font_html = """
                <label style="color:var(--text-muted); display:block; margin-bottom:5px;">Text Size (<span id="fontSizeDisplay">100%</span>)</label>
                <input type="range" id="fontSizeSlider" min="80" max="150" value="100" style="width:100%;">
                <div style="display:flex; justify-content:space-between; color:var(--text-muted); font-size:0.8rem; direction:ltr;">
                    <span>Small</span><span>Default</span><span>Large</span>
                </div>
            </div>"""
    
    # Only replace if old font html exists (it might have already been updated)
    if "resetFontSize()" not in content:
        content = content.replace(old_font_html.strip(), reset_font_html.strip())


    # 3. Add resetFontSize JS
    reset_js = """
        window.resetFontSize = function() {
            fontSizeSlider.value = 100;
            document.documentElement.style.fontSize = '100%';
            fontSizeDisplay.innerText = '100%';
            localStorage.setItem('dcFontSize', 100);
        };
        
        fontFamilySelect.addEventListener"""
    
    if "window.resetFontSize =" not in content:
        content = content.replace("fontFamilySelect.addEventListener", reset_js.strip())


    # 4. Filerobot Configs
    filerobot_config = """
                Text: { text: "Design Text..." },
                tabsIds: [window.FilerobotImageEditor.TABS.ADJUST, window.FilerobotImageEditor.TABS.ANNOTATE, window.FilerobotImageEditor.TABS.WATERMARK, window.FilerobotImageEditor.TABS.FILTERS],
                defaultTabId: window.FilerobotImageEditor.TABS.ANNOTATE,
                defaultToolId: window.FilerobotImageEditor.TOOLS.TEXT,
                translations: {"""
    
    if "tabsIds: [window.FilerobotImageEditor.TABS.ADJUST" not in content:
        content = content.replace('Text: { text: "Design Text..." },\n                translations: {', filerobot_config.lstrip('\n'))


    # 5. Fix TTS Glitch
    tts_func_start = """
        let ttsUtterances = []; // Global array to prevent garbage collection bug in Chrome
        window.playTTS = function"""
    
    if "ttsUtterances = [];" not in content:
         content = content.replace("window.playTTS = function", tts_func_start.strip())
         
         tts_logic = """
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel(); // Stop anything currently speaking
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = langCode;
                utterance.rate = 0.9;
                utterance.pitch = 1;
                
                // Chrome bug workaround: keep reference
                ttsUtterances.push(utterance);
                
                utterance.onend = function() {
                    ttsUtterances = ttsUtterances.filter(u => u !== utterance);
                };

                // Another Chrome fix: sometimes it gets stuck in paused state after cancel
                if (window.speechSynthesis.paused) {
                    window.speechSynthesis.resume();
                }

                window.speechSynthesis.speak(utterance);
            } else {"""
         
         old_tts = """
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel(); // Stop anything currently speaking
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = langCode;
                utterance.rate = 0.9;
                utterance.pitch = 1;
                window.speechSynthesis.speak(utterance);
            } else {"""
         content = content.replace(old_tts.strip(), tts_logic.strip())
         
    # 6. Re-add missing Print CSS
    print_css = """
        @media print {
            body * { visibility: hidden; }
            #resultsPanel, #resultsPanel * { visibility: visible; }
            #resultsPanel { position: absolute; left: 0; top: 0; width: 100%; margin: 0; padding: 20px; box-shadow: none; overflow: visible !important; max-height: none !important; background: #0c1626 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
            .export-actions, .panel-header-text, .panel-stripe { display: none !important; }
        }
        .admin-nav { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--border-dim); padding-bottom: 15px; }
        .admin-tab { background: none; border: none; color: var(--text-muted); padding: 8px 15px; cursor: pointer; border-radius: 6px; font-family: 'Outfit'; }
        .admin-tab.active { background: rgba(0, 240, 255, 0.1); color: var(--neon-cyan); border: 1px solid var(--neon-cyan); }
        .admin-section { display: none; }
        .admin-section.active { display: block; }

        /* Print Specific CSS Fixes */
        @media print {
            body, html { background: #ffffff !important; color: #000000 !important; margin: 0; padding: 0; }
            .top-nav, .scan-card, .preview-actions, .export-actions, footer { display: none !important; }
            .main-wrapper { padding: 0 !important; max-width: 100% !important; border:none; }
            .bento-grid { display: block !important; }
            .results-card { background: #ffffff !important; border: none !important; box-shadow: none !important; width: 100% !important; padding: 0 !important; height: auto !important; }
            .results-scroll-area { height: auto !important; overflow: visible !important; padding: 0 !important; }
            .panel-header-text, .panel-stripe { display: none !important; }
            .bento-inner-grid { display: block !important; }
            .inner-card {
                background: #ffffff !important; border: 1px solid #ddd !important;
                page-break-inside: avoid !important; margin-bottom: 20px !important;
                color: #000 !important; box-shadow: none !important;
            }
            .card-header, .score-label, .data-block label { color: #333 !important; }
            .data-value, .score-number { color: #000 !important; text-shadow: none !important; }
            .ai-tip-box p { color: #333 !important; }
            .chip-green, .chip-red, .chip-purple { background: transparent !important; color: #000 !important; border-color: #aaa !important; }
        }
    </style>"""
    
    if "/* Print Specific CSS Fixes */" not in content:
         content = content.replace("    </style>", print_css.lstrip("\n"))

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix()
print("Fixed missing old features")
