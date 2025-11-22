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
    },
    "Subharmonicon": {
        "name": "Subharmonicon Polyrhythmic Synthesizer",
        "manufacturer": "Moog",
        "controls": {
            # VCO 1
            "vco1_freq": {"min": -3, "max": 3, "default": 0, "unit": "octaves", "type": "knob"},
            "vco1_wave": {"options": ["Triangle", "Saw", "Square"], "default": "Saw", "type": "select"},
            "vco1_sub1": {"options": ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷9", "÷10", "÷11", "÷12", "÷13", "÷14", "÷15", "÷16"], "default": "÷2", "type": "select"},
            "vco1_sub2": {"options": ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷9", "÷10", "÷11", "÷12", "÷13", "÷14", "÷15", "÷16"], "default": "÷3", "type": "select"},
            # VCO 2
            "vco2_freq": {"min": -3, "max": 3, "default": 0, "unit": "octaves", "type": "knob"},
            "vco2_wave": {"options": ["Triangle", "Saw", "Square"], "default": "Saw", "type": "select"},
            "vco2_sub1": {"options": ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷9", "÷10", "÷11", "÷12", "÷13", "÷14", "÷15", "÷16"], "default": "÷4", "type": "select"},
            "vco2_sub2": {"options": ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷9", "÷10", "÷11", "÷12", "÷13", "÷14", "÷15", "÷16"], "default": "÷5", "type": "select"},
            # Filter & Mixer
            "vcf_cutoff": {"min": 20, "max": 20000, "default": 2000, "unit": "Hz", "type": "knob"},
            "vcf_resonance": {"min": 0, "max": 100, "default": 20, "unit": "%", "type": "knob"},
            "vcf_eg": {"min": -100, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "vco1_level": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "vco2_level": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "sub_level": {"min": 0, "max": 100, "default": 40, "unit": "%", "type": "knob"},
            # Envelope
            "eg_attack": {"min": 1, "max": 5000, "default": 50, "unit": "ms", "type": "knob"},
            "eg_decay": {"min": 1, "max": 10000, "default": 300, "unit": "ms", "type": "knob"},
            "eg_sustain": {"min": 0, "max": 100, "default": 60, "unit": "%", "type": "knob"},
            "eg_release": {"min": 1, "max": 10000, "default": 500, "unit": "ms", "type": "knob"},
            # Polyrhythm
            "rhythm1": {"min": 1, "max": 16, "default": 4, "unit": "steps", "type": "knob"},
            "rhythm2": {"min": 1, "max": 16, "default": 3, "unit": "steps", "type": "knob"},
        }
    },
    "Analog Four": {
        "name": "Analog Four MKII - 4-Voice Analog Synthesizer",
        "manufacturer": "Elektron",
        "controls": {
            # Voice 1 Oscillators
            "v1_osc1_wave": {"options": ["Saw", "Pulse", "Trans Pulse", "Triangle"], "default": "Saw", "type": "select"},
            "v1_osc1_tune": {"min": -24, "max": 24, "default": 0, "unit": "semitones", "type": "knob"},
            "v1_osc1_detune": {"min": -50, "max": 50, "default": 0, "unit": "cents", "type": "knob"},
            "v1_osc1_pwm": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "v1_osc2_wave": {"options": ["Saw", "Pulse", "Trans Pulse", "Triangle"], "default": "Pulse", "type": "select"},
            "v1_osc2_tune": {"min": -24, "max": 24, "default": 0, "unit": "semitones", "type": "knob"},
            "v1_osc2_detune": {"min": -50, "max": 50, "default": 5, "unit": "cents", "type": "knob"},
            "v1_sub_level": {"min": 0, "max": 100, "default": 30, "unit": "%", "type": "knob"},
            # Voice 1 Filter
            "v1_filter_type": {"options": ["LP", "BP", "HP", "Notch"], "default": "LP", "type": "select"},
            "v1_filter_cutoff": {"min": 20, "max": 20000, "default": 2000, "unit": "Hz", "type": "knob"},
            "v1_filter_res": {"min": 0, "max": 100, "default": 20, "unit": "%", "type": "knob"},
            "v1_filter_eg": {"min": -100, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            # Voice 1 Envelope
            "v1_eg_attack": {"min": 0, "max": 2000, "default": 5, "unit": "ms", "type": "knob"},
            "v1_eg_decay": {"min": 0, "max": 5000, "default": 300, "unit": "ms", "type": "knob"},
            "v1_eg_sustain": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "v1_eg_release": {"min": 0, "max": 5000, "default": 200, "unit": "ms", "type": "knob"},
            # Voice 1 LFO
            "v1_lfo_rate": {"min": 0.01, "max": 100.0, "default": 2.0, "unit": "Hz", "type": "knob", "step": 0.01},
            "v1_lfo_depth": {"min": 0, "max": 100, "default": 20, "unit": "%", "type": "knob"},
            "v1_lfo_wave": {"options": ["Sine", "Triangle", "Saw", "Square", "Random"], "default": "Sine", "type": "select"},
        }
    },
    "Analog Rytm": {
        "name": "Analog Rytm MKII - Hybrid Drum Machine",
        "manufacturer": "Elektron",
        "controls": {
            # Track 1 (Kick) - BD HARD (808 style)
            "t1_machine": {"options": ["BD HARD", "BD FM", "BD PLASTIC", "BD SILKY", "BD SHARP", "SD HARD", "SD CLASSIC", "RS HARD", "CP CLASSIC", "CH CLASSIC", "OH CLASSIC", "CY CLASSIC"], "default": "BD HARD", "type": "select"},
            "t1_tune": {"min": -24, "max": 24, "default": 0, "unit": "semitones", "type": "knob"},
            "t1_decay": {"min": 1, "max": 2000, "default": 300, "unit": "ms", "type": "knob"},
            "t1_punch": {"min": 0, "max": 100, "default": 60, "unit": "%", "type": "knob"},
            "t1_tone": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "t1_level": {"min": 0, "max": 100, "default": 85, "unit": "%", "type": "knob"},
            # Track 2 (Snare) - SD HARD (909 style)
            "t2_machine": {"options": ["BD HARD", "BD FM", "BD PLASTIC", "BD SILKY", "BD SHARP", "SD HARD", "SD CLASSIC", "RS HARD", "CP CLASSIC", "CH CLASSIC", "OH CLASSIC", "CY CLASSIC"], "default": "SD HARD", "type": "select"},
            "t2_tune": {"min": -24, "max": 24, "default": 0, "unit": "semitones", "type": "knob"},
            "t2_decay": {"min": 1, "max": 2000, "default": 150, "unit": "ms", "type": "knob"},
            "t2_snap": {"min": 0, "max": 100, "default": 40, "unit": "%", "type": "knob"},
            "t2_tone": {"min": 0, "max": 100, "default": 60, "unit": "%", "type": "knob"},
            "t2_level": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            # Filter (Global)
            "filter_cutoff": {"min": 20, "max": 20000, "default": 5000, "unit": "Hz", "type": "knob"},
            "filter_res": {"min": 0, "max": 100, "default": 10, "unit": "%", "type": "knob"},
            "distortion": {"min": 0, "max": 100, "default": 0, "unit": "%", "type": "knob"},
        }
    },
    "Sub 37": {
        "name": "Moog Sub 37 Tribute Edition",
        "manufacturer": "Moog",
        "controls": {
            # Oscillators
            "osc1_freq": {"min": -2, "max": 2, "default": 0, "unit": "octaves", "type": "knob"},
            "osc1_wave": {"options": ["Saw", "Square", "Triangle"], "default": "Saw", "type": "select"},
            "osc2_freq": {"min": -2, "max": 2, "default": 0, "unit": "octaves", "type": "knob"},
            "osc2_wave": {"options": ["Saw", "Square", "Triangle"], "default": "Square", "type": "select"},
            "sub_level": {"min": 0, "max": 100, "default": 40, "unit": "%", "type": "knob"},
            "noise_level": {"min": 0, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            # Filter
            "vcf_cutoff": {"min": 20, "max": 20000, "default": 2000, "unit": "Hz", "type": "knob"},
            "vcf_resonance": {"min": 0, "max": 100, "default": 20, "unit": "%", "type": "knob"},
            "vcf_eg": {"min": -100, "max": 100, "default": 40, "unit": "%", "type": "knob"},
            "vcf_kb_tracking": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            # Envelopes
            "eg1_attack": {"min": 1, "max": 3000, "default": 10, "unit": "ms", "type": "knob"},
            "eg1_decay": {"min": 1, "max": 5000, "default": 300, "unit": "ms", "type": "knob"},
            "eg1_sustain": {"min": 0, "max": 100, "default": 60, "unit": "%", "type": "knob"},
            "eg1_release": {"min": 1, "max": 5000, "default": 200, "unit": "ms", "type": "knob"},
            # LFO
            "lfo_rate": {"min": 0.1, "max": 500.0, "default": 2.0, "unit": "Hz", "type": "knob", "step": 0.1},
            "lfo_amount": {"min": 0, "max": 100, "default": 0, "unit": "%", "type": "knob"},
        }
    },
    "Xone:96": {
        "name": "Allen & Heath Xone:96 Analogue DJ Mixer",
        "manufacturer": "Allen & Heath",
        "controls": {
            # Channel 1
            "ch1_gain": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            "ch1_eq_high": {"min": -26, "max": 6, "default": 0, "unit": "dB", "type": "knob"},
            "ch1_eq_mid": {"min": -26, "max": 6, "default": 0, "unit": "dB", "type": "knob"},
            "ch1_eq_low": {"min": -26, "max": 6, "default": 0, "unit": "dB", "type": "knob"},
            "ch1_filter": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "ch1_fader": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            # Channel 2
            "ch2_gain": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            "ch2_eq_high": {"min": -26, "max": 6, "default": 0, "unit": "dB", "type": "knob"},
            "ch2_eq_mid": {"min": -26, "max": 6, "default": 0, "unit": "dB", "type": "knob"},
            "ch2_eq_low": {"min": -26, "max": 6, "default": 0, "unit": "dB", "type": "knob"},
            "ch2_filter": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "ch2_fader": {"min": 0, "max": 100, "default": 75, "unit": "%", "type": "knob"},
            # Master
            "crossfader": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
            "master_level": {"min": 0, "max": 100, "default": 80, "unit": "%", "type": "knob"},
            # Effects
            "fx_send": {"min": 0, "max": 100, "default": 0, "unit": "%", "type": "knob"},
            "fx_return": {"min": 0, "max": 100, "default": 50, "unit": "%", "type": "knob"},
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
    },
    "Subharmonicon": {
        "Harmonic Drone": {
            "description": "Rich harmonic drone using subharmonics",
            "source": "Official Patch Book",
            "steps": [
                {"control": "vco1_freq", "value": 0, "instruction": "VCO 1 FREQUENCY to center (0 octaves)"},
                {"control": "vco2_freq", "value": 0, "instruction": "VCO 2 FREQUENCY to center (0 octaves)"},
                {"control": "vco1_sub1", "value": "÷2", "instruction": "VCO 1 SUB 1 to ÷2 (octave down)"},
                {"control": "vco1_sub2", "value": "÷3", "instruction": "VCO 1 SUB 2 to ÷3 (fifth + octave)"},
                {"control": "vco2_sub1", "value": "÷4", "instruction": "VCO 2 SUB 1 to ÷4 (two octaves down)"},
                {"control": "vco2_sub2", "value": "÷5", "instruction": "VCO 2 SUB 2 to ÷5 (major third undertone)"},
                {"control": "vco1_level", "value": 50, "instruction": "VCO 1 LEVEL to 50%"},
                {"control": "vco2_level", "value": 50, "instruction": "VCO 2 LEVEL to 50%"},
                {"control": "sub_level", "value": 60, "instruction": "SUB LEVEL to 60% (emphasize low harmonics)"},
                {"control": "vcf_cutoff", "value": 3000, "instruction": "FILTER CUTOFF to 3000Hz"},
                {"control": "eg_attack", "value": 500, "instruction": "EG ATTACK to 500ms (slow)"},
                {"control": "eg_decay", "value": 1000, "instruction": "EG DECAY to 1000ms"},
                {"control": "eg_sustain", "value": 80, "instruction": "EG SUSTAIN to 80%"},
            ]
        },
        "Polyrhythmic Pattern": {
            "description": "Evolving polyrhythmic sequence",
            "source": "Community",
            "steps": [
                {"control": "vco1_freq", "value": 0, "instruction": "VCO 1 FREQUENCY to 0"},
                {"control": "vco2_freq", "value": 0.5, "instruction": "VCO 2 FREQUENCY to +0.5 octaves"},
                {"control": "rhythm1", "value": 4, "instruction": "RHYTHM 1 to 4 steps"},
                {"control": "rhythm2", "value": 3, "instruction": "RHYTHM 2 to 3 steps (creates 4:3 polyrhythm)"},
                {"control": "eg_attack", "value": 5, "instruction": "Fast ATTACK at 5ms"},
                {"control": "eg_decay", "value": 200, "instruction": "Short DECAY at 200ms"},
                {"control": "vcf_cutoff", "value": 1500, "instruction": "FILTER CUTOFF to 1500Hz"},
            ]
        }
    },
    "Analog Four": {
        "Classic Analog Bass": {
            "description": "Fat analog bass using dual oscillators",
            "source": "Official Manual",
            "steps": [
                {"control": "v1_osc1_wave", "value": "Saw", "instruction": "OSC 1 WAVE to Saw"},
                {"control": "v1_osc2_wave", "value": "Pulse", "instruction": "OSC 2 WAVE to Pulse"},
                {"control": "v1_osc1_tune", "value": 0, "instruction": "OSC 1 TUNE to 0 semitones"},
                {"control": "v1_osc2_tune", "value": -12, "instruction": "OSC 2 TUNE to -12 semitones (octave down)"},
                {"control": "v1_osc2_detune", "value": 5, "instruction": "OSC 2 DETUNE to 5 cents (slight detuning)"},
                {"control": "v1_sub_level", "value": 60, "instruction": "SUB OSC LEVEL to 60%"},
                {"control": "v1_filter_cutoff", "value": 800, "instruction": "FILTER CUTOFF to 800Hz"},
                {"control": "v1_filter_res", "value": 50, "instruction": "FILTER RESONANCE to 50%"},
                {"control": "v1_filter_eg", "value": 60, "instruction": "FILTER EG to +60%"},
                {"control": "v1_eg_attack", "value": 5, "instruction": "EG ATTACK to 5ms (fast)"},
                {"control": "v1_eg_decay", "value": 400, "instruction": "EG DECAY to 400ms"},
            ]
        },
        "Detuned Supersaw": {
            "description": "Wide stereo lead with parameter locks",
            "source": "Community",
            "steps": [
                {"control": "v1_osc1_wave", "value": "Saw", "instruction": "OSC 1 WAVE to Saw"},
                {"control": "v1_osc2_wave", "value": "Saw", "instruction": "OSC 2 WAVE to Saw"},
                {"control": "v1_osc1_detune", "value": -10, "instruction": "OSC 1 DETUNE to -10 cents"},
                {"control": "v1_osc2_detune", "value": 10, "instruction": "OSC 2 DETUNE to +10 cents (wide stereo)"},
                {"control": "v1_filter_cutoff", "value": 5000, "instruction": "FILTER CUTOFF to 5000Hz (open)"},
                {"control": "v1_lfo_rate", "value": 0.5, "instruction": "LFO RATE to 0.5Hz (slow)"},
                {"control": "v1_lfo_depth", "value": 30, "instruction": "LFO DEPTH to 30%"},
            ]
        }
    },
    "Analog Rytm": {
        "Classic 808 Kick": {
            "description": "TR-808 style kick drum",
            "source": "Official Manual",
            "steps": [
                {"control": "t1_machine", "value": "BD HARD", "instruction": "Select BD HARD machine (808 style)"},
                {"control": "t1_tune", "value": -3, "instruction": "TUNE to -3 semitones (low punch)"},
                {"control": "t1_decay", "value": 400, "instruction": "DECAY to 400ms"},
                {"control": "t1_punch", "value": 70, "instruction": "PUNCH to 70% (adds click)"},
                {"control": "t1_tone", "value": 45, "instruction": "TONE to 45%"},
                {"control": "t1_level", "value": 90, "instruction": "LEVEL to 90%"},
            ]
        },
        "909 Snare": {
            "description": "TR-909 style snare drum",
            "source": "Official Manual",
            "steps": [
                {"control": "t2_machine", "value": "SD HARD", "instruction": "Select SD HARD machine (909 style)"},
                {"control": "t2_tune", "value": 0, "instruction": "TUNE to 0 semitones"},
                {"control": "t2_decay", "value": 120, "instruction": "DECAY to 120ms (short snap)"},
                {"control": "t2_snap", "value": 60, "instruction": "SNAP to 60% (brightness)"},
                {"control": "t2_tone", "value": 65, "instruction": "TONE to 65%"},
                {"control": "t2_level", "value": 80, "instruction": "LEVEL to 80%"},
            ]
        }
    },
    "Sub 37": {
        "Fat Lead": {
            "description": "Thick mono lead sound",
            "source": "Manual",
            "steps": [
                {"control": "osc1_wave", "value": "Saw", "instruction": "OSC 1 WAVE to Saw"},
                {"control": "osc2_wave", "value": "Square", "instruction": "OSC 2 WAVE to Square"},
                {"control": "osc2_freq", "value": 0.1, "instruction": "OSC 2 FREQ slightly higher (+0.1 oct)"},
                {"control": "sub_level", "value": 50, "instruction": "SUB LEVEL to 50%"},
                {"control": "vcf_cutoff", "value": 1500, "instruction": "FILTER CUTOFF to 1500Hz"},
                {"control": "vcf_resonance", "value": 40, "instruction": "RESONANCE to 40%"},
                {"control": "vcf_eg", "value": 60, "instruction": "FILTER EG to +60%"},
                {"control": "eg1_attack", "value": 10, "instruction": "ATTACK to 10ms"},
                {"control": "eg1_decay", "value": 300, "instruction": "DECAY to 300ms"},
            ]
        }
    },
    "Xone:96": {
        "Basic Mix Setup": {
            "description": "Standard two-channel mixing setup",
            "source": "Manual",
            "steps": [
                {"control": "ch1_gain", "value": 75, "instruction": "Channel 1 GAIN to 75%"},
                {"control": "ch1_eq_high", "value": 0, "instruction": "CH1 HIGH EQ to 0dB (flat)"},
                {"control": "ch1_eq_mid", "value": 0, "instruction": "CH1 MID EQ to 0dB (flat)"},
                {"control": "ch1_eq_low", "value": 0, "instruction": "CH1 LOW EQ to 0dB (flat)"},
                {"control": "ch1_fader", "value": 75, "instruction": "CH1 FADER to 75%"},
                {"control": "ch2_gain", "value": 75, "instruction": "Channel 2 GAIN to 75%"},
                {"control": "ch2_fader", "value": 75, "instruction": "CH2 FADER to 75%"},
                {"control": "crossfader", "value": 50, "instruction": "CROSSFADER to center (50%)"},
                {"control": "master_level", "value": 80, "instruction": "MASTER LEVEL to 80%"},
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

elif device == "Subharmonicon":

    # VCO 1 ROW
    st.markdown("<div class='panel-section-label'>VCO 1 + SUBHARMONICS</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>VCO 1 FREQUENCY</div>", unsafe_allow_html=True)
        val = st.slider("", -3.0, 3.0, float(get_control_value(device, "vco1_freq")), 0.1, key="sub_vco1_freq", label_visibility="collapsed")
        set_control_value(device, "vco1_freq", val)
        st.markdown(f"<div class='value-display'>{val:+.1f} oct</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>VCO 1 WAVE</div>", unsafe_allow_html=True)
        val = st.selectbox("", ["Triangle", "Saw", "Square"], index=["Triangle", "Saw", "Square"].index(get_control_value(device, "vco1_wave")), key="sub_vco1_wave", label_visibility="collapsed")
        set_control_value(device, "vco1_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>SUB 1</div>", unsafe_allow_html=True)
        options = ["÷1", "÷2", "÷3", "÷4", "÷5", "÷6", "÷7", "÷8", "÷9", "÷10", "÷11", "÷12", "÷13", "÷14", "÷15", "÷16"]
        val = st.selectbox("", options, index=options.index(get_control_value(device, "vco1_sub1")), key="sub_vco1_sub1", label_visibility="collapsed")
        set_control_value(device, "vco1_sub1", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>SUB 2</div>", unsafe_allow_html=True)
        val = st.selectbox("", options, index=options.index(get_control_value(device, "vco1_sub2")), key="sub_vco1_sub2", label_visibility="collapsed")
        set_control_value(device, "vco1_sub2", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    # VCO 2 ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>VCO 2 + SUBHARMONICS</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>VCO 2 FREQUENCY</div>", unsafe_allow_html=True)
        val = st.slider("", -3.0, 3.0, float(get_control_value(device, "vco2_freq")), 0.1, key="sub_vco2_freq", label_visibility="collapsed")
        set_control_value(device, "vco2_freq", val)
        st.markdown(f"<div class='value-display'>{val:+.1f} oct</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>VCO 2 WAVE</div>", unsafe_allow_html=True)
        val = st.selectbox("", ["Triangle", "Saw", "Square"], index=["Triangle", "Saw", "Square"].index(get_control_value(device, "vco2_wave")), key="sub_vco2_wave", label_visibility="collapsed")
        set_control_value(device, "vco2_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>SUB 1</div>", unsafe_allow_html=True)
        val = st.selectbox("", options, index=options.index(get_control_value(device, "vco2_sub1")), key="sub_vco2_sub1", label_visibility="collapsed")
        set_control_value(device, "vco2_sub1", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>SUB 2</div>", unsafe_allow_html=True)
        val = st.selectbox("", options, index=options.index(get_control_value(device, "vco2_sub2")), key="sub_vco2_sub2", label_visibility="collapsed")
        set_control_value(device, "vco2_sub2", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    # MIXER ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>MIXER</div>", unsafe_allow_html=True)
    cols = st.columns(3)

    with cols[0]:
        st.markdown("<div class='control-label'>VCO 1 LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vco1_level")), 1, key="sub_vco1_level", label_visibility="collapsed")
        set_control_value(device, "vco1_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>VCO 2 LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vco2_level")), 1, key="sub_vco2_level", label_visibility="collapsed")
        set_control_value(device, "vco2_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>SUB LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "sub_level")), 1, key="sub_sub_level", label_visibility="collapsed")
        set_control_value(device, "sub_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # FILTER ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>FILTER</div>", unsafe_allow_html=True)
    cols = st.columns(3)

    with cols[0]:
        st.markdown("<div class='control-label'>CUTOFF</div>", unsafe_allow_html=True)
        val = st.slider("", 20, 20000, int(get_control_value(device, "vcf_cutoff")), 10, key="sub_cutoff", label_visibility="collapsed")
        set_control_value(device, "vcf_cutoff", val)
        st.markdown(f"<div class='value-display'>{val}Hz</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>RESONANCE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vcf_resonance")), 1, key="sub_res", label_visibility="collapsed")
        set_control_value(device, "vcf_resonance", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>FILTER EG</div>", unsafe_allow_html=True)
        val = st.slider("", -100, 100, int(get_control_value(device, "vcf_eg")), 1, key="sub_filter_eg", label_visibility="collapsed")
        set_control_value(device, "vcf_eg", val)
        st.markdown(f"<div class='value-display'>{val:+d}%</div>", unsafe_allow_html=True)

    # ENVELOPE ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>ENVELOPE</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>ATTACK</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 5000, int(get_control_value(device, "eg_attack")), 1, key="sub_attack", label_visibility="collapsed")
        set_control_value(device, "eg_attack", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 10000, int(get_control_value(device, "eg_decay")), 1, key="sub_decay", label_visibility="collapsed")
        set_control_value(device, "eg_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>SUSTAIN</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "eg_sustain")), 1, key="sub_sustain", label_visibility="collapsed")
        set_control_value(device, "eg_sustain", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>RELEASE</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 10000, int(get_control_value(device, "eg_release")), 1, key="sub_release", label_visibility="collapsed")
        set_control_value(device, "eg_release", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    # POLYRHYTHM ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>POLYRHYTHM</div>", unsafe_allow_html=True)
    cols = st.columns(2)

    with cols[0]:
        st.markdown("<div class='control-label'>RHYTHM 1</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 16, int(get_control_value(device, "rhythm1")), 1, key="sub_rhythm1", label_visibility="collapsed")
        set_control_value(device, "rhythm1", val)
        st.markdown(f"<div class='value-display'>{val} steps</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>RHYTHM 2</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 16, int(get_control_value(device, "rhythm2")), 1, key="sub_rhythm2", label_visibility="collapsed")
        set_control_value(device, "rhythm2", val)
        st.markdown(f"<div class='value-display'>{val} steps</div>", unsafe_allow_html=True)

elif device == "Analog Four":

    # OSCILLATORS ROW
    st.markdown("<div class='panel-section-label'>VOICE 1 - OSCILLATORS</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>OSC 1 WAVE</div>", unsafe_allow_html=True)
        options = ["Saw", "Pulse", "Trans Pulse", "Triangle"]
        val = st.selectbox("", options, index=options.index(get_control_value(device, "v1_osc1_wave")), key="a4_osc1_wave", label_visibility="collapsed")
        set_control_value(device, "v1_osc1_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>OSC 1 TUNE</div>", unsafe_allow_html=True)
        val = st.slider("", -24, 24, int(get_control_value(device, "v1_osc1_tune")), 1, key="a4_osc1_tune", label_visibility="collapsed")
        set_control_value(device, "v1_osc1_tune", val)
        st.markdown(f"<div class='value-display'>{val:+d} st</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>OSC 1 DETUNE</div>", unsafe_allow_html=True)
        val = st.slider("", -50, 50, int(get_control_value(device, "v1_osc1_detune")), 1, key="a4_osc1_detune", label_visibility="collapsed")
        set_control_value(device, "v1_osc1_detune", val)
        st.markdown(f"<div class='value-display'>{val:+d} ct</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>OSC 1 PWM</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "v1_osc1_pwm")), 1, key="a4_osc1_pwm", label_visibility="collapsed")
        set_control_value(device, "v1_osc1_pwm", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # OSC 2 + SUB ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 20px;'>VOICE 1 - OSC 2 + SUB</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>OSC 2 WAVE</div>", unsafe_allow_html=True)
        val = st.selectbox("", options, index=options.index(get_control_value(device, "v1_osc2_wave")), key="a4_osc2_wave", label_visibility="collapsed")
        set_control_value(device, "v1_osc2_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>OSC 2 TUNE</div>", unsafe_allow_html=True)
        val = st.slider("", -24, 24, int(get_control_value(device, "v1_osc2_tune")), 1, key="a4_osc2_tune", label_visibility="collapsed")
        set_control_value(device, "v1_osc2_tune", val)
        st.markdown(f"<div class='value-display'>{val:+d} st</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>OSC 2 DETUNE</div>", unsafe_allow_html=True)
        val = st.slider("", -50, 50, int(get_control_value(device, "v1_osc2_detune")), 1, key="a4_osc2_detune", label_visibility="collapsed")
        set_control_value(device, "v1_osc2_detune", val)
        st.markdown(f"<div class='value-display'>{val:+d} ct</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>SUB LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "v1_sub_level")), 1, key="a4_sub_level", label_visibility="collapsed")
        set_control_value(device, "v1_sub_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # FILTER ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>VOICE 1 - FILTER</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>FILTER TYPE</div>", unsafe_allow_html=True)
        filter_opts = ["LP", "BP", "HP", "Notch"]
        val = st.selectbox("", filter_opts, index=filter_opts.index(get_control_value(device, "v1_filter_type")), key="a4_filter_type", label_visibility="collapsed")
        set_control_value(device, "v1_filter_type", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>CUTOFF</div>", unsafe_allow_html=True)
        val = st.slider("", 20, 20000, int(get_control_value(device, "v1_filter_cutoff")), 10, key="a4_cutoff", label_visibility="collapsed")
        set_control_value(device, "v1_filter_cutoff", val)
        st.markdown(f"<div class='value-display'>{val}Hz</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>RESONANCE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "v1_filter_res")), 1, key="a4_res", label_visibility="collapsed")
        set_control_value(device, "v1_filter_res", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>FILTER EG</div>", unsafe_allow_html=True)
        val = st.slider("", -100, 100, int(get_control_value(device, "v1_filter_eg")), 1, key="a4_filter_eg", label_visibility="collapsed")
        set_control_value(device, "v1_filter_eg", val)
        st.markdown(f"<div class='value-display'>{val:+d}%</div>", unsafe_allow_html=True)

    # ENVELOPE ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>VOICE 1 - ENVELOPE</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>ATTACK</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 2000, int(get_control_value(device, "v1_eg_attack")), 1, key="a4_attack", label_visibility="collapsed")
        set_control_value(device, "v1_eg_attack", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 5000, int(get_control_value(device, "v1_eg_decay")), 1, key="a4_decay", label_visibility="collapsed")
        set_control_value(device, "v1_eg_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>SUSTAIN</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "v1_eg_sustain")), 1, key="a4_sustain", label_visibility="collapsed")
        set_control_value(device, "v1_eg_sustain", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>RELEASE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 5000, int(get_control_value(device, "v1_eg_release")), 1, key="a4_release", label_visibility="collapsed")
        set_control_value(device, "v1_eg_release", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    # LFO ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>VOICE 1 - LFO</div>", unsafe_allow_html=True)
    cols = st.columns(3)

    with cols[0]:
        st.markdown("<div class='control-label'>LFO RATE</div>", unsafe_allow_html=True)
        val = st.slider("", 0.01, 100.0, float(get_control_value(device, "v1_lfo_rate")), 0.01, key="a4_lfo_rate", label_visibility="collapsed")
        set_control_value(device, "v1_lfo_rate", val)
        st.markdown(f"<div class='value-display'>{val:.2f}Hz</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>LFO DEPTH</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "v1_lfo_depth")), 1, key="a4_lfo_depth", label_visibility="collapsed")
        set_control_value(device, "v1_lfo_depth", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>LFO WAVE</div>", unsafe_allow_html=True)
        lfo_opts = ["Sine", "Triangle", "Saw", "Square", "Random"]
        val = st.selectbox("", lfo_opts, index=lfo_opts.index(get_control_value(device, "v1_lfo_wave")), key="a4_lfo_wave", label_visibility="collapsed")
        set_control_value(device, "v1_lfo_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

elif device == "Analog Rytm":

    # TRACK 1 (KICK) ROW
    st.markdown("<div class='panel-section-label'>TRACK 1 - KICK DRUM</div>", unsafe_allow_html=True)
    cols = st.columns(6)

    with cols[0]:
        st.markdown("<div class='control-label'>MACHINE</div>", unsafe_allow_html=True)
        machines = ["BD HARD", "BD FM", "BD PLASTIC", "BD SILKY", "BD SHARP", "SD HARD", "SD CLASSIC", "RS HARD", "CP CLASSIC", "CH CLASSIC", "OH CLASSIC", "CY CLASSIC"]
        val = st.selectbox("", machines, index=machines.index(get_control_value(device, "t1_machine")), key="ar_t1_machine", label_visibility="collapsed")
        set_control_value(device, "t1_machine", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>TUNE</div>", unsafe_allow_html=True)
        val = st.slider("", -24, 24, int(get_control_value(device, "t1_tune")), 1, key="ar_t1_tune", label_visibility="collapsed")
        set_control_value(device, "t1_tune", val)
        st.markdown(f"<div class='value-display'>{val:+d} st</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 2000, int(get_control_value(device, "t1_decay")), 1, key="ar_t1_decay", label_visibility="collapsed")
        set_control_value(device, "t1_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>PUNCH</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "t1_punch")), 1, key="ar_t1_punch", label_visibility="collapsed")
        set_control_value(device, "t1_punch", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>TONE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "t1_tone")), 1, key="ar_t1_tone", label_visibility="collapsed")
        set_control_value(device, "t1_tone", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[5]:
        st.markdown("<div class='control-label'>LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "t1_level")), 1, key="ar_t1_level", label_visibility="collapsed")
        set_control_value(device, "t1_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # TRACK 2 (SNARE) ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>TRACK 2 - SNARE DRUM</div>", unsafe_allow_html=True)
    cols = st.columns(6)

    with cols[0]:
        st.markdown("<div class='control-label'>MACHINE</div>", unsafe_allow_html=True)
        val = st.selectbox("", machines, index=machines.index(get_control_value(device, "t2_machine")), key="ar_t2_machine", label_visibility="collapsed")
        set_control_value(device, "t2_machine", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>TUNE</div>", unsafe_allow_html=True)
        val = st.slider("", -24, 24, int(get_control_value(device, "t2_tune")), 1, key="ar_t2_tune", label_visibility="collapsed")
        set_control_value(device, "t2_tune", val)
        st.markdown(f"<div class='value-display'>{val:+d} st</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 2000, int(get_control_value(device, "t2_decay")), 1, key="ar_t2_decay", label_visibility="collapsed")
        set_control_value(device, "t2_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>SNAP</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "t2_snap")), 1, key="ar_t2_snap", label_visibility="collapsed")
        set_control_value(device, "t2_snap", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>TONE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "t2_tone")), 1, key="ar_t2_tone", label_visibility="collapsed")
        set_control_value(device, "t2_tone", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[5]:
        st.markdown("<div class='control-label'>LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "t2_level")), 1, key="ar_t2_level", label_visibility="collapsed")
        set_control_value(device, "t2_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # FILTER & FX ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>FILTER & DISTORTION</div>", unsafe_allow_html=True)
    cols = st.columns(3)

    with cols[0]:
        st.markdown("<div class='control-label'>FILTER CUTOFF</div>", unsafe_allow_html=True)
        val = st.slider("", 20, 20000, int(get_control_value(device, "filter_cutoff")), 10, key="ar_cutoff", label_visibility="collapsed")
        set_control_value(device, "filter_cutoff", val)
        st.markdown(f"<div class='value-display'>{val}Hz</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>RESONANCE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "filter_res")), 1, key="ar_res", label_visibility="collapsed")
        set_control_value(device, "filter_res", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>DISTORTION</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "distortion")), 1, key="ar_dist", label_visibility="collapsed")
        set_control_value(device, "distortion", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

elif device == "Sub 37":

    # OSCILLATORS ROW
    st.markdown("<div class='panel-section-label'>OSCILLATORS</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>OSC 1 FREQ</div>", unsafe_allow_html=True)
        val = st.slider("", -2.0, 2.0, float(get_control_value(device, "osc1_freq")), 0.1, key="s37_osc1_freq", label_visibility="collapsed")
        set_control_value(device, "osc1_freq", val)
        st.markdown(f"<div class='value-display'>{val:+.1f} oct</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>OSC 1 WAVE</div>", unsafe_allow_html=True)
        wave_opts = ["Saw", "Square", "Triangle"]
        val = st.selectbox("", wave_opts, index=wave_opts.index(get_control_value(device, "osc1_wave")), key="s37_osc1_wave", label_visibility="collapsed")
        set_control_value(device, "osc1_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>OSC 2 FREQ</div>", unsafe_allow_html=True)
        val = st.slider("", -2.0, 2.0, float(get_control_value(device, "osc2_freq")), 0.1, key="s37_osc2_freq", label_visibility="collapsed")
        set_control_value(device, "osc2_freq", val)
        st.markdown(f"<div class='value-display'>{val:+.1f} oct</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>OSC 2 WAVE</div>", unsafe_allow_html=True)
        val = st.selectbox("", wave_opts, index=wave_opts.index(get_control_value(device, "osc2_wave")), key="s37_osc2_wave", label_visibility="collapsed")
        set_control_value(device, "osc2_wave", val)
        st.markdown(f"<div class='value-display'>{val}</div>", unsafe_allow_html=True)

    # MIXER ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>MIXER</div>", unsafe_allow_html=True)
    cols = st.columns(2)

    with cols[0]:
        st.markdown("<div class='control-label'>SUB LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "sub_level")), 1, key="s37_sub", label_visibility="collapsed")
        set_control_value(device, "sub_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>NOISE LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "noise_level")), 1, key="s37_noise", label_visibility="collapsed")
        set_control_value(device, "noise_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # FILTER ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>FILTER (4-POLE MOOG LADDER)</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>CUTOFF</div>", unsafe_allow_html=True)
        val = st.slider("", 20, 20000, int(get_control_value(device, "vcf_cutoff")), 10, key="s37_cutoff", label_visibility="collapsed")
        set_control_value(device, "vcf_cutoff", val)
        st.markdown(f"<div class='value-display'>{val}Hz</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>RESONANCE</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vcf_resonance")), 1, key="s37_res", label_visibility="collapsed")
        set_control_value(device, "vcf_resonance", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>FILTER EG</div>", unsafe_allow_html=True)
        val = st.slider("", -100, 100, int(get_control_value(device, "vcf_eg")), 1, key="s37_filter_eg", label_visibility="collapsed")
        set_control_value(device, "vcf_eg", val)
        st.markdown(f"<div class='value-display'>{val:+d}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>KB TRACKING</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "vcf_kb_tracking")), 1, key="s37_kb", label_visibility="collapsed")
        set_control_value(device, "vcf_kb_tracking", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # ENVELOPE ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>ENVELOPE 1</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>ATTACK</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 3000, int(get_control_value(device, "eg1_attack")), 1, key="s37_attack", label_visibility="collapsed")
        set_control_value(device, "eg1_attack", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>DECAY</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 5000, int(get_control_value(device, "eg1_decay")), 1, key="s37_decay", label_visibility="collapsed")
        set_control_value(device, "eg1_decay", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>SUSTAIN</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "eg1_sustain")), 1, key="s37_sustain", label_visibility="collapsed")
        set_control_value(device, "eg1_sustain", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>RELEASE</div>", unsafe_allow_html=True)
        val = st.slider("", 1, 5000, int(get_control_value(device, "eg1_release")), 1, key="s37_release", label_visibility="collapsed")
        set_control_value(device, "eg1_release", val)
        st.markdown(f"<div class='value-display'>{val}ms</div>", unsafe_allow_html=True)

    # LFO ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>LFO</div>", unsafe_allow_html=True)
    cols = st.columns(2)

    with cols[0]:
        st.markdown("<div class='control-label'>LFO RATE</div>", unsafe_allow_html=True)
        val = st.slider("", 0.1, 500.0, float(get_control_value(device, "lfo_rate")), 0.1, key="s37_lfo_rate", label_visibility="collapsed")
        set_control_value(device, "lfo_rate", val)
        st.markdown(f"<div class='value-display'>{val:.1f}Hz</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>LFO AMOUNT</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "lfo_amount")), 1, key="s37_lfo_amt", label_visibility="collapsed")
        set_control_value(device, "lfo_amount", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

elif device == "Xone:96":

    # CHANNEL 1 ROW
    st.markdown("<div class='panel-section-label'>CHANNEL 1</div>", unsafe_allow_html=True)
    cols = st.columns(6)

    with cols[0]:
        st.markdown("<div class='control-label'>GAIN</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "ch1_gain")), 1, key="x96_ch1_gain", label_visibility="collapsed")
        set_control_value(device, "ch1_gain", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>HIGH EQ</div>", unsafe_allow_html=True)
        val = st.slider("", -26, 6, int(get_control_value(device, "ch1_eq_high")), 1, key="x96_ch1_high", label_visibility="collapsed")
        set_control_value(device, "ch1_eq_high", val)
        st.markdown(f"<div class='value-display'>{val:+d}dB</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>MID EQ</div>", unsafe_allow_html=True)
        val = st.slider("", -26, 6, int(get_control_value(device, "ch1_eq_mid")), 1, key="x96_ch1_mid", label_visibility="collapsed")
        set_control_value(device, "ch1_eq_mid", val)
        st.markdown(f"<div class='value-display'>{val:+d}dB</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>LOW EQ</div>", unsafe_allow_html=True)
        val = st.slider("", -26, 6, int(get_control_value(device, "ch1_eq_low")), 1, key="x96_ch1_low", label_visibility="collapsed")
        set_control_value(device, "ch1_eq_low", val)
        st.markdown(f"<div class='value-display'>{val:+d}dB</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>FILTER</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "ch1_filter")), 1, key="x96_ch1_filter", label_visibility="collapsed")
        set_control_value(device, "ch1_filter", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[5]:
        st.markdown("<div class='control-label'>FADER</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "ch1_fader")), 1, key="x96_ch1_fader", label_visibility="collapsed")
        set_control_value(device, "ch1_fader", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # CHANNEL 2 ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>CHANNEL 2</div>", unsafe_allow_html=True)
    cols = st.columns(6)

    with cols[0]:
        st.markdown("<div class='control-label'>GAIN</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "ch2_gain")), 1, key="x96_ch2_gain", label_visibility="collapsed")
        set_control_value(device, "ch2_gain", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>HIGH EQ</div>", unsafe_allow_html=True)
        val = st.slider("", -26, 6, int(get_control_value(device, "ch2_eq_high")), 1, key="x96_ch2_high", label_visibility="collapsed")
        set_control_value(device, "ch2_eq_high", val)
        st.markdown(f"<div class='value-display'>{val:+d}dB</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>MID EQ</div>", unsafe_allow_html=True)
        val = st.slider("", -26, 6, int(get_control_value(device, "ch2_eq_mid")), 1, key="x96_ch2_mid", label_visibility="collapsed")
        set_control_value(device, "ch2_eq_mid", val)
        st.markdown(f"<div class='value-display'>{val:+d}dB</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>LOW EQ</div>", unsafe_allow_html=True)
        val = st.slider("", -26, 6, int(get_control_value(device, "ch2_eq_low")), 1, key="x96_ch2_low", label_visibility="collapsed")
        set_control_value(device, "ch2_eq_low", val)
        st.markdown(f"<div class='value-display'>{val:+d}dB</div>", unsafe_allow_html=True)

    with cols[4]:
        st.markdown("<div class='control-label'>FILTER</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "ch2_filter")), 1, key="x96_ch2_filter", label_visibility="collapsed")
        set_control_value(device, "ch2_filter", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[5]:
        st.markdown("<div class='control-label'>FADER</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "ch2_fader")), 1, key="x96_ch2_fader", label_visibility="collapsed")
        set_control_value(device, "ch2_fader", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    # MASTER & FX ROW
    st.markdown("<div class='panel-section-label' style='margin-top: 30px;'>MASTER & EFFECTS</div>", unsafe_allow_html=True)
    cols = st.columns(4)

    with cols[0]:
        st.markdown("<div class='control-label'>CROSSFADER</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "crossfader")), 1, key="x96_xfader", label_visibility="collapsed")
        set_control_value(device, "crossfader", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("<div class='control-label'>MASTER LEVEL</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "master_level")), 1, key="x96_master", label_visibility="collapsed")
        set_control_value(device, "master_level", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[2]:
        st.markdown("<div class='control-label'>FX SEND</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "fx_send")), 1, key="x96_fx_send", label_visibility="collapsed")
        set_control_value(device, "fx_send", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

    with cols[3]:
        st.markdown("<div class='control-label'>FX RETURN</div>", unsafe_allow_html=True)
        val = st.slider("", 0, 100, int(get_control_value(device, "fx_return")), 1, key="x96_fx_return", label_visibility="collapsed")
        set_control_value(device, "fx_return", val)
        st.markdown(f"<div class='value-display'>{val}%</div>", unsafe_allow_html=True)

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
