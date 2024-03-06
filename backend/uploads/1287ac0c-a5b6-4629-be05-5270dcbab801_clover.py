from pytamaro import *

LEAF_COLOR = rgb_color(51, 102, 45);

def semicircle(radius: float) -> Graphic:
    assert radius >= 0
    return circular_sector(radius, 180, LEAF_COLOR)

def leaf(size: float) -> Graphic:
    left_top = pin(bottom_left, semicircle(size))
    right_top = rotate(90, pin(bottom_right, semicircle(size)))
    bottom = pin(top_left, rectangle(size * 2, size * 2, LEAF_COLOR))
    return pin(bottom_center, rotate(-45, compose(right_top, compose(left_top, bottom))))

def stem(height: float) -> Graphic:
    return pin(top_center, rectangle(height/4, height*4, LEAF_COLOR));

def clover(leaf_radius: float, four_leaves: bool) -> Graphic:
    result = empty_graphic();
    num_leaves = 3 if not four_leaves else 4
    for i in range(num_leaves):
        result = compose(result, rotate((360/num_leaves) *i, leaf(leaf_radius)));
    return compose(
        stem(leaf_radius),
        result
    )
show_graphic(clover(50, True))