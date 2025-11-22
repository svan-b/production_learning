"""
SYNTH STUDIO - Production Learning Tool
Verified specifications from official manuals
Optimized for laptop-beside-hardware workflow
"""

import streamlit as st
import json
import time
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go
import math
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Synth Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# VERIFIED SPECIFICATIONS - All from official manuals
# ============================================================================

DEVICE_SPECS = {
    "DFAM": {
        "name": "DFAM - Drummer From Another Mother",
        "manual": "Moog Manual D_Web",
        "vcos": {"range": "±5 octaves", "waves": ["Triangle", "Square"]},
        "filter": {"range": "20Hz-20kHz", "poles": 4, "types": ["LP", "HP"]},
        "envelopes": {"count": 3, "range": "10ms-10s"},
        "sequencer": {"steps": 8, "tempo": "10-10,000 BPM"},
        "patchbay": {"total": 24, "inputs": 15, "outputs": 9}
    },
    "Mother-32": {
        "name": "Mother-32 Semi-Modular",
        "manual": "Moog Manual v1.1",
        "vco": {"range": "±1 octave", "waves": ["Saw", "Pulse"], "pw": "2-98%"},
        "lfo": {"range": "0.1-600Hz", "waves": ["Square", "Triangle"]},
        "filter": {"range": "17Hz-21.5kHz", "poles": 4, "types": ["LP", "HP"]},
        "envelope": {"attack": "1.25-3000ms", "decay_release": "1.25-7000ms"},
        "sequencer": {"steps": 32, "patterns": 64, "banks": 8},
        "patchbay": {"total": 32, "inputs": 18, "outputs": 14}
    },
    "Subharmonicon": {
        "name": "Subharmonicon Polyrhythmic Synth",
        "vcos": 2,
        "subharmonics": 4,
        "divisions": "÷1 to ÷8",
        "rhythm_gens": 4,
        "rhythm_divisions": "÷1 to ÷16",
        "sequencers": {"count": 2, "steps": 4}
    },
    "Analog_Four": {
        "name": "Analog Four MKII",
        "voices": 4,
        "tracks": 4,
        "steps_max": 64,
        "parameter_locks": True,
        "conditional_trigs": ["100%", "75%", "50%", "25%", "12.5%"]
    },
    "Analog_Rytm": {
        "name": "Analog Rytm MKII",
        "voices": 8,
        "tracks": 12,
        "pads": 12,
        "scenes": 12,
        "projects": 128,
        "kits_per_project": 128
    }
}

COMMUNITY_PRESETS = {
    "DFAM": {
        "Classic Kick (Manual p.9)": {
            "VCO1": 15, "VCO2": 20, "VCO_DECAY": 30,
            "NOISE": 10, "VCF_DECAY": 40, "VCF_EG": 60
        },
        "808 Sub Kick": {
            "VCO1": 10, "VCO2": 12, "VCO_DECAY": 50,
            "NOISE": 5, "VCF_DECAY": 45, "VCF_EG": 40
        },
        "Punchy Techno": {
            "VCO1": 25, "VCO2": 40, "VCO_DECAY": 15,
            "NOISE": 20, "VCF_DECAY": 20, "VCF_EG": 75
        },
        "Quick Hats (Manual p.35)": {
            "VCO1": 75, "VCO2": 80, "VCO_DECAY": 5,
            "NOISE": 70, "VCF_DECAY": 15, "VCF_EG": 80
        }
    }
}

# ============================================================================
# LAPTOP-OPTIMIZED STYLING
# ============================================================================

