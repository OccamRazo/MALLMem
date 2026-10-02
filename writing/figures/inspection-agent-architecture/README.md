# 巡检机器人 Agent 架构图

版本：2026-09-21，设计 r1，最终渲染 r2。类型：概念系统框架，非实验结果。对应[完整架构说明与汇报讲稿](../../inspection-agent-architecture.md)。

## 交付文件

| 文件 | 用途 |
| --- | --- |
| `inspection-agent-architecture.svg` | 原生矢量主文件，1920 × 1080，16:9；文字、模块、图标和连线可分别编辑 |
| `inspection-agent-architecture.png` | 1920 × 1080 预览 |
| `inspection-agent-architecture-2x.png` | 3840 × 2160 汇报用高清图 |
| `generate.py` | 标准库生成器，保存图形几何、文案和设计记录 |
| `render.cjs` | 用 Sharp 将 SVG 渲染为两种分辨率 PNG |
| `design/` | FigurePlan、FigureSpec、ReferenceAnalysis、RenderAudit 与文件哈希 |
| `reference/` | 用户原草图及参考论文 Figure 1，保留输入追溯，不作为原创图交付 |

SVG 内含 `text`、`rect`、`path`、`g` 等原生元素，没有嵌入位图，也没有把文字转为轮廓。可以在支持 SVG 的矢量编辑器中按分组编辑，或直接修改生成器后重建。字体优先使用 PingFang SC，回退到 Noto Sans CJK SC、Microsoft YaHei 与 Arial；字体未嵌入，更换电脑可能改变字宽，导出前应重新检查。具体第三方编辑器的导入行为 **not run**，本次验证的是 SVG 原生结构与本机实际渲染。

## 输入与设计依据

- 用户提供的结构草图：`reference/user-sketch.png`。
- 风格来源：[ABot-AgentOS v3 Figure 1](https://arxiv.org/html/2607.10350v3#S2.F1)，[原始图片](https://arxiv.org/html/2607.10350v3/figure/agent_v7.png)，本机参考文件 `reference/abot-agentos-figure1.png`。于 2026-09-21 读取。借鉴分层布局、侧边栏、淡色圆角区域和图标，未复制端云模型或公共/私有记忆架构。
- 科学内容依据：项目路线图、2026-09-07 L3 提案、2026-09-17 Harness 调研及 2026-09-21 AgentOS 调研，详见完整说明的来源列表。
- 数值数据、模型权重、实验输入：不适用；图中没有性能结果或统计数字。

## 重建

从仓库根目录运行：

```sh
python3 writing/figures/inspection-agent-architecture/generate.py
node writing/figures/inspection-agent-architecture/render.cjs
```

第二步要求当前 Node 环境可解析 `sharp`。若依赖放在独立目录，通过 `NODE_PATH` 指向包含 `sharp` 的 `node_modules`。

本次设备：本地 macOS；生成器使用 Python 3.9.6；渲染使用 Codex 已有依赖 Sharp 0.35.4、libvips 8.18.6、librsvg 2.62.91。没有向项目添加依赖或安装环境。原生 SVG 生成只需 Python 标准库。

本次渲染命令的依赖目录：

```sh
NODE_PATH=/Users/erwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
/Users/erwin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
writing/figures/inspection-agent-architecture/render.cjs
```

若本机存在学术框架图技能的 `validate_figure_spec.py`，生成器会在输出 SVG 前执行严格校验。缺少技能不会阻止在其他设备重建 SVG；此时需独立复核语义连接和格式。

## 本次检查与边界

- FigureSpec 严格校验：通过，0 errors / 0 warnings。
- SVG XML 解析、文本清单、分组、无位图嵌入：通过，细节见 `design/verification.json`。
- 1920 × 1080 彩色图、缩小至 1440 × 810 的灰度图：已逐图检查中文、裁切、覆盖、连线和层级；灰度下虚线仍区分后续演化。
- 初版缺陷：技能反馈箭头穿过 Agent 顶部说明；r2 将其收敛为左侧短标题，已修正。无新增科学语义连接。
- 文字对比度：对实际使用的主要文字/背景组合进行了数值检查，结果见 `design/verification.json`。
- PNG 元数据清理：已执行；SVG 原生输出没有嵌入位图元数据。
- 设计适配全屏学术汇报，不声明在单栏论文宽度下仍可读。论文排版时建议拆分在线架构与记忆机制两个面板。
- 实机、仿真、准确率、长期收益：**not run**，不属于此次制图任务。

本机目录：`/Users/erwin/Desktop/mine/projects/mem-humanoid/writing/figures/inspection-agent-architecture/`。文件哈希保存在 `design/verification.json`；最终生成物、本次来源材料与设计记录均在当前设备可用。灰度质检图保存在已忽略的 `outputs/`，无需交接。
