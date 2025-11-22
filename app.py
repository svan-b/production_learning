"""
SYNTH STUDIO - Digital Twin Learning System
Exact replicas of hardware synthesizers with teaching indicators
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
    page_title="Synth Studio | Digital Twins",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# TEACHING INDICATOR CSS
# ============================================================================

st.markdown("""
<style>
    /* Clean dark background */
    .stApp {
        background: #0a0a0a;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    }

    /* Device navigation tabs */
    .device-nav {
        display: flex;
        justify-content: center;
        gap: 10px;
        padding: 20px;
        background: #1a1a1a;
        border-bottom: 2px solid #2a2a2a;
        margin-bottom: 20px;
    }

    .device-tab {
        background: #2a2a2a;
        color: #888;
        padding: 12px 24px;
        border-radius: 6px;
        border: 1px solid #3a3a3a;
        cursor: pointer;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.2s;
    }

    .device-tab:hover {
        background: #3a3a3a;
        color: #ccc;
    }

    .device-tab-active {
        background: #0f0;
        color: #000;
        border-color: #0f0;
        box-shadow: 0 0 15px rgba(0,255,0,0.3);
    }

    /* Hardware panel - exact replica styling */
    .twin-panel {
        background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
        border: 2px solid #3a3a3a;
        border-radius: 8px;
        padding: 30px;
        margin: 20px auto;
        max-width: 1400px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    /* Section labels - hardware style */
    .panel-section-label {
        color: #888;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        padding-bottom: 8px;
        border-bottom: 1px solid #333;
    }

    /* Teaching indicators */
    .control-active {
        outline: 3px solid #0f0 !important;
        outline-offset: 4px;
        animation: pulse-green 1.5s infinite;
    }

    .control-correct {
        outline: 3px solid #0f0 !important;
        outline-offset: 4px;
    }

    .control-optional {
        outline: 3px solid #ff0 !important;
        outline-offset: 4px;
        animation: pulse-yellow 2s infinite;
    }

    .control-wrong {
        outline: 3px solid #f00 !important;
        outline-offset: 4px;
        animation: pulse-red 1s infinite;
    }

    @keyframes pulse-green {
        0%, 100% { outline-color: #0f0; opacity: 1; }
        50% { outline-color: #0f0; opacity: 0.6; }
    }

    @keyframes pulse-yellow {
        0%, 100% { outline-color: #ff0; opacity: 1; }
        50% { outline-color: #ff0; opacity: 0.5; }
    }

    @keyframes pulse-red {
        0%, 100% { outline-color: #f00; opacity: 1; }
        50% { outline-color: #f00; opacity: 0.7; }
    }

    /* Value displays - real units */
    .value-display {
        background: #000;
        color: #0f0;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        font-weight: 700;
        padding: 6px 10px;
        border: 1px solid #1a1a1a;
        border-radius: 3px;
        text-align: center;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.8), 0 0 8px rgba(0,255,0,0.2);
        min-width: 80px;
        margin-top: 5px;
    }

    /* Teaching panel */
    .teaching-panel {
        position: fixed;
        right: 20px;
        top: 100px;
        width: 320px;
        background: #1a1a1a;
        border: 2px solid #2a2a2a;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        max-height: 80vh;
        overflow-y: auto;
    }

    .teaching-title {
        color: #0f0;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #0f0;
    }

    .teaching-step {
        background: #0d0d0d;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        border-left: 3px solid #333;
        font-size: 12px;
        line-height: 1.6;
    }

    .step-active {
        border-left-color: #0f0;
        background: #0d1a0d;
    }

    .step-complete {
        border-left-color: #0f0;
        background: #0d0d0d;
        opacity: 0.6;
    }

    .step-checkmark {
        color: #0f0;
        font-weight: 700;
        margin-right: 8px;
    }

    .step-number {
        color: #f90;
        font-weight: 700;
        margin-right: 8px;
    }

    /* Control containers */
    .control-group {
        display: inline-block;
        margin: 15px 10px;
        text-align: center;
    }

    .control-label {
        font-size: 9px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}

    /* Sliders compact */
    .stSlider {
        padding: 5px 0;
    }

    /* Compact columns */
    [data-testid="column"] {
        padding: 8px 4px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DEVICE SPECIFICATIONS - EXACT HARDWARE SPECS
# ============================================================================

DEVICES = {
    "DFAM": {
        "name": "DFAM - Drummer From Another Mother",
        "manufacturer": "Moog",
        "controls": {
            "vco1_freq": {"min": -5, "max": 5, "default": 0, "unit": "octaves", "type": "knob"},
            "vco1_wave": {"options": ["Triangle", "Square"], "default": "Triangle", "type": "toggle"},
            "vco1_eg": {"min": -100, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "vco2_freq": {"min": -5, "max": 5, "default": 0, "unit": "octaves", "type": "knob"},
            "vco2_wave": {"options": ["Triangle", "Square"], "default": "Triangle", "type": "toggle"},
            "vco2_eg": {"min": -100, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "vco_decay": {"min": 10, "max": 10000, "default": 300, "unit": "ms", "type": "knob"},
            "fm_amount": {"min": 0, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "hard_sync": {"default": False, "type": "button"},
            "vco1_level": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            "vco2_level": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "noise": {"min": 0, "max": 100, "default": 10, "unit": "%", "type": "knob"},
            "vcf_cutoff": {"min": 20, "max": 20000, "default": 1000, "unit": "Hz", "type": "knob"},
            "vcf_resonance": {"min": 0, "max": 100, "default": 30, "unit": "%", "type": "knob"},
            "vcf_eg": {"min": -100, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "vcf_decay": {"min": 10, "max": 10000, "default": 400, "unit": "ms", "type": "knob"},
            "vcf_mode": {"options": ["LP", "HP"], "default": "LP", "type": "toggle"},
            "vca_decay": {"min": 10, "max": 10000, "default": 500, "unit": "ms", "type": "knob"},
            "vca_attack": {"options": ["FAST", "SLOW"], "default": "FAST", "type": "toggle"},
            "volume": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            "tempo": {"min": 10, "max": 500, "default": 120, "unit": "BPM", "type": "knob"},
        }
    },
    "Mother-32": {
        "name": "Mother-32 Semi-Modular Synthesizer",
        "manufacturer": "Moog",
        "controls": {
            "glide": {"min": 0, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "vco_freq": {"min": -5, "max": 5, "default": 0, "unit": "octaves", "type": "knob"},
            "vco_wave": {"options": ["Saw", "Pulse"], "default": "Saw", "type": "toggle"},
            "lfo_rate": {"min": 0.1, "max": 600.0, "default": 2.0, "unit": "Hz", "type": "knob", "step": 0.1},
            "lfo_wave": {"options": ["Square", "Triangle"], "default": "Triangle", "type": "toggle"},
            "vcf_cutoff": {"min": 17, "max": 21500, "default": 1000, "unit": "Hz", "type": "knob"},
            "vcf_resonance": {"min": 0, "max": 100, "default": 30, "unit": "%", "type": "knob"},
            "vcf_eg": {"min": -100, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "vca_level": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            "eg_attack": {"min": 1.25, "max": 3000.0, "default": 10.0, "unit": "ms", "type": "knob", "step": 0.25},
            "eg_decay": {"min": 1.25, "max": 7000.0, "default": 500.0, "unit": "ms", "type": "knob", "step": 0.25},
        }
    }
}

# ============================================================================
# TEACHING PRESETS - STEP-BY-STEP LESSONS
# ============================================================================

LESSONS = {
    "DFAM": {
        "Classic Kick Drum": {
            "description": "Create a punchy 909-style kick drum",
            "source": "Official Manual Page 9",
            "steps": [
                {"control": "vco1_freq", "value": 0, "instruction": "Set VCO 1 FREQUENCY to center (0 octaves)"},
                {"control": "vco2_freq", "value": 0.5, "instruction": "Set VCO 2 FREQUENCY slightly higher (+0.5 octaves)"},
                {"control": "vco_decay", "value": 300, "instruction": "Set VCO DECAY to 300ms for pitch sweep"},
                {"control": "vco1_level", "value": 80, "instruction": "Set VCO 1 LEVEL to 80%"},
                {"control": "vco2_level", "value": 60, "instruction": "Set VCO 2 LEVEL to 60%"},
                {"control": "noise", "value": 10, "instruction": "Add slight NOISE at 10%"},
                {"control": "vcf_cutoff", "value": 800, "instruction": "Set FILTER CUTOFF to 800Hz"},
                {"control": "vcf_eg", "value": 60, "instruction": "Set FILTER EG to +60% for click"},
                {"control": "vcf_decay", "value": 400, "instruction": "Set FILTER DECAY to 400ms"},
                {"control": "vca_decay", "value": 150, "instruction": "Set VCA DECAY to 150ms for short hit"},
                {"control": "vca_attack", "value": "FAST", "instruction": "Set VCA ATTACK to FAST"},
            ]
        },
        "808 Sub Kick": {
            "description": "Deep sub bass kick like TR-808",
            "source": "Community",
            "steps": [
                {"control": "vco1_freq", "value": -1, "instruction": "Set VCO 1 FREQUENCY low (-1 octave)"},
                {"control": "vco2_freq", "value": -0.5, "instruction": "Set VCO 2 FREQUENCY to -0.5 octaves"},
                {"control": "vco_decay", "value": 500, "instruction": "Set VCO DECAY to 500ms for long boom"},
                {"control": "noise", "value": 5, "instruction": "Minimal NOISE at 5%"},
                {"control": "vcf_cutoff", "value": 600, "instruction": "Low FILTER CUTOFF at 600Hz"},
                {"control": "vca_decay", "value": 300, "instruction": "VCA DECAY 300ms for sustain"},
            ]
        }
    },
    "Mother-32": {
        "Analog Bass": {
            "description": "Classic analog bass sequence",
            "source": "Official Manual",
            "steps": [
                {"control": "vco_wave", "value": "Saw", "instruction": "Select SAW wave"},
                {"control": "vcf_cutoff", "value": 1200, "instruction": "FILTER CUTOFF to 1200Hz"},
                {"control": "vcf_resonance", "value": 60, "instruction": "RESONANCE to 60%"},
                {"control": "vcf_eg", "value": 70, "instruction": "FILTER EG to +70%"},
                {"control": "eg_attack", "value": 5.0, "instruction": "ATTACK to 5ms (fast)"},
                {"control": "eg_decay", "value": 300.0, "instruction": "DECAY to 300ms"},
                {"control": "glide", "value": 15, "instruction": "Add slight GLIDE at 15%"},
            ]
        }
    }
}

# ============================================================================
# STATE MANAGEMENT
# ============================================================================

def init_state():
    """Initialize session state"""
    if 'device' not in st.session_state:
        st.session_state.device = "DFAM"
    if 'active_lesson' not in st.session_state:
        st.session_state.active_lesson = None
    if 'lesson_step' not in st.session_state:
        st.session_state.lesson_step = 0
    if 'controls' not in st.session_state:
        st.session_state.controls = {}

def get_control_value(device, control):
    """Get current control value"""
    key = f"{device}_{control}"
    if key in st.session_state.controls:
        return st.session_state.controls[key]
    return DEVICES[device]["controls"][control]["default"]

def set_control_value(device, control, value):
    """Set control value"""
    key = f"{device}_{control}"
    st.session_state.controls[key] = value

def check_step_complete(device, step):
    """Check if lesson step is complete"""
    control = step["control"]
    target = step["value"]
    current = get_control_value(device, control)

    # Allow 5% tolerance for numeric values
    if isinstance(target, (int, float)):
        tolerance = abs(target * 0.05) if target != 0 else 5
        return abs(current - target) <= tolerance
    else:
        return current == target

# ============================================================================
# MAIN APP
# ============================================================================

init_state()

# Device Navigation
st.markdown("""
<div class='device-nav'>
    <div class='device-tab device-tab-active'>DFAM</div>
    <div class='device-tab'>Mother-32</div>
    <div class='device-tab'>Subharmonicon</div>
    <div class='device-tab'>Analog Four</div>
    <div class='device-tab'>Analog Rytm</div>
    <div class='device-tab'>Sub 37</div>
    <div class='device-tab'>Xone:96</div>
</div>
""", unsafe_allow_html=True)

# Device selector (temporary - will be replaced with clickable tabs)
device = st.selectbox("", list(DEVICES.keys()), label_visibility="collapsed")
st.session_state.device = device

# Lesson selector
col1, col2 = st.columns([3, 1])
with col1:
    if device in LESSONS:
        lesson_names = list(LESSONS[device].keys())
        selected_lesson = st.selectbox("Select Lesson", ["None"] + lesson_names)
        if selected_lesson != "None":
            st.session_state.active_lesson = LESSONS[device][selected_lesson]
            if st.button("Start Lesson"):
                st.session_state.lesson_step = 0
                st.rerun()

# ============================================================================
# DIGITAL TWIN INTERFACE
# ============================================================================

st.markdown(f"<div class='twin-panel'>", unsafe_allow_html=True)
st.markdown(f"<h2 style='color: #0f0; text-align: center; margin-bottom: 30px;'>{DEVICES[device]['name']}</h2>", unsafe_allow_html=True)

if device == "DFAM":

    # OSCILLATORS ROW
    st.markdown("<div class='panel-section-label'>OSCILLATORS</div>", unsafe_allow_html=True)
    cols = st.columns(6)

    with cols[0]:
        st.markdown("<div class='control-label'>VCO 1 FREQUENCY</div>", unsafe_allow_html=True)
        val = st.slider("", -5.0, 5.0, float(get_control_value(device, "vco1_freq")), 0.1, key="vco1_freq_slider", label_visibility="collapsed")
        set_control_value(device, "vco1_freq", val)
        st.markdown(f"<div class='value-display'>{val:+.1f} oct</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>VCO 1 WAVE</div>", unsafe_allow_html=True)
        val = st.select_slider("", ["Triangle", "Square"], value=get_control_value(device, "vco1_wave"), key="vco1_wave_slider", label_visibility="collapsed")
        set_control_value(device, "vco1_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>VCO 1 EG AMOUNT</div>", unsafe_allow_html=True)
        val = st.slider("", -100, 100, int(get_control_value(device, "vco1_eg")), 1, key="vco1_eg_slider", label_visibility="collapsed")
        set_control_value(device, "vco1_eg", val)
        st.markdown(f"<div class='value-display'>{val:+d}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>VCO 2 FREQUENCY</div>", unsafe_allow_html=True)
        val = st.slider("", -5.0, 5.0, float(get_control_value(device, "vco2_freq")), 0.1, key="vco2_freq_slider", label_visibility="collapsed")
        set_control_value(device, "vco2_freq", val)
        st.markdown(f"<div class='value-display'>{val:+.1f} oct</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>VCO 2 WAVE</div>", unsafe_allow_html=True)
        val = st.select_slider("", ["Triangle", "Square"], value=get_control_value(device, "vco2_wave"), key="vco2_wave_slider", label_visibility="collapsed")
        set_control_value(device, "vco2_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[5]:
        st.markdown("<div class='control-label'>VCO 2 EG AMOUNT</div>", unsafe_allow_html=True)
        val = st.slider("", -100, 100, int(get_control_value(device, "vco2_eg")), 1, key="vco2_eg_slider", label_visibility="collapsed")
        set_control_value(device, "vco2_eg", val)
        st.markdown(f"<div class='value-display'>{val:+d}%</div>", unsafe_allow_html=True)

    # VCO CONTROLS & MIXER ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>VCO CONTROLS & MIXER</div>", unsafe_allow_html=True)
    cols = st.columns(6)

    with cols[0]:
        st.markdown("<div class='control-label'>VCO DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 10, 10000, int(get_control_value(device, "vco_decay")), 10, key="vco_decay_slider", label_visibility="collapsed")
        set_control_value(device, "vco_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>FM AMOUNT</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "fm_amount")), 1, key="fm_amount_slider", label_visibility="collapsed")
        set_control_value(device, "fm_amount", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>HARD SYNC</div>", unsafe_allow_html=True)
        val = st.checkbox("", value=get_control_value(device, "hard_sync"), key="hard_sync_check", label_visibility="collapsed")
        set_control_value(device, "hard_sync", val)
        st.markdown(f"<div class='value-display'>{'ON' if val else 'OFF'}</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>VCO 1 LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vco1_level")), 1, key="vco1_level_slider", label_visibility="collapsed")
        set_control_value(device, "vco1_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>VCO 2 LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vco2_level")), 1, key="vco2_level_slider", label_visibility="collapsed")
        set_control_value(device, "vco2_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[5]:
        st.markdown("<div class='control-label'>NOISE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "noise")), 1, key="noise_slider", label_visibility="collapsed")
        set_control_value(device, "noise", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # FILTER ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>FILTER (4-POLE LADDER)</div>", unsafe_allow_html=True)
    cols = st.columns(5)

    with cols[0]:
        st.markdown("<div class='control-label'>CUTOFF</div>", unsafe_allow_html=True)
        val = st.slider("", 20, 20000, int(get_control_value(device, "vcf_cutoff")), 10, key="vcf_cutoff_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_cutoff", val)
        st.markdown(f"<div class='value-display'>{val}Hz</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>RESONANCE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vcf_resonance")), 1, key="vcf_res_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_resonance", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>VCF EG AMOUNT</div>", unsafe_allow_html=True)
        val = st.slider("", -100, 100, int(get_control_value(device, "vcf_eg")), 1, key="vcf_eg_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_eg", val)
        st.markdown(f"<div class='value-display'>{val:+d}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>VCF DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 10, 10000, int(get_control_value(device, "vcf_decay")), 10, key="vcf_decay_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>FILTER MODE</div>", unsafe_allow_html=True)
        val = st.select_slider("", ["LP", "HP"], value=get_control_value(device, "vcf_mode"), key="vcf_mode_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_mode", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    # VCA ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>VCA</div>", unsafe_allow_html=True)
    cols = st.columns(3)

    with cols[0]:
        st.markdown("<div class='control-label'>VCA DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 10, 10000, int(get_control_value(device, "vca_decay")), 10, key="vca_decay_slider", label_visibility="collapsed")
        set_control_value(device, "vca_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>VCA ATTACK</div>", unsafe_allow_html=True)
        val = st.select_slider("", ["FAST", "SLOW"], value=get_control_value(device, "vca_attack"), key="vca_attack_slider", label_visibility="collapsed")
        set_control_value(device, "vca_attack", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>VOLUME</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "volume")), 1, key="volume_slider", label_visibility="collapsed")
        set_control_value(device, "volume", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

elif device == "Mother-32":

    # OSCILLATOR & LFO ROW
    st.markdown("<div class='panel-section-label'>OSCILLATOR & LFO</div>", unsafe_allow_html=True)
    cols = st.columns(5)

    with cols[0]:
        st.markdown("<div class='control-label'>GLIDE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "glide")), 1, key="m32_glide_slider", label_visibility="collapsed")
        set_control_value(device, "glide", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>VCO FREQUENCY</div>", unsafe_allow_html=True)
        val = st.slider("", -5.0, 5.0, float(get_control_value(device, "vco_freq")), 0.1, key="m32_vco_freq_slider", label_visibility="collapsed")
        set_control_value(device, "vco_freq", val)
        st.markdown(f"<div class='value-display'>{val:+.1f} oct</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>VCO WAVE</div>", unsafe_allow_html=True)
        val = st.select_slider("", ["Saw", "Pulse"], value=get_control_value(device, "vco_wave"), key="m32_vco_wave_slider", label_visibility="collapsed")
        set_control_value(device, "vco_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>LFO RATE</div>", unsafe_allow_html=True)
        val = st.slider("", 0.1, 600.0, float(get_control_value(device, "lfo_rate")), 0.1, key="m32_lfo_rate_slider", label_visibility="collapsed")
        set_control_value(device, "lfo_rate", val)
        st.markdown(f"<div class='value-display'>{val:.1f}Hz</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>LFO WAVE</div>", unsafe_allow_html=True)
        val = st.select_slider("", ["Square", "Triangle"], value=get_control_value(device, "lfo_wave"), key="m32_lfo_wave_slider", label_visibility="collapsed")
        set_control_value(device, "lfo_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    # FILTER & VCA ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>FILTER & VCA</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>VCF CUTOFF</div>", unsafe_allow_html=True)
        val = st.slider("", 17, 21500, int(get_control_value(device, "vcf_cutoff")), 1, key="m32_vcf_cutoff_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_cutoff", val)
        st.markdown(f"<div class='value-display'>{val}Hz</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>VCF RESONANCE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vcf_resonance")), 1, key="m32_vcf_res_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_resonance", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>VCF EG AMOUNT</div>", unsafe_allow_html=True)
        val = st.slider("", -100, 100, int(get_control_value(device, "vcf_eg")), 1, key="m32_vcf_eg_slider", label_visibility="collapsed")
        set_control_value(device, "vcf_eg", val)
        st.markdown(f"<div class='value-display'>{val:+d}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>VCA LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vca_level")), 1, key="m32_vca_level_slider", label_visibility="collapsed")
        set_control_value(device, "vca_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # ENVELOPE ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>ENVELOPE GENERATOR</div>", unsafe_allow_html=True)
    cols = st.columns(2)

    with cols[0]:
        st.markdown("<div class='control-label'>EG ATTACK</div>", unsafe_allow_html=True)
        val = st.slider("", 1.25, 3000.0, float(get_control_value(device, "eg_attack")), 0.25, key="m32_eg_attack_slider", label_visibility="collapsed")
        set_control_value(device, "eg_attack", val)
        st.markdown(f"<div class='value-display'>{val:.2f}ms</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>EG DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 1.25, 7000.0, float(get_control_value(device, "eg_decay")), 0.25, key="m32_eg_decay_slider", label_visibility="collapsed")
        set_control_value(device, "eg_decay", val)
        st.markdown(f"<div class='value-display'>{val:.2f}ms</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TEACHING PANEL (SIDE)
# ============================================================================

if st.session_state.active_lesson:
    lesson = st.session_state.active_lesson
    current_step = st.session_state.lesson_step

    # Display lesson in sidebar
    with st.sidebar:
        st.markdown(f"<div class='teaching-title'>{list(LESSONS[device].keys())[0]}</div>", unsafe_allow_html=True)
        st.markdown(f"**{lesson['description']}**")
        st.caption(f"Source: {lesson['source']}")

        st.markdown("---")

        for i, step in enumerate(lesson['steps']):
            complete = check_step_complete(device, step)
            is_current = (i == current_step)

            if complete:
                st.markdown(f"""
                <div class='teaching-step step-complete'>
                    <span class='step-checkmark'>✓</span> {step['instruction']}
                </div>
                """, unsafe_allow_html=True)
            elif is_current:
                st.markdown(f"""
                <div class='teaching-step step-active'>
                    <span class='step-number'>{i+1}.</span> {step['instruction']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='teaching-step'>
                    <span class='step-number'>{i+1}.</span> {step['instruction']}
                </div>
                """, unsafe_allow_html=True)

        # Check if lesson complete
        all_complete = all(check_step_complete(device, step) for step in lesson['steps'])
        if all_complete:
            st.success("✅ Lesson Complete!")
            if st.button("Reset Lesson"):
                st.session_state.lesson_step = 0
                st.rerun()
        else:
            # Auto-advance to next incomplete step
            for i, step in enumerate(lesson['steps']):
                if not check_step_complete(device, step):
                    st.session_state.lesson_step = i
                    break

st.caption("Digital Twin Learning System • All values are hardware-accurate")
