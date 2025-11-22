"""
Synthesizer Studio Interactive Learning Tool
A comprehensive Streamlit app for learning synthesizers with visual, hands-on tutorials
Optimized for DFAM, Mother-32, Subharmonicon, Analog Four/Rytm, Sub 37, and Xone:96
"""

import streamlit as st
import json
import time
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math

# Page Configuration
st.set_page_config(
    page_title="Synthesizer Studio Learning Tool",
    page_icon="🎹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced visual learning
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }

    /* Knob styling */
    .knob-container {
        background: #2d2d2d;
        border-radius: 50%;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 2px solid #444;
        position: relative;
    }

    .knob-value {
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        text-shadow: 0 0 10px rgba(0,255,0,0.5);
    }

    /* Module cards */
    .module-card {
        background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6);
        border: 1px solid #333;
    }

    /* Success indicators */
    .success-badge {
        background: linear-gradient(90deg, #4caf50, #45a049);
        color: white;
        padding: 8px 15px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76,175,80,0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76,175,80,0); }
        100% { box-shadow: 0 0 0 0 rgba(76,175,80,0); }
    }

    /* Progress bar */
    .progress-bar {
        background: #333;
        border-radius: 10px;
        height: 25px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }

    .progress-fill {
        background: linear-gradient(90deg, #00ff00, #00aa00);
        height: 100%;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(0,255,0,0.5);
    }

    /* Step sequencer */
    .step-button {
        background: #333;
        border: 2px solid #555;
        border-radius: 5px;
        padding: 10px;
        transition: all 0.3s;
    }

    .step-button.active {
        background: #00ff00;
        box-shadow: 0 0 20px rgba(0,255,0,0.8);
        transform: scale(1.1);
    }

    /* Interactive elements */
    .stButton > button {
        background: linear-gradient(145deg, #333, #222);
        color: white;
        border: 2px solid #555;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: linear-gradient(145deg, #444, #333);
        border-color: #00ff00;
        box-shadow: 0 0 15px rgba(0,255,0,0.3);
    }

    /* Info boxes */
    .stAlert {
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = None
if 'progress' not in st.session_state:
    st.session_state.progress = {}
if 'session_start' not in st.session_state:
    st.session_state.session_start = None
if 'current_patch' not in st.session_state:
    st.session_state.current_patch = {}
if 'step_pattern' not in st.session_state:
    st.session_state.step_pattern = [False] * 16
if 'patches_library' not in st.session_state:
    st.session_state.patches_library = []

# Helper Functions
def create_knob_visualization(label, value, min_val=0, max_val=100, color="#00ff00"):
    """Create an interactive knob visualization"""
    fig = go.Figure()

    # Create knob circle
    fig.add_shape(type="circle",
        x0=-1, y0=-1, x1=1, y1=1,
        line=dict(color="white", width=2),
        fillcolor="rgba(45,45,45,0.9)"
    )

    # Add tick marks
    for i in range(0, 11):
        angle = -135 + (i * 27)  # -135 to +135 degrees
        rad = math.radians(angle)
        x1 = 0.8 * math.cos(rad)
        y1 = 0.8 * math.sin(rad)
        x2 = 0.9 * math.cos(rad)
        y2 = 0.9 * math.sin(rad)

        fig.add_shape(type="line",
            x0=x1, y0=y1, x1=x2, y1=y2,
            line=dict(color="#666", width=1)
        )

    # Position indicator
    normalized_value = (value - min_val) / (max_val - min_val)
    angle = -135 + (normalized_value * 270)  # Map to -135 to +135 degrees
    rad = math.radians(angle)
    end_x = 0.7 * math.cos(rad)
    end_y = 0.7 * math.sin(rad)

    fig.add_shape(type="line",
        x0=0, y0=0, x1=end_x, y1=end_y,
        line=dict(color=color, width=4)
    )

    # Add center dot
    fig.add_shape(type="circle",
        x0=-0.1, y0=-0.1, x1=0.1, y1=0.1,
        fillcolor=color,
        line=dict(width=0)
    )

    # Add label
    fig.add_annotation(
        x=0, y=-1.5,
        text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=12, color="white")
    )

    # Add value
    fig.add_annotation(
        x=0, y=0,
        text=f"<b>{value}</b>",
        showarrow=False,
        font=dict(size=14, color=color)
    )

    fig.update_layout(
        showlegend=False,
        height=150,
        width=150,
        margin=dict(l=0, r=0, t=0, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, range=[-2, 2]),
        yaxis=dict(visible=False, range=[-2, 2])
    )

    return fig

def create_waveform_display(waveform_type="saw", frequency=1.0, pulse_width=50):
    """Create waveform visualization"""
    x = np.linspace(0, 4 * np.pi, 1000)

    if waveform_type == "sine":
        y = np.sin(x * frequency)
    elif waveform_type == "saw":
        y = 2 * ((x * frequency) % (2 * np.pi)) / (2 * np.pi) - 1
    elif waveform_type == "pulse":
        duty = pulse_width / 100
        y = np.where(((x * frequency) % (2 * np.pi)) < (2 * np.pi * duty), 1, -1)
    elif waveform_type == "triangle":
        period = 2 * np.pi / frequency
        y = 2 * np.abs(2 * ((x / period) - np.floor((x / period) + 0.5))) - 1
    else:
        y = np.random.normal(0, 0.3, len(x))  # Noise

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(color='#00ff00', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,255,0,0.1)'
    ))

    fig.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0.2)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            visible=False,
            range=[0, 4 * np.pi]
        ),
        yaxis=dict(
            visible=True,
            range=[-1.5, 1.5],
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)',
            showticklabels=False
        )
    )

    return fig

