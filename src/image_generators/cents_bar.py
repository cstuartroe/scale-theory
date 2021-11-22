from PIL import Image, ImageFont, ImageDraw

from .utils import CORBERT_FILENAME


def cents_bar_infographic(top_intervals, bottom_intervals=None, total_cents=1200):
    bar_width = 2400
    side_padding = 200
    vertical_line_height = 80
    vertical_padding = 150
    image_height = vertical_padding*2 + 100

    img = Image.new('RGBA', (bar_width + 2*side_padding, image_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font_size = 45
    corbert_large = ImageFont.truetype(CORBERT_FILENAME, font_size)
    corbert_small = ImageFont.truetype(CORBERT_FILENAME, int(font_size*.6))

    draw.rectangle(
        xy=[
            side_padding,
            vertical_padding,
            bar_width + side_padding,
            image_height - vertical_padding,
        ],
        fill=(0, 0, 0, 0),
        outline="white",
        width=5,
    )

    for label, interval in top_intervals or []:
        x = side_padding + round(interval.cents()*bar_width/total_cents)

        draw.text(
            xy=(x, vertical_padding - vertical_line_height),
            anchor="md",
            text=label,
            fill="white",
            font=corbert_large,
        )

        draw.text(
            xy=(x, vertical_padding - (vertical_line_height // 2)),
            anchor="md",
            text=f"{round(interval.cents())} cents",
            fill="white",
            font=corbert_small,
        )

        draw.line(
            xy=[
                x,
                vertical_padding - (vertical_line_height // 2),
                x,
                vertical_padding + (vertical_line_height // 2),
            ],
            fill="white",
            width=5,
        )

    for label, interval in bottom_intervals or []:
        x = side_padding + round(interval.cents()*bar_width/total_cents)

        draw.text(
            xy=(x, image_height - vertical_padding + (vertical_line_height // 2)),
            anchor="ma",
            text=f"{round(interval.cents())} cents",
            fill="white",
            font=corbert_small,
        )

        draw.text(
            xy=(x, image_height - vertical_padding + vertical_line_height),
            anchor="ma",
            text=label,
            fill="white",
            font=corbert_large,
        )

        draw.line(
            xy=[
                x,
                image_height - vertical_padding - (vertical_line_height // 2),
                x,
                image_height - vertical_padding + (vertical_line_height // 2),
            ],
            fill="white",
            width=5,
        )

    img.save(f"cents_bar.png")