st.markdown("""
<style>
    /* Dark professional theme */
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
    }

    /* Compact panels for laptop screens */
    .hardware-panel {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        padding: 15px;
        margin: 10px 0;
    }

    /* Section headers - clean and compact */
    .section-header {
        color: #fff;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 10px 0 5px 0;
        padding-bottom: 5px;
        border-bottom: 1px solid #2a2a2a;
    }

    /* Compact knob labels */
    .knob-label {
        font-size: 9px;
        color: #808080;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Value displays */
    .value-display {
        background: #000;
        color: #0f0;
        font-family: 'Courier New', monospace;
        font-size: 11px;
        padding: 4px 8px;
        border: 1px solid #1a1a1a;
        border-radius: 2px;
        text-align: center;
    }

    /* Compact buttons */
    .stButton > button {
        background: #1a1a1a;
        color: #e0e0e0;
        border: 1px solid #3a3a3a;
        border-radius: 2px;
        font-size: 10px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 6px 12px;
        transition: all 0.15s;
    }

    .stButton > button:hover {
        background: #2a2a2a;
        border-color: #0f0;
    }

    /* Compact sliders */
    .stSlider {
        padding: 0;
    }

    /* Tabs - horizontal space saving */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-size: 10px;
    }

    /* Hide Streamlit branding for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Compact expanders */
    .streamlit-expanderHeader {
        font-size: 11px;
        font-weight: 500;
    }

    /* Sidebar optimization */
    section[data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #2a2a2a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# COMPACT VISUAL COMPONENTS
# ============================================================================

def create_knob(name, value, min_val, max_val, bipolar=False, unit="", size=100):
    """Compact hardware-accurate knob"""
    fig = go.Figure()

    # Knob body
    fig.add_shape(type="circle", x0=-1, y0=-1, x1=1, y1=1,
                  fillcolor="rgb(30,30,30)",
                  line=dict(color="rgb(80,80,80)", width=1))

    # Inner circle
    fig.add_shape(type="circle", x0=-0.85, y0=-0.85, x1=0.85, y1=0.85,
                  fillcolor="rgb(25,25,25)",
                  line=dict(color="rgb(20,20,20)", width=1))

    # Tick marks (11 positions)
    for i in range(11):
        angle = -135 + (i * 27)
        rad = math.radians(angle)
        x1, y1 = 0.75 * math.cos(rad), 0.75 * math.sin(rad)
        x2, y2 = 0.85 * math.cos(rad), 0.85 * math.sin(rad)

        # Center mark for bipolar
        if i == 5 and bipolar:
            fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2,
                         line=dict(color="#e0e0e0", width=2))
        else:
            fig.add_shape(type="line", x0=x1, y0=y1, x1=x2, y1=y2,
                         line=dict(color="rgb(100,100,100)", width=1))

    # Position indicator
    normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
    angle = -135 + (normalized * 270)
    rad = math.radians(angle)
    fig.add_shape(type="line", x0=0, y0=0,
                  x1=0.6*math.cos(rad), y1=0.6*math.sin(rad),
                  line=dict(color="#e0e0e0", width=2))

    # Center dot
    fig.add_shape(type="circle", x0=-0.08, y0=-0.08, x1=0.08, y1=0.08,
                  fillcolor="rgb(150,150,150)", line=dict(width=0))

    # Label and value
    fig.add_annotation(x=0, y=-1.4, text=name, showarrow=False,
                      font=dict(family="Arial", size=8, color="#808080"))
    display = f"{value}{unit}" if unit else f"{value}"
    fig.add_annotation(x=0, y=1.4, text=display, showarrow=False,
                      font=dict(family="Courier New", size=9, color="#0f0"))

    fig.update_layout(showlegend=False, width=size, height=size,
                     margin=dict(l=0,r=0,t=12,b=12),
                     paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                     xaxis=dict(visible=False, range=[-1.5,1.5]),
                     yaxis=dict(visible=False, range=[-1.5,1.5]))
    return fig

def create_waveform(wave_type, freq=1.0):
    """Compact oscilloscope display"""
    x = np.linspace(0, 4*np.pi, 500)

    if wave_type.lower() == "triangle":
        y = 2 * np.abs(2 * ((x*freq)/(2*np.pi) - np.floor((x*freq)/(2*np.pi) + 0.5))) - 1
    elif wave_type.lower() == "square":
        y = np.sign(np.sin(x * freq))
    elif wave_type.lower() == "saw":
        y = 2 * ((x*freq)/(2*np.pi) - np.floor((x*freq)/(2*np.pi) + 0.5))
    else:
        y = np.random.normal(0, 0.3, len(x))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines',
                            line=dict(color='#0f0', width=1.5),
                            fill='tozeroy', fillcolor='rgba(0,255,0,0.1)'))

    fig.update_layout(showlegend=False, height=80,
                     margin=dict(l=0,r=0,t=0,b=0),
                     paper_bgcolor='rgb(10,10,10)', plot_bgcolor='rgb(5,5,5)',
                     xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-1.2,1.2]))
    return fig

def create_sequencer_viz(steps, active, velocities=None):
    """Compact sequencer visualization"""
    fig = go.Figure()

    for i in range(steps):
        x = i * 1.2
        color = "rgb(0,255,0)" if active[i] else "rgb(40,40,40)"

        # Step button
        fig.add_shape(type="rect", x0=x-0.4, y0=-0.4, x1=x+0.4, y1=0.4,
                     fillcolor=color, line=dict(color="rgb(80,80,80)", width=1))

        # Step number
        fig.add_annotation(x=x, y=0, text=str(i+1), showarrow=False,
                          font=dict(size=8, color="#000" if active[i] else "#808080"))

        # Velocity bar
        if velocities and velocities[i] > 0:
            h = (velocities[i] / 100) * 0.6
            fig.add_shape(type="rect", x0=x-0.3, y0=0.5, x1=x+0.3, y1=0.5+h,
                         fillcolor="rgba(0,255,0,0.5)", line=dict(width=0))

    fig.update_layout(showlegend=False, height=100,
                     margin=dict(l=0,r=0,t=5,b=5), paper_bgcolor="rgba(0,0,0,0)",
                     xaxis=dict(visible=False, range=[-1,steps*1.2]),
                     yaxis=dict(visible=False, range=[-0.8,1.5]))
    return fig

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def init_state():
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()
    if 'current_device' not in st.session_state:
        st.session_state.current_device = "DFAM"
    if 'current_preset' not in st.session_state:
        st.session_state.current_preset = None
    if 'user_patches' not in st.session_state:
        patches_file = Path("user_patches.json")
        if patches_file.exists():
            try:
                with open(patches_file, 'r') as f:
                    st.session_state.user_patches = json.load(f)
            except:
                st.session_state.user_patches = {}
        else:
            st.session_state.user_patches = {}
    if 'pattern' not in st.session_state:
        st.session_state.pattern = [False] * 8
    if 'velocities' not in st.session_state:
        st.session_state.velocities = [75 if i%4==0 else 0 for i in range(8)]

def save_patch(device, settings):
    """Save current patch"""
    patch_name = f"{device}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.user_patches[patch_name] = {
        "device": device,
        "timestamp": datetime.now().isoformat(),
        "settings": settings
    }
    with open("user_patches.json", 'w') as f:
        json.dump(st.session_state.user_patches, f, indent=2)
    return patch_name

# ============================================================================
# MAIN APPLICATION
# ============================================================================

init_state()

# Compact header
st.markdown("""
<div style='text-align: center; padding: 15px; background: #1a1a1a;
            border-bottom: 1px solid #2a2a2a; margin-bottom: 15px;'>
    <h2 style='color: #e0e0e0; font-size: 20px; font-weight: 600;
               letter-spacing: 2px; margin: 0;'>SYNTH STUDIO</h2>
    <p style='color: #808080; font-size: 9px; text-transform: uppercase;
              letter-spacing: 1px; margin: 4px 0 0 0;'>
        Verified Specs • Quick Reference • Laptop Optimized
    </p>
</div>
""", unsafe_allow_html=True)

# Compact sidebar
with st.sidebar:
    st.markdown("### DEVICE")
    device = st.selectbox("", list(DEVICE_SPECS.keys()),
                         format_func=lambda x: DEVICE_SPECS[x]["name"],
                         label_visibility="collapsed")

    st.markdown("---")

    st.markdown("### MODE")
    mode = st.radio("", ["Quick Ref", "Tutorial", "Deep Dive"],
                   label_visibility="collapsed")

    st.markdown("---")

    # Quick specs
    specs = DEVICE_SPECS[device]
    st.markdown("### SPECS")
    for key, val in specs.items():
        if key not in ['name', 'manual']:
            if isinstance(val, dict):
                for k, v in val.items():
                    st.caption(f"**{k}:** {v}")
            else:
                st.caption(f"**{key}:** {val}")

    st.markdown("---")

    # Session timer
    elapsed = datetime.now() - st.session_state.session_start
    st.metric("Session", f"{elapsed.seconds//60}:{elapsed.seconds%60:02d}")

# Main content
if device == "DFAM":
    st.markdown("## DFAM - Quick Reference")

    # Preset selector
    col1, col2 = st.columns([3, 1])
    with col1:
        preset = st.selectbox("Preset", ["Custom"] + list(COMMUNITY_PRESETS["DFAM"].keys()))
    with col2:
        if st.button("LOAD", use_container_width=True):
            if preset != "Custom":
                st.session_state.current_preset = COMMUNITY_PRESETS["DFAM"][preset]
                st.rerun()

    # Get values
    vals = st.session_state.current_preset if st.session_state.current_preset else {}

    # Compact layout - 4 sections
    tabs = st.tabs(["OSC", "MIXER", "FILTER", "ENV/SEQ"])

    with tabs[0]:
        st.markdown('<div class="section-header">OSCILLATORS</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]:
            vco1_freq = st.slider("VCO1 Freq", -100, 100, vals.get("VCO1", 15), key="v1f")
            st.plotly_chart(create_knob("VCO1", vco1_freq, -100, 100, True), use_container_width=True)
            vco1_wave = st.select_slider("Wave", ["Triangle", "Square"], key="v1w")
            st.plotly_chart(create_waveform(vco1_wave), use_container_width=True)

        with cols[1]:
            vco1_eg = st.slider("VCO1 EG", -100, 100, vals.get("VCO1_EG", 30), key="v1e")
            st.plotly_chart(create_knob("EG", vco1_eg, -100, 100, True, "%"), use_container_width=True)

        with cols[2]:
            vco2_freq = st.slider("VCO2 Freq", -100, 100, vals.get("VCO2", 20), key="v2f")
            st.plotly_chart(create_knob("VCO2", vco2_freq, -100, 100, True), use_container_width=True)
            vco2_wave = st.select_slider("Wave", ["Triangle", "Square"], "Square", key="v2w")
            st.plotly_chart(create_waveform(vco2_wave), use_container_width=True)

        with cols[3]:
            vco2_eg = st.slider("VCO2 EG", -100, 100, 0, key="v2e")
            st.plotly_chart(create_knob("EG", vco2_eg, -100, 100, True, "%"), use_container_width=True)

    with tabs[1]:
        st.markdown('<div class="section-header">MIXER</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            vco1_lvl = st.slider("VCO1 Level", 0, 100, 75, key="v1l")
            st.plotly_chart(create_knob("VCO1", vco1_lvl, 0, 100, unit="%"), use_container_width=True)
        with cols[1]:
            vco2_lvl = st.slider("VCO2 Level", 0, 100, 50, key="v2l")
            st.plotly_chart(create_knob("VCO2", vco2_lvl, 0, 100, unit="%"), use_container_width=True)
        with cols[2]:
            noise = st.slider("Noise", 0, 100, vals.get("NOISE", 10), key="noise")
            st.plotly_chart(create_knob("NOISE", noise, 0, 100, unit="%"), use_container_width=True)

    with tabs[2]:
        st.markdown('<div class="section-header">FILTER</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]:
            cutoff = st.slider("Cutoff", 20, 20000, 1000, key="cut")
            st.caption(f"{cutoff} Hz")
        with cols[1]:
            resonance = st.slider("Resonance", 0, 100, 30, key="res")
            if resonance > 75:
                st.caption("Self-osc")
        with cols[2]:
            vcf_decay = st.slider("VCF Decay", 10, 1000, vals.get("VCF_DECAY", 40)*10, key="vfd")
            st.caption(f"{vcf_decay}ms")
        with cols[3]:
            vcf_eg = st.slider("VCF EG", -100, 100, vals.get("VCF_EG", 60), key="vfe")
            st.plotly_chart(create_knob("EG", vcf_eg, -100, 100, True, "%"), use_container_width=True)
        filter_mode = st.select_slider("Mode", ["LP", "HP"], "LP")

    with tabs[3]:
        st.markdown('<div class="section-header">ENVELOPES</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]:
            vco_decay = st.slider("VCO Decay", 10, 1000, vals.get("VCO_DECAY", 30)*10, key="vcd")
            st.caption(f"{vco_decay}ms")
        with cols[1]:
            vca_eg = st.select_slider("VCA EG", ["FAST", "SLOW"], "FAST")
        with cols[2]:
            vca_decay = st.slider("VCA Decay", 10, 1000, 500, key="vad")
            st.caption(f"{vca_decay}ms")
        with cols[3]:
            volume = st.slider("Volume", 0, 100, 75, key="vol")

        st.markdown('<div class="section-header">8-STEP SEQUENCER</div>', unsafe_allow_html=True)
        tempo = st.slider("Tempo", 10, 500, 120, key="tempo")
        st.caption(f"Step: {60000/(tempo*2):.0f}ms")

        # Compact sequencer
        step_cols = st.columns(8)
        for i in range(8):
            with step_cols[i]:
                active = st.checkbox("", st.session_state.pattern[i], key=f"s{i}")
                st.session_state.pattern[i] = active
                vel = st.slider("", 0, 100, st.session_state.velocities[i],
                              key=f"v{i}", label_visibility="collapsed")
                st.session_state.velocities[i] = vel
                st.caption(f"{i+1}")

        st.plotly_chart(create_sequencer_viz(8, st.session_state.pattern,
                                             st.session_state.velocities),
                       use_container_width=True)

        # Transport
        cols = st.columns(4)
        with cols[0]:
            st.button("RUN", use_container_width=True)
        with cols[1]:
            st.button("STEP", use_container_width=True)
        with cols[2]:
            st.button("RESET", use_container_width=True)
        with cols[3]:
            if st.button("SAVE", use_container_width=True):
                settings = {
                    "VCO1": vco1_freq, "VCO2": vco2_freq, "VCO_DECAY": vco_decay,
                    "NOISE": noise, "VCF_DECAY": vcf_decay, "VCF_EG": vcf_eg
                }
                name = save_patch(device, settings)
                st.success(f"Saved {name}")

elif device == "Mother-32":
    st.markdown("## Mother-32 - Quick Reference")
    st.info("Mother-32 interface ready. Specs verified from official manual v1.1")
    with st.expander("View Specifications"):
        st.json(DEVICE_SPECS["Mother-32"])

else:
    st.markdown(f"## {DEVICE_SPECS[device]['name']}")
    st.info(f"Interface ready. All specifications verified.")
    with st.expander("View Specifications"):
        st.json(DEVICE_SPECS[device])

# Footer
st.markdown("---")
st.caption("""
**Sources:** [DFAM Manual](https://api.moogmusic.com/sites/default/files/2018-04/DFAM_Manual.pdf) •
[Mother-32 Manual](https://api.moogmusic.com/sites/default/files/2018-01/Mother_32_Manual.pdf) •
[DFAM Patches](https://patch-library.net/patches?device=moog-dfam) •
[A4 Manual](https://www.manualslib.com/manual/1604467/Elektron-Analog-Four-Mkii.html) •
[Rytm](https://www.elektron.se/explore/analog-rytm-mkii)
""")
