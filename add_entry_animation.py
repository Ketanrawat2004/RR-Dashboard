import base64
import re
from pathlib import Path

# Verify rr_official_logo.png exists
logo_path = Path("rr_official_logo.png")
if not logo_path.exists():
    raise FileNotFoundError("rr_official_logo.png not found")

with open(logo_path, "rb") as f:
    rr_official_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# Read fix_dashboard_and_wagon.py
with open("fix_dashboard_and_wagon.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Ensure rr_official_logo_b64 is loaded at the top
if "rr_official_logo_b64" not in code:
    code = code.replace(
        'rr_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")',
        'rr_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")\n\nwith open("rr_official_logo.png", "rb") as f:\n    rr_official_logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")'
    )
    print("✓ Added rr_official_logo_b64 loading")

# 2. Add Entry Animation CSS inside <style>
entry_css = """
        /* ==========================================================================
           CINEMATIC WAR ROOM ENTRY ANIMATION OVERLAY
           ========================================================================== */
        .rr-entry-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 9999999;
            background: radial-gradient(circle at 50% 38%, #0E1E38 0%, #081220 55%, #03060C 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            opacity: 1;
            transform: scale(1);
            transition: opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), transform 0.75s cubic-bezier(0.16, 1, 0.3, 1), filter 0.75s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .rr-entry-overlay.fade-out {{
            opacity: 0;
            transform: scale(1.06);
            filter: blur(8px);
            pointer-events: none;
        }}

        .intro-grid-bg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: linear-gradient(rgba(235, 26, 141, 0.05) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0, 176, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            opacity: 0.7;
            pointer-events: none;
        }}

        .intro-glow-orb {{
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            pointer-events: none;
            opacity: 0.35;
            animation: orbFloat 6s ease-in-out infinite alternate;
        }}
        .orb-pink {{
            width: 440px;
            height: 440px;
            background: #EB1A8D;
            top: -100px;
            right: 15%;
        }}
        .orb-gold {{
            width: 380px;
            height: 380px;
            background: #FFD700;
            bottom: -60px;
            left: 15%;
            animation-delay: -3s;
        }}

        @keyframes orbFloat {{
            0% {{ transform: translate(0, 0) scale(1); }}
            100% {{ transform: translate(30px, 40px) scale(1.1); }}
        }}

        .intro-skip-pill {{
            position: absolute;
            top: 24px;
            right: 28px;
            z-index: 10;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            color: #94A3B8;
            font-size: 12px;
            font-weight: 600;
            padding: 7px 16px;
            border-radius: 24px;
            cursor: pointer;
            backdrop-filter: blur(8px);
            transition: all 0.2s ease;
        }}
        .intro-skip-pill:hover {{
            color: #FFFFFF;
            background: rgba(235, 26, 141, 0.35);
            border-color: #EB1A8D;
            box-shadow: 0 0 16px rgba(235, 26, 141, 0.4);
            transform: translateY(-1px);
        }}

        .intro-card {{
            position: relative;
            z-index: 5;
            background: rgba(14, 26, 47, 0.84);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(235, 26, 141, 0.38);
            border-radius: 26px;
            padding: 38px 46px;
            max-width: 530px;
            width: 92%;
            text-align: center;
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.75), 0 0 60px rgba(235, 26, 141, 0.25);
            animation: introCardEntrance 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        @keyframes introCardEntrance {{
            0% {{ opacity: 0; transform: translateY(30px) scale(0.92); }}
            100% {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        .intro-logo-plate {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #FFFFFF;
            border-radius: 20px;
            padding: 14px 28px;
            margin: 0 auto;
            box-shadow: 0 10px 35px rgba(235, 26, 141, 0.4), 0 0 0 2px rgba(255, 215, 0, 0.3);
            animation: logoBreathing 3s ease-in-out infinite;
        }}

        .intro-rr-logo {{
            max-width: 220px;
            max-height: 100px;
            width: auto;
            height: auto;
            display: block;
            object-fit: contain;
        }}

        @keyframes logoBreathing {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 10px 35px rgba(235, 26, 141, 0.4), 0 0 0 2px rgba(255, 215, 0, 0.3); }}
            50% {{ transform: scale(1.025); box-shadow: 0 14px 45px rgba(235, 26, 141, 0.65), 0 0 20px rgba(255, 215, 0, 0.5); }}
        }}

        .intro-badge {{
            display: inline-block;
            margin-top: 20px;
            padding: 4px 14px;
            background: rgba(235, 26, 141, 0.16);
            border: 1px solid #EB1A8D;
            color: #FFD700;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 3px;
            border-radius: 20px;
            text-transform: uppercase;
        }}

        .intro-title {{
            font-size: 23px;
            font-weight: 900;
            letter-spacing: 4px;
            color: #FFFFFF;
            margin-top: 10px;
            margin-bottom: 0;
            text-transform: uppercase;
            text-shadow: 0 0 18px rgba(235, 26, 141, 0.5);
        }}

        .intro-subtitle {{
            font-size: 12.5px;
            color: #94A3B8;
            margin-top: 5px;
            margin-bottom: 0;
            letter-spacing: 0.5px;
        }}

        .intro-terminal-box {{
            margin-top: 20px;
            background: rgba(6, 14, 26, 0.85);
            border: 1px solid rgba(0, 229, 255, 0.25);
            border-radius: 8px;
            padding: 8px 14px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 11px;
            color: #00E5FF;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 6px;
            text-shadow: 0 0 6px rgba(0, 229, 255, 0.5);
            min-height: 36px;
            overflow: hidden;
            white-space: nowrap;
        }}
        .terminal-prefix {{
            color: #EB1A8D;
            font-weight: bold;
        }}
        .terminal-text {{
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .terminal-cursor {{
            animation: cursorBlink 0.8s infinite;
            font-weight: bold;
            color: #00E5FF;
        }}
        @keyframes cursorBlink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}

        .intro-progress-bar-wrap {{
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 3px;
            margin-top: 14px;
            overflow: hidden;
            position: relative;
        }}
        .intro-progress-bar-fill {{
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #EB1A8D 0%, #FFD700 70%, #00E5FF 100%);
            border-radius: 3px;
            box-shadow: 0 0 14px rgba(235, 26, 141, 0.8);
            transition: width 0.08s linear;
        }}

        .intro-meta-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 8px;
            font-size: 11px;
            font-weight: 600;
            color: #64748B;
        }}
        .intro-status-label {{
            letter-spacing: 0.5px;
        }}
        .intro-pct-label {{
            color: #FFD700;
            font-family: ui-monospace, monospace;
        }}

        .intro-enter-btn {{
            margin-top: 22px;
            width: 100%;
            padding: 13px 24px;
            background: linear-gradient(135deg, #EB1A8D 0%, #C2185B 100%);
            color: #FFFFFF;
            font-weight: 800;
            font-size: 13px;
            letter-spacing: 2px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            box-shadow: 0 6px 25px rgba(235, 26, 141, 0.45);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.25s ease;
        }}
        .intro-enter-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 32px rgba(235, 26, 141, 0.7);
            background: linear-gradient(135deg, #FF1E9D 0%, #D81B60 100%);
        }}

        .header-replay-btn {{
            background: rgba(235, 26, 141, 0.08);
            border: 1px solid rgba(235, 26, 141, 0.28);
            color: var(--rr-pink);
            font-size: 11px;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        .header-replay-btn:hover {{
            background: var(--rr-pink);
            color: #FFFFFF;
            box-shadow: 0 2px 10px rgba(235, 26, 141, 0.35);
        }}

        @media (max-width: 600px) {{
            .intro-card {{
                padding: 26px 20px;
            }}
            .intro-rr-logo {{
                max-width: 170px;
            }}
            .intro-title {{
                font-size: 18px;
                letter-spacing: 2px;
            }}
            .intro-subtitle {{
                font-size: 11px;
            }}
        }}
"""

if ".rr-entry-overlay" not in code:
    code = code.replace("    </style>\n</head>", entry_css + "\n    </style>\n</head>")
    print("✓ Added entry CSS")

# 3. Add Intro Overlay HTML right after <body>
intro_html = """
<body>

<!-- CINEMATIC WAR ROOM STARTING ENTRY OVERLAY -->
<div id="rr-entry-overlay" class="rr-entry-overlay">
    <div class="intro-grid-bg"></div>
    <div class="intro-glow-orb orb-pink"></div>
    <div class="intro-glow-orb orb-gold"></div>

    <button class="intro-skip-pill" onclick="dismissIntro()" aria-label="Skip Intro Animation">
        Skip Intro &rarr;
    </button>

    <div class="intro-card">
        <div class="intro-logo-plate">
            <img src="{rr_official_logo_b64}" alt="Rajasthan Royals Official Logo" class="intro-rr-logo">
        </div>

        <div class="intro-badge">IPL 2027 AUCTION INTELLIGENCE</div>
        <h1 class="intro-title">RAJASTHAN ROYALS WAR ROOM</h1>
        <p class="intro-subtitle">SupeRR Selector Season 2 &bull; High-Leverage Pressure Analytics</p>

        <div class="intro-terminal-box">
            <span class="terminal-prefix">></span>
            <span id="intro-ticker-text" class="terminal-text">INITIALIZING QUANTUM LEVERAGE ENGINE...</span>
            <span class="terminal-cursor">_</span>
        </div>

        <div class="intro-progress-bar-wrap">
            <div id="intro-progress-bar" class="intro-progress-bar-fill"></div>
        </div>

        <div class="intro-meta-row">
            <span id="intro-status-label" class="intro-status-label">ANALYZING 883 SENIOR FIXTURES...</span>
            <span id="intro-pct-label" class="intro-pct-label">0%</span>
        </div>

        <button id="intro-enter-btn" class="intro-enter-btn" onclick="dismissIntro()">
            <span>ACCESS WAR ROOM DASHBOARD &rarr;</span>
        </button>
    </div>
</div>
"""

if "id=\"rr-entry-overlay\"" not in code:
    code = code.replace("<body>\n\n<div class=\"dashboard-container\">", intro_html.strip() + "\n\n<div class=\"dashboard-container\">")
    print("✓ Added entry HTML overlay")

# 4. Add Replay Button in the Executive Header
header_replay_target = """        <div class="header-meta">
            <strong>Cricket Operations Scouting Model</strong>"""

header_replay_replacement = """        <div class="header-meta">
            <div style="display:flex;align-items:center;justify-content:flex-end;gap:8px;margin-bottom:2px;">
                <strong>Cricket Operations Scouting Model</strong>
                <button class="header-replay-btn" onclick="replayIntro()" title="Replay Opening Sequence">🎬 Replay Intro</button>
            </div>"""

if "header-replay-btn" not in code:
    code = code.replace(header_replay_target, header_replay_replacement)
    print("✓ Added replay button to header")

# 5. Add JavaScript controller before </body>
intro_js = """
<!-- Cinematic War Room Intro Controller -->
<script>
var introTimer = null;
var introAnimFrame = null;
var isIntroDismissed = false;

function startIntroSequence() {
    isIntroDismissed = false;
    var overlay = document.getElementById('rr-entry-overlay');
    if (!overlay) return;
    
    overlay.style.display = 'flex';
    overlay.classList.remove('fade-out');
    
    var fill = document.getElementById('intro-progress-bar');
    var pctLabel = document.getElementById('intro-pct-label');
    var ticker = document.getElementById('intro-ticker-text');
    var statusLabel = document.getElementById('intro-status-label');
    var enterBtn = document.getElementById('intro-enter-btn');
    
    if (fill) fill.style.width = '0%';
    if (pctLabel) pctLabel.innerText = '0%';
    
    var steps = [
        { pct: 15, tick: "ACCESSING RAJASTHAN ROYALS CRICKET OPERATIONS...", status: "CONNECTING TO SECURE WAR ROOM..." },
        { pct: 35, tick: "INGESTING 883 SENIOR T20 MATCHES (2022–2026)...", status: "PARSING 28,381 INNINGS & 1,217 PLAYERS..." },
        { pct: 60, tick: "ISOLATING 180 HIGH-PRESSURE MATCHES (MLI >= 30)...", status: "APPLYING MATCH LEVERAGE WEIGHTS..." },
        { pct: 85, tick: "CALIBRATING CPPI SCORES & EMPIRICAL BAYES LIFT...", status: "REGULARIZING WIN DIFFERENTIALS..." },
        { pct: 100, tick: "SYSTEM READY: IPL 2027 TARGETS OPTIMIZED.", status: "AUTHENTICATED — ENTERING WAR ROOM..." }
    ];
    
    var startTime = performance.now();
    var duration = 2300; // 2.3 seconds smooth boot sequence
    
    function animate(currentTime) {
        if (isIntroDismissed) return;
        var elapsed = currentTime - startTime;
        var progress = Math.min(elapsed / duration, 1);
        
        var currentPct = Math.floor(progress * 100);
        if (fill) fill.style.width = currentPct + '%';
        if (pctLabel) pctLabel.innerText = currentPct + '%';
        
        for (var i = steps.length - 1; i >= 0; i--) {
            if (currentPct >= steps[i].pct) {
                if (ticker && ticker.innerText !== steps[i].tick) ticker.innerText = steps[i].tick;
                if (statusLabel && statusLabel.innerText !== steps[i].status) statusLabel.innerText = steps[i].status;
                break;
            }
        }
        
        if (progress < 1) {
            introAnimFrame = requestAnimationFrame(animate);
        } else {
            if (enterBtn) {
                enterBtn.style.boxShadow = '0 8px 32px rgba(235, 26, 141, 0.9)';
            }
            introTimer = setTimeout(function() {
                dismissIntro();
            }, 400);
        }
    }
    
    introAnimFrame = requestAnimationFrame(animate);
}

function dismissIntro() {
    if (isIntroDismissed) return;
    isIntroDismissed = true;
    if (introTimer) clearTimeout(introTimer);
    if (introAnimFrame) cancelAnimationFrame(introAnimFrame);
    
    var overlay = document.getElementById('rr-entry-overlay');
    if (!overlay) return;
    
    overlay.classList.add('fade-out');
    setTimeout(function() {
        overlay.style.display = 'none';
    }, 750);
}

function replayIntro() {
    startIntroSequence();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startIntroSequence);
} else {
    startIntroSequence();
}
</script>
"""

if "startIntroSequence" not in code:
    code = code.replace("</body>\n</html>", intro_js + "\n</body>\n</html>")
    print("✓ Added intro JavaScript controller")

with open("fix_dashboard_and_wagon.py", "w", encoding="utf-8") as f:
    f.write(code)

print("✓ Updated fix_dashboard_and_wagon.py successfully.")

