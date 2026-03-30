# 电感式编码器板载线圈生成器 (Inductive Encoder Coil Generator)

[![KiCad Plugin](https://img.shields.io/badge/KiCad-Plugin-blue.svg)](https://www.kicad.org)
[![Language](https://img.shields.io/badge/语言-中英文自动切换-green.svg)]()

一个用于 KiCad 的插件，用于生成电感式编码器的正弦/余弦差分感应线圈。支持贝塞尔曲线平滑、自动过孔放置和分层防交叉。

A KiCad plugin for generating sin/cos differential coils for inductive encoders. Supports Bezier curve smoothing, automatic via placement, and layer‑staggered routing.

## 概述 / Overview

本插件可在 KiCad PCB 编辑器中快速生成用于电感式编码器的正弦（SIN）和余弦（COS）差分线圈。线圈采用正余弦波形调制，过孔自动放置在波峰/波谷处并切换层，确保同层走线永不交叉短路。生成后的线圈自动按网络分组，便于后续编辑。

This plugin quickly generates sine (SIN) and cosine (COS) differential coils for inductive encoders in KiCad PCB Editor. The coils are modulated with sine/cosine waveforms; vias are automatically placed at peaks/valleys and switch layers, ensuring that traces on the same layer never cross or short. Generated coils are automatically grouped by net for easy later editing.

## 功能特性 / Features

- **正余弦线圈** – 生成符合正弦/余弦函数的差分感应线圈
- **贝塞尔曲线支持** – 可选使用三次贝塞尔曲线获得更平滑的走线
- **自动过孔与换层** – 在波峰/波谷处自动添加过孔并切换层（F.Cu ↔ B.Cu）
- **分层防交叉** – 同层走线永不交叉，避免短路
- **自动分组** – 生成的线圈按网络（COIL_SIN、COIL_COS）自动分组
- **多语言界面** – 根据系统语言自动切换中文/英文界面
- **非模态对话框** – 参数设置窗口不锁死主界面，可同时操作 PCB

## 安装指南 / Installation

1. 将本插件文件夹（`inductive_encoder_coil`）复制到 KiCad 的插件目录：
   - **Windows**: `%APPDATA%\kicad\10.0\scripting\plugins\`
   - **Linux/macOS**: `~/.local/share/kicad/10.0/scripting/plugins/`

2. 重启 KiCad（或重新扫描插件）。

3. 在 PCB 编辑器中，点击工具栏按钮 **电感编码器线圈**（或 **Inductive Encoder Coil**）启动插件。

## 使用方法 / Usage

1. 打开一个 PCB 文件。
2. 点击工具栏按钮 **电感编码器线圈**（或 **Inductive Encoder Coil**）。
3. 在参数设置对话框中调整各项参数（见下文）。
4. 点击 **生成线圈**（**Generate**）按钮，线圈将自动放置在当前 PCB 上。
5. 生成的线圈已按网络分组，可在 PCB 中移动、旋转或进一步编辑。

## 参数说明 / Parameters

| 参数 | 英文 | 默认值 | 说明 |
|------|------|--------|------|
| 中心半径 (mm) | Mid Radius | 10.0 | 线圈的平均半径 |
| 波形幅度 (mm) | Amplitude | 1.2 | 正弦波的幅度（径向调制量） |
| 极对数 | Pole Pairs | 8 | 正弦波周期的对数（决定线圈的极数） |
| 走线宽度 (mm) | Track Width | 0.2 | 线圈走线的宽度 |
| 过孔外径 (mm) | Via Outer | 0.6 | 过孔的外径（焊盘直径） |
| 过孔孔径 (mm) | Via Drill | 0.3 | 过孔的钻孔直径 |
| 单段平滑点数 | Smooth Segments | 48 | 每段（半周期）使用的直线段点数（仅当不使用贝塞尔曲线时生效） |
| 使用贝塞尔曲线 | Use Bezier Curve | 否 | 启用后使用三次贝塞尔曲线绘制，走线更平滑 |

## 截图 / Screenshots

![插件界面](https://github.com/user-attachments/assets/88eea0ed-3479-432a-944a-e25aa7472907)

![生成的线圈示例](https://github.com/user-attachments/assets/a0683b23-c61b-4c22-845a-2df604c6795e)

## 贡献 / Contributing

欢迎提交 Issue 或 Pull Request 来改进本插件。

1. Fork 本仓库。
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request。

## 许可证 / License

本项目采用 [MIT License](LICENSE)（如果存在 LICENSE 文件）或按原样提供。详情请参阅项目根目录的许可证文件。

## 致谢 / Acknowledgments

- 感谢 KiCad 团队提供的强大 PCB 设计平台。
- 感谢所有测试者和贡献者的反馈。

---

**提示**：如果插件未出现在工具栏，请检查插件目录是否正确，并确保 KiCad 已重新扫描插件（工具 → 外部插件 → 重新扫描插件）。

**Tip**: If the plugin does not appear in the toolbar, check that the plugin directory is correct and ensure KiCad has rescanned plugins (Tools → External Plugins → Rescan Plugins).