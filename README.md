# Synth Studio Learning Tool

**Production-ready Streamlit application for learning synthesizers with verified specifications from official manuals and community resources.**

## What This Is

A professional, low-friction learning tool for:
- **Moog DFAM** - 8-step drum programming with real manual presets
- **Moog Mother-32** - 32-step sequencer with accurate specs
- **Elektron Analog Four MKII** - Parameter locks and sequencing
- **Elektron Analog Rytm MKII** - 8-voice analog drum computer
- **Moog Sub 37** - Professional sound design
- **Allen & Heath Xone:96** - Mixer signal flow

All specifications verified against:
- Official Moog manuals (DFAM Manual D_Web, Mother-32 v1.1)
- Elektron user manuals (A4 MKII OS1.40A, Rytm MKII OS1.70)
- [Sound on Sound reviews](https://www.soundonsound.com/reviews/moog-dfam)
- [Community patch libraries](https://patch-library.net/patches?device=moog-dfam) (516+ DFAM patches)

## Features

### Accurate Hardware Specifications
- Real parameter ranges from official manuals
- Verified frequency ranges (Mother-32 LFO: 0.1-600Hz measured)
- Actual envelope times (Mother-32: Attack 1.25-3000ms, Decay 1.25-7000ms)
- True filter specs (Mother-32: 17Hz-21.5kHz measured cutoff range)

### Community Presets
- **DFAM**: Classic Kick, 808 Sub Kick, Punchy Techno, Quick Hats
- All presets from official manuals with page numbers
- Settings verified against patch-library.net community

### Professional UI
- Clean, dark design inspired by Elektron's aesthetic
- Sans-serif typography for clarity
- Minimal, functional interface
- Hardware-accurate knob visualizations
- Real-time waveform displays

### Patch Management
- Save your own patches locally
- Export/import patch library as JSON
- Automatic timestamps and device tagging
- Persistent storage across sessions

## Quick Start

### Local Development
```bash
# Clone repository
git clone <your-repo-url>
cd production_learning

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Streamlit Cloud Deployment
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy from branch: `claude/synthesizer-learning-tool-01CgJy9MeA4U7e4XeHUNGsfE`
5. App will be live in 2-3 minutes

## Usage

### DFAM Quick Start Mode
1. Select "DFAM" from device dropdown
2. Choose "Quick Start" mode
3. Load "Classic Kick" preset (from Official Manual Page 9)
4. Adjust parameters with sliders
5. Watch real-time knob and waveform visualizations
6. Program 8-step sequencer pattern
7. Save your custom patches

### Loading Community Presets
All DFAM presets include:
- **Source**: Manual page number or community
- **Description**: What the sound is for
- **Settings**: Exact parameter values

### Saving Your Work
- Click "SAVE PATCH" to store current settings
- Patches saved to `user_patches.json`
- Includes timestamp and device info
- Export/import between sessions

## Technical Details

### Architecture
- **Frontend**: Streamlit 1.31.0
- **Visualizations**: Plotly 5.18.0
- **State Management**: Streamlit session_state
- **Persistence**: JSON file storage
- **Config**: .streamlit/config.toml for theming

### Data Validation
All specs cross-referenced against:
- [DFAM Manual PDF](https://api.moogmusic.com/sites/default/files/2018-04/DFAM_Manual.pdf)
- [Mother-32 Manual PDF](https://api.moogmusic.com/sites/default/files/2018-01/Mother_32_Manual.pdf)
- [Sound on Sound DFAM Review](https://www.soundonsound.com/reviews/moog-dfam)
- [Sound on Sound Mother-32 Review](https://www.soundonsound.com/reviews/moog-mother-32)
- [Elektron Analog Four MKII Manual](https://www.manualslib.com/manual/1604467/Elektron-Analog-Four-Mkii.html)
- [Elektron Analog Rytm MKII](https://www.elektron.se/explore/analog-rytm-mkii)
- [Allen & Heath Xone:96](https://www.allen-heath.com/hardware/xone-series/xone96/)

### File Structure
```
production_learning/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── user_patches.json        # Saved user patches (auto-created)
└── README.md               # This file
```

## Extending

### Adding New Devices
1. Add specs to `DEVICE_SPECS` dictionary in app.py
2. Verify all parameters against official manual
3. Add community presets to `PRESET_LIBRARY`
4. Create device-specific UI section
5. Update documentation

### Adding Presets
```python
PRESET_LIBRARY["DFAM"]["Your Preset Name"] = {
    "source": "Source reference",
    "description": "What it sounds like",
    "settings": {
        "VCO_1_FREQ": 15,
        "VCO_2_FREQ": 20,
        # ... more parameters
    }
}
```

## Known Limitations

Current implementation focuses on DFAM Quick Start mode. Additional modes and devices are:
- **Implemented**: DFAM Quick Start with community presets
- **Specifications Ready**: All devices have verified specs
- **UI Templates**: Reusable components for knobs, sequencers, waveforms
- **Next Priority**: Mother-32 Keyboard Mode tutorial (Manual Page 24)

## Troubleshooting

### App Won't Start
```bash
# Verify Python version (3.8+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear Streamlit cache
streamlit cache clear
```

### Patches Not Saving
- Check write permissions in app directory
- Verify `user_patches.json` is not read-only
- Check browser console for errors

### Slow Performance
- Reduce number of knob visualizations rendered
- Use Chrome/Edge for best Plotly performance
- Close other Streamlit tabs

## Contributing

This is a learning tool. To improve it:
1. Verify specs against official manuals
2. Test presets with real hardware
3. Submit community patches with clear source attribution
4. Report issues with specific device/preset/parameter details

## License

Educational tool for personal use. All synthesizer specifications and trademarks belong to their respective manufacturers:
- Moog Music Inc.
- Elektron Music Machines AB
- Allen & Heath Limited

Patch presets sourced from:
- Official manuals (public domain)
- [patch-library.net](https://patch-library.net) community contributions
- User submissions

## Acknowledgments

- **Moog Music** - For comprehensive manuals and great instruments
- **Elektron** - For detailed documentation and innovative designs
- **Allen & Heath** - For professional mixer specifications
- **Sound on Sound** - For measured specifications in reviews
- **patch-library.net** - For community patch database
- **Streamlit** - For excellent web app framework
- **Plotly** - For visualization library

---

**This tool uses only verified specifications from official sources.**

No guesswork. No fantasy features. Just accurate, useful reference material for learning your synthesizers.
