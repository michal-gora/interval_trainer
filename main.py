# MIT License
# Copyright (c) 2025 michal-gora
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import logging
logging.getLogger().setLevel(logging.ERROR)

import shutil
import sys

# Check if espeak is installed
if shutil.which("espeak") is None:
    print("❌ Error: 'espeak' is not installed on this system.")
    print("👉 Please install it (e.g., 'sudo apt install espeak') and try again.")
    sys.exit(1)


import subprocess
import time
import random
import argparse
from enum import Enum
from scamp import Session

session = Session()
instrument = None
# random.seed(42)

# ---------------- Enums ----------------

class IntervalStyle(Enum):
    HARMONIC = "harmonic"
    ASCENDING = "ascending"
    DESCENDING = "descending"

class PlaybackFormat(Enum):
    SINGLE_HARMONIC = "single_harmonic"
    SINGLE_ASCENDING = "single_ascending"
    SINGLE_DESCENDING = "single_descending"
    REPEAT_HARMONIC = "repeat_harmonic"
    REPEAT_ASCENDING = "repeat_ascending"
    REPEAT_DESCENDING = "repeat_descending"
    MIXED = "mixed"

class IntervalType(Enum):
    UNISON = 0
    MINOR_SECOND = 1
    MAJOR_SECOND = 2
    MINOR_THIRD = 3
    MAJOR_THIRD = 4
    PERFECT_FOURTH = 5
    TRITONE = 6
    PERFECT_FIFTH = 7
    MINOR_SIXTH = 8
    MAJOR_SIXTH = 9
    MINOR_SEVENTH = 10
    MAJOR_SEVENTH = 11
    OCTAVE = 12


# ---------------- Constants ----------------

INTERVAL_NAMES = {
    0: "Unison",
    1: "Minor second",
    2: "Major second",
    3: "Minor third",
    4: "Major third",
    5: "Perfect fourth",
    6: "Tritone",
    7: "Perfect fifth",
    8: "Minor sixth",
    9: "Major sixth",
    10: "Minor seventh",
    11: "Major seventh",
    12: "Octave"
}

perfect_consonance_intervals = [IntervalType.PERFECT_FOURTH, IntervalType.PERFECT_FIFTH, IntervalType.OCTAVE]
imperfect_consonance_intervals = [IntervalType.MINOR_THIRD, IntervalType.MAJOR_THIRD, IntervalType.MINOR_SIXTH, IntervalType.MAJOR_SIXTH]
soft_dissonance_intervals = [IntervalType.MAJOR_SECOND, IntervalType.MINOR_SEVENTH]
sharp_dissonance_intervals = [IntervalType.MINOR_SECOND, IntervalType.TRITONE, IntervalType.MAJOR_SEVENTH]

# ---------------- Utilities ----------------

def get_random_interval(allowed_intervals: list[IntervalType] = None):
    if allowed_intervals is None:
        allowed_intervals = list(IntervalType)

    interval_enum = random.choice(allowed_intervals)
    semitone_diff = interval_enum.value
    bottom_note = random.randint(48, 72)
    return bottom_note, semitone_diff


def speak(text: str):
    subprocess.run(["espeak", str(text)])

# ---------------- Core Functions ----------------

def play_interval(
    bottom_note: int,
    top_note: int,
    duration: float = 1.0,
    velocity: float = 1.0,
    style: IntervalStyle = IntervalStyle.HARMONIC,
    gap: float = 0.0
):
    if style == IntervalStyle.HARMONIC:
        instrument.play_chord([bottom_note, top_note], duration, velocity)
    elif style == IntervalStyle.ASCENDING:
        instrument.play_note(bottom_note, velocity, duration)
        session.wait(gap)
        instrument.play_note(top_note, velocity, duration)
    elif style == IntervalStyle.DESCENDING:
        instrument.play_note(top_note, velocity, duration)
        session.wait(gap)
        instrument.play_note(bottom_note, velocity, duration)
    else:
        raise ValueError(f"Unsupported style: {style}")

def play_random_interval(
    duration: float = 0.8,
    velocity: float = 1.0,
    pause_between_repeats: float = 1.0,
    pause_before_speak: float = 1.0,
    gap: float = 0.0,
    format: PlaybackFormat = PlaybackFormat.REPEAT_HARMONIC,
    allowed_intervals: list[IntervalType] = None  # Now using Enum
):
    bottom_note, semitone_diff = get_random_interval(allowed_intervals)
    top_note = bottom_note + semitone_diff

    format_to_styles = {
        PlaybackFormat.SINGLE_HARMONIC: [IntervalStyle.HARMONIC],
        PlaybackFormat.SINGLE_ASCENDING: [IntervalStyle.ASCENDING],
        PlaybackFormat.SINGLE_DESCENDING: [IntervalStyle.DESCENDING],
        PlaybackFormat.REPEAT_HARMONIC: [IntervalStyle.HARMONIC] * 3,
        PlaybackFormat.REPEAT_ASCENDING: [IntervalStyle.ASCENDING] * 3,
        PlaybackFormat.REPEAT_DESCENDING: [IntervalStyle.DESCENDING] * 3,
        PlaybackFormat.MIXED: [IntervalStyle.ASCENDING, IntervalStyle.DESCENDING, IntervalStyle.HARMONIC],
        PlaybackFormat.SINGLE_HARMONIC: [IntervalStyle.HARMONIC]
    }

    styles = format_to_styles.get(format)
    if styles is None:
        raise ValueError(f"Unknown playback format: {format}")

    for i, style in enumerate(styles):
        play_interval(
            bottom_note,
            top_note,
            style=style,
            duration=duration,
            velocity=velocity,
            gap=gap
        )
        if i < len(styles) - 1:
            session.wait(pause_between_repeats)

    session.wait(pause_before_speak)

    name = name = INTERVAL_NAMES.get(int(semitone_diff), f"{semitone_diff} semitones")

    print(name)
    speak(name)


