---
name: viryoke-workflow
description: |
  快速初始化完整的开发环境工作流。
  
  **触发场景：**
  - 用户提到"初始化环境"、"搭建开发环境"、"setup workflow"、"新机器配置"、"装工具"
  - 用户要求按 toolchain.md 配置工具链
  
  **覆盖平台：** macOS / Linux / WSL2
  
  **为什么这样设计：** 
  统一通过 Homebrew 安装避免 sudo 依赖，幂等检查避免重复安装，分阶段执行便于定位问题。
  
  当用户说"帮我配置开发环境"、"在新机器上装工具"、"初始化我的工具链"时使用本技能。
---

# Viryoke Workflow Setup

## 设计理念

**问题：** 传统环境配置依赖 sudo、交互式安装、分散的包管理器，导致脚本难以自动化且容易失败。

**解决方案：**
```
统一包管理器（Homebrew）→ 幂等安装（先检查再装）→ 分阶段执行（定位问题）
```

**为什么有效：**
- Homebrew 安装在用户目录，之后所有 `brew install` 无需 sudo
- 幂等检查：`brew list` / `command -v` 已存在则跳过
- 分阶段：失败时能快速定位哪个阶段出问题

---

## 核心原则

| 原则 | 为什么 |
|------|--------|
| **幂等安装** | 重复执行不会破坏已有配置 |
| **平台感知** | macOS/Linux/WSL2 有差异，自动选择正确指令 |
| **批量安装** | 同阶段工具合并为一条命令，减少网络往返 |
| **非交互** | 所有命令带 `-y`，适合脚本自动化 |
| **零 sudo** | 仅 Homebrew 安装和 `.pkg` cask 需 sudo |
| **Dry-run** | 先列出操作清单，确认后再执行 |

---

## 参考文档

| 文档 | 用途 |
|------|------|
| `references/toolchain.md` | 工具选型定义（权威参考） |
| `references/scripts.md` | 详细安装命令 |
| `references/configs.md` | 配置文件内容 |

执行时查阅 toolchain.md，不要凭记忆执行。

---

## 执行流程

10 个阶段顺序执行，预估总耗时 20-35 分钟。

### 阶段 0：平台检测与前置检查

**目标：** 确认平台、网络、Homebrew 状态，识别需手动安装的项目。

**成功标准：** 用户知道平台类型、网络是否通畅、哪些工具需手动安装。

**检测命令：**
```bash
uname -s   # Darwin=macOS, Linux=Linux
uname -m   # arm64=Apple Silicon, x86_64=Intel
grep -qi microsoft /proc/version 2>/dev/null && echo "WSL2"
```

**关键检查：**
- 网络连通性：github.com, pypi.org, raw.githubusercontent.com
- sudo 可用性：`sudo -n true` 失败 → `.pkg` cask 标记手动
- gh 登录状态：未登录 → `gh extension install` 标记手动

**平台策略：**
| 平台 | 安装策略 |
|------|----------|
| macOS | Xcode CLI + Homebrew |
| Linux | build-essential + Homebrew on Linux |
| WSL2 | Docker Engine（不用 Colima） |

---

### 阶段 1：终端 & Shell & 字体

**目标：** 安装终端、Shell 提示符、复用器、字体。

**成功标准：** Ghostty 能启动、Starship prompt 正常渲染、字体正确显示图标。

**命令：** 见 `references/scripts.md`

**注意：** Linux 字体装后需 `fc-cache -fv`

---

### 阶段 2：输入法 & 编辑器

**目标：** 安装中文输入法、编辑器、剪贴板工具。

**成功标准：** 输入法可用、Neovim/VS Code 能启动。

**平台差异：**
| 平台 | 输入法 |
|------|--------|
| macOS | Squirrel + im-select + cc-switch |
| Linux | fcitx5 + fcitx5-rime |
| WSL2 | 跳过（Windows 侧装 weasel） |

**注意：** cc-switch / temurin 是 `.pkg` cask，需 sudo

---

### 阶段 3：文件 & 搜索

**目标：** 安装现代文件/搜索工具替代传统命令。

