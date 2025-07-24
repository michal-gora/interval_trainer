# 🎵 Interval Trainer

A command-line ear training tool for practicing musical intervals.
It plays ascending, descending, or harmonic intervals and quizzes you based on lesson presets.

For listening only — no looking required. 
Interval names are spoken aloud after each playback.
---

## 🎹 Features

- Supports different interval types (consonance, dissonance, etc.)
- Customizable playback formats: harmonic, melodic ascending/descending, mixed
- Spoken interval names using `espeak`
- Lesson selection via command-line
- Runs offline using a virtual environment

---

## 🧰 Requirements

- Python 3.7+
- `espeak` (for speech output, automatically installed in setup.sh script)
- Linux (Debian-based recommended)

Install `espeak` on Debian/Ubuntu (or let the setup.sh script install it for you):

```bash
sudo apt install espeak
```

---

## 🚀 Setup

1. Clone or download this repository.

2. Run the setup script (installs dependencies and optional `espeak`):

   ```bash
   ./setup.sh
   ```

   > This will create a virtual environment and install required Python packages.

3. Run a lesson:

   ```bash
   ./run.sh 1 -i piano
   ```

---

## 🧠 Usage

```bash
python3 main.py <lesson_number> [-i INSTRUMENT]
```

### Arguments:

- `<lesson_number>`: Choose a lesson (1–4)
- `-i, --instrument`: SCAMP instrument to use (default: `piano`)

---

## 📄 License

MIT License

Copyright (c) 2025 michal-gora

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
