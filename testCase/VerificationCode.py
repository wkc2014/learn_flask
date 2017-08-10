# encoding: utf-8

"""
@author: wangkunchun
@file: VerificationCode.py
@time: 2017/8/7 21:42
"""

import string, random
import Image, ImageFont, ImageDraw


def func():
    code_num = 6
    source = list(string.letters)
    for index in range(0, 10):
        source.append(str(index))
    code = ''.join(random.sample(source, code_num))

    print code

    # 设置图片大小
    width = 45 * 6
    height = 50
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 选择字体
    font = ImageFont.truetype('Arial.ttf', 36)
    draw = ImageDraw.Draw(image)

    for x in range(width):
        for y in range(height):
            colorRandom1 = (random.randint(255, 255), random.randint(255, 255), random.randint(255, 255))
            draw.point((x, y), fill=colorRandom1)

        for t in range(code_num):
            colorRandom2 = (random.randint(85, 155), random.randint(85, 155), random.randint(85, 155))
            draw.text((45 * t + 25, 10), code[t], font=font, fill=colorRandom2)
    image_d = ImageDraw.Draw(image)
    for i in range(5):
        colorRandom3 = (random.randint(85, 100), random.randint(85, 100), random.randint(85, 100))
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        image_d.line([begin, end], fill=colorRandom3)


if __name__ == '__main__':
    func()
