from PIL import Image, ImageFont, ImageDraw
import math

from .utils import euler_dissonance, CORBERT_FILENAME, Colors, DISSONANCE_FUNCTION_NAMES
from ..edo import MAJOR_EDOS, EDO
from ..ji import just_chords

CHORD_SIZE_NAMES = [
    None,
    None,
    "interval",
    "trichord",
    "tetrachord",
    "pentatonic",
]


def chords_with_dissonance(tones=3, dissonance_function=euler_dissonance, max_ratio=100):
    out = []

    for chord in just_chords(tones, max_ratio=max_ratio):
        out.append((chord, dissonance_function(chord)))

    out.sort(key=lambda x: x[1])
    return out


def intervals_infographic(notes=2, dissonance_function=euler_dissonance, min_to_describe=30, edos=MAJOR_EDOS):
    c_w_d = chords_with_dissonance(notes, dissonance_function=dissonance_function)

    _, max_dissonance = c_w_d[min_to_describe]
    num_to_describe = min_to_describe
    while c_w_d[num_to_describe][1] == max_dissonance:
        num_to_describe += 1
    intervals_to_describe = c_w_d[:num_to_describe]

    bumper_height = 80
    header_height = 300
    interval_block_height = 250 if (notes == 2) else 100
    image_height = 2*bumper_height + header_height + (interval_block_height * len(intervals_to_describe))
    edo_spacing = 150

    margin_width = 100
    image_width = edo_spacing*len(edos) + margin_width*2 if (notes == 2) else 1500

    img = Image.new('RGB', (image_width, image_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    corbert32 = ImageFont.truetype(CORBERT_FILENAME, 32)
    corbert48 = ImageFont.truetype(CORBERT_FILENAME, 48)
    corbert64 = ImageFont.truetype(CORBERT_FILENAME, 64)

    # bumpers

    draw.rectangle([0, 0, image_width, bumper_height], fill=Colors.LIGHT_BLUE)
    draw.rectangle([0, image_height - bumper_height, image_width, image_height], fill=Colors.LIGHT_BLUE)

    # header

    draw.text(
        xy=(image_width // 2, bumper_height + 20),
        anchor='ma',
        text=f"The {len(intervals_to_describe)} most consonant {CHORD_SIZE_NAMES[notes]}s",
        fill=(0, 0, 0),
        font=corbert64,
    )

    draw.multiline_text(
        xy=(image_width // 2, bumper_height + 110),
        anchor='ma',
        text=f"and their approximation error (in cents)\nin selected equal temperament tunings",
        fill=(0, 0, 0),
        font=corbert32,
        align='left',
    )

    # intervals info

    for i, (chord, dissonance) in enumerate(intervals_to_describe):
        block_y = bumper_height + header_height + (interval_block_height * i)

        # line

        circle_radius = 6

        draw.line(
            xy=[
                margin_width + circle_radius,
                block_y,
                image_width - margin_width - circle_radius,
                block_y,
            ],
            fill=(0, 0, 0),
            width=2,
        )

        draw.arc(
            xy=[
                margin_width - circle_radius,
                block_y - circle_radius,
                margin_width + circle_radius,
                block_y + circle_radius,
            ],
            start=0,
            end=360,
            fill=(0, 0, 0),
            width=2,
        )

        draw.arc(
            xy=[
                image_width - margin_width - circle_radius,
                block_y - circle_radius,
                image_width - margin_width + circle_radius,
                block_y + circle_radius,
            ],
            start=0,
            end=360,
            fill=(0, 0, 0),
            width=2,
        )

        # first row

        first_row_y = block_y + 0

        draw.text(
            xy=(margin_width, first_row_y),
            anchor='la',
            text=chord.name_with_inversion() or "",
            fill=(0, 0, 0),
            font=corbert32,
        )

        draw.text(
            xy=(image_width - margin_width, first_row_y),
            anchor='ra',
            text=f"{DISSONANCE_FUNCTION_NAMES[dissonance_function]} dissonance: {dissonance}",
            fill=(0, 0, 0),
            font=corbert32,
        )

        draw.text(
            xy=(image_width//2, first_row_y),
            anchor='ma',
            text=' : '.join(map(str, chord.ratio)),
            fill=(0, 0, 0),
            font=corbert48,
        )

        if notes > 2:
            continue

        # second row

        second_row_y = first_row_y + 80

        draw.text(
            xy=(image_width // 2, second_row_y),
            anchor='ma',
            text=', '.join(map(str, chord.cents())) + " cents",
            fill=(0, 0, 0),
            font=corbert32,
        )

        # third + fourth row

        third_row_y = second_row_y + 60

        fourth_row_y = third_row_y + 35

        for j, edo_steps in enumerate(edos):
            edo = EDO(edo_steps)

            edo_x = (image_width // 2) + (edo_spacing * (j - len(edos)/2 + .5))

            draw.text(
                xy=(edo_x, third_row_y),
                anchor='ma',
                text=f"{edo_steps}EDO",
                fill=(0, 0, 0),
                font=corbert32,
            )

            for tone in chord.intervals():
                error = round(edo.approximate(tone).cents() - tone.cents())
                if math.fabs(error) < 5.0:
                    color = Colors.GRASS_GREEN
                elif math.fabs(error) < 15.0:
                    color = Colors.YELLOW
                else:
                    color = Colors.ORANGE

                draw.text(
                    xy=(edo_x, fourth_row_y),
                    anchor='ma',
                    text=f"{'+' if error > 0 else ''}{error}",
                    fill=color,
                    font=corbert48,
                )

    img.save(f"{CHORD_SIZE_NAMES[notes]}s.png")
