#!/usr/bin/env python3

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CELL_WIDTH = 192
CELL_HEIGHT = 208

# name, row, frame count, milliseconds per frame
STATES = [
    ("idle",          0, 6, 140),
    ("running-right", 1, 8, 90),
    ("running-left",  2, 8, 90),
    ("waving",        3, 4, 140),
    ("jumping",       4, 5, 110),
    ("failed",        5, 8, 130),
    ("waiting",       6, 6, 170),
    ("running",       7, 6, 110),
    ("review",        8, 6, 150),
]

LABEL_HEIGHT = 24
BACKGROUND = (40, 44, 52, 255)


def crop_frame(sheet: Image.Image, row: int, column: int) -> Image.Image:
    left = column * CELL_WIDTH
    top = row * CELL_HEIGHT

    return sheet.crop((
        left,
        top,
        left + CELL_WIDTH,
        top + CELL_HEIGHT,
    ))


def render_preview_frame(
    sprite: Image.Image,
    state_name: str,
) -> Image.Image:
    canvas = Image.new(
        "RGBA",
        (CELL_WIDTH, CELL_HEIGHT + LABEL_HEIGHT),
        BACKGROUND,
    )

    canvas.alpha_composite(sprite, (0, LABEL_HEIGHT))

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((6, 6), state_name, fill="white", font=font)

    # Opaque background avoids GIF transparency/disposal artifacts.
    return canvas.convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spritesheet", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    sheet = Image.open(args.spritesheet).convert("RGBA")

    if sheet.width != 1536:
        raise ValueError(
            f"Unexpected width: {sheet.width}; expected 1536"
        )

    if sheet.height not in (1872, 2288):
        raise ValueError(
            f"Unexpected height: {sheet.height}; "
            "expected 1872 (v1) or 2288 (v2)"
        )

    frames: list[Image.Image] = []
    durations: list[int] = []

    for state_name, row, frame_count, frame_duration in STATES:
        for column in range(frame_count):
            sprite = crop_frame(sheet, row, column)
            frames.append(render_preview_frame(sprite, state_name))

            # Pause briefly when entering each state.
            duration = frame_duration
            if column == 0:
                duration += 400

            durations.append(duration)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=False,
    )


if __name__ == "__main__":
    main()