<div align="center">

<a href="https://github.com/MuRainBot/MuRainBot2" style="text-decoration:none" >
    <img src="https://mrb2.xiaosu.icu/icon.webp" width="200px" height="200px">
</a>

# murainbot-plugin-codeshare

***✨MuRainBot2插件，生成美丽的可供分享的代码图片✨***

![example](https://cdn.jsdelivr.net/gh/xiaosuyyds/murainbot-plugin-codeshare/@master/example.png)

</div>


## 安装

下载本仓库代码

```bash
git clone https://github.com/xiaosuyyds/murainbot-plugin-codeshare.git
```

或[直接下载zip](https://github.com/xiaosuyyds/murainbot-plugin-codeshare/archive/refs/heads/master.zip)

参考[MRB2文档](https://mrb2.xiaosu.icu/start/getting-started)

然后将本项目的CodeShare目录放在框架的 `plugins` 文件夹内

然后将本项目的 `data` 目录内的文件放在框架的 `data` 文件夹内

注：本项目的data目录并不包含emoji资源（因为emoji的大小过大），请自行下载后放到框架的`data/emoji`文件夹内，下载地址：https://github.com/googlefonts/noto-emoji/tree/main/png
任选一种分辨率即可，直接将全部emoji文件放进`data/emoji`文件夹，当然，如果你并不需要渲染代码中的emoji，可以忽略这一步。

然后`python -m pip install -r /path/to/your/download/CodeShare/requirements.txt`
下载所需依赖库

最后运行MRB2即可

## 使用

支持命令 `/codeshare` (别名 `/cs`)。

会自动识别输入的代码语言，但是可能会识别错误。

**用法示例:**

1.  **直接跟代码:**
    ```
    /cs print("Hello, MuRainBot!")
    ```

2.  **回复消息:**
    *   然后回复需要绘制的消息，回复后跟上发送命令 `/cs` 或 `/codeshare`，注意！QQ默认回复会添加at，请删除他。

## 配置项

首次启动会自动生成默认配置文件，位于/plugin_configs/CodeShare.yml

内有注释，照着改即可

## 许可证
版权所有 2025 Xiaosu。

根据 [Apache 2.0 许可证](https://github.com/xiaosuyyds/murainbot-plugin-codeshare/blob/master/LICENSE) 的条款分发。
