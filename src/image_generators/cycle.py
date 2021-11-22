from PIL import Image, ImageDraw
import math

from src.scales import Mode
from src.edo import EDOInterval
from .utils import Colors


def mode_image(mode: Mode, fill: Colors = Colors.BLACK, background: Colors = Colors.TRANSPARENT):
    dot_radius = 10
    radius = (mode.edo_steps() * dot_radius)/2.5
    padding = dot_radius*2

    image_side = round((radius+padding)*2)

    img = Image.new('RGB', (image_side, image_side), color=background)
    draw = ImageDraw.Draw(img)

    step_angle = 2*math.pi/mode.edo_steps()
    for i in range(mode.edo().steps):
        center_x = image_side//2 + round(math.sin(step_angle*i)*radius)
        center_y = image_side//2 - round(math.cos(step_angle*i)*radius)

        xy = [
            center_x - dot_radius,
            center_y - dot_radius,
            center_x + dot_radius,
            center_y + dot_radius,
        ]

        draw.ellipse(
            xy=xy,
            fill=(fill if i == 0 or EDOInterval(i, mode.edo_steps()) in mode.intervals() else background),
            outline=Colors.BLACK,
            width=2
        )

    img.save(f"cycle {mode.edo_steps()}edo {mode.name()}.png")
