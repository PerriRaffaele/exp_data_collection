from pytamaro import *

gold = rgb_color(255, 204, 0);

def german_flag(width: float) -> Graphic:
    return above(
        rectangle(width, width/3, black),
        above(
            rectangle(width, width/3, red),
            rectangle(width, width/3, gold)
        )
    )

italian_green = rgb_color(0, 140, 69)
italian_white = rgb_color(244, 245, 240)
italian_red = rgb_color(205, 33, 42)

def italian_flag(height: float) -> Graphic:
    return beside(
        rectangle(height/3, height, italian_green),
        beside(
            rectangle(height/3, height, italian_white),
            rectangle(height/3, height, italian_red)
        )
    )

french_blue = rgb_color(0, 85, 164)
french_red = rgb_color(239, 65, 53)

def french_flag(height: float) -> Graphic:
    return beside(
        rectangle(height/3, height, french_blue),
        beside(
            rectangle(height/3, height, white),
            rectangle(height/3, height, french_red)
        )
    )

show_graphic(german_flag(300))
show_graphic(italian_flag(300))
show_graphic(french_flag(300))
