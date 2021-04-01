from PIL import Image, ImageDraw

SIZES = {19: [45, 50], 13: [70, 40], 9: [105, 25]}


def draw(size):
    img = Image.new('RGBA', (1000, 1000), '#dfbd6d')
    idraw = ImageDraw.Draw(img)
    size_slot, padding = SIZES[size]
    for row in range(size):
        for col in range(size):
            idraw.rectangle((padding + size_slot * col,
                             padding + size_slot * row,
                             padding + size_slot + size_slot * col,
                             padding + size_slot + size_slot * row), outline='black', width=2)

    img.save('board.png')

