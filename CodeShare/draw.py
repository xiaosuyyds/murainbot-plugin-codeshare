# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/xiaosuyyds/murainbot-plugin-codeshare/blob/master/NOTICE

import uuid
import string
from PIL import ImageFont, Image, ImageDraw, ImageFilter
from power_text import *
from PowerBlur import rounded_rectangle
from power_text.local_emoji_source import LocalEmojiSource

from Lib.constants import *
from Lib import PluginConfig, Logger, common

logger = Logger.get_logger()

config = PluginConfig.PluginConfig(
    default_config="""# CodeShare插件配置文件
font:  # 字体相关，字体目录位于data/fonts/
  chinese_font: "MapleMono-NF-CN-Medium.ttf"
  english_font: "MapleMono-NF-CN-Medium.ttf"
  fallback_font: "NotoSans-Medium.ttf"
"""
)

font_config = config.get("font", {})

fonts_path = os.path.join(DATA_PATH, "fonts")
if not os.path.exists(fonts_path):
    os.makedirs(fonts_path)

try:
    chinese_font = ImageFont.truetype(os.path.join(fonts_path, font_config.get("chinese_font")), 20)
    english_font = ImageFont.truetype(os.path.join(fonts_path, font_config.get("english_font")), 20)
    fallback_font = ImageFont.truetype(os.path.join(fonts_path, font_config.get("fallback_font")), 20)
except FileNotFoundError as e:
    logger.error("字体文件不存在，请检查字体文件路径")
    raise e


def is_english_char(char: dict[str, str]) -> bool:
    return (
            'a' <= str(char["text"]).lower() <= 'z'
            or str(char["text"]) in string.digits
            or str(char["text"]) in string.punctuation
            or str(char["text"]) in string.whitespace
    )


def any_char(_: dict[str, str]) -> bool:
    return True


@common.function_cache(500)
def get_font(raw_font, matcher, color):
    return Font(raw_font, matcher, color)


def text_matcher(c, color, other):
    return c["color"] == color and other(c)


def draw_code(colors_code):
    message = None

    max_x = 1550
    img = Image.new("RGBA", (max_x, 3200), (30, 30, 46, 0))

    fonts = []
    unique_colors = {color for _, color in colors_code}

    for color in unique_colors:
        matcher_en = lambda c, bound_color=color: text_matcher(c, bound_color, is_english_char)
        fonts.append(get_font(english_font, matcher_en, color))

    # 行号
    fonts.append(get_font(english_font, is_english_char, (127, 132, 156)))

    fonts.append(get_font(english_font, is_english_char, None))

    for color in unique_colors:
        matcher_ch = lambda c, bound_color=color: text_matcher(c, bound_color, any_char)
        fonts.append(get_font(chinese_font, matcher_ch, color))
    fonts.append(get_font(chinese_font, any_char, None))

    for color in unique_colors:
        matcher_ch = lambda c, bound_color=color: text_matcher(c, bound_color, any_char)
        fonts.append(get_font(fallback_font, matcher_ch, color))
    fonts.append(get_font(fallback_font, any_char, None))

    code_lines = []
    current_line = []
    for text_segment, color in colors_code:
        # 处理可能包含多个换行符的段落
        parts = text_segment.split('\n')
        for i, part in enumerate(parts):
            if i > 0:  # 如果不是第一部分，说明遇到了一个 '\n'
                code_lines.append(current_line)  # 完成上一行
                current_line = []
            if part:  # 如果部分不为空，添加到当前行
                current_line += [{"text": part, "color": color}]
        # 检查行数限制
        if len(code_lines) > 150:
            message = "你的代码太长了，已自动截断"
            break

    if current_line:
        code_lines.append(current_line)

    code_lines = [
        [{"text": f"{i + 1:>3}  ", "color": (127, 132, 156)}] + code_lines[i] + [{"text": "\n", "color": None}]
        for i in range(len(code_lines))
    ]
    code_lines = [_ for code_line in code_lines for _ in code_line]
    draw_text(
        img, (0, 0), code_lines, fonts, (0, 0, 0),
        max_x=max_x - 50,
        max_y=3200,
        line_height=25,
        end_text="",
        end_text_font=english_font.font,
        has_emoji=True,
        emoji_source=LocalEmojiSource(os.path.join(DATA_PATH, "emoji")),
        wrap_indent="     "
    )

    path = os.path.join(CACHE_PATH, f"code-{uuid.uuid4().hex}.webp")

    left, upper, right, lower = img.getbbox()
    img = img.crop((0, 0, max(right + 40, 400), lower + 20))

    window = Image.new("RGBA", (img.size[0] + 40, img.size[1] + 80), (30, 30, 46, 255))
    window.paste(img, (20, 60), img)

    circle_colors = [
        (255, 95, 90),
        (255, 190, 46),
        (42, 202, 68)
    ]

    base_circle = Image.new("L", (25 * 3, 25 * 3), 0)
    draw = ImageDraw.Draw(base_circle)
    draw.ellipse((0, 0, 25 * 3, 25 * 3), fill=255)
    base_circle = base_circle.resize((25, 25), Image.Resampling.LANCZOS)

    for i, color in enumerate(circle_colors):
        circle = Image.new("RGBA", (25, 25), color)
        circle.putalpha(base_circle)
        window.paste(circle, (20 + i * 35, 20), circle)

    window_mask = Image.new("RGBA", window.size, (0, 0, 0, 0))
    rounded_rectangle(
        image=window_mask,
        size=(0, 0, window_mask.size[0], window_mask.size[1]),
        radius=15,
        color=(255, 255, 255),
        outline_width=0,
    )

    shadow_blur_radius = 10

    bg = Image.new("RGBA", (window.size[0] + 80, window.size[1] + 80), (167, 180, 190, 255))

    rounded_rectangle(
        image=bg,
        size=(40, 40, window_mask.size[0] + 40, window_mask.size[1] + 40),
        radius=15,
        color=(0, 0, 0),
        outline_width=0,
    )

    bg = bg.filter(ImageFilter.GaussianBlur(shadow_blur_radius))

    bg.paste(window, (40, 40), window_mask)

    draw = ImageDraw.Draw(bg)

    draw.text((10, bg.size[1] - 36), "by xiaosuyyds/murainbot-plugin-codeshare", (100, 100, 100), english_font)

    bg.save(path, quality=95)
    return path, message
