from src.ji.consonance import euler_dissonance, vogel_dissonance, gill_purves_dissonance

CORBERT_FILENAME = "static/font/Corbert-Regular.ttf"


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class Colors:
    LIGHT_BLUE = hex_to_rgb("#1bb9d7")
    GRASS_GREEN = hex_to_rgb("#7ed957")
    ORANGE = hex_to_rgb("#ff914d")
    YELLOW = hex_to_rgb("#ffde59")


DISSONANCE_FUNCTION_NAMES = {
    euler_dissonance: "Euler",
    vogel_dissonance: "Vogel",
    gill_purves_dissonance: "Gill-Purves",
}
