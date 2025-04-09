# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/xiaosuyyds/murainbot-plugin-codeshare/blob/master/NOTICE

from Lib import *
from plugins.CodeShare import highlight, draw

import os


def get_leading_whitespace(s: str) -> str:
    count = 0
    for char in s:
        if char.isspace():
            count += 1
        else:
            break
    return s[:count]


def dedent_lines(lines):
    if not lines:
        return []

    lines_with_content = [line for line in lines if line.strip()]

    if not lines_with_content:
        return lines[:]

    leading_whitespaces = [get_leading_whitespace(line) for line in lines_with_content]

    if not leading_whitespaces:
        common_prefix = ""
    else:
        common_prefix = os.path.commonprefix(leading_whitespaces)

    prefix_len = len(common_prefix)

    if prefix_len == 0:
        return lines[:]

    result_lines = [line[prefix_len:] for line in lines]

    return result_lines


matcher = EventHandlers.on_event(EventClassifier.MessageEvent, rules=[EventHandlers.CommandRule(
    "codeshare", {"cs"}, reply=True
)])


@matcher.register_handler()
def codeshare_handler(event_data: EventClassifier.MessageEvent):
    is_reply = False
    if event_data.message.rich_array[0].type == "reply":
        code_msg = Actions.GetMsg(
            message_id=event_data.message.rich_array[0].data["id"]
        ).call().get_result()
        if code_msg.is_ok:
            code_msg = code_msg.unwrap()
            message = QQRichText.QQRichText(code_msg["message"])
        else:
            message = QQRichText.QQRichText(
                QQRichText.Text(
                    f"获取代码失败，请换条消息稍后再试\n错误信息{repr(code_msg.unwrap_err())}"
                )
            )
            if event_data.message_type == "group":
                Actions.SendMsg(message=message, group_id=event_data["group_id"]).call()
            else:
                Actions.SendMsg(message=message, user_id=event_data.user_id).call()
            raise code_msg.unwrap_err()
        is_reply = True
    else:
        message = event_data.message
    code = ""
    for rich in message.rich_array:
        if isinstance(rich, QQRichText.Text):
            code += rich.data.get("text")

    cmd = code.split("codeshare", 1)[-1].strip().split(" ", 1)

    if not is_reply:
        code = cmd[-1]

    language_name = "guess"

    if len(cmd) == 2:
        language_name = cmd[0]
        if language_name not in [
            "python",
            "c",
            "cpp",
            "java",
            "cs",
            "js",
            "ts",
            "rust",
            "go",
            "php",
            "ruby",
            "kotlin",
            "swift",
            "perl",
            "lua",
            "sql"
        ]:
            if not is_reply:
                code = language_name + " " + code
            language_name = "guess"

    code = "\n".join(dedent_lines(code.split("\n")))

    if code.startswith(" "):
        code = code[1:]

    print(f"code: {code}")

    if not code or not code.strip():
        message = QQRichText.QQRichText("请输入代码")
        if event_data.message_type == "group":
            Actions.SendMsg(message=message, group_id=event_data["group_id"]).call()
        else:
            Actions.SendMsg(message=message, user_id=event_data.user_id).call()
        return
    try:
        code_colors = highlight.get_token_colors(code, language=language_name)
    except Exception as e:
        message = QQRichText.QQRichText(
            QQRichText.Text(
                f"代码高亮处理失败，请检查代码是否正确。\n错误信息：{repr(e)}"
            )
        )
        if event_data.message_type == "group":
            Actions.SendMsg(message=message, group_id=event_data["group_id"]).call()
        else:
            Actions.SendMsg(message=message, user_id=event_data.user_id).call()
        raise e

    try:
        output_path, draw_message = draw.draw_code(code_colors)
    except Exception as e:
        message = QQRichText.QQRichText(
            QQRichText.Text(
                f"图片绘制失败，请稍后再试。\n错误信息：{repr(e)}"
            )
        )
        if event_data.message_type == "group":
            Actions.SendMsg(message=message, group_id=event_data["group_id"]).call()
        else:
            Actions.SendMsg(message=message, user_id=event_data.user_id).call()
        raise e

    message = QQRichText.QQRichText(
        QQRichText.Reply(event_data.message_id),
        QQRichText.Image(output_path),
    )
    if draw_message:
        message += QQRichText.Text(draw_message)

    if event_data.message_type == "group":
        Actions.SendMsg(message=message, group_id=event_data["group_id"]).call()
    else:
        Actions.SendMsg(message=message, user_id=event_data.user_id).call()
