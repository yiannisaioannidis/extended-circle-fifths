# Extended Circle of Fifths Visualizer

An interactive Python application that visualizes the extended circle of fifths with chord transformation capabilities. Perfect for musicians, music students, and composers to explore harmonic relationships.

## Features

- **24-Chord Extended Circle**: Includes all major and relative minor keys
- **Interactive Chord Selection**: Click to create chord progressions
- **Transformations**: Mirror across horizontal, vertical, and diagonal axes
- **Rotation**: Transpose entire progressions clockwise or counterclockwise
- **Drag & Drop**: Adjust chord positions manually with drag mode
- **Visual Feedback**: Real-time display of selected and transformed chords

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation Methods

Choose the installation method that works best for you:

### Method 1: Using Virtual Environment (Recommended for Most Users)

This method creates an isolated Python environment to prevent conflicts with other projects.

```bash
# 1. Download or clone this repository
git clone https://github.com/your-username/circle-of-fifths-visualizer.git
cd circle-of-fifths-visualizer

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install required packages
pip install -r requirements.txt

# 5. Run the application
python circle_of_fifths.py

# 6. When finished, deactivate the environment
deactivate

```
### Method 2: Direct Installation

```bash
# 1. Download or clone this repository

# 2. Install dependencies directly
pip install numpy matplotlib

# 3. Run the application
python circle_of_fifths.py
