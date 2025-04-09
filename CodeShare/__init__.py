# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/xiaosuyyds/murainbot-plugin-codeshare/blob/master/NOTICE

from Lib.core import PluginManager


plugin_info = PluginManager.PluginInfo(
    NAME="CodeShare",
    AUTHOR="Xiaosu",
    VERSION="1.0",
    DESCRIPTION="生成美丽的可供分享的代码图片",
    HELP_MSG="生成美丽的可供分享的代码图片 /codeshare 或 /cs 后面直接跟上代码即可\n"
             "或回复一条消息，再加上/codeshare 或 /cs\n"
             "可自动猜测语言，也支持手动指定语言，在命令后面跟上语言的名字，支持python,c,cpp,java,cs,js,ts,rust,go,php,ruby,kotlin,swift,perl,lua,"
             "sql]，如果不在这些里面则认为是代码的一部分"
)

from plugins.CodeShare import handlers
