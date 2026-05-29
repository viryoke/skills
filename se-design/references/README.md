# References

本目录存放 SE Design SKILL 运行时需要参考的外部文档、规范、工具指南等。

## 建议存放内容

- IPD 流程规范文档
- 4+1 视图建模指南
- DFX 分析 Checklist 标准
- FMEA 分析模版
- 公司级架构治理规范
- Docx 文档模版（可选，如需自定义样式可自行提供 `docx_template.docx`）

---

## 图形化表达工具参考

### ASCII 字符图（交互阶段）

- **用途**：交互阶段（Phase 1-4）所有图表展示
- **优势**：终端直读、零渲染依赖、CLI 完全可见
- **字符集**：Unicode box-drawing（┌ ─ ┐ │ └ ┘ → ← ↑ ↓ v）
- **类型**：系统上下文、时序图、用例图、状态图、组件图、追踪矩阵、部署图
- **详细指南**：`references/diagram_guide.md` ASCII 部分

### PlantUML（归档阶段）

- **用途**：专业 UML 视图（系统上下文、用例图、类图、时序图、状态图、活动图、组件图、部署图）
- **语法**：`@startuml/@enduml` 包裹
- **渲染方式**：
  - 内置：`scripts/plantuml.jar`（~16MB，需 Java）
  - 系统：`plantuml` 命令（如已安装）
  - macOS 需安装 Java：`brew install openjdk`
  - VS Code 插件：PlantUML (jebbs.plantuml)
- **官方文档**：https://plantuml.com/

### Mermaid（可选补充，需 mmdc）

- **用途**：通用视图（流程图、甘特图、ER图、思维导图）— **非默认归档格式，推荐优先使用 PlantUML 替代**
- **语法**：```mermaid 代码块
- **渲染方式**：
  - mermaid-cli：`npm install -g @mermaid-js/mermaid-cli && mmdc -i diagram.mmd -o diagram.png`
  - GitHub / Markdown 内嵌渲染
  - VS Code 插件：Mermaid Markdown Syntax Highlighting
- **官方文档**：https://mermaid.js.org/

### GraphViz (DOT)（归档阶段）

- **用途**：复杂依赖关系（模块依赖网、子系统拓扑、需求追踪矩阵图）
- **语法**：`digraph/graph` 声明 + `rankdir` 方向
- **渲染方式**：
  - 内置 Windows：`scripts/graphviz/win64/bin/dot.exe`（~20MB）
  - Mac/Linux：`brew install graphviz` / `apt-get install graphviz`
  - VS Code 插件：GraphViz (jojoco.graphviz)
- **官方文档**：https://graphviz.org/documentation/

---

## 文档归档工具（自包含）

> **无需联网。PlantUML jar 和 GraphViz Windows portable 已内置在 `scripts/` 目录。macOS 需安装 Java（`brew install openjdk`）和 GraphViz（`brew install graphviz`）。**

### 内置离线工具

| 工具 | 文件路径 | 大小 | 平台 | 前置条件 |
|------|---------|------|------|---------|
| PlantUML | `scripts/plantuml.jar` | ~16MB | 全平台 | Java (JRE) |
| GraphViz | `scripts/graphviz/win64/bin/dot.exe` | ~20MB | Windows | 无（独立运行） |

**Mac/Linux GraphViz 说明**：这两个平台无官方 portable 版，推荐系统安装：
- Mac: `brew install graphviz`
- Linux: `sudo apt-get install graphviz`

### 图表渲染与 Docx 转换（一体化）

> **Markdown 保留图表源码，Docx 自动渲染嵌入。无需单独渲染步骤，无需联网。**

- **脚本**：`scripts/convert_docx.py`（Python 3.6+，自动 pip install python-docx）
- **工作方式**：Markdown 中的 PlantUML/DOT 代码块 → 自动渲染为 PNG → 嵌入 Docx（Mermaid 需 mmdc，非默认）
- **渲染策略**：
  1. 内置打包工具（scripts/plantuml.jar, scripts/graphviz/{platform}/）→ 优先使用
  2. Homebrew openjdk（macOS: `/opt/homebrew/opt/openjdk/bin/java`）→ macOS Java stub 回退方案
  3. 系统工具（plantuml / dot / mmdc in PATH）→ 如已安装则使用
  4. 源码文本 → 都不可用时，代码块以文本形式保留在 Docx 中
- **GraphViz CJK**：macOS 使用 `-Tpng:quartz`（Core Text），Linux 使用 `-Tpng:cairo`（Pango），确保中文不乱码
- **支持**：标题、表格、代码块、列表、Callout、PNG 图片嵌入、粗体/斜体/链接

### 独立图表渲染工具（可选）

- **脚本**：`scripts/render_diagrams.py`（Python 3.6+，纯标准库）
- **用途**：单独渲染 .puml / .dot 源文件为 PNG（如需手动渲染）