def create_envelope_visualization(attack, decay, sustain, release):
    """Create ADSR envelope visualization"""
    # Time points
    attack_time = attack / 100 * 0.5
    decay_time = decay / 100 * 0.5
    sustain_level = sustain / 100
    release_time = release / 100 * 0.5

    # Create envelope points
    t = [0, attack_time, attack_time + decay_time, 1.5, 1.5 + release_time]
    envelope = [0, 1, sustain_level, sustain_level, 0]

    fig = go.Figure()

    # Add envelope line
    fig.add_trace(go.Scatter(
        x=t, y=envelope,
        mode='lines',
        line=dict(color='#00ff00', width=3),
        fill='tozeroy',
        fillcolor='rgba(0,255,0,0.2)'
    ))

    # Add phase markers
    fig.add_vline(x=attack_time, line=dict(color='rgba(255,255,255,0.3)', dash='dot'))
    fig.add_vline(x=attack_time + decay_time, line=dict(color='rgba(255,255,255,0.3)', dash='dot'))
    fig.add_vline(x=1.5, line=dict(color='rgba(255,255,255,0.3)', dash='dot'))

    # Add phase labels
    fig.add_annotation(x=attack_time/2, y=0.5, text="A", showarrow=False, font=dict(color='white', size=12))
    fig.add_annotation(x=attack_time + decay_time/2, y=0.9, text="D", showarrow=False, font=dict(color='white', size=12))
    fig.add_annotation(x=0.75 + attack_time + decay_time/2, y=sustain_level/2, text="S", showarrow=False, font=dict(color='white', size=12))
    fig.add_annotation(x=1.5 + release_time/2, y=sustain_level/2, text="R", showarrow=False, font=dict(color='white', size=12))

    fig.update_layout(
        showlegend=False,
        height=250,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0.2)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            visible=False,
            range=[0, 2]
        ),
        yaxis=dict(
            visible=True,
            range=[0, 1.1],
            gridcolor='rgba(255,255,255,0.1)',
            showticklabels=False
        )
    )

    return fig

def create_filter_response(cutoff, resonance):
    """Create filter frequency response visualization"""
    freqs = np.logspace(1, 4, 200)
    cutoff_freq = 20 + (cutoff / 100) * 20000

    # Simple lowpass response
    response = 1 / np.sqrt(1 + ((freqs / cutoff_freq) ** 4))

    # Add resonance peak
    if resonance > 0:
        q = 0.7 + (resonance / 100) * 10
        peak_gain = 1 + (resonance / 100) * 3
        peak_width = 0.2 / q
        resonance_curve = peak_gain * np.exp(-((np.log(freqs) - np.log(cutoff_freq)) ** 2) / (2 * peak_width ** 2))
        response = response * resonance_curve

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=freqs, y=response,
        mode='lines',
        line=dict(color='#ff6b6b', width=2),
        fill='tozeroy',
        fillcolor='rgba(255,107,107,0.2)'
    ))

    # Add cutoff marker
    fig.add_vline(x=cutoff_freq, line=dict(color='#00ff00', dash='dash', width=2))
    fig.add_annotation(
        x=np.log10(cutoff_freq),
        y=max(response) * 1.1,
        text=f"Cutoff: {cutoff_freq:.0f} Hz",
        showarrow=False,
        font=dict(color='#00ff00', size=10)
    )

    fig.update_layout(
        showlegend=False,
        height=250,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0.2)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            type="log",
            range=[1, 4],
            gridcolor='rgba(255,255,255,0.1)',
            title="Frequency (Hz)",
            titlefont=dict(size=10, color='white'),
            tickfont=dict(size=8, color='white')
        ),
        yaxis=dict(
            range=[0, max(response) * 1.2],
            gridcolor='rgba(255,255,255,0.1)',
            showticklabels=False
        )
    )

    return fig