**成功标准：** fd、rg、bat、fzf、zoxide、yazi 命令可用。

---

### 阶段 4：Git & GitHub

**目标：** 安装 Git 工具链，配置 gitconfig。

**成功标准：** git、gh、lazygit 可用，delta diff 美化生效。

**配置：** 见 `references/configs.md`

**注意：**
- 必须询问真实 email
- gh-dash 需先 `gh auth login`

---

### 阶段 5：编程语言

**目标：** 安装多语言开发环境。

**成功标准：** node、go、java、rustc、python、kotlin 命令可用，conda 环境创建成功。

**安装顺序（重要）：**
1. Node.js（在 bat 之后，避免 llhttp 冲突）
2. Miniconda → init → tos accept
3. Java（.pkg cask）
4. Go/Kotlin/CMake/Ninja/Maven/Gradle
5. Rust（优先 brew，回退 curl）
6. TypeScript/ruff

---

### 阶段 6：容器化 & AI

**目标：** 安装容器运行时和 AI 学习工具。

**成功标准：** Docker 可用、Ollama 能拉取模型、AI conda 环境可用。

**平台差异：**
| 平台 | 容器方案 |
|------|----------|
| macOS/Linux | Colima |
| WSL2 | Docker Engine（apt install） |

**AI 环境：**
- macOS Apple Silicon：PyTorch MPS + MLX
- Linux/WSL2 NVIDIA：PyTorch CUDA

---

### 阶段 7：笔记工具

**目标：** 安装 Obsidian 和 Markdown 工具链。

**成功标准：** Obsidian 能打开、marksman LSP 可用。

---

### 阶段 8：配置文件部署

**目标：** 部署统一主题的配置文件。

**成功标准：** Dracula 主题生效、JetBrainsMono 14pt 字体生效。

**统一标准：**
- 主题：Dracula
- 字体：JetBrainsMono Nerd Font 14pt
- 透明度：0.92 + blur

**配置内容：** 见 `references/configs.md`

---

### 阶段 9：验证

**目标：** 验证所有工具和配置正确。

**成功标准：** 核心验证全部通过。

**验证脚本：** 见 `references/scripts.md`

**验证范围：**
- Shell 语法
- 工具启动（Starship、Neovim、Conda）
- 语言运行时（node/go/java/rustc/python/kotlin）
- 容器状态
- 关键工具可用性

---

## 平台特殊处理

| 平台 | 要点 |
|------|------|
| **macOS** | Homebrew 在 `/opt/homebrew`(ARM) 或 `/usr/local`(Intel)；`.pkg` cask 需 sudo |
| **Linux** | Homebrew 在 `/home/linuxbrew`；`fc-cache -fv`；xclip/wl-clipboard |
| **WSL2** | Docker Engine 替代 Colima；跳过输入法和字体 |

---

## cask sudo 分类

| 类型 | 示例 | sudo |
|------|------|------|
| `.app` cask | ghostty, visual-studio-code | 否 |
| `.pkg` cask | squirrel-app, temurin, cc-switch | **是** |
| 字体 cask | font-jetbrains-mono-nerd-font | 否 |

---

## 错误处理

- 失败不中断，继续执行后续阶段
- 最后汇总失败列表和修复建议
- `.pkg` cask 失败 → 加入手动安装列表
- gh-dash 失败 → 提示先 `gh auth login`

---

## 完成报告

```
## 环境初始化完成

### 耗时：阶段 0-9 各 Xs / 总计 Xs
### 已安装 X/Y · 跳过 A · 失败 B

### 失败详情：工具名 → 错误信息 + 修复建议
### 需手动安装：.pkg cask 列表

### 后续步骤：
1. source ~/.zshrc 或重启终端
2. Neovim 首次启动自动装 LazyVim 插件
3. ollama pull qwen3:latest
4. colima start（非 WSL2）

### 回滚：
- brew uninstall <name>
- conda env remove -n <name>
- rustup self uninstall
```

---

## 目录结构

```
references/
├── toolchain.md    # 工具选型定义（权威参考）
├── scripts.md      # 详细安装命令
└── configs.md      # 配置文件内容
```