# 开发环境工具链

> 本文件描述本地开发环境完整工具链，供 AI Agent 在新机器上自动化搭建环境时参考。
> 选型维度权重：流行度(★) > 跨平台(★) > 性能(★) > 实时性/维护活跃度 > 趋势

## 目录

- [0. 前置条件](#0-前置条件)
- [1. 终端 & Shell](#1-终端--shell)
- [2. 主题 & 字体](#2-主题--字体)
- [3. 输入法](#3-输入法)
- [4. 编辑器](#4-编辑器)
- [5. 文件 & 搜索](#5-文件--搜索)
- [6. Git & GitHub 工具链](#6-git--github-工具链)
- [7. 编程语言开发环境](#7-编程语言开发环境)
- [8. 容器化](#8-容器化)
- [9. AI 学习工具链](#9-ai-学习工具链)
- [10. AI Agent 平台](#10-ai-agent-平台)
- [11. 其他 CLI 工具](#11-其他-cli-工具)
- [12. 笔记工具链](#12-笔记工具链)
- [13. 声明式依赖管理](#13-声明式依赖管理)
- [14. 一键安装脚本](#14-一键安装脚本)
- [15. 配置文件清单](#15-配置文件清单)
- [16. 一键更新](#16-一键更新)
- [17. 跨平台差异](#17-跨平台差异)
- [18. 自动化约束](#18-自动化约束)

---

## 0. 前置条件

| 平台 | 包管理器 | 编译链 | 安装方式 |
|------|----------|--------|----------|
| **macOS** | Homebrew | Xcode CLI | `xcode-select --install` |
| **Linux** | apt + cargo + curl/snap | build-essential | `sudo apt install build-essential` |

### 0.1 macOS

```bash
# 安装 Xcode Command Line Tools（含 git、make、gcc、clang 等编译链）
xcode-select --install 2>/dev/null || true

# 安装 Homebrew（非交互）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 将 Homebrew 加入 PATH
eval "$(/opt/homebrew/bin/brew shellenv)"                  # Apple Silicon
eval "$(/usr/local/bin/brew shellenv)"                     # Intel
```

### 0.2 Linux (Ubuntu/Debian)

```bash
# 安装编译依赖链
sudo apt-get update -y
sudo apt-get install -y build-essential curl file git procps zsh
```

### 0.3 说明

| 操作 | 是否需 sudo | 原因 |
|------|-------------|------|
| 安装 Xcode CLT / build-essential | 是（仅首次） | 系统级编译链 |
| 安装 Homebrew (macOS) | 是（仅首次） | 需写 `/opt/homebrew` 或 `/usr/local` |
| `brew install` (macOS) | 否 | Homebrew 运行在用户目录下 |
| `apt install` (Linux) | 是 | 系统包管理器 |
| `cargo install` (Linux) | 否 | Rust 工具链在用户目录 |
| macOS `.pkg` cask | 是 | temurin 等需管理员权限 |

---

## 1. 终端 & Shell

| 工具 | 用途 | macOS 安装 | Linux 安装 | 备选 |
|------|------|------------|------------|------|
| **Ghostty** | 终端模拟器 | `brew install --cask ghostty` | GitHub Release (deb/AppImage) | Kitty (Linux apt) |
| **zsh** | 交互 Shell | 系统内置 | `apt install zsh` | fish（不兼容 bash） |
| **Starship** | Shell 提示符 | `brew install starship` | `cargo install starship` | oh-my-posh |
| **Zellij** | 终端复用器 | `brew install zellij` | `cargo install zellij` | tmux |

### 1.1 Shell 别名

```bash
alias ll="ls -la" l="ls -l" ..="cd .." ...="cd ../.."
alias g="git" v="nvim" vi="nvim" vim="nvim" y="yazi"
alias ls="eza --group-directories-first"
alias top="btm 2>/dev/null || top"

# bat 主题
export BAT_THEME="Dracula"
```

### 1.2 Zellij 手动使用

Ghostty 已内置 Tab/Split，**Zellij 不与 Ghostty 绑定**——不会在 Ghostty 启动时自动开启 Zellij。Zellij 作为独立工具按需手动启动，主要用于 session 持久化和浮动面板场景。

以下为手动启动 Zellij 的命令参考，**不注入到默认 zshrc**：

```bash
# Zellij auto-attach（跳过 Ghostty / VS Code / 非标准终端）
if [ -z "$ZELLIJ" ] && [ -z "$VSCODE_INJECTION" ] && [ "$TERM" != "xterm-ghostty" ] && [ "$TERM_PROGRAM" != "Ghostty" ]; then
  if command -v zellij &>/dev/null; then
    zellij attach -c 2>/dev/null || zellij
  fi
fi
```

> Ghostty 设置 `TERM=xterm-ghostty` 而非 `TERM_PROGRAM=Ghostty`，检查需同时覆盖两者，另有 `VSCODE_INJECTION` 排除 VS Code 终端。

---

## 2. 主题 & 字体

| 组件 | 选型 | macOS 安装 | Linux 安装 | 备选 |
|------|------|------------|------------|------|
| 主题 | **Dracula** | 全局配色 #282a36 / #f8f8f2 | 同左 | Catppuccin、Tokyo Night |
| 主字体 | **JetBrainsMono Nerd Font** | `brew install --cask font-jetbrains-mono-nerd-font` | 下载到 `~/.local/share/fonts/`，`fc-cache -fv` | FiraCode Nerd Font |
| 字号 | **14pt** | 终端/GUI 编辑器统一 | 同左 | — |

**统一透明度/模糊度标准**（支持的工具）：
- **opacity** = 0.92
- **blur** = true（毛玻璃效果）

### 2.1 字体覆盖范围

| 工具类型 | 字体设置 | 字号设置 | 透明度 | 模糊度 | 配置方式 |
|---------|---------|---------|--------|--------|---------|
| **Ghostty** | JetBrainsMono Nerd Font | 14pt | 0.92 | ✓ blur | `~/.config/ghostty/config` |
| **VS Code** | JetBrainsMono Nerd Font | 14pt | macOS 可选 | macOS 可选 | `settings.json` |
| **Obsidian** | JetBrainsMono Nerd Font | 14pt | ❌ | ❌ | Obsidian 设置 |
| **Neovim (GUI)** | JetBrainsMono Nerd Font | 14pt | ✓ 可选 | ✓ 可选 | Neovide 配置 |
| **Neovim (终端)** | 继承 Ghostty | 继承 | ✓ 可选 | 继承 | 终端内运行 |
| **Zellij** | 继承终端 | 继承 | ✓ 透明背景 | 继承 | `~/.config/zellij/config.kdl` |
| **Yazi** | 继承终端 | 继承 | ✓ | 继承 | `~/.config/yazi/theme.toml` |
| **Starship** | 继承终端 | 继承 | 继承 | 继承 | Nerd Font 图标依赖 |
| **FZF/bat/lazygit/lazydocker/bottom/gh-dash/git-delta** | 继承终端 | 继承 | 继承 | 继承 | TUI 工具 |

### 2.2 主题覆盖范围

| 工具 | Dracula 主题 | 透明度支持 | 配置方式 |
|------|-------------|-----------|---------|
| Ghostty | ✓ | opacity=0.92 + blur | `~/.config/ghostty/config` |
| Zellij | ✓ | 透明背景 | `~/.config/zellij/config.kdl` |
| Neovim | ✓ (dracula.nvim) | 可选透明背景 | `~/.config/nvim/` 插件配置 |
| Yazi | ✓ (Dracula flavor) | 支持 | `~/.config/yazi/theme.toml` |
| Starship | ✓ | 继承终端 | `~/.config/starship.toml` |
| FZF | ✓ (Dracula 颜色) | 继承终端 | `FZF_DEFAULT_OPTS` 环境变量 |
| bat | ✓ (`--theme=Dracula`) | 继承终端 | `BAT_THEME` 环境变量 |
| lazygit | ✓ | 继承终端 | `~/.config/lazygit/config.yml` |
| lazydocker | ✓ | 继承终端 | `~/.config/lazydocker/config.yml` |
| bottom (btm) | ✓ | 继承终端 | `~/.config/bottom/bottom.toml` |
| gh-dash | ✓ | 继承终端 | `~/.config/gh-dash/config.yml` |
| git-delta | ✓ (Dracula 颜色) | 继承终端 | `~/.gitconfig` delta 配色 |
| VS Code | ✓ (Dracula Official) | macOS 可选 | 扩展 + settings.json |
| Obsidian | ✓ (Dracula Theme) | ❌ | 社区主题插件 |
| OpenCode | ✓ | 继承终端 | `~/.config/opencode/config.toml` |
| Claude Code | 继承终端 | 继承 Ghostty | 终端内运行 |
| 其他 CLI | 继承终端 | 继承 Ghostty | 终端内运行 |

> **字体统一原则**：终端（Ghostty）和 GUI 编辑器（VS Code、Obsidian）使用 JetBrainsMono Nerd Font 14pt。TUI 工具继承终端字体。Starship 使用 Nerd Font 图标。

---

## 3. 输入法

| 平台 | 工具 | 安装方式 |
|------|------|----------|
| **macOS** | **Squirrel (Rime)** | `brew install --cask squirrel-app` |
| **Linux** | **fcitx5 + fcitx5-rime** | `sudo apt install fcitx5 fcitx5-rime` |

### 3.1 输入法自动切换（Neovim）

| 工具 | macOS 安装 | Linux 安装 | 用途 |
|------|-----------|-----------|------|
| **im-select** | `brew tap daipeihust/tap && brew install im-select` | 不需要 | 获取/设置当前输入法 |

Linux 下 Neovim 配置 `fcitx5-remote` 切换中英文：

```lua
-- ~/.config/nvim/lua/plugins/input.lua
return {
  {
    "keaising/im-select.nvim",
    opts = {
      default_command = "fcitx5-remote",    -- Linux
      -- default_command = "im-select",     -- macOS
    },
  },
}
```

---

## 4. 编辑器

| 工具 | 用途 | macOS 安装 | Linux 安装 | 备选 |
|------|------|------------|------------|------|
| **Neovim** | 主力编辑器 | `brew install neovim` | `apt install neovim` | Helix、Zed |
| **VS Code** | 辅助编辑器 | `brew install --cask visual-studio-code` | `snap install code --classic` | Cursor（AI 增强） |

| 工具 | 配置 | 选型理由 |
|------|------|----------|
| **Neovim** (主) | LazyVim v8 + dracula.nvim | 终端原生，Lua 生态活跃，LSP/DAP/Treesitter 开箱即用 |
| VS Code (辅助) | JetBrainsMono 14pt + Dracula | 仅用于 Neovim 不适配的图形化场景 |

### 4.1 VS Code 字体与主题配置

安装 Dracula 主题扩展：
```bash
code --install-extension dracula-theme.theme-dracula
```

配置文件：
- macOS: `~/Library/Application Support/Code/User/settings.json`
- Linux: `~/.config/Code/User/settings.json`

```json
{
  "editor.fontFamily": "'JetBrainsMono Nerd Font', 'Cascadia Mono NF', monospace",
  "editor.fontSize": 14,
  "workbench.colorTheme": "Dracula"
}
```

### 4.2 Obsidian 字体与主题配置

安装 Dracula 主题：打开 Obsidian → Settings → Community plugins → Browse → 搜索 "Dracula Theme"

配置文件 `<vault>/.obsidian/app.json`：

```json
{
  "theme": "dracula",
  "textFont": "JetBrainsMono Nerd Font",
  "textFontSize": 14,
  "interfaceFont": "JetBrainsMono Nerd Font",
  "interfaceFontSize": 14
}
```

> Obsidian 不支持窗口透明度，使用系统默认窗口样式。

---

## 5. 文件 & 搜索

| 工具 | 替代 | macOS 安装 | Linux 安装 | 选型理由 |
|------|------|------------|------------|----------|
| **fd** | find | `brew install fd` | `apt install fd-find` (→ `fdfind`) | Rust，默认忽略 .gitignore |
| **ripgrep (rg)** | grep | `brew install ripgrep` | `apt install ripgrep` | Rust，PCRE2 正则 |
| **bat** | cat | `brew install bat` | `apt install bat` (→ `batcat`) | Rust，语法高亮、行号 |
| **fzf** | - | `brew install fzf` | `apt install fzf` | Go，模糊搜索 |
| **zoxide** | cd | `brew install zoxide` | `cargo install zoxide` | Rust，智能目录跳转 |
| **Yazi** | ranger/lf | `brew install yazi` | `cargo install yazi-fm` | Rust，异步 I/O，Dracula flavor |

> Linux：`bat` → `batcat`、`fd` → `fdfind`，需建立 `~/.local/bin/bat` 和 `~/.local/bin/fd` 符号链接。

FZF 配置（Dracula 配色）：

```bash
export FZF_DEFAULT_COMMAND="fd --type f --hidden --exclude .git"
export FZF_DEFAULT_OPTS="--color=bg+:#44475a,bg:#282a36,spinner:#f1fa8c,hl:#50fa7b,fg:#f8f8f2,header:#bd93f9,info:#8be9fd,pointer:#ff79c6,marker:#ff79c6,fg+:#f8f8f2,prompt:#bd93f9,hl+:#50fa7b"
```

---

## 6. Git & GitHub 工具链

| 工具 | 用途 | macOS 安装 | Linux 安装 | 选型理由 |
|------|------|------------|------------|----------|
| **git** | 分布式版本控制 | `brew install git` | `apt install git` | 行业标准 |
| **gh** | GitHub CLI | `brew install gh` | `apt install gh` | PR/Issue/Actions 终端管理 |
| **lazygit** | 终端 Git TUI | `brew install lazygit` | `apt install lazygit` | Go，交互式 staging/commit/log |
| **git-delta** | Git diff 美化 | `brew install git-delta` | `cargo install git-delta` | Rust，syntax-highlighted diff |
| **git-extras** | Git 扩展命令集 | `brew install git-extras` | `apt install git-extras` | `git pr`、`git changelog` 等 |
| **act** | 本地运行 GitHub Actions | `brew install act` | `go install github.com/nektos/act@latest` | Go，免推送测试 CI |
| **gh-dash** | 终端 GitHub Dashboard | `gh extension install dlvhdr/gh-dash` | 同左 | Go，TUI 面板查看 PR/Issue |
| **gitleaks** | Git 密钥扫描 | `brew install gitleaks` | `go install github.com/gitleaks/gitleaks/v8@latest` | Go，pre-commit 密钥检测 |

### 6.1 gitconfig 基础配置

```bash
git config --global user.name "viryoke"
git config --global user.email "<USER_EMAIL>"     # ⚠️ 必须替换为真实邮箱
git config --global core.editor "nvim"
git config --global init.defaultBranch "main"
git config --global pull.rebase true
git config --global core.pager "delta"
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global delta.side-by-side true
git config --global delta.light false
# delta Dracula 主题配色
git config --global delta.plus-style "syntax #50fa7b"
git config --global delta.minus-style "syntax #ff5555"
git config --global delta.commit-decoration-style "#50fa7b bold box"
git config --global delta.file-style "#bd93f9 bold"
git config --global delta.hunk-header-style "#ff79c6 bold"
git config --global delta.line-numbers-minus-style "#ff5555"
git config --global delta.line-numbers-plus-style "#50fa7b"
git config --global merge.conflictstyle zdiff3
```

---

## 7. 编程语言开发环境

| 语言/工具 | 用途 | macOS 包管理 | Linux 包管理 | 备选 |
|-----------|------|-------------|-------------|------|
| **Python (Pixi + uv)** | 通用开发 + AI/ML | Pixi (curl) + uv (brew) | Pixi (curl) + uv (curl) | pyenv |
| **Bun** | JavaScript/TypeScript 运行时 | `brew install bun` | `curl -fsSL https://bun.sh/install \| bash` | Node.js、deno |
| **Java** | JVM 生态开发 | `brew install --cask temurin` | `apt install openjdk-21-jdk` | GraalVM |
| **C / C++** | 系统编程 | Xcode CLT + cmake/ninja (brew) | build-essential + cmake/ninja (apt) | Bazel、Meson |
| **Go** | 高性能后端/CLI | `brew install go` | `apt install golang-go` | — |
| **Rust** | 系统编程/CLI 工具 | rustup (brew → curl 回退) | `curl https://sh.rustup.rs \| sh -s -- -y` | — |
| **Kotlin** | JVM 原生语言 | `brew install kotlin` | `snap install kotlin --classic` | — |
| **ArkTS** | 鸿蒙原生开发 | macOS（DevEco Studio） | ❌ 不可用 | — |
| **ruff** | Python Linter + Formatter | `brew install ruff` | `cargo install ruff` | Flake8+Black |

> **Bun 替代 Node.js + TypeScript**：Bun 内置 TypeScript 支持，`bun run` 直接执行 `.ts` 文件，无需 `npm install -g typescript`。
> **Pixi + uv 替代 conda**：Pixi 管理 Python 环境和 conda 级依赖，uv 管理 pip 包（比 pip 快 10-100x）。

### 7.1 多语言运行时安装详情

| 语言 | macOS 安装 | Linux 安装 | 说明 |
|------|-----------|-----------|------|
| **Python** | `curl -fsSL https://pixi.sh/install.sh \| bash` | 同左 | pixi 管理环境；uv 管理 pip 包 |
| **Bun** | `brew install bun` | `curl -fsSL https://bun.sh/install \| bash` | 内置 TS，替代 Node + npm + tsc |
| **Java** | `brew install --cask temurin`（.pkg，手动安装） | `sudo apt install openjdk-21-jdk` | Eclipse Temurin JDK |
| **C / C++** | Xcode CLT (已安装) | `sudo apt install build-essential` (已安装) | 编译链在 §0 已安装 |
| **Go** | `brew install go` | `sudo apt install golang-go` | 当前稳定版 |
| **Rust** | `brew install rustup && rustup-init -y \|\| curl ... sh.rustup.rs \| sh -s -- -y` | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh -s -- -y` | 优先 brew，回退 curl |
| **Kotlin** | `brew install kotlin` | `sudo snap install kotlin --classic` | JVM 原生语言 |

### 7.2 构建工具

| 工具 | macOS 安装 | Linux 安装 | 用途 |
|------|-----------|-----------|------|
| **CMake** | `brew install cmake` | `sudo apt install cmake` | C/C++ 跨平台构建 |
| **Ninja** | `brew install ninja` | `sudo apt install ninja-build` | 高性能增量构建 |
| **Maven** | `brew install maven` | `sudo apt install maven` | Java 构建与依赖管理 |
| **Gradle** | `brew install gradle` | `sudo apt install gradle` | JVM 多语言构建 |

### 7.3 推荐语言环境初始化

```bash
# === Rust（优先安装，cargo 后续会大量使用）===
# macOS
brew install rustup && rustup-init -y || \
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Linux
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# === Bun ===
# macOS: brew install bun
# Linux: curl -fsSL https://bun.sh/install | bash

# === Pixi + uv ===
# macOS: curl -fsSL https://pixi.sh/install.sh | bash && brew install uv
# Linux: curl -fsSL https://pixi.sh/install.sh | bash && curl -LsSf https://astral.sh/uv/install.sh | sh

# === Java ===
# macOS: brew install --cask temurin  # .pkg，手动安装
# Linux: sudo apt install -y openjdk-21-jdk

# === Go ===
# macOS: brew install go
# Linux: sudo apt install -y golang-go

# === Kotlin / 构建工具 ===
# macOS: brew install kotlin cmake ninja maven gradle
# Linux: sudo snap install kotlin --classic && sudo apt install -y cmake ninja-build maven gradle

# === ruff ===
# macOS: brew install ruff
# Linux: cargo install ruff
```

### 7.4 Python 环境（Pixi + uv）

```bash
# 通用开发环境
pixi init ~/projects/py-dev && cd ~/projects/py-dev
pixi add python=3.13
pixi run uv pip install ruff

# AI 学习环境
pixi init ~/projects/ai-learn && cd ~/projects/ai-learn
pixi add python=3.13
```

---

## 8. 容器化

| 平台 | 方案 | 安装 |
|------|------|------|
| **macOS** | Colima + Docker CLI | `brew install colima docker docker-compose lazydocker dive` |
| **Linux** | Docker Engine (原生) | `sudo apt install docker.io docker-compose-v2` |

### 8.1 macOS Colima

```bash
brew install colima docker docker-compose lazydocker dive
colima start --cpu 4 --memory 8 --disk 60
```

### 8.2 Linux Docker Engine

```bash
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
sudo systemctl enable --now docker

# Docker TUI 工具
go install github.com/jesseduffield/lazydocker@latest
go install github.com/wagoodman/dive@latest
```

### 8.3 选型说明

| 方案 | macOS | Linux | 资源占用 |
|------|-------|-------|----------|
| **Colima + Docker CLI** | ✅ 首选 | ❌ 不推荐（原生引擎更好） | 低（≈200MB） |
| **Docker Engine (原生)** | ❌ 不可用 | ✅ 首选 | 极低 |
| OrbStack | ✅ 优质付费 | ❌ 仅 macOS | 极低 |

---

## 9. AI 学习工具链

| 工具 | 用途 | macOS 安装 | Linux 安装 |
|------|------|------------|------------|
| **Ollama** | 本地 LLM 运行时 | `brew install ollama` | `curl -fsSL https://ollama.com/install.sh \| sh` |
| **Open WebUI** | 本地 ChatGPT 风格聊天 | Docker Compose 部署 | 同左 |
| **uv** | Python 包管理器 | `brew install uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **PyTorch** | 深度学习框架 | pixi + uv pip（见下方） | 同左 |
| **MLX** | Apple Silicon 原生 ML | `uv pip install mlx mlx-lm mlx-vlm` | ❌ macOS 独占 |
| **HuggingFace CLI** | 模型/数据集下载 | `uv pip install huggingface-hub` | 同左 |
| **DVC** | 数据与模型版本管理 | `brew install dvc` | `pipx install dvc` |
| **MLflow** | 实验追踪与模型注册 | `uv pip install mlflow` | 同左 |
| **Jupyter Lab** | 交互式数据科学 | `uv pip install jupyterlab` | 同左 |
| **Marimo** | 响应式 Python Notebook | `uv pip install marimo` | 同左 |
| **Aider** | AI 结对编程 | `uv pip install aider-chat` | 同左 |
| **llm** | 终端调用大模型 | `uv pip install llm llm-ollama` | 同左 |

### 9.1 跨平台 AI 概述

| 维度 | macOS (Apple Silicon) | Linux |
|------|-----------------------|-------|
| GPU 后端 | **MPS** (Metal) + **MLX** | **CUDA** (NVIDIA) / **ROCm** (AMD) |
| PyTorch 加速 | `torch` 默认集成 MPS | `torch --index-url cuXXX` |
| 本地推理首选 | MLX (统一内存，零拷贝) | Ollama + CUDA |
| 不可用工具 | CUDA 系、bitsandbytes | **MLX**（Apple Silicon 独占） |

> 各平台优先原生加速方案（MLX / CUDA），再回退到 Ollama + HuggingFace 流水线。

### 9.2 PyTorch 分平台安装

```bash
# macOS (MPS 加速)
uv pip install torch torchvision torchaudio

# Linux (CUDA 12.x)
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Linux (仅 CPU)
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 9.3 AI 环境布局（Pixi + uv）

**macOS (Apple Silicon)**：

```bash
cd ~/projects/ai-learn
pixi run uv pip install torch torchvision torchaudio    # PyTorch MPS
pixi run uv pip install mlx mlx-lm mlx-vlm             # Apple Silicon 原生推理
pixi run uv pip install huggingface-hub jupyterlab marimo mlflow
pixi run uv pip install aider-chat llm llm-ollama
```

**Linux (NVIDIA GPU)**：

```bash
cd ~/projects/ai-learn
pixi run uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pixi run uv pip install huggingface-hub jupyterlab marimo mlflow
pixi run uv pip install aider-chat llm llm-ollama
```

> **Open WebUI**：通过 Docker Compose 部署（`docker compose -f open-webui up -d`）。

---

## 10. AI Agent 平台

| 工具 | 用途 | macOS 安装 | Linux 安装 |
|------|------|------------|------------|
| **OpenCode** | 主 Agent 平台 | `brew install opencode` | `bun install -g opencode` |
| **Claude Code** | 辅助 Agent | `bun install -g @anthropic-ai/claude-code` | 同左 |

---

## 11. 其他 CLI 工具

| 工具 | 用途 | 替代 | macOS 安装 | Linux 安装 |
|------|------|------|------------|------------|
| **bottom (btm)** | 系统资源监控 | top / htop | `brew install bottom` | `cargo install bottom` |
| **eza** | 现代文件列表 | ls | `brew install eza` | `cargo install eza` |
| **tokei** | 代码行数统计 | cloc | `brew install tokei` | `cargo install tokei` |
| **hyperfine** | 命令行基准测试 | time | `brew install hyperfine` | `sudo apt install hyperfine` |
| **dust** | 磁盘使用可视化 | du | `brew install dust` | `cargo install du-dust` |
| **procs** | 进程列表查看 | ps | `brew install procs` | `cargo install procs` |
| **sd** | 直观的查找替换 | sed | `brew install sd` | `cargo install sd-find` |
| **xh** | HTTP 客户端 | httpie / curl | `brew install xh` | `sudo apt install xh` |
| **watchexec** | 文件变更自动执行 | watch | `brew install watchexec` | `cargo install watchexec-cli` |
| **ouch** | 统一解压工具 | tar / unzip / 7z | `brew install ouch` | `cargo install ouch` |
| **gdu** | 磁盘使用分析 TUI | ncdu | `brew install gdu` | `sudo apt install gdu` |

---

## 12. 笔记工具链

| 工具 | 用途 | macOS 安装 | Linux 安装 |
|------|------|------------|------------|
| **Obsidian** | Markdown 知识库（GUI） | `brew install --cask obsidian` | `sudo snap install obsidian --classic` |
| **marksman** | Markdown LSP | `brew install marksman` | `cargo install marksman` |
| **pandoc** | 通用文档格式转换 | `brew install pandoc` | `sudo apt install pandoc` |

### 12.1 Obsidian + Neovim 集成

| 组件 | 安装方式 | 用途 |
|------|----------|------|
| **Obsidian** | macOS brew cask / Linux snap | 图形界面知识库管理 |
| **obsidian.nvim** | LazyVim 插件（`epwalsh/obsidian.nvim`） | Neovim 内编辑 Obsidian Vault |
| **marksman** | macOS brew / Linux cargo | Markdown LSP，链接/引用补全 |

### 12.2 PDF 导出（按需）

| 工具 | macOS | Linux |
|------|-------|-------|
| **basictex** | `brew install --cask basictex` | `sudo apt install texlive-latex-base` |

---

## 13. 声明式依赖管理

### macOS (Brewfile)

```ruby
# Brewfile — macOS 声明式工具链
# 使用方式：brew bundle --file=Brewfile
# 注意：仅适用于 macOS，Linux 使用 apt list / Cargo.toml

# === 终端 & Shell ===
brew "starship"
brew "zellij"
cask "ghostty"

# === 字体 ===
cask "font-jetbrains-mono-nerd-font"
cask "font-cascadia-mono-nf"

# === 编辑器 ===
brew "neovim"
cask "visual-studio-code"

# === 文件 & 搜索 ===
brew "fd"
brew "ripgrep"
brew "bat"
brew "fzf"
brew "zoxide"
brew "yazi"

# === Git ===
brew "git"
brew "gh"
brew "lazygit"
brew "git-delta"
brew "git-extras"
brew "act"
brew "gitleaks"

# === 编程语言 ===
brew "bun"
brew "go"
brew "kotlin"
brew "cmake"
brew "ninja"
brew "maven"
brew "gradle"
brew "ruff"
brew "rustup"
brew "uv"
cask "temurin"

# === 容器化 ===
brew "colima"
brew "docker"
brew "docker-compose"
brew "lazydocker"
brew "dive"

# === AI ===
brew "ollama"
brew "dvc"
brew "opencode"

# === CLI 工具 ===
brew "bottom"
brew "eza"
brew "tokei"
brew "hyperfine"
brew "dust"
brew "procs"
brew "sd"
brew "xh"
brew "watchexec"
brew "ouch"
brew "gdu"

# === 笔记 ===
cask "obsidian"
brew "marksman"
brew "pandoc"
```

### Linux (脚本化)

Linux 工具链通过 apt/cargo/curl/snap 组合安装，不便用单一声明式文件管理。推荐将安装命令写入脚本，参考 `scripts.md`。

---

## 14. 一键安装脚本

### macOS

```bash
# === 终端 & Shell ===
brew install --cask ghostty
brew install starship zellij

# === 字体 ===
brew install --cask font-jetbrains-mono-nerd-font font-cascadia-mono-nf

# === 输入法 ===
brew install --cask squirrel-app
brew tap daipeihust/tap && brew install im-select


# === 编辑器 ===
brew install neovim
brew install --cask visual-studio-code

# === 文件 & 搜索 ===
brew install fd ripgrep bat fzf zoxide yazi
$(brew --prefix)/opt/fzf/install --all --no-bash --no-fish --no-update-rc

# === Git & GitHub ===
brew install git gh lazygit git-delta git-extras act gitleaks
# gh extension install dlvhdr/gh-dash    # 需先 gh auth login

# === 编程语言 ===
# Rust（优先，cargo 后续被大量使用）
brew install rustup && rustup-init -y || \
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

brew install bun
curl -fsSL https://pixi.sh/install.sh | bash
brew install uv
# brew install --cask temurin    # .pkg cask，手动安装
brew install go kotlin cmake ninja maven gradle ruff

# === 容器化 ===
brew install colima docker docker-compose lazydocker dive
# colima start --cpu 4 --memory 8 --disk 60    # 手动执行

# === AI ===
brew install ollama dvc opencode
bun install -g @anthropic-ai/claude-code

# pixi 环境
pixi init ~/projects/py-dev -y && cd ~/projects/py-dev && pixi add python=3.13
pixi init ~/projects/ai-learn -y && cd ~/projects/ai-learn && pixi add python=3.13

# === CLI 工具 ===
brew install bottom eza tokei hyperfine dust procs sd xh watchexec ouch gdu

# === 笔记 ===
brew install --cask obsidian
brew install marksman pandoc
```

### Linux (Ubuntu/Debian)

```bash
# === 前置 ===
sudo apt update -y
sudo apt install -y build-essential curl file git procps zsh

# === 终端 & Shell ===
# Ghostty（从 GitHub Release 下载）
curl -fsSL https://github.com/ghostty-org/ghostty/releases/latest/download/ghostty_amd64.deb -o /tmp/ghostty.deb
sudo dpkg -i /tmp/ghostty.deb

# === 字体 ===
mkdir -p ~/.local/share/fonts
curl -fsSL https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.tar.xz -o /tmp/JetBrainsMono.tar.xz
tar -xf /tmp/JetBrainsMono.tar.xz -C ~/.local/share/fonts/ && fc-cache -fv

# === 输入法 ===
sudo apt install -y fcitx5 fcitx5-rime xclip wl-clipboard

# === 编辑器 ===
sudo apt install -y neovim
sudo snap install code --classic

# === 文件 & 搜索 ===
sudo apt install -y ripgrep fd-find bat fzf lazygit git-extras
# bat/fd 符号链接
mkdir -p ~/.local/bin
ln -sf $(which batcat) ~/.local/bin/bat 2>/dev/null || true
ln -sf $(which fdfind) ~/.local/bin/fd 2>/dev/null || true

# === Git & GitHub ===
sudo apt install -y git gh

# === 编程语言 ===
# Rust（优先，cargo 后续被大量使用）
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

curl -fsSL https://bun.sh/install | bash
curl -fsSL https://pixi.sh/install.sh | bash
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo apt install -y openjdk-21-jdk golang-go cmake ninja-build maven gradle
sudo snap install kotlin --classic

# Rust CLI 工具（通过 cargo）
cargo install starship zellij zoxide yazi-fm git-delta eza bottom tokei du-dust procs sd-find watchexec-cli ouch ruff marksman

# === 容器化 ===
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER

# Docker TUI
go install github.com/jesseduffield/lazydocker@latest
go install github.com/wagoodman/dive@latest

# Git 工具
go install github.com/nektos/act@latest
go install github.com/gitleaks/gitleaks/v8@latest

# === AI ===
curl -fsSL https://ollama.com/install.sh | sh
pipx install dvc
bun install -g opencode
bun install -g @anthropic-ai/claude-code

# pixi 环境
pixi init ~/projects/py-dev -y && cd ~/projects/py-dev && pixi add python=3.13
pixi init ~/projects/ai-learn -y && cd ~/projects/ai-learn && pixi add python=3.13

# === CLI 工具 ===
sudo apt install -y hyperfine gdu xh

# === 笔记 ===
sudo snap install obsidian --classic
sudo apt install -y pandoc
```

---

## 15. 配置文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| Shell 配置 | `~/.zshrc` | PATH、别名、Starship/Zellij 初始化、FZF 配置 |
| Starship 配置 | `~/.config/starship.toml` | Dracula 主题，模块化 prompt |
| Ghostty 配置 | `~/.config/ghostty/config` | Dracula 主题，JetBrainsMono Nerd Font 14pt，透明度 0.92 + blur |
| Zellij 配置 | `~/.config/zellij/config.kdl` | Dracula 主题，透明背景 |
| Neovim 配置 | `~/.config/nvim/` | LazyVim v8，dracula.nvim |
| Yazi 配置 | `~/.config/yazi/` | `package.toml` 声明插件，`theme.toml` Dracula flavor |
| lazygit 配置 | `~/.config/lazygit/config.yml` | Dracula 主题配色 |
| lazydocker 配置 | `~/.config/lazydocker/config.yml` | Dracula 主题配色 |
| bottom 配置 | `~/.config/bottom/bottom.toml` | Dracula 主题配色 |
| gh-dash 配置 | `~/.config/gh-dash/config.yml` | Dracula 主题配色 |
| gitconfig delta | `~/.gitconfig` | `[delta]` 样式 key 配置 Dracula 色板 |
| VS Code 配置 | `settings.json` | JetBrainsMono Nerd Font 14pt，Dracula 扩展 |
| Obsidian 配置 | `<vault>/.obsidian/app.json` | JetBrainsMono Nerd Font 14pt，Dracula 主题插件 |
| OpenCode 配置 | `~/.config/opencode/config.toml` | `theme = "dracula"` |

---

## 16. 一键更新

```bash
# macOS
brew update && brew upgrade && brew upgrade --cask --greedy
bun update

# Linux
sudo apt update && sudo apt upgrade -y
# cargo-installed 工具
cargo install --list | grep -E '^[a-zA-Z]' | awk '{print $1}' | xargs -n1 cargo install
bun update

# pixi 更新
pixi self-update

# Neovim 插件更新（在 nvim 内）
:Lazy update

# Yazi 插件更新
ya pkg upgrade

# Docker 清理
docker system prune -f

# Ollama 模型拉取
ollama pull qwen3:latest
```

---

## 17. 跨平台差异

| 场景 | macOS | Linux |
|------|-------|-------|
| 包管理器 | Homebrew | apt (系统包) + cargo (Rust CLI) + curl (脚本安装) + snap (GUI) |
| 终端 | Ghostty.app (cask) | Ghostty (deb/AppImage) |
| 中文输入法 | Squirrel (Rime) | fcitx5-rime (apt) |
| 输入法切换 | im-select | fcitx5-remote |
| 剪贴板 | 内置 pbcopy/pbpaste | xclip / wl-clipboard (apt) |
| 字体注册 | 系统级安装 (cask) | 手动 → `~/.local/share/fonts/` → `fc-cache -fv` |
| 容器运行时 | Colima (Lima VM) | Docker Engine 原生 (apt) |
| C/C++ 编译器 | Apple Clang (Xcode CLT) | GCC (build-essential) |
| JDK | Temurin (brew cask, .pkg) | OpenJDK (apt) |
| Kotlin | brew | snap |
| JS 运行时 | Bun (brew) | Bun (curl) |
| Python 环境 | Pixi (curl) + uv (brew) | Pixi (curl) + uv (curl) |
| AI 推理加速 | MLX (Apple Silicon 专用) + MPS | CUDA (NVIDIA) / ROCm (AMD) |
| LLM 运行时 | Ollama (brew) | Ollama (curl) |
| 笔记 | Obsidian.app (brew cask) | Obsidian (snap) |

---

## 18. 自动化约束

Agent 执行安装时必须遵循：

- 所有安装命令必须带非交互参数（`--yes` / `-y` / `--no-confirm`）
- macOS 优先 Homebrew；Linux 使用 apt（系统包）、cargo（Rust CLI）、curl/snap 组合
- 禁止 `git clone ... && make && make install` 源码编译（Rust 除外）
- 禁止 GUI 安装指引，所有操作在终端内完成
- 创建文件/目录前需先用 `ls` 验证父路径存在