# ---------------- Example Lesson ----------------

def simpletest(allowed_intervals = None):
    for _ in range(10):
        play_random_interval(format=PlaybackFormat.REPEAT_ASCENDING, allowed_intervals=allowed_intervals)
        session.wait(3.0)
    for _ in range(10):
        play_random_interval(format=PlaybackFormat.REPEAT_DESCENDING, allowed_intervals=allowed_intervals)
        session.wait(3.0)
    for _ in range(10):
        play_random_interval(format=PlaybackFormat.REPEAT_HARMONIC, allowed_intervals=allowed_intervals)
        session.wait(3.0)

def harmonictest(allowed_intervals = None):
    for _ in range(20):
        play_random_interval(format=PlaybackFormat.REPEAT_HARMONIC, allowed_intervals=allowed_intervals)
        session.wait(3.0)

def movingtest(allowed_intervals = None, format = PlaybackFormat.SINGLE_HARMONIC):
    for _ in range(20):
        play_random_interval(format=format, allowed_intervals=allowed_intervals)
        session.wait(3.0)

def lesson1():
    print("Lesson 1: Perfect Consonance")
    simpletest(perfect_consonance_intervals)

def lesson2():
    print("Lesson 2: Imperfect Consonance")
    simpletest(imperfect_consonance_intervals)

def lesson3():
    print("Lesson 3: Soft and Sharp Dissonance")
    simpletest(soft_dissonance_intervals + sharp_dissonance_intervals)

def lesson4():
    print("Lesson 4: All Intervals")
    simpletest(None)

def lesson5():
    print("Lesson 5: Only harmonic intervals")
    harmonictest(None)

def lesson6():
    print("Lesson 6: Only ascending intervals")
    movingtest(None, format=PlaybackFormat.SINGLE_ASCENDING)

def lesson7():
    print("Lesson 7: Only descending intervals")
    movingtest(None, format=PlaybackFormat.SINGLE_DESCENDING)

def lesson8():
    print("Lesson 8: Custom/Placeholder")
    harmonictest(None)

# ---------------- CLI Entry ----------------

class HelpfulArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f"\n❌ Error: {message}\n")
        sys.stderr.write("💡 Use -h or --help to see usage information.\n\n")
        # self.print_usage(sys.stderr)
        sys.exit(2)



if __name__ == "__main__":
    lesson_map = {
        1: lesson1,
        2: lesson2,
        3: lesson3,
        4: lesson4,
        5: lesson5,
        6: lesson6,
        7: lesson7,
        8: lesson8
    }

    parser = HelpfulArgumentParser(
        description=(
            "🎵 Interval Trainer // © 2025 michal-gora\n"
            "Train your ear by listening to ascending, descending, and harmonic intervals.\n"
            "The interval name is spoken aloud after each playback.\n\n"
            "Use -h or --help to see available options."
        ),
        usage=argparse.SUPPRESS,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
    "lesson",
    type=int,
    choices=range(1, len(lesson_map) + 1),
    nargs="?",  # 👈 makes it optional
    help="Lesson number to run (1–" + str(len(lesson_map)) + ")"
)

    parser.add_argument(
        "-i", "--instrument",
        type=str,
        default="piano",
        help="Choose which instrument to use (default: piano)"
    )
    
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List available lessons"
    )


    args = parser.parse_args()

    if args.list:
        print("🎵 Available Lessons:")
        print("  1: Perfect Consonance       - Perfect 4th, 5th, Octave")
        print("  2: Imperfect Consonance     - Minor/Major 3rds and 6ths")
        print("  3: Dissonance               - Minor 2nd, Tritone, Major 7th, etc.")
        print("  4: All Intervals            - Full set from Unison to Octave")
        print("  5: Harmonic Chords Only     - Full set from Unison to Octave, only harmonic chords")
        print("  6: Ascending Chords Only    - Full set from Unison to Octave, only ascending chords")
        print("  7: Descending Chords Only    - Full set from Unison to Octave, only descending chords")
        print("  8: Custom / Future Lesson   - Reserved for custom sets")
        sys.exit(0)

    ## If no argument passed
    if args.lesson is None:
        parser.print_help()
        sys.exit(1)

    instrument = session.new_part(args.instrument)

    try:
        print("❌ Press Ctrl+C at any time to exit.\n")
        selected_lesson = lesson_map.get(args.lesson)
        selected_lesson()
    except KeyboardInterrupt:
        print("\n👋 Exiting. Goodbye!")
