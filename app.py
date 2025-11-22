"""
SYNTH STUDIO - Hardware Reference & Learning Tool
Hardware-accurate layouts • Science-backed learning • Laptop-optimized workflow
"""

import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime, timedelta
from pathlib import Path

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
# PROFESSIONAL CSS - HARDWARE-INSPIRED DESIGN
# ============================================================================

st.markdown("""
<style>
    /* Clean professional background */
    .stApp {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 50%, #0d0d0d 100%);
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }

    /* Hardware panel container - resembles actual device */
    .hardware-panel {
        background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
        border: 2px solid #3a3a3a;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
    }

    /* Section dividers like physical panels */
    .panel-section {
        border: 1px solid #333;
        background: rgba(0,0,0,0.2);
        border-radius: 4px;
        padding: 12px;
        margin: 8px 0;
    }

    /* Section headers - clean typography */
    .section-header {
        color: #fff;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 0 12px 0;
        padding: 8px 0 8px 0;
        border-bottom: 2px solid #0f0;
        text-align: left;
    }

    /* Control labels - hardware style */
    .control-label {
        font-size: 8px;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 4px 0;
        text-align: center;
    }

    /* LED-style value display */
    .led-display {
        background: #000;
        color: #0f0;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 10px;
        border: 2px solid #1a1a1a;
        border-radius: 3px;
        text-align: center;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.8), 0 0 8px rgba(0,255,0,0.3);
        min-width: 60px;
    }

    /* Hardware buttons */
    .stButton > button {
        background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
        color: #e0e0e0;
        border: 1px solid #4a4a4a;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 8px 16px;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #3a3a3a 0%, #2a2a2a 100%);
        border-color: #0f0;
        box-shadow: 0 0 12px rgba(0,255,0,0.4);
    }

    .stButton > button:active {
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
        transform: translateY(1px);
    }

    /* Sliders - hardware pots */
    .stSlider {
        padding: 4px 0;
    }

    /* Sidebar - control center */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #151515 100%);
        border-right: 2px solid #2a2a2a;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f0;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        border-bottom: 1px solid #2a2a2a;
        padding-bottom: 6px;
    }

    /* Learning callout boxes */
    .learning-tip {
        background: linear-gradient(135deg, #1a2a1a 0%, #0d1a0d 100%);
        border-left: 4px solid #0f0;
        padding: 12px 16px;
        margin: 12px 0;
        border-radius: 4px;
        font-size: 11px;
        line-height: 1.6;
    }

    .try-hardware {
        background: linear-gradient(135deg, #2a1a1a 0%, #1a0d0d 100%);
        border-left: 4px solid #f90;
        padding: 12px 16px;
        margin: 12px 0;
        border-radius: 4px;
        font-size: 11px;
        line-height: 1.6;
    }

    /* Patch cable visualization */
    .patch-point {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 2px solid #666;
        background: #111;
        margin: 2px;
    }

    .patch-point-output {
        border-color: #0f0;
        box-shadow: 0 0 8px rgba(0,255,0,0.4);
    }

    .patch-point-input {
        border-color: #f90;
        box-shadow: 0 0 8px rgba(255,153,0,0.4);
    }

    /* Compact metrics */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        color: #0f0;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Responsive optimizations */
    @media (max-width: 1200px) {
        .hardware-panel {
            padding: 12px;
        }
        .section-header {
            font-size: 9px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HARDWARE SPECIFICATIONS - VERIFIED FROM OFFICIAL MANUALS
# ============================================================================

DEVICES = {
    "DFAM": {
        "name": "DFAM - Drummer From Another Mother",
        "manufacturer": "Moog Music",
        "manual": "Manual D_Web",
        "panel_layout": {
            "top_row": ["VCO1 FREQ", "VCO1 WAVE", "VCO1 EG", "VCO2 FREQ", "VCO2 WAVE", "VCO2 EG"],
            "second_row": ["VCO DECAY", "FM AMOUNT", "HARD SYNC", "VCO1 LEVEL", "VCO2 LEVEL", "NOISE"],
            "third_row": ["CUTOFF", "RESONANCE", "VCF EG", "VCF DECAY", "MODE"],
            "fourth_row": ["VCA DECAY", "VCA ATTACK", "VOLUME"],
            "bottom": "8-STEP SEQUENCER"
        },
        "specs": {
            "vco_range": "±5 octaves",
            "filter": "4-pole 20Hz-20kHz",
            "envelopes": "3 (VCO, VCF, VCA)",
            "sequencer": "8 steps",
            "patchbay": "24 points (15 in, 9 out)"
        }
    },
    "Mother-32": {
        "name": "Mother-32 Semi-Modular Synthesizer",
        "manufacturer": "Moog Music",
        "manual": "Manual v1.1",
        "panel_layout": {
            "top_row": ["GLIDE", "VCO FREQ", "VCO WAVE", "LFO RATE", "LFO WAVE"],
            "second_row": ["VCF CUTOFF", "VCF RES", "VCF EG AMT", "VCA LEVEL"],
            "third_row": ["EG ATTACK", "EG DECAY"],
            "bottom": "32-STEP SEQUENCER + KEYBOARD"
        },
        "specs": {
            "vco": "Saw/Pulse with PWM",
            "lfo": "0.1-600Hz measured",
            "filter": "4-pole 17Hz-21.5kHz",
            "sequencer": "32 steps, 64 patterns",
            "patchbay": "32 points (18 in, 14 out)"
        }
    },
    "Subharmonicon": {
        "name": "Subharmonicon Polyrhythmic Synthesizer",
        "manufacturer": "Moog Music",
        "panel_layout": {
            "top_row": ["VCO1 FREQ", "VCO1 SUBS", "VCO2 FREQ", "VCO2 SUBS"],
            "second_row": ["MIXER", "FILTER", "ENVELOPE"],
            "third_row": ["RHYTHM 1", "RHYTHM 2", "RHYTHM 3", "RHYTHM 4"],
            "bottom": "2x4-STEP SEQUENCERS"
        },
        "specs": {
            "vcos": "2 analog VCOs",
            "subharmonics": "4 per VCO (÷1 to ÷16)",
            "rhythms": "4 polyrhythmic generators",
            "sequencers": "2x4-step",
            "patchbay": "16 points"
        }
    }
}

# ============================================================================
# LEARNING SYSTEM - SPACED REPETITION & ACTIVE RECALL
# ============================================================================

LEARNING_CHALLENGES = {
    "DFAM": [
        {
            "title": "Classic Kick Drum",
            "difficulty": "Beginner",
            "goal": "Create a punchy kick using VCO pitch sweep and fast VCA decay",
            "patch": {
                "VCO1_FREQ": 15, "VCO2_FREQ": 20, "VCO_DECAY": 300,
                "VCO1_LEVEL": 80, "VCO2_LEVEL": 60, "NOISE": 10,
                "VCF_CUTOFF": 800, "VCF_EG": 60, "VCF_DECAY": 400,
                "VCA_DECAY": 150, "VCA_ATTACK": "FAST"
            },
            "try_hardware": "Start with VCO1 and VCO2 at noon. Slowly increase VCO_DECAY while tapping TRIGGER. Listen for pitch sweep.",
            "learn": "Kick drums use fast pitch envelope (VCO EG) from high to low frequency. The 'thump' comes from this pitch sweep."
        },
        {
            "title": "Hi-Hat Pattern",
            "difficulty": "Intermediate",
            "goal": "Create metallic hi-hats using noise and high-pass filter",
            "patch": {
                "VCO1_FREQ": 85, "VCO2_FREQ": 90, "VCO_DECAY": 50,
                "VCO1_LEVEL": 30, "VCO2_LEVEL": 35, "NOISE": 85,
                "VCF_CUTOFF": 8000, "VCF_EG": -40, "VCF_DECAY": 80,
                "VCA_DECAY": 60, "VCA_ATTACK": "FAST", "FILTER_MODE": "HP"
            },
            "try_hardware": "Switch filter to HP mode. Set VCOs very high. Increase NOISE to 75%. Note how filter EG shapes the 'tss' sound.",
            "learn": "Hi-hats = HIGH frequency oscillators + NOISE + short decay. HP filter removes low end for crisp sound."
        },
        {
            "title": "FM Bass Stab",
            "difficulty": "Advanced",
            "goal": "Use frequency modulation for harmonic bass stabs",
            "patch": {
                "VCO1_FREQ": 30, "VCO2_FREQ": 35, "VCO_DECAY": 200,
                "FM_AMOUNT": 70, "HARD_SYNC": "ON",
                "VCO1_LEVEL": 90, "VCO2_LEVEL": 45, "NOISE": 5,
                "VCF_CUTOFF": 1200, "VCF_EG": 80, "VCF_DECAY": 300,
                "VCA_DECAY": 250
            },
            "try_hardware": "Enable HARD SYNC. Patch VCO2→FM input. Adjust FM_AMOUNT while listening. Hear harmonic content change.",
            "learn": "FM (Frequency Modulation) = one oscillator modulating another's frequency. Creates complex harmonic tones. SYNC locks VCO2 to VCO1 for tighter sound."
        }
    ],
    "Mother-32": [
        {
            "title": "Analog Bass",
            "difficulty": "Beginner",
            "goal": "Program a classic analog bass sequence",
            "patch": {
                "VCO_FREQ": 0, "WAVE": "SAW", "GLIDE": 20,
                "VCF_CUTOFF": 40, "VCF_RES": 60, "VCF_EG": 70,
                "EG_ATTACK": 5, "EG_DECAY": 300,
                "VCA_LEVEL": 75
            },
            "try_hardware": "Set sequencer to 8 steps. Program root note pattern: C-C-G-C-C-G-Bb-C. Add slight GLIDE for legato.",
            "learn": "Saw wave = rich harmonics, perfect for bass. Low-pass filter removes highs. Resonance adds 'squelch' character."
        }
    ]
}

RECALL_PROMPTS = {
    "DFAM": [
        "What does VCO DECAY control? (Answer: Pitch envelope decay time)",
        "Which filter mode removes low frequencies? (Answer: HP / High-Pass)",
        "How many patch points total? (Answer: 24 - 15 inputs, 9 outputs)",
        "What creates the 'kick' in a kick drum patch? (Answer: Fast pitch envelope from high to low)",
        "What does FM AMOUNT control? (Answer: How much VCO2 modulates VCO1 frequency)"
    ],
    "Mother-32": [
        "What is the LFO range? (Answer: 0.1-600Hz measured)",
        "How many sequencer steps? (Answer: 32 steps)",
        "How many patterns can be stored? (Answer: 64 patterns in 8 banks)",
        "What waveforms does the VCO produce? (Answer: Saw and Pulse with PWM)"
    ]
}

# ============================================================================
# VISUAL COMPONENTS - HARDWARE ACCURATE
# ============================================================================

def create_hardware_knob(label, value, min_val, max_val, bipolar=False, unit="", size=110):
    """Hardware-accurate knob with proper scaling"""
    fig = go.Figure()

    # Outer bezel
    fig.add_shape(type="circle", x0=-1.1, y0=-1.1, x1=1.1, y1=1.1,
                  fillcolor="rgb(40,40,40)",
                  line=dict(color="rgb(70,70,70)", width=2))

    # Knob body - realistic gradient
    fig.add_shape(type="circle", x0=-1, y0=-1, x1=1, y1=1,
                  fillcolor="rgb(30,30,30)",
                  line=dict(color="rgb(20,20,20)", width=1))

    # Inner shadow circle
    fig.add_shape(type="circle", x0=-0.88, y0=-0.88, x1=0.88, y1=0.88,
                  fillcolor="rgb(25,25,25)",
                  line=dict(color="rgb(15,15,15)", width=1))

    # 11-position tick marks (hardware standard)
    for i in range(11):
        angle = -135 + (i * 27)  # 270° travel / 10 steps
        rad = math.radians(angle)
        x1, y1 = 0.72 * math.cos(rad), 0.72 * math.sin(rad)
        x2, y2 = 0.88 * math.cos(rad), 0.88 * math.sin(rad)

        # Highlight center mark for bipolar controls
        if i == 5 and bipolar:
            fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2,
                         line=dict(color="#ffffff", width=3))
        else:
            fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2,
                         line=dict(color="rgb(120,120,120)", width=1.5))

    # Position indicator (white line from center)
    normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
    angle = -135 + (normalized * 270)
    rad = math.radians(angle)
    fig.add_shape(type="line", x0=0, y0=0,
                  x1=0.65*math.cos(rad), y1=0.65*math.sin(rad),
                  line=dict(color="#ffffff", width=3))

    # Center cap
    fig.add_shape(type="circle", x0=-0.12, y0=-0.12, x1=0.12, y1=0.12,
                  fillcolor="rgb(180,180,180)", line=dict(width=0))

    # Label below
    fig.add_annotation(x=0, y=-1.5, text=label, showarrow=False,
                      font=dict(family="Arial", size=9, color="#999"))

    # Value above (LED style)
    display_val = f"{value}{unit}" if unit else f"{value}"
    fig.add_annotation(x=0, y=1.5, text=display_val, showarrow=False,
                      font=dict(family="Courier New", size=11, color="#0f0", weight=700))

    fig.update_layout(
        showlegend=False,
        width=size, height=size,
        margin=dict(l=0,r=0,t=15,b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, range=[-1.6,1.6]),
        yaxis=dict(visible=False, range=[-1.6,1.6])
    )

    return fig

def create_waveform_scope(wave_type, freq=1.0, height=100):
    """Oscilloscope-style waveform display"""
    x = np.linspace(0, 4*np.pi, 600)

    if wave_type.lower() == "triangle":
        y = 2 * np.abs(2 * ((x*freq)/(2*np.pi) - np.floor((x*freq)/(2*np.pi) + 0.5))) - 1
    elif wave_type.lower() == "square":
        y = np.sign(np.sin(x * freq))
    elif wave_type.lower() == "saw":
        y = 2 * ((x*freq)/(2*np.pi) - np.floor((x*freq)/(2*np.pi) + 0.5))
    elif wave_type.lower() == "pulse":
        y = (np.sin(x * freq) > 0.5).astype(float) * 2 - 1
    else:  # noise
        y = np.random.normal(0, 0.3, len(x))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(color='#0f0', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,255,0,0.15)'
    ))

    # Grid lines for scope realism
    for i in np.linspace(-1, 1, 5):
        fig.add_hline(y=i, line_dash="dot", line_color="rgba(0,255,0,0.2)", line_width=1)

    fig.update_layout(
        showlegend=False,
        height=height,
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor='rgb(5,5,5)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, range=[-1.3,1.3])
    )

    return fig

def create_sequencer_display(steps, active_steps, velocities, current_step=0):
    """Hardware-style step sequencer display"""
    fig = go.Figure()

    for i in range(steps):
        x = i * 1.3
        is_active = active_steps[i]
        is_current = (i == current_step)

        # Step pad
        if is_current:
            color = "rgb(255,153,0)"  # Orange for current step
        elif is_active:
            color = "rgb(0,255,0)"  # Green for active
        else:
            color = "rgb(30,30,30)"  # Dark for inactive

        border_color = "rgb(100,100,100)" if not is_current else "rgb(255,153,0)"

        fig.add_shape(
            type="rect",
            x0=x-0.5, y0=-0.5, x1=x+0.5, y1=0.5,
            fillcolor=color,
            line=dict(color=border_color, width=2)
        )

        # Step number
        text_color = "#000" if (is_active or is_current) else "#666"
        fig.add_annotation(
            x=x, y=0, text=str(i+1),
            showarrow=False,
            font=dict(size=10, color=text_color, weight=700)
        )

        # Velocity bar
        if velocities and velocities[i] > 0:
            vel_height = (velocities[i] / 100) * 0.8
            fig.add_shape(
                type="rect",
                x0=x-0.4, y0=0.6, x1=x+0.4, y1=0.6+vel_height,
                fillcolor="rgba(0,255,0,0.6)",
                line=dict(width=0)
            )

    fig.update_layout(
        showlegend=False,
        height=120,
        margin=dict(l=5,r=5,t=5,b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, range=[-1, steps*1.3]),
        yaxis=dict(visible=False, range=[-1, 2])
    )

    return fig

def create_patch_bay(inputs, outputs):
    """Visual patchbay representation"""
    html = '<div style="background: #0a0a0a; padding: 15px; border-radius: 4px; border: 1px solid #333;">'
    html += '<div style="font-size: 9px; color: #0f0; font-weight: 700; margin-bottom: 10px; letter-spacing: 1px;">PATCH BAY</div>'

    html += '<div style="margin-bottom: 8px;">'
    html += '<div style="font-size: 8px; color: #f90; margin-bottom: 4px;">OUTPUTS</div>'
    for output in outputs[:6]:  # Show first 6
        html += f'<span class="patch-point patch-point-output" title="{output}"></span>'
    html += '</div>'

    html += '<div>'
    html += '<div style="font-size: 8px; color: #0f0; margin-bottom: 4px;">INPUTS</div>'
    for inp in inputs[:8]:  # Show first 8
        html += f'<span class="patch-point patch-point-input" title="{inp}"></span>'
    html += '</div>'

    html += '</div>'
    return html

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def init_session_state():
    """Initialize all session state variables"""
    if 'device' not in st.session_state:
        st.session_state.device = "DFAM"
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()
    if 'challenges_completed' not in st.session_state:
        st.session_state.challenges_completed = []
    if 'active_challenge' not in st.session_state:
        st.session_state.active_challenge = None
    if 'learning_mode' not in st.session_state:
        st.session_state.learning_mode = "Practice"
    if 'dfam_pattern' not in st.session_state:
        st.session_state.dfam_pattern = [True, False, True, False, True, False, True, False]
    if 'dfam_velocities' not in st.session_state:
        st.session_state.dfam_velocities = [100, 0, 80, 0, 100, 0, 70, 0]
    if 'user_patches' not in st.session_state:
        st.session_state.user_patches = {}
    if 'show_recall' not in st.session_state:
        st.session_state.show_recall = False
    if 'recall_interval' not in st.session_state:
        st.session_state.recall_interval = 5  # minutes

def save_user_patch(device, name, settings):
    """Save patch with timestamp for spaced repetition"""
    st.session_state.user_patches[name] = {
        "device": device,
        "settings": settings,
        "created": datetime.now().isoformat(),
        "last_practiced": datetime.now().isoformat(),
        "practice_count": 0
    }
    # Persist to file
    with open("user_patches.json", "w") as f:
        json.dump(st.session_state.user_patches, f, indent=2)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

init_session_state()

# Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #1a1a1a 0%, #0d0d0d 50%, #1a1a1a 100%);
            border-bottom: 2px solid #0f0; margin-bottom: 20px;'>
    <h1 style='color: #e0e0e0; font-size: 28px; font-weight: 700;
               letter-spacing: 4px; margin: 0;'>SYNTH STUDIO</h1>
    <p style='color: #0f0; font-size: 10px; text-transform: uppercase;
              letter-spacing: 2px; margin: 8px 0 0 0;'>
        Hardware Reference • Learning System • Laptop Workflow
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - DEVICE & MODE SELECTION
# ============================================================================

with st.sidebar:
    st.markdown("### DEVICE SELECT")
    device = st.selectbox(
        "",
        list(DEVICES.keys()),
        format_func=lambda x: DEVICES[x]["name"],
        label_visibility="collapsed",
        key="device_selector"
    )
    st.session_state.device = device

    st.markdown("---")

    st.markdown("### LEARNING MODE")
    mode = st.radio(
        "",
        ["Practice", "Challenge", "Active Recall"],
        label_visibility="collapsed"
    )
    st.session_state.learning_mode = mode

    st.markdown("---")

    # Quick specs
    st.markdown("### QUICK SPECS")
    specs = DEVICES[device]["specs"]
    for key, val in specs.items():
        st.markdown(f"**{key.replace('_', ' ').upper()}**  \n`{val}`")

    st.markdown("---")

    # Session stats
    elapsed = datetime.now() - st.session_state.session_start
    mins = elapsed.seconds // 60
    secs = elapsed.seconds % 60
    st.metric("Session Time", f"{mins}:{secs:02d}")
    st.metric("Challenges Done", len(st.session_state.challenges_completed))

    st.markdown("---")

    # Help
    with st.expander("💡 How to Use"):
        st.markdown("""
        **Laptop-Beside-Hardware Workflow:**

        1. **Practice Mode**: Mirror your hardware settings
        2. **Challenge Mode**: Follow guided patches
        3. **Active Recall**: Test your knowledge

        **Learning Tips:**
        - Complete challenges in order
        - Try patches on real hardware
        - Use recall prompts every 5 min
        - Save your own patches
        """)

# ============================================================================
# MAIN CONTENT - DEVICE INTERFACES
# ============================================================================

if device == "DFAM":

    # Mode-specific content
    if mode == "Challenge":
        st.markdown("## 🎯 Learning Challenges")

        challenges = LEARNING_CHALLENGES["DFAM"]
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
            challenge = st.session_state.active_challenge

            st.markdown(f"""
            <div class='learning-tip'>
            <strong>GOAL:</strong> {challenge['goal']}<br>
            <strong>DIFFICULTY:</strong> {challenge['difficulty']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='try-hardware'>
            <strong>🎛️ TRY ON HARDWARE:</strong><br>
            {challenge['try_hardware']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='learning-tip'>
            <strong>📚 LEARN:</strong><br>
            {challenge['learn']}
            </div>
            """, unsafe_allow_html=True)

            # Load patch settings
            patch = challenge['patch']

            if st.button("✅ Mark Complete", use_container_width=True):
                if challenge['title'] not in st.session_state.challenges_completed:
                    st.session_state.challenges_completed.append(challenge['title'])
                    st.success(f"Challenge '{challenge['title']}' completed! 🎉")
                st.session_state.active_challenge = None
                st.rerun()

        st.markdown("---")

    elif mode == "Active Recall":
        st.markdown("## 🧠 Active Recall Practice")

        st.markdown("""
        <div class='learning-tip'>
        <strong>Science-backed learning:</strong> Active recall strengthens neural pathways.
        Answer these questions without looking at your hardware.
        </div>
        """, unsafe_allow_html=True)

        prompts = RECALL_PROMPTS.get(device, [])

        for i, prompt in enumerate(prompts):
            with st.expander(f"Question {i+1}"):
                st.markdown(f"**{prompt.split('(Answer:')[0].strip()}**")
                if st.button(f"Show Answer", key=f"ans_{i}"):
                    answer = prompt.split('(Answer:')[1].strip().rstrip(')')
                    st.success(f"✓ {answer}")

        st.markdown("---")

    # Hardware panel layout
    st.markdown("## DFAM Control Panel")
    st.markdown("*Layout matches physical hardware - follow along with your device*")

    # Top row - Oscillators
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">OSCILLATORS</div>', unsafe_allow_html=True)

    cols = st.columns(6)
    with cols[0]:
        vco1_freq = st.slider("VCO1 FREQ", -100, 100, 0, key="vco1f")
        st.plotly_chart(create_hardware_knob("VCO1 FREQ", vco1_freq, -100, 100, True), use_container_width=True)

    with cols[1]:
        vco1_wave = st.select_slider("VCO1 WAVE", ["Triangle", "Square"], key="vco1w")
        st.plotly_chart(create_waveform_scope(vco1_wave, height=90), use_container_width=True)

    with cols[2]:
        vco1_eg = st.slider("VCO1 EG", -100, 100, 0, key="vco1eg")
        st.plotly_chart(create_hardware_knob("VCO1 EG", vco1_eg, -100, 100, True, "%"), use_container_width=True)

    with cols[3]:
        vco2_freq = st.slider("VCO2 FREQ", -100, 100, 0, key="vco2f")
        st.plotly_chart(create_hardware_knob("VCO2 FREQ", vco2_freq, -100, 100, True), use_container_width=True)

    with cols[4]:
        vco2_wave = st.select_slider("VCO2 WAVE", ["Triangle", "Square"], key="vco2w")
        st.plotly_chart(create_waveform_scope(vco2_wave, height=90), use_container_width=True)

    with cols[5]:
        vco2_eg = st.slider("VCO2 EG", -100, 100, 0, key="vco2eg")
        st.plotly_chart(create_hardware_knob("VCO2 EG", vco2_eg, -100, 100, True, "%"), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Second row - VCO Controls & Mixer
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">VCO CONTROLS & MIXER</div>', unsafe_allow_html=True)

    cols = st.columns(6)
    with cols[0]:
        vco_decay = st.slider("VCO DECAY", 10, 10000, 300, key="vcod")
        st.caption(f"{vco_decay}ms")

    with cols[1]:
        fm_amt = st.slider("FM AMOUNT", 0, 100, 0, key="fm")
        st.plotly_chart(create_hardware_knob("FM AMT", fm_amt, 0, 100, unit="%"), use_container_width=True)

    with cols[2]:
        hard_sync = st.checkbox("HARD SYNC", False, key="sync")
        st.markdown(f"<div class='led-display'>{'ON' if hard_sync else 'OFF'}</div>", unsafe_allow_html=True)

    with cols[3]:
        vco1_lvl = st.slider("VCO1 LVL", 0, 100, 75, key="vco1l")
        st.plotly_chart(create_hardware_knob("VCO1", vco1_lvl, 0, 100, unit="%"), use_container_width=True)

    with cols[4]:
        vco2_lvl = st.slider("VCO2 LVL", 0, 100, 50, key="vco2l")
        st.plotly_chart(create_hardware_knob("VCO2", vco2_lvl, 0, 100, unit="%"), use_container_width=True)

    with cols[5]:
        noise = st.slider("NOISE", 0, 100, 10, key="noise")
        st.plotly_chart(create_hardware_knob("NOISE", noise, 0, 100, unit="%"), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Third row - Filter
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">FILTER (4-POLE LADDER)</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    with cols[0]:
        vcf_cutoff = st.slider("CUTOFF", 20, 20000, 1000, key="cutoff")
        st.caption(f"{vcf_cutoff}Hz")

    with cols[1]:
        vcf_res = st.slider("RESONANCE", 0, 100, 30, key="res")
        st.plotly_chart(create_hardware_knob("RES", vcf_res, 0, 100, unit="%"), use_container_width=True)
        if vcf_res > 85:
            st.caption("⚠️ Self-oscillation")

    with cols[2]:
        vcf_eg = st.slider("VCF EG AMT", -100, 100, 0, key="vcfeg")
        st.plotly_chart(create_hardware_knob("VCF EG", vcf_eg, -100, 100, True, "%"), use_container_width=True)

    with cols[3]:
        vcf_decay = st.slider("VCF DECAY", 10, 10000, 400, key="vcfd")
        st.caption(f"{vcf_decay}ms")

    with cols[4]:
        vcf_mode = st.select_slider("FILTER MODE", ["LP", "HP"], key="fmode")
        st.markdown(f"<div class='led-display'>{vcf_mode}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Fourth row - VCA
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">VCA (VOLTAGE CONTROLLED AMPLIFIER)</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        vca_decay = st.slider("VCA DECAY", 10, 10000, 500, key="vcad")
        st.caption(f"{vca_decay}ms")

    with cols[1]:
        vca_attack = st.select_slider("VCA ATTACK", ["FAST", "SLOW"], key="vcaa")
        st.markdown(f"<div class='led-display'>{vca_attack}</div>", unsafe_allow_html=True)

    with cols[2]:
        volume = st.slider("VOLUME", 0, 100, 75, key="vol")
        st.plotly_chart(create_hardware_knob("VOL", volume, 0, 100, unit="%"), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Bottom - Sequencer
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">8-STEP ANALOG SEQUENCER</div>', unsafe_allow_html=True)

    tempo = st.slider("TEMPO (BPM)", 10, 500, 120, key="tempo")
    step_time = 60000 / (tempo * 2)
    st.caption(f"Step time: {step_time:.1f}ms • Pattern length: {step_time*8:.1f}ms")

    # Step editor
    st.markdown("**STEP PATTERN** (Active steps)")
    step_cols = st.columns(8)
    for i in range(8):
        with step_cols[i]:
            active = st.checkbox("", st.session_state.dfam_pattern[i], key=f"step_{i}")
            st.session_state.dfam_pattern[i] = active
            st.markdown(f"<div style='text-align:center; font-size:9px; color:#999;'>STEP {i+1}</div>", unsafe_allow_html=True)

    st.markdown("**VELOCITY** (Per step)")
    vel_cols = st.columns(8)
    for i in range(8):
        with vel_cols[i]:
            vel = st.slider("", 0, 100, st.session_state.dfam_velocities[i], key=f"vel_{i}", label_visibility="collapsed")
            st.session_state.dfam_velocities[i] = vel

    # Sequencer visualization
    st.plotly_chart(
        create_sequencer_display(8, st.session_state.dfam_pattern, st.session_state.dfam_velocities),
        use_container_width=True
    )

    # Transport controls
    transport = st.columns(5)
    with transport[0]:
        st.button("▶ RUN", use_container_width=True)
    with transport[1]:
        st.button("⏸ STOP", use_container_width=True)
    with transport[2]:
        st.button("⏭ STEP", use_container_width=True)
    with transport[3]:
        st.button("↻ RESET", use_container_width=True)
    with transport[4]:
        if st.button("💾 SAVE", use_container_width=True):
            settings = {
                "vco1_freq": vco1_freq, "vco2_freq": vco2_freq,
                "vco_decay": vco_decay, "fm_amount": fm_amt,
                "vco1_level": vco1_lvl, "vco2_level": vco2_lvl, "noise": noise,
                "vcf_cutoff": vcf_cutoff, "vcf_res": vcf_res, "vcf_eg": vcf_eg,
                "vcf_decay": vcf_decay, "vca_decay": vca_decay,
                "pattern": st.session_state.dfam_pattern,
                "velocities": st.session_state.dfam_velocities
            }
            name = f"DFAM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            save_user_patch("DFAM", name, settings)
            st.success(f"✓ Saved as {name}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Patchbay
    st.markdown("### Patchbay")
    outputs = ["VCA", "VCA EG", "VCF EG", "VCO EG", "VCO1", "VCO2", "TRIGGER", "VELOCITY", "PITCH"]
    inputs = ["TRIGGER", "VCA CV", "VELOCITY", "VCA DECAY", "EXT AUDIO", "VCF DECAY", "NOISE", "VCO DECAY", "VCF MOD", "VCO1 CV", "FM AMT", "VCO2 CV", "TEMPO", "RUN/STOP", "ADV/CLK"]
    st.markdown(create_patch_bay(inputs, outputs), unsafe_allow_html=True)

elif device == "Mother-32":

    st.markdown("## Mother-32 Control Panel")
    st.markdown("*32-step sequencer with full patchbay - layout matches hardware*")

    # Top row
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">OSCILLATOR & LFO</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    with cols[0]:
        glide = st.slider("GLIDE", 0, 100, 0, key="m32_glide")
        st.plotly_chart(create_hardware_knob("GLIDE", glide, 0, 100, unit="%"), use_container_width=True)

    with cols[1]:
        m32_vco_freq = st.slider("VCO FREQ", -100, 100, 0, key="m32_vco")
        st.plotly_chart(create_hardware_knob("VCO", m32_vco_freq, -100, 100, True), use_container_width=True)

    with cols[2]:
        m32_wave = st.select_slider("WAVE", ["Saw", "Pulse"], key="m32_wave")
        st.plotly_chart(create_waveform_scope(m32_wave, height=90), use_container_width=True)
        if m32_wave == "Pulse":
            pw = st.slider("Pulse Width", 2, 98, 50, key="m32_pw")
            st.caption(f"PW: {pw}%")

    with cols[3]:
        lfo_rate = st.slider("LFO RATE", 0.1, 600, 2.0, key="m32_lfo")
        st.caption(f"{lfo_rate:.1f}Hz")

    with cols[4]:
        lfo_wave = st.select_slider("LFO WAVE", ["Square", "Triangle"], key="m32_lfowave")
        st.plotly_chart(create_waveform_scope(lfo_wave, 0.3, height=90), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Second row - Filter & VCA
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">FILTER & VCA</div>', unsafe_allow_html=True)

    cols = st.columns(4)
    with cols[0]:
        m32_cutoff = st.slider("VCF CUTOFF", 17, 21500, 1000, key="m32_cut")
        st.caption(f"{m32_cutoff}Hz")

    with cols[1]:
        m32_res = st.slider("VCF RES", 0, 100, 30, key="m32_res")
        st.plotly_chart(create_hardware_knob("RES", m32_res, 0, 100, unit="%"), use_container_width=True)

    with cols[2]:
        m32_vcf_eg = st.slider("VCF EG AMT", -100, 100, 0, key="m32_vcfeg")
        st.plotly_chart(create_hardware_knob("EG AMT", m32_vcf_eg, -100, 100, True, "%"), use_container_width=True)

    with cols[3]:
        m32_vca = st.slider("VCA LEVEL", 0, 100, 75, key="m32_vca")
        st.plotly_chart(create_hardware_knob("VCA", m32_vca, 0, 100, unit="%"), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Envelope
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">ENVELOPE GENERATOR</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]:
        m32_attack = st.slider("ATTACK", 1.25, 3000, 10, key="m32_att")
        st.caption(f"{m32_attack:.1f}ms")

    with cols[1]:
        m32_decay = st.slider("DECAY/RELEASE", 1.25, 7000, 500, key="m32_dec")
        st.caption(f"{m32_decay:.1f}ms")

    st.markdown('</div>', unsafe_allow_html=True)

    # Sequencer
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">32-STEP SEQUENCER</div>', unsafe_allow_html=True)

    st.info("32-step sequencer with 64 patterns in 8 banks")

    seq_tempo = st.slider("TEMPO", 10, 300, 120, key="m32_tempo")
    st.caption(f"{seq_tempo} BPM")

    st.markdown("**Sequencer features:**")
    st.markdown("- 32 steps per pattern")
    st.markdown("- 64 patterns (8 banks × 8 patterns)")
    st.markdown("- Real-time transpose via keyboard")
    st.markdown("- Gate length control")
    st.markdown("- Ratcheting")

    st.markdown('</div>', unsafe_allow_html=True)

    # Patchbay
    st.markdown("### Patchbay (32 points)")
    outputs = ["VCA", "NOISE", "VCF", "VCO SAW", "VCO PULSE", "LFO TRI", "LFO SQ", "VC MIX", "MULT 1", "MULT 2", "ASSIGN", "EG", "KB", "GATE"]
    inputs = ["EXT AUDIO", "MIX CV", "VCA CV", "VCF CUTOFF", "VCF RES", "VCO 1V/OCT", "VCO LIN FM", "VCO MOD", "LFO RATE", "MIX 1", "MIX 2", "VC MIX", "MULT", "GATE", "TEMPO", "RUN/STOP", "RESET", "HOLD"]
    st.markdown(create_patch_bay(inputs, outputs), unsafe_allow_html=True)

    st.markdown("""
    <div class='try-hardware'>
    <strong>🎛️ WORKFLOW TIP:</strong><br>
    Mother-32's 13-note keyboard makes it perfect for bass sequences. Program a pattern on your hardware,
    then use this reference to understand which patch points to explore for modulation.
    </div>
    """, unsafe_allow_html=True)

elif device == "Subharmonicon":

    st.markdown("## Subharmonicon Control Panel")
    st.markdown("*Polyrhythmic synthesizer - subharmonics & rhythm generators*")

    # Oscillators & Subharmonics
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">VCO 1 & SUBHARMONICS</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    with cols[0]:
        sub_vco1 = st.slider("VCO1 FREQ", -100, 100, 0, key="sub_vco1")
        st.plotly_chart(create_hardware_knob("VCO1", sub_vco1, -100, 100, True), use_container_width=True)

    with cols[1]:
        sub_1a = st.selectbox("SUB 1A", ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷10", "÷12", "÷16"], index=0, key="sub1a")

    with cols[2]:
        sub_1b = st.selectbox("SUB 1B", ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷10", "÷12", "÷16"], index=1, key="sub1b")

    with cols[3]:
        sub_vco2 = st.slider("VCO2 FREQ", -100, 100, 0, key="sub_vco2")
        st.plotly_chart(create_hardware_knob("VCO2", sub_vco2, -100, 100, True), use_container_width=True)

    with cols[4]:
        sub_2a = st.selectbox("SUB 2A", ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷10", "÷12", "÷16"], index=2, key="sub2a")

    st.markdown('</div>', unsafe_allow_html=True)

    # Rhythm generators
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">POLYRHYTHM GENERATORS</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class='learning-tip'>
    <strong>POLYRHYTHM CONCEPT:</strong><br>
    Each rhythm generator divides the master clock by different values, creating complex interlocking patterns.
    Example: Rhythm 1 = ÷4, Rhythm 2 = ÷3 creates a 4-against-3 polyrhythm.
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            st.selectbox(f"RHYTHM {i+1}", ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷8", "÷12", "÷16"], index=i, key=f"rhythm{i}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Sequencers
    st.markdown('<div class="hardware-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">DUAL 4-STEP SEQUENCERS</div>', unsafe_allow_html=True)

    st.info("2 independent 4-step sequencers, each driven by rhythm generators")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**SEQUENCER 1**")
        for i in range(4):
            st.slider(f"Step {i+1}", 0, 100, 50, key=f"seq1_{i}")

    with col2:
        st.markdown("**SEQUENCER 2**")
        for i in range(4):
            st.slider(f"Step {i+1}", 0, 100, 50, key=f"seq2_{i}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class='try-hardware'>
    <strong>🎛️ WORKFLOW TIP:</strong><br>
    Subharmonicon excels at drones and evolving patterns. Start with simple ÷1 divisions,
    then gradually add complexity. Listen to how subharmonics create harmonic series.
    Use polyrhythms to create evolving, non-repeating patterns.
    </div>
    """, unsafe_allow_html=True)

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

with col2:
    st.markdown("**🧠 Learning Science**")
    st.markdown("This tool uses:")
    st.markdown("- Spaced repetition")
    st.markdown("- Active recall")
    st.markdown("- Hands-on practice")

with col3:
    st.markdown("**💡 Pro Tip**")
    st.markdown("Practice patches in order.")
    st.markdown("Review every 5 minutes.")
    st.markdown("Always try on hardware.")

st.caption("Built for laptop-beside-hardware learning • All specs verified from official manuals")
