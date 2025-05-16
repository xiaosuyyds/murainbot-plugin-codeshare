# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/xiaosuyyds/murainbot-plugin-codeshare/blob/master/NOTICE

from Lib import Logger

from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.styles import get_style_by_name
from pygments.token import Token, Error

logger = Logger.get_logger()


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    elif len(hex_color) == 3:
        return tuple(int(c * 2, 16) for c in hex_color)
    return None


language_mapping = {
    "py": "python",
    "c": "c",
    "c++": "cpp",
    "cpp": "cpp",
    "cs": "csharp",
    "js": "javascript",
    "ts": "typescript",
    "rust": "rust",
    "go": "go",
    "php": "php",
    "ruby": "ruby",
    "kt": "kotlin",
    "java": "java",
    "swift": "swift",
    "perl": "perl",
    "lua": "lua",
    "sql": "sql",
    "json": "json",
    "md": "markdown"
}


def get_token_colors(code_snippet, style_name='lightbulb', language='guess', _flag=False):
    style = get_style_by_name(style_name)

    default_hex = style.style_for_token(Token.Text).get('color')
    default_rgb = hex_to_rgb(default_hex) if default_hex else (200, 200, 200)

    error_style = style.style_for_token(Error)
    error_rgb = hex_to_rgb(error_style['color']) if error_style.get('color') else (255, 0, 0)

    results = []
    try:
        if language == 'guess':
            lexer = guess_lexer(code_snippet)
        else:
            lexer = get_lexer_by_name(language)

        tokens = lexer.get_tokens(code_snippet)

        for ttype, ttext in tokens:
            try:
                token_style = style.style_for_token(ttype)
                rgb_color = default_rgb
                if ttype is Error:
                    rgb_color = error_rgb
                elif token_style.get('color'):
                    rgb_color = hex_to_rgb(token_style['color']) or default_rgb

            except Exception as e:
                logger.warning(f"An unexpected error occurred: from get_token_colors:"
                               f"{ttext} {ttype}\n"
                               f"{repr(e)}", exc_info=True)
                rgb_color = default_rgb

            results.append((ttext, rgb_color))

    except Exception as e:
        # Catch other potential errors during processing
        logger.warning(f"An unexpected error occurred: {repr(e)}", exc_info=True)
        if _flag:
            results.append((f"<Internal Error: {e}>", error_rgb))
            return results
        else:
            res = [(f"似乎出现了一些问题，已自动回退到默认语言\n", error_rgb)]
            res += get_token_colors(code_snippet, style_name, "python", _flag=True)
            return res

    return results
