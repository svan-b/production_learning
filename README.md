# 🎛️ Synth Studio Quick Reference & Patch Library

A **simple, practical, offline-capable** reference tool for your synthesizer studio. No fluff, no fantasy features - just real specifications, patch management, and links to actual resources.

## What This Actually Is

A single HTML file you can:
- Open in any browser (works offline)
- Bookmark for instant access
- Print for studio reference
- Use to save and organize your patches locally

## Equipment Covered (With Real Specs)

Based on official manuals and community resources:

- **🥁 Moog DFAM** - Actual parameter ranges, drum recipes
- **🎹 Moog Mother-32** - Real oscillator/filter specs, common patches
- **🌊 Moog Subharmonicon** - Polyrhythm system, subharmonic divisions
- **🎼 Elektron Analog Four MKII** - Parameter lock workflow
- **🎨 Moog Sub 37** - Specifications (based on Subsequent 37 info)
- **🔊 Allen & Heath Xone:96** - Actual EQ ranges and signal flow

## Features

### ✅ Quick Reference Sheets
- Real parameter ranges from official manuals
- Actual drum/bass/lead recipes
- Signal flow diagrams
- EQ specifications

### ✅ Patch Library
- Save patches locally (browser localStorage)
- Export/import patches as JSON
- Organize by synth and category
- Add notes and settings

### ✅ Learning Resources
- Links to official manuals (PDF)
- Community patch libraries (516+ DFAM patches, etc.)
- Actual learning tools (Syntorial, Patch Deck)
- Printable cheat sheets

### ✅ Full Specifications
- Sourced from official documentation
- Real numbers and ranges
- No guesswork or fantasy specs

## How to Use

### Option 1: Just Open It
```bash
# Open index.html in your browser
# Works immediately, no installation
open index.html  # Mac
start index.html # Windows
xdg-open index.html # Linux
```

### Option 2: Local Server (Optional)
```bash
# If you want a local server
python3 -m http.server 8000
# Then open: http://localhost:8000
```

### Option 3: Deploy to GitHub Pages (Free Hosting)
```bash
# Your HTML file is already in the repo
# Just enable GitHub Pages in repo settings
# Settings → Pages → Source: Branch (main/claude branch) → / (root)
# Your URL will be: https://yourusername.github.io/production_learning/
```

## Data Sources

All specifications sourced from:

### Official Manuals
- [DFAM Manual (PDF)](https://api.moogmusic.com/sites/default/files/2018-04/DFAM_Manual.pdf)
- [Mother-32 Manual (PDF)](https://api.moogmusic.com/sites/default/files/2018-01/Mother_32_Manual.pdf)
- [Xone:96 Resources](https://www.allen-heath.com/hardware/xone-series/xone96/)
- [Analog Four MKII Manual](https://www.manualslib.com/manual/1604467/Elektron-Analog-Four-Mkii.html)

### Community Patch Libraries
- [DFAM Patch Library](https://patch-library.net/patches?device=moog-dfam) - 516 community patches
- [Mother-32 Patch Library](https://patch-library.net/patches?device=moog-mother-32)
- [Subharmonicon Patches](https://moogsubharmoniconpatches.com/) - Dedicated library with audio samples
- [SynthLib](https://synthlib.com/) - Multi-synth library

### Learning Resources
- [Syntorial](https://www.syntorial.com/) - Ear training for synthesis
- [Patch Deck](https://www.patchdeck.cards/) - Modular patch idea cards
- [Synth Modes](https://synthmodes.com/) - Mobile-friendly cheat sheets
- [Synthesizer Cheat Sheet (PDF)](https://mastering.com/wp-content/uploads/2019/06/Synthesizer-Cheat.pdf)
- [Analog Four Course by Thavius Beck](https://ask.video/course/elektron-102-analog-four-explained-and-explored)

## Why This Approach?

After researching actual synthesizer learning methods and professional workflows, here's what actually works:

1. **Patch Sheets** - Document what works (like David Sparks notebooks)
2. **Quick Reference** - Real specs at your fingertips
3. **Community Resources** - 516+ real DFAM patches exist already
4. **Simple Tools** - One HTML file beats complex apps
5. **Offline Access** - No internet needed once downloaded

## Actual Workflows Supported

### DFAM Drum Programming
Based on [Sound on Sound review](https://www.soundonsound.com/reviews/moog-dfam) and community patches:
- Quick kick drum recipe (VCO1: 10-20, Noise: 10-15%)
- Snare settings (VCO1: 40-60, Noise: 60-80%)
- Real parameter ranges from manual

### Mother-32 Patching
Based on [official manual specs](https://api.moogmusic.com/sites/default/files/2018-01/Mother_32_Manual.pdf):
- LFO actual range: 0.1 - 600 Hz
- Filter cutoff: 17Hz - 21.5kHz (measured)
- Envelope times: 1.25ms - 7000ms (actual specs)

### Elektron Parameter Locks
From [official manual](https://www.manualslib.com/manual/1604467/Elektron-Analog-Four-Mkii.html):
- Hold TRIG + turn knobs (actual workflow)
- Grid recording mode
- Conditional trigs: 100%, 75%, 50%, 25%, 12.5%

### Xone:96 EQ Settings
From [official specs](https://www.allen-heath.com/hardware/xone-series/xone96/):
- CH 1-4: +6dB/-∞ (HI/LO), +10dB/-27dB (MID)
- CH A/B: +6dB/-∞ (HI/LO), +10dB/-24dB (swept MID)
- Actual signal flow documented

## What This Doesn't Do

❌ No fantasy "interactive knobs" that don't match real hardware
❌ No made-up parameter values
❌ No complex installation or dependencies
❌ No subscription or cloud service
❌ No "AI-generated patches" nonsense

## What It Actually Does

✅ Provides real specifications from official sources
✅ Links to 516+ actual community patches
✅ Saves your patches locally
✅ Works offline
✅ Prints for studio reference
✅ One HTML file - that's it

## Advanced Usage

### Export Your Patches
Click "Export All Patches" to get a JSON file of your saved patches. Back it up, share it, or import it on another device.

### Print Reference Sheets
Click the print button or use Ctrl/Cmd+P. The CSS is optimized for printing clean reference sheets.

### Customize for Your Setup
Edit the HTML file to add your own notes, remove equipment you don't have, or add custom sections.

## Contributing Your Patches

If you create great patches, consider sharing them:
- [DFAM Patch Library](https://patch-library.net/patches?device=moog-dfam)
- [Mother-32 Patch Library](https://patch-library.net/patches?device=moog-mother-32)
- [Subharmonicon Patches](https://moogsubharmoniconpatches.com/)

## Technical Notes

- Uses browser localStorage for patch saving
- No server required
- Works on mobile (responsive design)
- Print-optimized CSS
- No external dependencies
- Pure HTML/CSS/JavaScript

## Sources & Attribution

All specifications verified against:
- Official Moog manuals
- Allen & Heath official documentation
- Elektron user manuals
- Sound on Sound reviews
- Community patch libraries

Links provided to all sources in the Resources tab.

## License

This is a reference tool. All synthesizer specifications and trademarks belong to their respective manufacturers (Moog Music Inc., Elektron, Allen & Heath).

---

**This tool is grounded in reality.** Every specification comes from official documentation or verified community sources. No fantasy features, just practical reference material and patch management for actual synthesizers.

Open `index.html` and start documenting your studio work.