# Main Application Header
st.markdown("""
<div style='text-align: center; padding: 20px; background: rgba(0,0,0,0.3); border-radius: 15px; margin-bottom: 30px;'>
    <h1 style='color: white; font-size: 3em; margin: 0; text-shadow: 0 0 20px rgba(0,255,0,0.5);'>
        🎛️ Synthesizer Studio Learning Tool
    </h1>
    <p style='color: #aaa; font-size: 1.2em; margin-top: 10px;'>
        Master your synths with visual, hands-on learning
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🎯 Learning Path")

    # Session Timer
    if st.session_state.session_start:
        elapsed = datetime.now() - st.session_state.session_start
        total_minutes = 45
        remaining = timedelta(minutes=total_minutes) - elapsed

        if remaining.total_seconds() > 0:
            progress = elapsed.total_seconds() / (total_minutes * 60)
            st.progress(min(progress, 1.0))
            mins, secs = divmod(int(elapsed.total_seconds()), 60)
            st.info(f"⏱️ Session Time: {mins:02d}:{secs:02d} / 45:00")
        else:
            st.success("✅ Session Complete! Great work!")
    else:
        if st.button("🎬 Start Session", use_container_width=True):
            st.session_state.session_start = datetime.now()
            st.rerun()

    st.divider()

    # Learning Mode Selection
    learning_mode = st.selectbox(
        "Choose Your Path",
        [
            "🥁 Quick Start: DFAM Drum Programming",
            "🎹 Fundamentals: Mother-32 Synthesis",
            "🌊 Polyrhythms: Subharmonicon",
            "🎼 Sequencing: Analog Four",
            "🎛️ Sound Design: Sub 37",
            "🔊 Mixing: Xone:96 Signal Flow",
            "🔌 Modular Patching: Cross-Device",
            "📚 Reference Library"
        ],
        key="learning_mode"
    )

    st.divider()

    # Progress Overview
    st.markdown("### 📊 Your Progress")

    # Calculate progress
    total_lessons = 25
    completed = len([l for l in st.session_state.progress.values() if l.get('completed', False)])
    progress_pct = (completed / total_lessons) * 100

    # Progress bar
    st.progress(progress_pct / 100)
    st.caption(f"{completed}/{total_lessons} lessons completed ({progress_pct:.0f}%)")

    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔥 Streak", "3 days", "↑2")
    with col2:
        st.metric("⏱️ Total Time", "12.5 hrs", "+45m")

    st.divider()

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")

    if st.button("💾 Save Current Patch", use_container_width=True):
        if st.session_state.current_patch:
            st.session_state.patches_library.append(st.session_state.current_patch)
            st.success("Patch saved!")

    if st.button("🎲 Random Patch", use_container_width=True):
        st.session_state.current_patch = {
            'name': f"Random_{datetime.now().strftime('%H%M')}",
            'vco_freq': np.random.randint(0, 100),
            'filter_cutoff': np.random.randint(20, 80),
            'resonance': np.random.randint(0, 60),
            'attack': np.random.randint(0, 50),
            'decay': np.random.randint(20, 60),
            'sustain': np.random.randint(40, 80),
            'release': np.random.randint(10, 70)
        }
        st.success("Random patch generated!")
        st.rerun()

# Main Content Area
if "DFAM Drum Programming" in learning_mode:
    st.markdown("## 🥁 DFAM Quick Start: Instant Drum Patterns")

    # Lesson tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Kick Drum", "🥁 Snare", "🎩 Hi-Hats", "🎼 Full Pattern"])

    with tab1:
        st.info("**Goal:** Create a punchy kick drum in under 5 minutes!")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 🎛️ Knob Settings")
            st.markdown("*Set these exact values for instant results:*")

            # DFAM Kick Parameters
            vco1 = st.slider("VCO 1 FREQUENCY", 0, 100, 15, help="Fundamental frequency - lower for deeper kicks")
            vco2 = st.slider("VCO 2 FREQUENCY", 0, 100, 20, help="Adds harmonic punch")
            vco_decay = st.slider("VCO DECAY", 0, 100, 30, help="How quickly pitch drops")
            noise = st.slider("NOISE LEVEL", 0, 100, 10, help="Adds 'click' to attack")
            vcf_decay = st.slider("VCF DECAY", 0, 100, 40, help="Filter envelope time")
            vcf_eg = st.slider("VCF EG AMOUNT", 0, 100, 60, help="How much filter opens")

            # Store current settings
            st.session_state.current_patch = {
                'type': 'dfam_kick',
                'vco1': vco1,
                'vco2': vco2,
                'vco_decay': vco_decay,
                'noise': noise,
                'vcf_decay': vcf_decay,
                'vcf_eg': vcf_eg
            }

        with col2:
            st.markdown("### 📊 Visual Feedback")

            # Knob visualization grid
            knob_col1, knob_col2, knob_col3 = st.columns(3)

            with knob_col1:
                st.plotly_chart(create_knob_visualization("VCO 1", vco1), use_container_width=True)
                st.plotly_chart(create_knob_visualization("VCO DECAY", vco_decay), use_container_width=True)

            with knob_col2:
                st.plotly_chart(create_knob_visualization("VCO 2", vco2), use_container_width=True)
                st.plotly_chart(create_knob_visualization("VCF DECAY", vcf_decay), use_container_width=True)

            with knob_col3:
                st.plotly_chart(create_knob_visualization("NOISE", noise, color="#ff6b6b"), use_container_width=True)
                st.plotly_chart(create_knob_visualization("VCF EG", vcf_eg, color="#6b6bff"), use_container_width=True)

        # Step Sequencer
        st.markdown("### 🎼 Program Your Pattern")
        st.markdown("*Click steps to activate them in your pattern:*")

        step_cols = st.columns(8)
        for i, col in enumerate(step_cols):
            with col:
                if st.button(f"{i+1}", key=f"kick_step_{i}", use_container_width=True,
                            type="primary" if i % 4 == 0 else "secondary"):
                    st.session_state.step_pattern[i] = not st.session_state.step_pattern[i]

                # Visual indicator
                if st.session_state.step_pattern[i]:
                    st.markdown(f"<div class='success-badge'>ON</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height: 29px;'></div>", unsafe_allow_html=True)

        # Play button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶️ PLAY PATTERN", type="primary", use_container_width=True, key="play_kick"):
                placeholder = st.empty()
                progress_bar = st.progress(0)

                for cycle in range(2):  # Play pattern twice
                    for i in range(8):
                        if st.session_state.step_pattern[i]:
                            placeholder.success(f"🥁 **KICK** - Step {i+1}")
                        else:
                            placeholder.info(f"➖ Silent - Step {i+1}")

                        progress_bar.progress((i + 1) / 8)
                        time.sleep(0.125)  # 120 BPM

                placeholder.success("✅ Pattern complete!")

        # Preset variations
        st.markdown("### 🎨 Preset Variations")

        var_col1, var_col2, var_col3 = st.columns(3)

        with var_col1:
            with st.expander("808 Sub Kick"):
                st.code("""
VCO 1: 10
VCO 2: 12
VCO DECAY: 50
NOISE: 5
VCF DECAY: 45
VCF EG: 40
                """)

        with var_col2:
            with st.expander("Punchy Techno"):
                st.code("""
VCO 1: 25
VCO 2: 40
VCO DECAY: 15
NOISE: 20
VCF DECAY: 20
VCF EG: 75
                """)

        with var_col3:
            with st.expander("Boomy House"):
                st.code("""
VCO 1: 18
VCO 2: 22
VCO DECAY: 40
NOISE: 8
VCF DECAY: 50
VCF EG: 55
                """)

        # Completion tracking
        if st.button("✅ Complete Kick Drum Lesson", use_container_width=True):
            st.session_state.progress['dfam_kick'] = {'completed': True, 'timestamp': datetime.now()}
            st.balloons()
            st.success("🎉 Excellent! You've mastered the DFAM kick drum!")

    with tab2:
        st.markdown("### 🥁 Creating a Snare")
        st.info("Snares need higher frequencies and more noise than kicks")
        st.markdown("*Coming soon: Interactive snare drum programming lesson*")

    with tab3:
        st.markdown("### 🎩 Hi-Hat Synthesis")
        st.info("Use metallic noise and fast envelopes for crisp hi-hats")
        st.markdown("*Coming soon: Hi-hat programming techniques*")

    with tab4:
        st.markdown("### 🎼 Full Drum Pattern")
        st.info("Combine all elements into a complete rhythm")
        st.markdown("*Coming soon: Complete pattern composition*")

elif "Mother-32 Synthesis" in learning_mode:
    st.markdown("## 🎹 Mother-32: Subtractive Synthesis Fundamentals")

    tabs = st.tabs(["🔊 Oscillator", "🎚️ Filter", "📈 Envelope", "🔌 Patching", "📝 Quiz"])

    with tabs[0]:
        st.markdown("### Understanding the Oscillator")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### Controls")

            waveform = st.radio("WAVEFORM", ["SAW", "PULSE"], horizontal=True)
            frequency = st.slider("FREQUENCY", -5.0, 5.0, 0.0, 0.1, help="Octave tuning")

            if waveform == "PULSE":
                pulse_width = st.slider("PULSE WIDTH", 0, 100, 50)
            else:
                pulse_width = 50

            mix_level = st.slider("MIX LEVEL", 0, 100, 75)

        with col2:
            st.markdown("#### Waveform Display")
            fig = create_waveform_display(
                waveform_type=waveform.lower(),
                frequency=2**(frequency/12),
                pulse_width=pulse_width
            )
            st.plotly_chart(fig, use_container_width=True)

            # Educational info
            if waveform == "SAW":
                st.success("**Saw Wave:** Contains all harmonics, bright and buzzy. Perfect for bass and leads!")
            else:
                st.info("**Pulse Wave:** Hollow, woody character. Narrow = nasal, Wide = hollow")

    with tabs[1]:
        st.markdown("### The Filter Section")

        col1, col2 = st.columns([1, 1])

        with col1:
            cutoff = st.slider("CUTOFF", 0, 100, 50, help="Frequency where filtering begins")
            resonance = st.slider("RESONANCE", 0, 100, 30, help="Emphasis at cutoff")
            eg_amount = st.slider("EG AMOUNT", -100, 100, 50, help="Envelope modulation")

        with col2:
            st.markdown("#### Filter Response")
            fig = create_filter_response(cutoff, resonance)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.markdown("### Envelope Generator (ADSR)")

        col1, col2 = st.columns([1, 1])

        with col1:
            attack = st.slider("ATTACK", 0, 100, 10, help="Time to reach maximum")
            decay = st.slider("DECAY", 0, 100, 30, help="Time to reach sustain")
            sustain = st.slider("SUSTAIN", 0, 100, 70, help="Level while held")
            release = st.slider("RELEASE", 0, 100, 40, help="Time to silence")

        with col2:
            st.markdown("#### Envelope Shape")
            fig = create_envelope_visualization(attack, decay, sustain, release)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        st.markdown("### Patch Bay Basics")

        # Simple patch visualization
        st.markdown("""
<div class='module-card'>
    <h4>Common Patches to Try:</h4>
    <ul>
        <li><b>LFO → VCO:</b> Creates vibrato (pitch wobble)</li>
        <li><b>EG → VCF:</b> Filter envelope (classic synth sweep)</li>
        <li><b>LFO → VCF:</b> Filter wobble (dubstep bass)</li>
        <li><b>MULT → Everything:</b> Split one signal to multiple destinations</li>
    </ul>
</div>
        """, unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("### Knowledge Check")

        q1 = st.radio(
            "What does the filter CUTOFF control?",
            ["Volume", "Frequency where filtering begins", "Waveform shape", "Pitch"],
            key="quiz_q1"
        )

        q2 = st.radio(
            "Which waveform contains all harmonics?",
            ["Sine", "Triangle", "Saw", "Pulse"],
            key="quiz_q2"
        )

        if st.button("Check Answers", key="check_quiz"):
            score = 0
            if q1 == "Frequency where filtering begins":
                st.success("✅ Q1 Correct!")
                score += 1
            else:
                st.error("❌ Q1: Cutoff controls where filtering begins")

            if q2 == "Saw":
                st.success("✅ Q2 Correct!")
                score += 1
            else:
                st.error("❌ Q2: Saw waves contain all harmonics")

            st.info(f"Score: {score}/2")

            if score == 2:
                st.balloons()
                st.session_state.progress['mother32_quiz'] = {'completed': True}

elif "Polyrhythms" in learning_mode:
    st.markdown("## 🌊 Subharmonicon: Polyrhythmic Magic")

    st.info("The Subharmonicon creates complex rhythms using mathematical relationships")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Rhythm Generators")

        rg1 = st.slider("Rhythm Gen 1 Division", 1, 16, 4, help="Divides the master tempo")
        rg2 = st.slider("Rhythm Gen 2 Division", 1, 16, 3, help="Creates polyrhythm against RG1")
        rg3 = st.slider("Rhythm Gen 3 Division", 1, 16, 5, help="Adds complexity")
        rg4 = st.slider("Rhythm Gen 4 Division", 1, 16, 7, help="Maximum rhythmic interest")

        tempo = st.slider("TEMPO (BPM)", 60, 180, 120)

    with col2:
        st.markdown("### Polyrhythm Visualization")

        # Create polyrhythm pattern visualization
        fig = go.Figure()

        # Calculate pattern
        pattern_length = 16
        colors = ['#ff6b6b', '#6b6bff', '#6bff6b', '#ffff6b']

        for i, (rg, color) in enumerate(zip([rg1, rg2, rg3, rg4], colors)):
            beats = [j for j in range(pattern_length) if j % rg == 0]
            y_pos = 3 - i

            fig.add_trace(go.Scatter(
                x=beats,
                y=[y_pos] * len(beats),
                mode='markers',
                marker=dict(size=15, color=color),
                name=f'RG{i+1}'
            ))

        fig.update_layout(
            height=300,
            xaxis=dict(
                range=[-0.5, pattern_length-0.5],
                gridcolor='rgba(255,255,255,0.2)',
                title="Steps",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                range=[-0.5, 4.5],
                showticklabels=False,
                gridcolor='rgba(255,255,255,0.1)'
            ),
            plot_bgcolor='rgba(0,0,0,0.2)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(font=dict(color='white'))
        )

        st.plotly_chart(fig, use_container_width=True)

    # Subharmonic section
    st.markdown("### Subharmonic Oscillators")

    sub_col1, sub_col2, sub_col3, sub_col4 = st.columns(4)

    with sub_col1:
        vco1_sub1 = st.select_slider("VCO1 SUB1", options=[1, 2, 3, 4, 5, 6, 7, 8], value=2)
    with sub_col2:
        vco1_sub2 = st.select_slider("VCO1 SUB2", options=[1, 2, 3, 4, 5, 6, 7, 8], value=3)
    with sub_col3:
        vco2_sub1 = st.select_slider("VCO2 SUB1", options=[1, 2, 3, 4, 5, 6, 7, 8], value=4)
    with sub_col4:
        vco2_sub2 = st.select_slider("VCO2 SUB2", options=[1, 2, 3, 4, 5, 6, 7, 8], value=5)

    st.info(f"""
**Current Harmonic Series:**
- Base Frequency: 100 Hz (example)
- VCO1 SUB1: {100/vco1_sub1:.1f} Hz (÷{vco1_sub1})
- VCO1 SUB2: {100/vco1_sub2:.1f} Hz (÷{vco1_sub2})
- VCO2 SUB1: {100/vco2_sub1:.1f} Hz (÷{vco2_sub1})
- VCO2 SUB2: {100/vco2_sub2:.1f} Hz (÷{vco2_sub2})

These mathematical relationships create harmonically rich, musical intervals!
    """)

elif "Analog Four" in learning_mode:
    st.markdown("## 🎼 Analog Four: Advanced Sequencing")

    st.info("Master parameter locks, probability, and the Elektron workflow")

    # Elektron sequencer interface mockup
    st.markdown("### Step Sequencer with Parameter Locks")

    # Create 16-step grid
    for row in range(4):
        cols = st.columns(4)
        for col_idx, col in enumerate(cols):
            step_num = row * 4 + col_idx + 1
            with col:
                if st.button(f"Step {step_num}", key=f"a4_step_{step_num}", use_container_width=True):
                    st.session_state[f'a4_step_{step_num}_active'] = not st.session_state.get(f'a4_step_{step_num}_active', False)

    st.markdown("### Parameter Locks")
    st.markdown("*Hold a step and turn knobs to lock parameters per-step*")

    selected_step = st.selectbox("Select step to edit:", range(1, 17))

    param_col1, param_col2, param_col3 = st.columns(3)

    with param_col1:
        step_pitch = st.slider(f"Step {selected_step} Pitch", -24, 24, 0)
        step_filter = st.slider(f"Step {selected_step} Filter", 0, 127, 64)

    with param_col2:
        step_resonance = st.slider(f"Step {selected_step} Resonance", 0, 127, 0)
        step_amp = st.slider(f"Step {selected_step} Amp", 0, 127, 100)

    with param_col3:
        step_probability = st.select_slider(
            f"Step {selected_step} Probability",
            options=["100%", "75%", "50%", "25%", "12.5%"],
            value="100%"
        )

    st.success(f"Step {selected_step} parameters locked! These values will play only on this step.")

elif "Sub 37" in learning_mode:
    st.markdown("## 🎨 Sub 37: Professional Sound Design")

    st.info("Two oscillators, ladder filter, and extensive modulation for rich patches")

    # Sub 37 interface
    tabs = st.tabs(["Oscillators", "Filter", "Envelopes", "Modulation", "Arpeggiator"])

    with tabs[0]:
        osc_col1, osc_col2 = st.columns(2)

        with osc_col1:
            st.markdown("### Oscillator 1")
            osc1_octave = st.select_slider("Octave", options=[16, 8, 4, 2], value=8)
            osc1_waveform = st.select_slider("Wave", options=["Tri", "Saw", "Square", "Pulse"])
            osc1_level = st.slider("Level", 0, 100, 50)

        with osc_col2:
            st.markdown("### Oscillator 2")
            osc2_octave = st.select_slider("Octave", options=[16, 8, 4, 2], value=4, key="osc2_oct")
            osc2_detune = st.slider("Detune", -7, 7, 0, help="Semitones from Osc 1")
            osc2_level = st.slider("Level", 0, 100, 50, key="osc2_lvl")

    with tabs[1]:
        st.markdown("### Ladder Filter")
        filter_cutoff = st.slider("Cutoff", 0, 127, 64)
        filter_res = st.slider("Resonance", 0, 127, 0)
        filter_eg_amt = st.slider("EG Amount", -127, 127, 0)
        filter_kb_track = st.slider("KB Track", 0, 100, 100, help="Keyboard tracking")
        multidrive = st.slider("Multidrive", 0, 127, 0, help="Pre-filter distortion")

    with tabs[2]:
        st.markdown("### Envelopes")
        st.info("Sub 37 has two envelopes: Filter and Amplitude")

    with tabs[3]:
        st.markdown("### Modulation")
        st.info("LFOs, modulation bus, and more")

    with tabs[4]:
        st.markdown("### Arpeggiator")
        st.info("Powerful arpeggiator with multiple patterns")

elif "Signal Flow" in learning_mode:
    st.markdown("## 🔊 Xone:96 Mixer: Signal Flow & FX")

    st.info("Understanding signal routing, EQ, and effects sends")

    # Mixer channel strip
    st.markdown("### Channel Strip Signal Flow")

    ch_col1, ch_col2, ch_col3 = st.columns([1, 2, 1])

    with ch_col2:
        st.markdown("""
<div class='module-card' style='text-align: center;'>
    <h4>Signal Path:</h4>
    <p>⬇️ INPUT (Line/Phono)</p>
    <p>⬇️ GAIN</p>
    <p>⬇️ HIGH EQ</p>
    <p>⬇️ MID EQ</p>
    <p>⬇️ LOW EQ</p>
    <p>⬇️ FILTER (HPF/LPF)</p>
    <p>⬇️ FX SEND 1</p>
    <p>⬇️ FX SEND 2</p>
    <p>⬇️ CHANNEL FADER</p>
    <p>⬇️ CROSSFADER (optional)</p>
    <p>⬇️ MASTER OUTPUT</p>
</div>
        """, unsafe_allow_html=True)

    # EQ Section
    st.markdown("### 4-Band EQ")

    eq_col1, eq_col2, eq_col3, eq_col4 = st.columns(4)

    with eq_col1:
        hi_eq = st.slider("HIGH", -26, 6, 0, help="10 kHz shelf")
    with eq_col2:
        hi_mid_eq = st.slider("HI-MID", -26, 6, 0, help="2.5 kHz bell")
    with eq_col3:
        lo_mid_eq = st.slider("LO-MID", -26, 6, 0, help="250 Hz bell")
    with eq_col4:
        lo_eq = st.slider("LOW", -26, 6, 0, help="90 Hz shelf")

elif "Reference Library" in learning_mode:
    st.markdown("## 📚 Reference Library")

    ref_tabs = st.tabs(["📖 Manuals", "🎨 Patch Sheets", "💡 Tips", "🔍 Glossary"])

    with ref_tabs[0]:
        st.markdown("### Equipment Manuals")

        manual_col1, manual_col2 = st.columns(2)

        with manual_col1:
            st.markdown("""
**Moog Instruments:**
- 📘 DFAM Manual
- 📘 Mother-32 Manual
- 📘 Subharmonicon Manual
- 📘 Sub 37 Manual
            """)

        with manual_col2:
            st.markdown("""
**Elektron & Mixer:**
- 📘 Analog Four MKII Manual
- 📘 Analog Rytm MKII Manual
- 📘 Xone:96 Manual
            """)

    with ref_tabs[1]:
        st.markdown("### Patch Sheet Library")

        # Display saved patches
        if st.session_state.patches_library:
            for patch in st.session_state.patches_library:
                with st.expander(f"📋 {patch.get('name', 'Untitled')}"):
                    st.json(patch)
        else:
            st.info("No saved patches yet. Create and save patches from the learning modules!")

    with ref_tabs[2]:
        st.markdown("### Pro Tips")

        with st.expander("🎯 DFAM Tips"):
            st.markdown("""
- Start with VCO DECAY around 30 for punchy drums
- Add 10-20% noise for realistic drum attacks
- Use VCF EG AMOUNT to control brightness over time
- Patch VELOCITY out to VCA CV for dynamics
            """)

        with st.expander("🎹 Mother-32 Tips"):
            st.markdown("""
- LFO to VCO creates vibrato; to VCF creates wobble
- Use GLIDE for portamento between notes
- VC MIX can be an extra VCA or ring modulator
- MULT duplicates any signal to multiple destinations
            """)

        with st.expander("🌊 Subharmonicon Tips"):
            st.markdown("""
- Start with simple polyrhythm ratios (3:4, 5:4)
- Use subharmonics to create chord progressions
- Patch rhythm outs to other gear for complex clocking
- Quantizer helps keep everything in tune
            """)

    with ref_tabs[3]:
        st.markdown("### Synthesis Glossary")

        glossary = {
            "ADSR": "Attack, Decay, Sustain, Release - envelope stages",
            "Cutoff": "Frequency where filter begins attenuating",
            "CV": "Control Voltage - analog parameter control",
            "Envelope": "Time-based modulation shape",
            "Filter": "Removes frequencies from a signal",
            "Gate": "On/off signal for triggering envelopes",
            "LFO": "Low Frequency Oscillator for modulation",
            "Oscillator": "Sound source generating waveforms",
            "Patch": "Cable connection or saved sound",
            "Resonance": "Emphasis at filter cutoff frequency",
            "Sequencer": "Pattern-based note/parameter recorder",
            "VCA": "Voltage Controlled Amplifier",
            "VCF": "Voltage Controlled Filter",
            "VCO": "Voltage Controlled Oscillator"
        }

        search_term = st.text_input("Search glossary:")

        for term, definition in glossary.items():
            if not search_term or search_term.lower() in term.lower():
                st.markdown(f"**{term}:** {definition}")

# Footer with session summary
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 Session Progress")
    if st.session_state.session_start:
        elapsed = datetime.now() - st.session_state.session_start
        st.info(f"Session time: {str(elapsed).split('.')[0]}")
    else:
        st.info("Session not started")

with col2:
    st.markdown("### 🎯 Today's Goal")
    st.success("Complete 3 lessons ✓")

with col3:
    st.markdown("### 🏆 Next Achievement")
    st.info("5 more lessons to unlock 'Synthesis Master' badge!")

# Hidden debug info
with st.expander("🔧 Debug Info", expanded=False):
    st.json({
        "session_state": {
            "progress_count": len(st.session_state.progress),
            "current_patch": st.session_state.current_patch,
            "patches_saved": len(st.session_state.patches_library)
        }
    })
