# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Show the progress through the year with text and a progress bar.

Copy epilogue18.bdf into fonts/ on your CIRCUITPY drive.

"""
import time
from adafruit_magtag.magtag import MagTag
from adafruit_progressbar import ProgressBar
import rtc

time.sleep(4)


def days_in_year(date_obj):
    # check for leap year
    if date_obj.tm_year % 4 == 0:
        return 366
    return 365


def text_transform(val):
    return "{:.2f}%".format(val)


magtag = MagTag()

magtag.network.connect()

magtag.add_text(
    text_font="fonts/epilogue18.bdf",
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        50,
    ),
    text_scale=1,
    text_transform=text_transform,
    text_anchor_point=(0.5, 0.5),
    is_data=False,
)

top_lbl_txt = "Year Progress:"
magtag.add_text(
    text_font="fonts/epilogue18.bdf",
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        24,
    ),
    text_scale=1,
    text_transform=text_transform,
    text_anchor_point=(0.5, 0.5),
    is_data=False,
)

magtag.set_text(top_lbl_txt, index=1)

# set progress bar width and height relative to board's display
BAR_WIDTH = magtag.graphics.display.width - 80
BAR_HEIGHT = 30

BAR_X = magtag.graphics.display.width // 2 - BAR_WIDTH // 2
BAR_Y = 80

# Create a new progress_bar object at (x, y)
progress_bar = ProgressBar(
    BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT, 1.0, bar_color=0x999999, outline_color=0x000000
)

magtag.graphics.splash.append(progress_bar)

timestamp = None

time.sleep(5)

while True:
    try:
        magtag.network.get_local_time()
        now = rtc.RTC().datetime
        progress_bar.progress = now.tm_yday / days_in_year(now)
        magtag.set_text(
            text_transform(now.tm_yday / days_in_year(now) * 100.0), index=0
        )

        print(now)
        time.sleep(24 * 60 * 60)  # one day
        # We will use deep sleep once it's available in CircuitPython.

    except (ValueError, RuntimeError) as e:
        print("Some error occurred, retrying! -", e)
        time.sleep(60)  # one  minute
