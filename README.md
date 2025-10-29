# Keyboard Visualizer

Visualize Vial keyboard layouts with web interface and CLI.

## Quick Start

### Web Interface (Easiest)
```bash
./start.sh
# Opens on http://localhost:9010
# Automatically handles port conflicts
```

### Alternative: Manual Start
```bash
source venv/bin/activate
python run_web.py
# Opens on http://localhost:5000
```

### Command Line
```bash
source venv/bin/activate
python cli.py input.vil output.png
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Features
- 🎮 **Interactive HTML visualization** - Click keys, switch layers with buttons or keyboard shortcuts
- 📋 **All-layers view** - Toggle to see all keyboard layers at once in a grid layout
- 📊 Multi-layer visualization with PNG export
- 🎨 Color-coded keys
- 🔄 Keycode transformation
- 📝 Comprehensive logging
- 🌐 Modern web interface + CLI
- 🚀 Auto-restart with port management
- ⌨️ **Keyboard shortcuts**: 0-9 for layers, arrow keys to navigate, 'A' to toggle all-layers view

