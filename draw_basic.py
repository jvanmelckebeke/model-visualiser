
def draw_rectangle(ctx, x, y, width, height, fill_color=(1, 1, 1), stroke_color=(0, 0, 0), stroke_width=1):
    ctx.rectangle(x, y, width, height)
    ctx.set_source_rgb(*fill_color)
    ctx.fill()
    ctx.set_source_rgb(*stroke_color)
    ctx.set_line_width(stroke_width)
    ctx.stroke()

    ctx.save()


def draw_text(ctx, x, y, text, align='left', color=(0, 0, 0), font_size=12):
    ctx.set_source_rgb(*color)
    ctx.set_font_size(font_size)
    if align == 'left':
        ctx.move_to(x, y)
    elif align == 'center':
        ctx.move_to(x - ctx.text_extents(text)[2] / 2, y)
    elif align == 'right':
        ctx.move_to(x - ctx.text_extents(text)[2], y)
    ctx.show_text(text)
    ctx.stroke()
    ctx.save()


def draw_annotated_rectangle(ctx, x, y, width, height, label, font_size=20, fill_color=(0.95, 0.95, 0.95),
                             stroke_color=(0, 0, 0), stroke_width=1, align_text_vertical='center'):
    draw_rectangle(ctx, x, y, width, height, fill_color, stroke_color, stroke_width)
    if align_text_vertical == 'center':
        draw_text(ctx, x + width / 2, y + height / 2, label, 'center', font_size=font_size)
    elif align_text_vertical == 'top':
        draw_text(ctx, x + width / 2, y + height / 2 - 15, label, 'center', font_size=font_size)
    elif align_text_vertical == 'bottom':
        draw_text(ctx, x + width / 2, y + height - 10, label, 'center', font_size=font_size)