<div align="center">

<a href="https://github.com/MuRainBot/MuRainBot2" style="text-decoration:none" >
    <img src="https://mrb2.xiaosu.icu/icon.webp" width="200px" height="200px" alt="MuRainBot2 Logo">
</a>

# murainbot-plugin-codeshare

***✨ MuRainBot2 插件，生成美观、可供分享的代码图片 ✨***

![示例图片](https://cdn.jsdelivr.net/gh/xiaosuyyds/murainbot-plugin-codeshare/@master/example.png)

> 麻麻再也不用担心我看群里的文本代码看的头晕眼花了

</div>

## ✨ 功能特性

*   **代码图片生成：** 将代码片段转换为易于分享的精美图片。
*   **自动语言识别：** 尝试自动检测输入代码的编程语言。
*   **Emoji 支持 (可选)：** 可在生成的图片中渲染代码注释或字符串中的 Emoji（需要额外下载资源）。
*   **MuRainBot2 集成：** 作为 MRB2 插件，易于安装和使用。
*   **配置灵活：** 提供配置文件以调整部分行为。

## 🔧 环境要求

*   **Python:** >= 3.12
*   **MuRainBot2:** 需要先正确安装并运行 MuRainBot2 框架。请参考 [MRB2 文档](https://mrb2.xiaosu.icu/start/getting-started)。
*   **Git:** 用于克隆本仓库（可选，也可以直接下载zip压缩包）。

## 🚀 安装步骤

1.  **克隆仓库:**
    打开你的终端或命令行，导航到你希望存放插件代码的位置，然后运行：
    ```bash
    git clone https://github.com/xiaosuyyds/murainbot-plugin-codeshare.git
    ```
    或者，你也可以 [直接下载 ZIP 压缩包](https://github.com/xiaosuyyds/murainbot-plugin-codeshare/archive/refs/heads/master.zip) 并解压。

2.  **放置插件:**
    将克隆（或解压）得到的 `CodeShare` 文件夹，完整地移动到你的 MuRainBot2 框架的 `plugins` 目录下。
    最终路径应类似于：`[你的 MRB2 根目录]/plugins/CodeShare/`

3.  **放置数据文件:**
    将本仓库 `data` 目录下的 **所有文件** 复制到你的 MuRainBot2 框架的 `data` 目录下。
    最终路径应类似于：`[你的 MRB2 根目录]/data/`

5.  **安装依赖:**
    进入你刚刚克隆（或解压）的 `murainbot-plugin-codeshare` 目录，然后安装所需的 Python 库：
    ```bash
    cd murainbot-plugin-codeshare
    python -m pip install -r requirements.txt
    ```
    *(请确保你使用的 `python` 和 `pip` 命令对应你运行 MRB2 的 Python 环境)*

6.  **(可选) 配置 Emoji 资源:**
    请参考下面的 **[🤔 Emoji 支持 (可选)](#-emoji-支持-可选)** 部分进行操作。

7.  **运行 MRB2:**
    正常启动或重启你的 MuRainBot2，插件应该会被加载。

## 🤔 Emoji 支持 (可选)

本插件可以在生成的代码图片中渲染 Emoji 字符，但这需要 Noto Emoji 资源。由于资源文件较大，未包含在本仓库中。

*   **是否需要？** 如果你不需要在代码图片中显示 Emoji (例如，代码注释或字符串里的 😀)，可以完全跳过此步骤。
*   **下载资源:** 前往 [Noto Emoji 官方仓库](https://github.com/googlefonts/noto-emoji/tree/main/png) 下载 PNG 格式的 Emoji 文件。
*   **选择分辨率:** 你只需要选择其中一种分辨率下载即可（例如 `128px`）。
*   **放置资源:** 将下载到的 **所有 PNG 图片文件** 直接放入你的 MuRainBot2 框架的 `data/emoji` 目录下。
    *   确保目标路径是：`[你的 MRB2 根目录]/data/emoji/`
    *   该目录下应该直接包含 `emoji_u1f600.png`, `emoji_u1f601.png` 等大量 PNG 文件。
    *   如果 `emoji` 目录不存在，请手动创建它。

## 💡 使用方法

使用命令 `/codeshare` 或其别名 `/cs`。

插件会自动尝试识别你提供的代码语言，但有时可能识别不准确（目前暂不支持手动指定语言）。

**两种用法:**

1.  **命令后直接跟代码:**
    ```
    /cs print("Hello, MuRainBot!")
    ```
    ```
    /cs #include <stdio.h>
    int main() {
       printf("Hello, World!");
       return 0;
    }
    ```

2.  **回复消息:**
    *   先发送包含代码的消息。
    *   然后 **回复** 该消息，并发送命令 `/cs` 或 `/codeshare`。
    *   **重要提示:** 在 QQ 中，回复消息默认会带上 `@对方`，你需要 **手动删除这个 `@提及`**，只留下 `/cs` 或 `/codeshare` 命令本身与回复再发送。

## ⚙️ 配置项

插件首次运行时，会在 `[你的 MRB2 根目录]/plugin_configs/` 目录下自动生成默认配置文件 `CodeShare.yml`。

文件内包含注释说明，你可以根据需要参考注释进行修改。常见的可配置项可能包括图片主题、字体等（具体请查看生成的配置文件）。

## 📜 许可证

版权所有 © 2025 Xiaosu。

本项目根据 [Apache License 2.0](https://github.com/xiaosuyyds/murainbot-plugin-codeshare/blob/master/LICENSE) 许可证的条款进行分发。
