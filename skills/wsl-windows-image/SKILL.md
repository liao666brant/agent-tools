---
name: wsl-windows-image
description: 用户消息中出现 Windows 图片文件路径（如 C:\\Users\\...\\image.png、D:\\截图\\a.jpg）时使用。无需等待用户要求，主动转换为 WSL 的 /mnt/<盘符>/ 路径并用读取工具打开图片。
---

# 在 WSL 中读取 Windows 图片

当消息中出现 Windows 图片路径时，立即读取图片，再处理用户围绕图片提出的问题。不要要求用户手动转换路径，也不要只回复转换后的路径。

## 路径转换

| Windows 路径 | WSL 路径 |
| --- | --- |
| `C:\Users\Name\image.png` | `/mnt/c/Users/Name/image.png` |
| `D:\Screenshots\image.png` | `/mnt/d/Screenshots/image.png` |

按以下规则转换：

1. 去掉路径前后的引号、反引号和多余空白。
2. 若反斜杠被转义（如 `C:\\Users\\...`），先还原为单个反斜杠。
3. 盘符改为小写；将 `X:\path\to\file` 转为 `/mnt/x/path/to/file`。
4. 保留路径中的空格和 Unicode 字符，不要自行改名、移动或复制文件。

## 读取与失败处理

1. 对转换后的绝对路径直接使用文件读取工具；该工具可识别 PNG、JPG、JPEG、WEBP 等常见图片。
2. 文件读取成功后，根据图片内容回答；若用户要定位代码，再检索仓库，不要仅凭图片猜文件位置。
3. 若读取失败，明确给出已尝试的 WSL 路径，并请用户确认文件是否仍存在或重新提供路径；不要猜测图片内容。
4. 路径不是 Windows 盘符格式时，不适用本技能，按原路径处理。

示例：

```text
C:\Users\Syspetro\AppData\Local\PixPin\Temp\capture.png
→ /mnt/c/Users/Syspetro/AppData/Local/PixPin/Temp/capture.png
```
