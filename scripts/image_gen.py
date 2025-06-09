import math
import os
import subprocess


def gen_favicon():
    paths = []

    image_size = 350
    center = image_size//2
    num_slices = 12
    outer_radius = 110
    inner_radius = 55
    slice_radians = 2*math.pi/num_slices

    for i, note in enumerate([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]):
        arc_center_radians = slice_radians*i - math.pi/2
        arc_start_radians = arc_center_radians - slice_radians / 2
        arc_end_radians = arc_center_radians + slice_radians / 2

        d = f"""
        M {center + outer_radius*math.cos(arc_start_radians)} {center + outer_radius*math.sin(arc_start_radians)}
        A {outer_radius} {outer_radius} 0 0 1 {center + outer_radius*math.cos(arc_end_radians)} {center + outer_radius*math.sin(arc_end_radians)}
        L {center + inner_radius*math.cos(arc_end_radians)} {center + inner_radius*math.sin(arc_end_radians)}
        A {inner_radius} {inner_radius} 0 0 0 {center + inner_radius*math.cos(arc_start_radians)} {center + inner_radius*math.sin(arc_start_radians)}
        Z
        """

        paths.append(f'<path d="{d}" stroke="black" stroke-width="1" fill="{"black" if note else "white"}"/>')

    headphone_inner_radius = 130
    headphone_outer_radius = 170
    headphone_side_radius = 50
    headphone_inner_angle = math.pi/8
    headphone_outer_angle = math.pi/18
    headphone_start_angle = 0
    headphone_under_angle = math.pi - 2*headphone_start_angle

    for i in range(2):
        outer_start_angle = headphone_start_angle - headphone_outer_angle + i*headphone_under_angle
        outer_end_angle = headphone_start_angle + headphone_outer_angle + i*headphone_under_angle
        inner_start_angle = headphone_start_angle - headphone_inner_angle + i*headphone_under_angle
        inner_end_angle = headphone_start_angle + headphone_inner_angle + i*headphone_under_angle

        d = f"""
        M {center + headphone_outer_radius*math.cos(outer_start_angle)} {center + headphone_outer_radius*math.sin(outer_start_angle)}
        A {headphone_outer_radius} {headphone_outer_radius} 0 0 1 {center + headphone_outer_radius*math.cos(outer_end_angle)} {center + headphone_outer_radius*math.sin(outer_end_angle)}
        A {headphone_side_radius} {headphone_side_radius} 0 0 1 {center + headphone_inner_radius*math.cos(inner_end_angle)} {center + headphone_inner_radius*math.sin(inner_end_angle)}
        L {center + headphone_inner_radius*math.cos(inner_start_angle)} {center + headphone_inner_radius*math.sin(inner_start_angle)}
        A {headphone_side_radius} {headphone_side_radius} 0 0 1 {center + headphone_outer_radius*math.cos(outer_start_angle)} {center + headphone_outer_radius*math.sin(outer_start_angle)}
        """

        paths.append(f'<path d="{d}" fill="black"/>')

    loop_inner_radius = (headphone_outer_radius + headphone_inner_radius)//2
    top_loop_d = f"""
    M {center + headphone_outer_radius*math.cos(headphone_start_angle + headphone_under_angle)} {center + headphone_outer_radius*math.sin(headphone_start_angle + headphone_under_angle)}
    A {headphone_outer_radius} {headphone_outer_radius} 0 0 1 {center + headphone_outer_radius*math.cos(headphone_start_angle)} {center + headphone_outer_radius*math.sin(headphone_start_angle)}
    L {center + loop_inner_radius*math.cos(headphone_start_angle)} {center + loop_inner_radius*math.sin(headphone_start_angle)}
    A {loop_inner_radius} {loop_inner_radius} 0 0 0 {center + loop_inner_radius*math.cos(headphone_start_angle + headphone_under_angle)} {center + loop_inner_radius*math.sin(headphone_start_angle + headphone_under_angle)}
    Z
    """
    paths.append(f'<path d="{top_loop_d}" fill="black"/>')

    content = (
        f'<svg width="{image_size}" height="{image_size}" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'
        f'  {'\n  '.join(paths)}\n'
        f'</svg>'
    )

    with open("src/img/favicon.svg", "w") as fh:
        fh.write(content)


if __name__ == "__main__":
    gen_favicon()

    for root, _, files in os.walk("src/img"):
        new_dir = root.replace("src", "static")
        os.makedirs(new_dir, exist_ok=True)
        for filename in files:
            if filename.endswith(".svg"):
                new_filename = filename.replace(".svg", ".png")
                subprocess.run(['/Applications/Inkscape.app/Contents/MacOS/inkscape', f'--export-filename={os.path.join(new_dir, new_filename)}', os.path.join(root, filename)])
