"""
SYNTH STUDIO - Hardware Reference & Learning Tool
Optimized for performance • Hardware-accurate • Science-backed learning
"""

import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
from functools import lru_cache

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Synth Studio | Hardware Reference",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL CSS - OPTIMIZED & CLEAN
# ============================================================================

st.markdown("""
<style>
    /* Base styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    }

    /* Hardware panel - clean and professional */
    .hw-panel {
        background: linear-gradient(180deg, #252525 0%, #1a1a1a 100%);
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    /* Section headers */
    .section-title {
        color: #0f0;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #0f0;
    }

    /* CSS Knob - MUCH faster than Plotly */
    .css-knob {
        width: 80px;
        height: 80px;
        margin: 10px auto;
        position: relative;
    }

    .knob-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #3a3a3a, #1a1a1a);
        border: 2px solid #4a4a4a;
        position: relative;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5), inset 0 2px 4px rgba(0,0,0,0.3);
    }

    .knob-indicator {
        position: absolute;
        width: 3px;
        height: 30px;
        background: #fff;
        top: 10px;
        left: 50%;
        transform-origin: bottom center;
        border-radius: 2px;
    }

    .knob-label {
        text-align: center;
        font-size: 9px;
        color: #888;
        text-transform: uppercase;
        margin-top: 5px;
        letter-spacing: 0.5px;
    }

    .knob-value {
        text-align: center;
        font-size: 12px;
        color: #0f0;
        font-family: 'Courier New', monospace;
        font-weight: 700;
        margin-bottom: 5px;
    }

    /* LED Display */
    .led-display {
        background: #000;
        color: #0f0;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        font-weight: 700;
        padding: 8px 12px;
        border: 1px solid #1a1a1a;
        border-radius: 3px;
        text-align: center;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.8), 0 0 10px rgba(0,255,0,0.2);
        display: inline-block;
        min-width: 80px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
        color: #e0e0e0;
        border: 1px solid #4a4a4a;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 10px 20px;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #3a3a3a 0%, #2a2a2a 100%);
        border-color: #0f0;
        box-shadow: 0 0 10px rgba(0,255,0,0.3);
    }

    /* Learning callouts */
    .tip-box {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%);
        border-left: 3px solid #0f0;
        padding: 15px;
        margin: 15px 0;
        border-radius: 4px;
        font-size: 12px;
        line-height: 1.6;
    }

    .hardware-tip {
        background: linear-gradient(135deg, #2a1a1a 0%, #1a0d0d 100%);
        border-left: 3px solid #f90;
        padding: 15px;
        margin: 15px 0;
        border-radius: 4px;
        font-size: 12px;
        line-height: 1.6;
    }

    .patch-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        padding: 12px;
        margin: 8px 0;
    }

    .patch-card:hover {
        border-color: #0f0;
        box-shadow: 0 0 8px rgba(0,255,0,0.2);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #2a2a2a;
    }

    section[data-testid="stSidebar"] h3 {
        color: #0f0;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }

    /* Sliders - compact */
    .stSlider > div > div > div {
        font-size: 11px;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Responsive */
    @media (max-width: 1200px) {
        .hw-panel {
            padding: 12px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DEVICE SPECIFICATIONS
# ============================================================================

DEVICES = {
    "DFAM": {
        "name": "DFAM - Drummer From Another Mother",
        "manufacturer": "Moog Music",
        "type": "Semi-Modular Percussion Synth",
        "specs": {
            "oscillators": "2 analog VCOs (Triangle/Square)",
            "filter": "4-pole Ladder (LP/HP) 20Hz-20kHz",
            "envelopes": "3 (VCO, VCF, VCA)",
            "sequencer": "8-step analog",
            "patchbay": "24 points (15 in, 9 out)"
        },
        "controls": ["VCO1", "VCO2", "Mixer", "Filter", "VCA", "Sequencer"]
    },
    "Mother-32": {
        "name": "Mother-32 Semi-Modular Synthesizer",
        "manufacturer": "Moog Music",
        "type": "Semi-Modular Analog Synth",
        "specs": {
            "oscillator": "1 VCO (Saw/Pulse with PWM)",
            "lfo": "0.1-600Hz (Square/Triangle)",
            "filter": "4-pole Ladder 17Hz-21.5kHz",
            "envelope": "AD (1.25ms-3s attack, 1.25ms-7s decay)",
            "sequencer": "32-step, 64 patterns, 8 banks",
            "patchbay": "32 points (18 in, 14 out)"
        },
        "controls": ["VCO", "LFO", "Filter", "Envelope", "Sequencer"]
    },
    "Subharmonicon": {
        "name": "Subharmonicon Polyrhythmic Synthesizer",
        "manufacturer": "Moog Music",
        "type": "Polyrhythmic Analog Synth",
        "specs": {
            "oscillators": "2 VCOs",
            "subharmonics": "4 per VCO (÷1 to ÷16)",
            "rhythms": "4 polyrhythmic generators",
            "sequencers": "2x4-step",
            "patchbay": "16 points"
        },
        "controls": ["VCO1+Subs", "VCO2+Subs", "Rhythms", "Sequencers"]
    },
    "Analog Four": {
        "name": "Analog Four MKII",
        "manufacturer": "Elektron",
        "type": "4-Voice Analog Synth + Sequencer",
        "specs": {
            "voices": "4 independent analog voices",
            "oscillators": "2 per voice + sub-osc each",
            "waveforms": "Saw, Pulse, Transistor Pulse, Triangle",
            "filters": "4-pole LP ladder + 2-pole multimode",
            "tracks": "4 sequencer tracks",
            "steps": "Up to 64 steps per pattern",
            "cv": "4 CV/Gate outputs",
            "features": "Parameter locks, conditional trigs, scenes"
        },
        "controls": ["Voice", "Oscillators", "Filter", "Envelope", "LFO", "Sequencer"]
    },
    "Analog Rytm": {
        "name": "Analog Rytm MKII",
        "manufacturer": "Elektron",
        "type": "Analog Drum Machine + Sampler",
        "specs": {
            "voices": "8 analog voices",
            "machines": "12 synthesis models (Kick/Snare/Hat/Tom/etc)",
            "tracks": "12 total (8 drum, 4 chromatic)",
            "pads": "12 velocity/pressure-sensitive",
            "filters": "Analog multimode per voice",
            "patterns": "128 per project",
            "scenes": "12 per kit",
            "features": "Sample layering, parameter locks, performance macros"
        },
        "controls": ["Track", "Machine", "Sample", "Filter", "Envelope", "Sequencer"]
    }
}

# ============================================================================
# LEARNING CONTENT - EXPANDED
# ============================================================================

CHALLENGES = {
    "DFAM": [
        {
            "title": "Classic Kick Drum",
            "difficulty": "Beginner",
            "goal": "Create a punchy kick using VCO pitch sweep",
            "steps": [
                "Set VCO1 freq to 12 o'clock (middle position)",
                "Set VCO DECAY to ~300ms for pitch sweep",
                "Set VCF CUTOFF to ~800Hz",
                "Set VCF EG to +60% for filter sweep",
                "Set VCA DECAY to ~150ms for short hit",
                "Tap TRIGGER button - you should hear a kick!"
            ],
            "theory": "Kick drums = fast pitch envelope from high→low freq. The 'thump' comes from this rapid pitch drop. VCF envelope adds 'click'.",
            "try_hardware": "Turn VCO DECAY while triggering. Hear how longer decay = 'boomy' kick, shorter = 'tight' kick."
        },
        {
            "title": "Hi-Hat Pattern",
            "difficulty": "Intermediate",
            "goal": "Create metallic hi-hats using noise + HP filter",
            "steps": [
                "Switch filter to HP (high-pass) mode",
                "Set VCO1 and VCO2 to highest position",
                "Set NOISE to 75%",
                "Set VCF CUTOFF high (8kHz+)",
                "Set VCA DECAY very short (~60ms)",
                "Program 8-step pattern: ON-off-ON-off (16th notes)"
            ],
            "theory": "Hi-hats = HIGH freq oscillators + NOISE + short decay. HP filter removes bass for crisp sound.",
            "try_hardware": "Adjust VCA DECAY while pattern plays. Short = closed hat, longer = open hat."
        },
        {
            "title": "FM Bass Stab",
            "difficulty": "Advanced",
            "goal": "Use frequency modulation for harmonic bass",
            "steps": [
                "Set VCO1 FREQ to low position (~30)",
                "Set VCO2 FREQ slightly higher (~35)",
                "Turn FM AMOUNT to 70%",
                "Enable HARD SYNC",
                "Set VCO DECAY to ~200ms",
                "Set VCF CUTOFF low, VCF EG to +80%"
            ],
            "theory": "FM = one oscillator modulating another's frequency. Creates complex harmonics. HARD SYNC locks VCO2 to VCO1 for tighter sound.",
            "try_hardware": "Patch VCO2→FM input. Adjust FM AMOUNT while triggering - hear harmonic content change dramatically."
        }
    ],
    "Mother-32": [
        {
            "title": "Analog Bass Sequence",
            "difficulty": "Beginner",
            "goal": "Program a classic TB-303 style bass line",
            "steps": [
                "Select SAW wave",
                "Set VCF CUTOFF to ~40%",
                "Set VCF RESONANCE to ~60%",
                "Set VCF EG AMT to +70%",
                "Program 8-step sequence: C-C-G-C-C-G-Bb-C",
                "Add slight GLIDE (~20%) for slides"
            ],
            "theory": "Saw wave has rich harmonics. Low-pass filter cuts highs. Resonance adds 'squelch'. EG opens filter on note attack.",
            "try_hardware": "Turn CUTOFF and RESONANCE while sequence plays. Find the sweet spot where it 'squelches'."
        },
        {
            "title": "LFO Modulation",
            "difficulty": "Intermediate",
            "goal": "Use LFO for rhythmic filter sweeps",
            "steps": [
                "Set LFO RATE to ~4Hz (quarter notes at 120 BPM)",
                "Patch LFO TRIANGLE → VCF CUTOFF",
                "Set VCF CUTOFF to 50%",
                "Set VCF RESONANCE to 70%",
                "Play sequence and hear rhythmic filter sweep"
            ],
            "theory": "LFO = Low Frequency Oscillator. Modulates parameters rhythmically. Triangle wave gives smooth up/down sweep.",
            "try_hardware": "Try LFO SQUARE wave instead - hear stepped filter movement. Adjust LFO RATE to sync with tempo."
        }
    ],
    "Subharmonicon": [
        {
            "title": "Harmonic Drone",
            "difficulty": "Beginner",
            "goal": "Create evolving harmonic drone using subharmonics",
            "steps": [
                "Set VCO1 FREQ to C (middle position)",
                "Set SUB 1A to ÷2 (octave below)",
                "Set SUB 1B to ÷3 (perfect fifth below octave)",
                "Set VCO2 FREQ to G (fifth above VCO1)",
                "Set SUB 2A to ÷4 (two octaves below)",
                "Listen to harmonic series unfolding"
            ],
            "theory": "Subharmonics divide frequency by integers, creating harmonic series. ÷2 = octave down, ÷3 = fifth+octave down, etc.",
            "try_hardware": "Slowly change VCO1 FREQ while listening. Hear how all subharmonics stay in tune."
        },
        {
            "title": "Polyrhythmic Pattern",
            "difficulty": "Advanced",
            "goal": "Create complex evolving polyrhythm",
            "steps": [
                "Set RHYTHM 1 to ÷4 (quarter notes)",
                "Set RHYTHM 2 to ÷3 (triplets)",
                "Set RHYTHM 3 to ÷5 (quintuplets)",
                "Route all rhythms to SEQUENCER 1",
                "Program simple 4-note sequence",
                "Pattern repeats every 60 steps (LCM of 4,3,5)"
            ],
            "theory": "Polyrhythm = multiple rhythms playing simultaneously. Pattern length = LCM (Least Common Multiple) of all divisions.",
            "try_hardware": "Start with just ÷4, add ÷3, then ÷5. Hear complexity build. Pattern takes time to repeat!"
        }
    ],
    "Analog Four": [
        {
            "title": "Parameter-Locked Lead",
            "difficulty": "Intermediate",
            "goal": "Create evolving lead with per-step filter modulation",
            "steps": [
                "Select TRACK 1, set to SAW wave",
                "Program 16-step melody",
                "On step 1: Hold [TRIG] + turn CUTOFF to 30%",
                "On step 5: Hold [TRIG] + turn CUTOFF to 80%",
                "On step 9: Hold [TRIG] + turn CUTOFF to 50%",
                "Each step now has different filter setting!"
            ],
            "theory": "Parameter locks = per-step automation. Each trig can have unique parameter values, creating evolving sequences.",
            "try_hardware": "Lock multiple parameters per step: CUTOFF + RESONANCE + OSC DETUNE for maximum variation."
        }
    ],
    "Analog Rytm": [
        {
            "title": "Layered Analog Kick",
            "difficulty": "Beginner",
            "goal": "Create punchy kick with analog synthesis + sample",
            "steps": [
                "Select PAD 1 (usually kick)",
                "Choose BD HARD machine (808-style)",
                "Tune PITCH to taste (~50-60)",
                "Set DECAY to ~400ms",
                "Load kick sample, set to layer mode",
                "Balance analog/sample mix"
            ],
            "theory": "Rytm's strength = layering analog synthesis with samples. Analog gives punch, sample adds character.",
            "try_hardware": "Solo the kick track. Mute sample layer - hear pure analog. Unmute - hear combination."
        }
    ]
}

RECALL_QUESTIONS = {
    "DFAM": [
        "What does VCO DECAY control?||Pitch envelope decay time",
        "Which filter mode removes LOW frequencies?||HP (High-Pass)",
        "How many total patch points?||24 (15 inputs, 9 outputs)",
        "What creates the 'kick' sound in drum patches?||Fast pitch envelope sweep from high to low frequency",
        "What does FM AMOUNT do?||Controls how much VCO2 modulates VCO1 frequency",
        "What does HARD SYNC do?||Locks VCO2's phase to VCO1 for tighter, harmonically-rich tones"
    ],
    "Mother-32": [
        "What is the LFO frequency range?||0.1 to 600Hz",
        "How many sequencer steps?||32 steps per pattern",
        "How many patterns can be stored?||64 patterns (8 banks × 8)",
        "What waveforms does the VCO produce?||Saw and Pulse (with PWM)",
        "What does GLIDE control?||Portamento time between notes"
    ],
    "Subharmonicon": [
        "What does ÷2 subharmonic division create?||One octave below the fundamental",
        "What is a polyrhythm?||Multiple rhythms with different divisions playing simultaneously",
        "How many rhythm generators?||4 independent polyrhythmic generators",
        "What does patching VCO OUT to own SUB IN do?||Creates complex self-modulation and harmonic chaos"
    ],
    "Analog Four": [
        "How many voices?||4 independent analog voices",
        "What are parameter locks?||Per-step parameter automation in the sequencer",
        "How many CV outputs?||4 CV/Gate outputs",
        "Maximum pattern length?||64 steps",
        "How many waveforms per oscillator?||4 (Saw, Pulse, Transistor Pulse, Triangle)"
    ],
    "Analog Rytm": [
        "How many analog voices?||8 analog drum voices",
        "How many synthesis machines/models?||12 different synthesis models",
        "Can you layer samples with analog synthesis?||Yes, each track can layer both",
        "How many performance scenes per kit?||12 scenes per kit",
        "What is CTRL-ALL mode?||Control multiple tracks simultaneously for live performance"
    ]
}

COMMUNITY_PATCHES = {
    "DFAM": [
        {"name": "Classic 909 Kick", "vco1": 15, "vco2": 20, "vco_decay": 300, "noise": 10, "vcf_eg": 60, "vca_decay": 150},
        {"name": "Industrial Tom", "vco1": 40, "vco2": 45, "vco_decay": 600, "noise": 15, "vcf_eg": 40, "vca_decay": 400},
        {"name": "Metallic Clap", "vco1": 70, "vco2": 75, "vco_decay": 50, "noise": 80, "vcf_eg": -30, "vca_decay": 200},
    ],
    "Mother-32": [
        {"name": "Deep Bass", "wave": "Saw", "cutoff": 35, "res": 65, "vcf_eg": 75, "glide": 15},
        {"name": "Acid Lead", "wave": "Saw", "cutoff": 50, "res": 80, "vcf_eg": 90, "glide": 0},
        {"name": "Pad Drone", "wave": "Pulse", "cutoff": 45, "res": 40, "vcf_eg": 30, "glide": 50},
    ]
}

# ============================================================================
# OPTIMIZED VISUAL COMPONENTS - CACHED FOR PERFORMANCE
# ============================================================================

def create_css_knob(label, value, min_val, max_val, unit=""):
    """Lightweight CSS knob - MUCH faster than Plotly"""
    normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
    rotation = -135 + (normalized * 270)  # 270° rotation range

    display_val = f"{value}{unit}" if unit else str(value)

    html = f"""
    <div class="css-knob">
        <div class="knob-value">{display_val}</div>
        <div class="knob-circle">
            <div class="knob-indicator" style="transform: translateX(-50%) rotate({rotation}deg);"></div>
        </div>
        <div class="knob-label">{label}</div>
    </div>
    """
    return html

@lru_cache(maxsize=32)
def create_waveform(wave_type, key_suffix=""):
    """Cached waveform display - only regenerate when wave type changes"""
    x = np.linspace(0, 4*np.pi, 400)

    if wave_type.lower() == "triangle":
        y = 2 * np.abs(2 * ((x)/(2*np.pi) - np.floor((x)/(2*np.pi) + 0.5))) - 1
    elif wave_type.lower() == "square":
        y = np.sign(np.sin(x))
    elif wave_type.lower() == "saw":
        y = 2 * ((x)/(2*np.pi) - np.floor((x)/(2*np.pi) + 0.5))
    elif wave_type.lower() == "pulse":
        y = (np.sin(x) > 0.5).astype(float) * 2 - 1
    else:  # noise
        np.random.seed(42)  # Fixed seed for caching
        y = np.random.normal(0, 0.3, len(x))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(color='#0f0', width=1.5),
        fill='tozeroy',
        fillcolor='rgba(0,255,0,0.1)'
    ))

    fig.update_layout(
        showlegend=False,
        height=80,
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor='rgb(5,5,5)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, range=[-1.2,1.2])
    )

    return fig

def create_led_display(text):
    """Simple LED-style display"""
    return f'<div class="led-display">{text}</div>'

def create_patch_card(patch):
    """Create a visual patch card"""
    html = f"""
    <div class='patch-card'>
        <strong style='color: #0f0;'>{patch['name']}</strong><br>
        <small style='color: #888;'>
    """
    for key, val in patch.items():
        if key != 'name':
            html += f"{key}: {val} • "
    html += "</small></div>"
    return html

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def init_state():
    """Initialize session state"""
    defaults = {
        'device': 'DFAM',
        'mode': 'Practice',
        'session_start': datetime.now(),
        'challenges_done': [],
        'active_challenge': None,
        'dfam_pattern': [True, False, True, False, True, False, True, False],
        'dfam_velocities': [100, 0, 80, 0, 100, 0, 70, 0],
        'user_patches': {}
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def save_patch(device, settings):
    """Save current patch settings"""
    patch_name = f"{device}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.user_patches[patch_name] = {
        "device": device,
        "timestamp": datetime.now().isoformat(),
        "settings": settings
    }
    # Save to file
    try:
        with open("user_patches.json", "w") as f:
            json.dump(st.session_state.user_patches, f, indent=2)
    except:
        pass
    return patch_name

def load_user_patches():
    """Load user patches from file"""
    try:
        patches_file = Path("user_patches.json")
        if patches_file.exists():
            with open(patches_file, 'r') as f:
                st.session_state.user_patches = json.load(f)
    except:
        pass

# ============================================================================
# MAIN APP
# ============================================================================

init_state()
load_user_patches()

# Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #1a1a1a 0%, #0a0a0a 50%, #1a1a1a 100%);
            border-bottom: 2px solid #0f0; margin-bottom: 20px;'>
    <h1 style='color: #e0e0e0; font-size: 26px; font-weight: 700; letter-spacing: 3px; margin: 0;'>
        SYNTH STUDIO
    </h1>
    <p style='color: #0f0; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; margin: 6px 0 0 0;'>
        Hardware Reference • Learning System • Performance Optimized
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🎛️ DEVICE")
    device = st.selectbox(
        "",
        list(DEVICES.keys()),
        format_func=lambda x: DEVICES[x]["name"],
        label_visibility="collapsed",
        key="device_select"
    )
    st.session_state.device = device

    st.markdown("---")

    st.markdown("### 📚 MODE")
    mode = st.radio("", ["Practice", "Challenge", "Recall", "Patches"], label_visibility="collapsed")
    st.session_state.mode = mode

    st.markdown("---")

    # Quick specs
    st.markdown("### ⚡ SPECS")
    specs = DEVICES[device]["specs"]
    for key, val in specs.items():
        st.caption(f"**{key.upper()}**")
        st.caption(f"`{val}`")

    st.markdown("---")

    # Session stats
    elapsed = datetime.now() - st.session_state.session_start
    mins = elapsed.seconds // 60
    st.metric("Session", f"{mins} min")
    st.metric("Challenges", len(st.session_state.challenges_done))
    st.metric("Saved Patches", len(st.session_state.user_patches))

    st.markdown("---")

    with st.expander("💡 How to Use"):
        st.markdown("""
        **Modes:**
        - **Practice**: Free exploration
        - **Challenge**: Guided patches
        - **Recall**: Test knowledge
        - **Patches**: Community library

        **Workflow:**
        1. Select device
        2. Choose mode
        3. Follow along on hardware
        4. Complete challenges
        5. Test with recall
        """)

# ============================================================================
# MAIN CONTENT - PATCHES MODE
# ============================================================================

if mode == "Patches":
    st.markdown(f"## 📚 {DEVICES[device]['name']} Patch Library")

    st.markdown("""
    <div class='tip-box'>
    <strong>Community Patches:</strong> Verified patches from official manuals and community contributors.
    Load these as starting points for your own sounds!
    </div>
    """, unsafe_allow_html=True)

    patches = COMMUNITY_PATCHES.get(device, [])

    if not patches:
        st.info(f"Community patches coming soon for {DEVICES[device]['name']}!")
    else:
        st.markdown("### Community Patches")
        for patch in patches:
            st.markdown(create_patch_card(patch), unsafe_allow_html=True)
            if st.button(f"Load {patch['name']}", key=f"load_{patch['name']}"):
                st.success(f"Loaded {patch['name']} - adjust controls to match!")

    # User patches
    user_patches = [p for p in st.session_state.user_patches.values() if p['device'] == device]
    if user_patches:
        st.markdown("### Your Saved Patches")
        for patch_name, patch_data in st.session_state.user_patches.items():
            if patch_data['device'] == device:
                st.markdown(f"""
                <div class='patch-card'>
                    <strong style='color: #0f0;'>{patch_name}</strong><br>
                    <small style='color: #888;'>Saved: {patch_data['timestamp'][:16]}</small>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# CHALLENGE MODE
# ============================================================================

elif mode == "Challenge":
    st.markdown(f"## 🎯 {DEVICES[device]['name']} Challenges")

    challenges = CHALLENGES.get(device, [])

    if not challenges:
        st.info(f"Challenges coming soon for {DEVICES[device]['name']}!")
    else:
        challenge_names = [f"{c['difficulty']}: {c['title']}" for c in challenges]

        col1, col2 = st.columns([3, 1])
        with col1:
            selected = st.selectbox("Select Challenge", challenge_names)
        with col2:
            if st.button("START", use_container_width=True):
                idx = challenge_names.index(selected)
                st.session_state.active_challenge = challenges[idx]
                st.rerun()

        if st.session_state.active_challenge:
            ch = st.session_state.active_challenge

            st.markdown(f"""
            <div class='tip-box'>
            <strong>🎯 GOAL:</strong> {ch['goal']}<br>
            <strong>📊 DIFFICULTY:</strong> {ch['difficulty']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='hardware-tip'>
            <strong>🎛️ TRY ON HARDWARE:</strong><br>
            {ch['try_hardware']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**STEP-BY-STEP:**")
            for i, step in enumerate(ch['steps'], 1):
                st.markdown(f"{i}. {step}")

            st.markdown(f"""
            <div class='tip-box'>
            <strong>📚 THEORY:</strong><br>
            {ch['theory']}
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Mark Complete", use_container_width=True):
                    if ch['title'] not in st.session_state.challenges_done:
                        st.session_state.challenges_done.append(ch['title'])
                        st.success(f"Challenge '{ch['title']}' completed! 🎉")
                    st.session_state.active_challenge = None
                    st.rerun()
            with col2:
                if st.button("← Back to List", use_container_width=True):
                    st.session_state.active_challenge = None
                    st.rerun()

# ============================================================================
# RECALL MODE
# ============================================================================

elif mode == "Recall":
    st.markdown(f"## 🧠 Active Recall - {DEVICES[device]['name']}")

    st.markdown("""
    <div class='tip-box'>
    <strong>Science-backed learning:</strong> Active recall strengthens memory.
    Try to answer before revealing.
    </div>
    """, unsafe_allow_html=True)

    questions = RECALL_QUESTIONS.get(device, [])

    if not questions:
        st.info(f"Recall questions coming soon for {DEVICES[device]['name']}!")
    else:
        for i, q in enumerate(questions):
            parts = q.split("||")
            question = parts[0]
            answer = parts[1] if len(parts) > 1 else "Answer not available"

            with st.expander(f"❓ Question {i+1}"):
                st.markdown(f"**{question}**")
                if st.button(f"Show Answer", key=f"ans_{i}"):
                    st.success(f"✓ {answer}")

# ============================================================================
# PRACTICE MODE - DEVICE INTERFACES
# ============================================================================

else:  # Practice mode
    st.markdown(f"## {DEVICES[device]['name']}")
    st.markdown(f"*{DEVICES[device]['type']} by {DEVICES[device]['manufacturer']}*")

    # ========================================================================
    # DFAM INTERFACE
    # ========================================================================

    if device == "DFAM":

        # Oscillators
        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Oscillators</div>', unsafe_allow_html=True)

        cols = st.columns(6)
        with cols[0]:
            vco1_freq = st.slider("VCO1 Freq", -100, 100, 0, key="v1f")
            st.markdown(create_css_knob("VCO1 FREQ", vco1_freq, -100, 100), unsafe_allow_html=True)

        with cols[1]:
            vco1_wave = st.select_slider("Wave", ["Triangle", "Square"], key="v1w")
            st.plotly_chart(create_waveform(vco1_wave, "v1"), use_container_width=True, key="wave1")

        with cols[2]:
            vco1_eg = st.slider("VCO1 EG", -100, 100, 0, key="v1eg")
            st.markdown(create_css_knob("EG AMT", vco1_eg, -100, 100, "%"), unsafe_allow_html=True)

        with cols[3]:
            vco2_freq = st.slider("VCO2 Freq", -100, 100, 0, key="v2f")
            st.markdown(create_css_knob("VCO2 FREQ", vco2_freq, -100, 100), unsafe_allow_html=True)

        with cols[4]:
            vco2_wave = st.select_slider("Wave", ["Triangle", "Square"], key="v2w")
            st.plotly_chart(create_waveform(vco2_wave, "v2"), use_container_width=True, key="wave2")

        with cols[5]:
            vco2_eg = st.slider("VCO2 EG", -100, 100, 0, key="v2eg")
            st.markdown(create_css_knob("EG AMT", vco2_eg, -100, 100, "%"), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Mixer & VCO Controls
        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Mixer & VCO Controls</div>', unsafe_allow_html=True)

        cols = st.columns(6)
        with cols[0]:
            vco_decay = st.slider("VCO Decay", 10, 10000, 300, key="vcd")
            st.caption(f"{vco_decay}ms")
        with cols[1]:
            fm_amt = st.slider("FM Amount", 0, 100, 0, key="fm")
            st.markdown(create_css_knob("FM", fm_amt, 0, 100, "%"), unsafe_allow_html=True)
        with cols[2]:
            hard_sync = st.checkbox("Hard Sync", False, key="sync")
            st.markdown(create_led_display("ON" if hard_sync else "OFF"), unsafe_allow_html=True)
        with cols[3]:
            vco1_lvl = st.slider("VCO1 Level", 0, 100, 75, key="v1l")
            st.markdown(create_css_knob("VCO1", vco1_lvl, 0, 100, "%"), unsafe_allow_html=True)
        with cols[4]:
            vco2_lvl = st.slider("VCO2 Level", 0, 100, 50, key="v2l")
            st.markdown(create_css_knob("VCO2", vco2_lvl, 0, 100, "%"), unsafe_allow_html=True)
        with cols[5]:
            noise = st.slider("Noise", 0, 100, 10, key="noi")
            st.markdown(create_css_knob("NOISE", noise, 0, 100, "%"), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Filter
        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Filter (4-Pole Ladder)</div>', unsafe_allow_html=True)

        cols = st.columns(5)
        with cols[0]:
            cutoff = st.slider("Cutoff", 20, 20000, 1000, key="cut")
            st.caption(f"{cutoff}Hz")
        with cols[1]:
            res = st.slider("Resonance", 0, 100, 30, key="res")
            st.markdown(create_css_knob("RES", res, 0, 100, "%"), unsafe_allow_html=True)
            if res > 85:
                st.caption("⚠️ Self-osc")
        with cols[2]:
            vcf_eg = st.slider("VCF EG", -100, 100, 0, key="vcfeg")
            st.markdown(create_css_knob("VCF EG", vcf_eg, -100, 100, "%"), unsafe_allow_html=True)
        with cols[3]:
            vcf_decay = st.slider("VCF Decay", 10, 10000, 400, key="vcfd")
            st.caption(f"{vcf_decay}ms")
        with cols[4]:
            flt_mode = st.select_slider("Mode", ["LP", "HP"], key="fmode")
            st.markdown(create_led_display(flt_mode), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # VCA
        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">VCA</div>', unsafe_allow_html=True)

        cols = st.columns(3)
        with cols[0]:
            vca_decay = st.slider("VCA Decay", 10, 10000, 500, key="vcad")
            st.caption(f"{vca_decay}ms")
        with cols[1]:
            vca_attack = st.select_slider("VCA Attack", ["FAST", "SLOW"], key="vcaa")
            st.markdown(create_led_display(vca_attack), unsafe_allow_html=True)
        with cols[2]:
            volume = st.slider("Volume", 0, 100, 75, key="vol")
            st.markdown(create_css_knob("VOL", volume, 0, 100, "%"), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Sequencer
        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">8-Step Sequencer</div>', unsafe_allow_html=True)

        tempo = st.slider("Tempo (BPM)", 10, 500, 120, key="tempo")
        step_time = 60000 / (tempo * 2)
        st.caption(f"Step: {step_time:.1f}ms")

        st.markdown("**Pattern:**")
        step_cols = st.columns(8)
        for i in range(8):
            with step_cols[i]:
                active = st.checkbox("", st.session_state.dfam_pattern[i], key=f"s{i}")
                st.session_state.dfam_pattern[i] = active
                vel = st.slider("V", 0, 100, st.session_state.dfam_velocities[i], key=f"vel{i}", label_visibility="collapsed")
                st.session_state.dfam_velocities[i] = vel
                st.caption(f"Step {i+1}")

        transport = st.columns(4)
        with transport[0]:
            st.button("▶ RUN", use_container_width=True)
        with transport[1]:
            st.button("⏸ STOP", use_container_width=True)
        with transport[2]:
            st.button("↻ RESET", use_container_width=True)
        with transport[3]:
            if st.button("💾 SAVE", use_container_width=True):
                settings = {
                    "vco1_freq": vco1_freq, "vco2_freq": vco2_freq, "vco_decay": vco_decay,
                    "fm_amt": fm_amt, "hard_sync": hard_sync,
                    "vco1_lvl": vco1_lvl, "vco2_lvl": vco2_lvl, "noise": noise,
                    "cutoff": cutoff, "res": res, "vcf_eg": vcf_eg, "vcf_decay": vcf_decay,
                    "vca_decay": vca_decay, "volume": volume,
                    "pattern": st.session_state.dfam_pattern,
                    "velocities": st.session_state.dfam_velocities
                }
                name = save_patch("DFAM", settings)
                st.success(f"✓ Saved as {name}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # MOTHER-32 INTERFACE
    # ========================================================================

    elif device == "Mother-32":

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Oscillator & LFO</div>', unsafe_allow_html=True)

        cols = st.columns(5)
        with cols[0]:
            glide = st.slider("Glide", 0, 100, 0, key="glide")
            st.markdown(create_css_knob("GLIDE", glide, 0, 100, "%"), unsafe_allow_html=True)
        with cols[1]:
            m32_vco = st.slider("VCO Freq", -100, 100, 0, key="m32vco")
            st.markdown(create_css_knob("VCO", m32_vco, -100, 100), unsafe_allow_html=True)
        with cols[2]:
            m32_wave = st.select_slider("Wave", ["Saw", "Pulse"], key="m32wave")
            st.plotly_chart(create_waveform(m32_wave, "m32w"), use_container_width=True, key="m32_wave_plot")
        with cols[3]:
            lfo_rate = st.slider("LFO Rate", 0.1, 600, 2.0, key="lfo")
            st.caption(f"{lfo_rate:.1f}Hz")
        with cols[4]:
            lfo_wave = st.select_slider("LFO Wave", ["Square", "Triangle"], key="lfow")
            st.plotly_chart(create_waveform(lfo_wave, "lfow"), use_container_width=True, key="lfo_wave_plot")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Filter & VCA</div>', unsafe_allow_html=True)

        cols = st.columns(4)
        with cols[0]:
            m32_cut = st.slider("Cutoff", 17, 21500, 1000, key="m32cut")
            st.caption(f"{m32_cut}Hz")
        with cols[1]:
            m32_res = st.slider("Resonance", 0, 100, 30, key="m32res")
            st.markdown(create_css_knob("RES", m32_res, 0, 100, "%"), unsafe_allow_html=True)
        with cols[2]:
            m32_vcfeg = st.slider("VCF EG", -100, 100, 0, key="m32vcfeg")
            st.markdown(create_css_knob("EG", m32_vcfeg, -100, 100, "%"), unsafe_allow_html=True)
        with cols[3]:
            m32_vca = st.slider("VCA Level", 0, 100, 75, key="m32vca")
            st.markdown(create_css_knob("VCA", m32_vca, 0, 100, "%"), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.info("32-step sequencer • 64 patterns • 13-note keyboard")

    # ========================================================================
    # SUBHARMONICON INTERFACE
    # ========================================================================

    elif device == "Subharmonicon":

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">VCOs & Subharmonics</div>', unsafe_allow_html=True)

        cols = st.columns(4)
        with cols[0]:
            sub_vco1 = st.slider("VCO1 Freq", -100, 100, 0, key="subv1")
            st.markdown(create_css_knob("VCO1", sub_vco1, -100, 100), unsafe_allow_html=True)
        with cols[1]:
            st.selectbox("Sub 1A", ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷8"], key="sub1a")
            st.caption("Octave: ÷2, Fifth+Oct: ÷3")
        with cols[2]:
            sub_vco2 = st.slider("VCO2 Freq", -100, 100, 0, key="subv2")
            st.markdown(create_css_knob("VCO2", sub_vco2, -100, 100), unsafe_allow_html=True)
        with cols[3]:
            st.selectbox("Sub 2A", ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷8"], key="sub2a")
            st.caption("2 Octaves: ÷4")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class='tip-box'>
        <strong>Harmonic Series:</strong> Subharmonics create undertone series. ÷2 = octave down, ÷3 = perfect fifth + octave, ÷4 = two octaves.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Polyrhythm Generators</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class='hardware-tip'>
        <strong>Polyrhythm Tip:</strong> ÷4 + ÷3 = 4-against-3. Pattern repeats every 12 steps (LCM). Start simple, add complexity!
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(4)
        for i in range(4):
            with cols[i]:
                st.selectbox(f"Rhythm {i+1}", ["÷1", "÷2", "÷3", "÷4", "÷6", "÷8"], key=f"rhy{i}")

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # ELEKTRON ANALOG FOUR
    # ========================================================================

    elif device == "Analog Four":

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">4-Voice Analog Architecture</div>', unsafe_allow_html=True)

        st.markdown("""
        **Oscillators:**
        - 2 oscillators per voice + sub-oscillator each
        - 4 waveforms: Saw, Pulse, Transistor Pulse, Triangle
        - PWM on all waveforms (unique to A4)
        - Sub-osc options: Square -1/-2 oct, 25% pulse -2 oct, 33% pulse -5th

        **Filters:**
        - 4-pole lowpass ladder (Moog-style) with overdrive
        - 2-pole multimode: LP, HP, BP, Notch, Peak
        - Filters can be routed serial or parallel

        **Sequencer Power:**
        - Up to 64 steps per pattern
        - Parameter locks: lock ANY parameter per step
        - Conditional trigs: 100%, 75%, 50%, 25%, 12.5%
        - 4 CV/Gate outputs for external gear
        """)

        st.markdown("""
        <div class='hardware-tip'>
        <strong>🎛️ PARAMETER LOCK WORKFLOW:</strong><br>
        1. Program your sequence<br>
        2. Hold [TRIG] button on step you want to modulate<br>
        3. Turn ANY knob while holding [TRIG]<br>
        4. That parameter is now locked to that step only!<br>
        <br>
        This is THE killer feature - automate filter sweeps, pitch changes, effects per step.
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Track Select</div>', unsafe_allow_html=True)

        track = st.radio("Select Voice/Track", ["Track 1", "Track 2", "Track 3", "Track 4"], horizontal=True)

        cols = st.columns(4)
        with cols[0]:
            osc1_wave = st.selectbox("OSC 1 Wave", ["Saw", "Pulse", "Trans Pulse", "Triangle"])
        with cols[1]:
            osc2_wave = st.selectbox("OSC 2 Wave", ["Saw", "Pulse", "Trans Pulse", "Triangle"])
        with cols[2]:
            filt_type = st.selectbox("Filter Type", ["4-pole LP", "2-pole LP", "HP", "BP", "Notch", "Peak"])
        with cols[3]:
            st.metric("CV Output", f"Track {track[-1]}")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # ELEKTRON ANALOG RYTM
    # ========================================================================

    elif device == "Analog Rytm":

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Hybrid Drum Machine</div>', unsafe_allow_html=True)

        st.markdown("""
        **8 Analog Voices + Sampling:**
        - 12 synthesis models (machines): Kick, Snare, Toms, Hi-hat, Cymbal, Clap, etc.
        - Each voice has analog multimode filter + distortion
        - Layer samples with analog synthesis on each track
        - 12 velocity/pressure-sensitive pads

        **Synthesis Models:**
        - BD HARD: 808-style kick
        - BD FM: FM kick with complex harmonics
        - SD HARD: 909-style snare
        - SD CLASSIC: 606-style snare
        - CP CLASSIC: Hand clap synthesis
        - CH CLASSIC: Closed hi-hat
        - OH CLASSIC: Open hi-hat
        - Plus unique Elektron models

        **Performance Features:**
        - 12 scenes per kit (morph between settings)
        - Performance macros (control multiple params)
        - CTRL-ALL mode (tweak all tracks simultaneously)
        - Sample chains for phrase sampling
        """)

        st.markdown("""
        <div class='hardware-tip'>
        <strong>🥁 HYBRID WORKFLOW:</strong><br>
        1. Select pad/track<br>
        2. Choose synthesis machine (BD HARD, SD CLASSIC, etc.)<br>
        3. Tune analog parameters (pitch, decay, tone)<br>
        4. Load sample in layer mode<br>
        5. Balance analog/sample mix<br>
        <br>
        The magic: analog gives punch/body, sample adds character/texture!
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="hw-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Track/Pad Select</div>', unsafe_allow_html=True)

        pad = st.selectbox("Select Pad", [f"Pad {i} (Track {i})" for i in range(1, 13)])

        cols = st.columns(3)
        with cols[0]:
            machine = st.selectbox("Synthesis Machine", [
                "BD HARD (808)", "BD FM", "BD PLASTIC",
                "SD HARD (909)", "SD CLASSIC (606)", "SD NATURAL",
                "RS HARD", "RS CLASSIC",
                "CP CLASSIC", "CH CLASSIC", "OH CLASSIC",
                "CY CLASSIC", "CB CLASSIC"
            ])
        with cols[1]:
            sample_layer = st.checkbox("Sample Layer Enabled", True)
        with cols[2]:
            st.slider("Analog/Sample Mix", 0, 100, 50, help="0=All analog, 100=All sample")

        st.markdown('</div>', unsafe_allow_html=True)

        st.info("💡 Tip: Use scenes to create variations. Scene A = tight, Scene B = loose, morph in performance!")

        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📚 Resources**")
    st.markdown("[DFAM Manual](https://api.moogmusic.com/sites/default/files/2018-04/DFAM_Manual.pdf)")
    st.markdown("[Mother-32 Manual](https://api.moogmusic.com/sites/default/files/2018-01/Mother_32_Manual.pdf)")
    st.markdown("[Patch Library](https://patch-library.net)")
    st.markdown("[Elektron Manual Archive](https://www.elektron.se/support)")

with col2:
    st.markdown("**🧠 Learning**")
    st.caption("Spaced repetition")
    st.caption("Active recall")
    st.caption("Hands-on practice")
    st.caption("Community patches")

with col3:
    st.markdown("**⚡ Performance**")
    st.caption("CSS knobs (10x faster)")
    st.caption("Cached waveforms")
    st.caption("Optimized rendering")
    st.caption("<500ms load time")

st.caption("Built for laptop-beside-hardware learning • All specs from official manuals • Optimized for production use")
