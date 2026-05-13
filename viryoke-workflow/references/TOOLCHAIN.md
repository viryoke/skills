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
- [13. 声明式依赖管理 (Brewfile)](#13-声明式依赖管理-brewfile)
- [14. 一键安装脚本](#14-一键安装脚本)
- [15. 配置文件清单](#15-配置文件清单)
- [16. 一键更新](#16-一键更新)
- [17. 跨平台差异](#17-跨平台差异)
- [18. 自动化约束](#18-自动化约束)

---

## 0. 前置条件

| 工具 | 用途 | 兼容平台 | 备选/备注 |
|------|------|----------|-----------|
| **Xcode Command Line Tools** | 编译链（git/make/gcc/clang） | macOS | 仅 macOS 需要，Linux 用 build-essential |
| **Homebrew** | 统一包管理器 | macOS / Linux / WSL2 | 唯一 sudo 步骤 |

后续所有工具统一通过 Homebrew 安装，因此 **Homebrew 本身是唯一的 sudo 例外**——必须事先手动完成。

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
# 安装编译依赖链（需要 sudo，Homebrew 编译公式时依赖）
sudo apt-get update -y
sudo apt-get install -y build-essential curl file git procps

# 安装 Homebrew on Linux（非交互，安装到 /home/linuxbrew/.linuxbrew）
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 将 Homebrew 加入 PATH
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# 安装后移除 sudo 权限 —— 此后所有 brew install 均为普通用户执行
```

### 0.3 Windows (WSL2)

以管理员身份打开 PowerShell：

```powershell
# 启用 WSL 并安装 Ubuntu
wsl --install -d Ubuntu
```

进入 WSL2 Ubuntu 后，按 **0.2 Linux** 步骤执行。Windows 侧字体和输入法在 **0.4** 单独处理。

### 0.4 说明

| 操作 | 是否需 sudo | 原因 |
|------|-------------|------|
| 安装 Homebrew | **是（仅此一次）** | macOS 安装脚本需写 `/opt/homebrew`；Linux 需装 `build-essential` 等系统包 |
| 之后所有 `brew install` | **否** | Homebrew 在用户目录 `/home/linuxbrew` 或 `/opt/homebrew` 下运行，无需 root |
| Windows 侧 winget/字体 | **否** | 用户级安装 |

---

## 1. 终端 & Shell

| 工具 | 用途 | 安装方式 | 兼容平台 | 备选/选型理由 |
|------|------|----------|----------|---------------|
| **Ghostty** | 终端模拟器 | `brew install --cask ghostty` | macOS / Linux | Zig + Swift，GPU 加速，内置 Tab/Split。备选：Alacritty、Kitty |
| **zsh** | 交互 Shell | 系统内置 | macOS / Linux / WSL2 | 默认 Shell，插件生态丰富。备选：fish（不兼容 bash） |
| **Starship** | Shell 提示符 | `brew install starship` | 全平台（所有 Shell） | Rust，<1ms 渲染，单一 TOML 配置。备选：oh-my-posh |
| **Zellij** | 终端复用器 | `brew install zellij` | macOS / Linux / WSL2 | Rust，session/layout/浮动面板。Ghostty 已内置 Tab/Split，Zellij 用于持久化 |

### 1.1 Shell 别名

```bash
alias ll="ls -la"
alias l="ls -l"
alias ..="cd .."
alias ...="cd ../.."
alias g="git"
alias v="nvim"
alias vi="nvim"
alias vim="nvim"
alias ls="eza --group-directories-first"
alias top="btm 2>/dev/null || top"
alias y="yazi"

# bat 主题（通过环境变量设置，不覆盖 cat 避免破坏脚本）
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

> 说明：Ghostty 设置 `TERM=xterm-ghostty` 而非 `TERM_PROGRAM=Ghostty`，检查需同时覆盖 `TERM`（识别 Ghostty）和 `TERM_PROGRAM`（识别 iTerm2/Apple Terminal），另有 `VSCODE_INJECTION` 排除 VS Code 终端。

---

## 2. 主题 & 字体

| 组件 | 选型 | 安装方式 | 备选 |
|------|------|----------|------|
| 主题 | **Dracula** | 全局配色 #282a36 / #f8f8f2 | Catppuccin、Tokyo Night |
| 主字体 | **JetBrainsMono Nerd Font** | `brew install --cask font-jetbrains-mono-nerd-font` | FiraCode Nerd Font |
| 备用字体 | **Cascadia Mono NF** | `brew install --cask font-cascadia-mono-nf` | — |
| 字号 | **14pt** | 终端/GUI 编辑器统一 | — |

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

> **字体统一原则**：终端（Ghostty）和 GUI 编辑器（VS Code、Obsidian）使用 JetBrainsMono Nerd Font 14pt。TUI 工具继承终端字体。Starship 使用 Nerd Font 图标，需确保字体包含图标支持。
>
> **透明度统一原则**：Ghostty 设置 opacity=0.92 + blur，Zellij、Neovim 终端版继承此效果。GUI 应用（VS Code macOS、Neovide）可选透明度。Obsidian 不支持透明度。
>
> **TUI 工具主题统一**：lazygit、lazydocker、bottom、gh-dash 均支持自定义配色，应配置 Dracula 颜色以保持视觉一致性。git-delta 通过 `[delta]` 节下的样式 key 配置 Dracula 色板。

---

## 3. 输入法

| 工具 | 用途 | 兼容平台 | 备选 |
|------|------|----------|------|
| **Rime**（Squirrel/fcitx5-rime/Weasel） | 中文输入法引擎 | macOS / Linux / Windows | 系统自带拼音 |
| **im-select** | 输入法切换（Neovim Normal 切英文） | macOS / Linux | — |
| **cc-switch** | 输入法切换守护进程 | macOS | 非必装 |

### 3.1 中文拼音输入法

| 平台 | 工具 | 安装方式 | 说明 |
|------|------|----------|------|
| **macOS** | **Squirrel (Rime)** | `brew install --cask squirrel-app` | 开源可定制，拼音/五笔/双拼统一支持 |
| **Linux** | **fcitx5 + fcitx5-rime** | `brew install fcitx5 fcitx5-rime` | 通过 Rime 配置拼音方案，跨发行版一致 |
| **Windows (WSL2)** | Windows 侧安装 **小狼毫 (weasel)** | `winget install Rime.Weasel` | Rime 前端，与 macOS/Linux Rime 共用配置 |

### 3.2 输入法自动切换（Neovim）

| 工具 | 安装 | 用途 |
|------|------|------|
| **im-select** | `brew tap daipeihust/tap && brew install im-select` | 获取/设置当前输入法，Neovim Normal 模式切为英文 |
| **cc-switch** | `brew install --cask cc-switch` | 输入法切换守护进程，配合 im-select 使用（仅 macOS，非必装） |

Linux/WSL2 下 Neovim 需配置调用 fcitx5-remote 切换中英文：
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

| 工具 | 用途 | 兼容平台 | 备选 |
|------|------|----------|------|
| **Neovim** | 主力编辑器（终端原生） | macOS / Linux / WSL2 | Helix、Zed |
| **VS Code** | 辅助编辑器（图形化场景） | 全平台 | Cursor（AI 增强）、Zed（GPU 加速） |

| 工具 | 安装 | 配置 | 选型理由 |
|------|------|------|----------|
| **Neovim** (主) | `brew install neovim` | LazyVim v8 + dracula.nvim | 终端原生，Lua 生态活跃，LSP/DAP/Treesitter 开箱即用 |
| VS Code (辅助) | `brew install --cask visual-studio-code` | JetBrainsMono 14pt + Dracula | 仅用于 Neovim 不适配的图形化场景 |

### 4.1 VS Code 字体与主题配置

安装 Dracula 主题扩展：
```bash
code --install-extension dracula-theme.theme-dracula
```

配置文件 `~/Library/Application Support/Code/User/settings.json`（macOS）：
```json
{
  "editor.fontFamily": "'JetBrainsMono Nerd Font', 'Cascadia Mono NF', monospace",
  "editor.fontSize": 14,
  "editor.fontLigatures": true,
  "workbench.colorTheme": "Dracula",
  "workbench.fontAliasing": "antialiased",
  // macOS 透明度（可选，需第三方扩展支持）
  "window.opacity": 0.92
}
```

> Linux/WSL2 路径：`~/.config/Code/User/settings.json`

### 4.2 Obsidian 字体与主题配置

安装 Dracula 主题：
- 打开 Obsidian → Settings → Community plugins → Browse → 搜索 "Dracula Theme"

配置文件 `~/Obsidian/Notes/.obsidian/app.json`：
```json
{
  "theme": "dracula",
  "accentColor": "#bd93f9",
  "textFont": "JetBrainsMono Nerd Font",
  "textFontSize": 14,
  "interfaceFont": "JetBrainsMono Nerd Font",
  "interfaceFontSize": 14
}
```

> Obsidian 不支持窗口透明度，使用系统默认窗口样式。

---

## 5. 文件 & 搜索

| 工具 | 替代 | 安装 | 选型理由 |
|------|------|------|----------|
| **fd** | find | `brew install fd` | Rust，默认忽略 .gitignore |
| **ripgrep (rg)** | grep | `brew install ripgrep` | Rust，默认忽略 .gitignore，PCRE2 正则 |
| **bat** | cat | `brew install bat` | Rust，语法高亮、行号、Git 变更标记 |
| **fzf** | - | `brew install fzf` | Go，模糊搜索，交互式选择 |
| **zoxide** | cd | `brew install zoxide` | Rust，智能目录跳转 |
| **Yazi** | ranger/lf | `brew install yazi` | Rust，异步 I/O，图像预览，Dracula flavor |

FZF 配置（Dracula 配色）：
```bash
export FZF_DEFAULT_COMMAND="fd --type f --hidden --exclude .git"
export FZF_DEFAULT_OPTS="--color=bg+:#44475a,bg:#282a36,spinner:#f1fa8c,hl:#50fa7b,fg:#f8f8f2,header:#bd93f9,info:#8be9fd,pointer:#ff79c6,marker:#ff79c6,fg+:#f8f8f2,prompt:#bd93f9,hl+:#50fa7b"
```

---

## 6. Git & GitHub 工具链

| 工具 | 用途 | 安装 | 选型理由 |
|------|------|------|----------|
| **git** | 分布式版本控制 | `brew install git` | 行业标准，无替代 |
| **gh** | GitHub CLI | `brew install gh` | PR/Issue/Actions/Release 全终端管理 |
| **lazygit** | 终端 Git TUI | `brew install lazygit` | Go，交互式 staging/commit/log/branch/rebase。备选：gitui |
| **git-delta** | Git diff 美化 | `brew install git-delta` | Rust，语法高亮 diff、行号、side-by-side 视图 |
| **git-extras** | Git 扩展命令集 | `brew install git-extras` | `git pr`、`git changelog`、`git summary` 等便捷子命令 |
| **act** | 本地运行 GitHub Actions | `brew install act` | Go，免推送测试 CI 流程。需 Docker（Colima） |
| **gh-dash** | 终端 GitHub Dashboard | `gh extension install dlvhdr/gh-dash` | Go，TUI 面板查看 PR/Issue/Workflow |
| **gitleaks** | Git 密钥扫描 | `brew install gitleaks` | Go，pre-commit 自动检测硬编码密钥 |

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

> delta 是 pager 而非 difftool，通过 `core.pager` 和 `interactive.diffFilter` 配置，不要设置 `diff.tool`。delta 配色使用 Dracula 色板（`[delta]` 节下的顶层 key，无 `colors` 子命名空间）。

---

## 7. 编程语言开发环境

| 语言/工具 | 用途 | 兼容平台 | 包管理 | 备选 |
|-----------|------|----------|--------|------|
| **Python (Miniconda)** | 通用开发 + AI/ML | macOS / Linux / WSL2 | conda / uv | pyenv |
| **Node.js** | JavaScript/TypeScript 运行时 | 全平台 | npm / npx | bun、deno |
| **Java (Temurin)** | JVM 生态开发 | 全平台 | Maven / Gradle | OpenJDK、GraalVM |
| **C / C++** | 系统编程 | 全平台 | CMake + Ninja | Bazel、Meson |
| **Go** | 高性能后端/CLI 开发 | 全平台 | go mod | — |
| **Rust** | 系统编程/CLI 工具开发 | 全平台 | cargo | — |
| **Kotlin** | JVM 原生语言 | 全平台 | Gradle (Kotlin DSL) | — |
| **ArkTS** | 鸿蒙原生开发 | macOS（DevEco Studio） | ohpm | — |
| **ruff** | Python Linter + Formatter | macOS / Linux / WSL2 | — | Flake8+Black |
| **TypeScript** | 类型检查 + 编译 (tsc) | 全平台 | npm | — |
| **mise** | 多语言运行时版本管理 | 全平台 | — | asdf、nvm、pyenv（mise 统一替代） |

### 7.1 多语言运行时

| 语言 | 安装方式 | 包管理器 | 构建工具 | 说明 |
|------|----------|----------|----------|------|
| **Python** | Miniconda (`brew install --cask miniconda`) | conda / uv | ruff | conda 环境隔离；ruff 替代 Flake8+Black+isort |
| **JavaScript / TypeScript** | `brew install node` | npm / npx | - | Node.js 当前 LTS |
| **TypeScript** | `npm install -g typescript` | - | tsc | 类型检查 + 编译 |
| **Java** | `brew install --cask temurin` | - | Maven / Gradle | Eclipse Temurin JDK（如需 LTS：`brew install --cask temurin@21`），跨平台一致 |
| **C / C++** | Xcode CLT (macOS) / `brew install gcc` (Linux) | - | CMake + Ninja | 编译链在 0.1 已安装 |
| **Go** | `brew install go` | go mod | go build | 当前稳定版 |
| **Rust** | `brew install rustup && rustup-init -y` | cargo | cargo | 优先 brew 安装 rustup，回退 curl 官方脚本 |
| **Kotlin** | `brew install kotlin` | - | Gradle (Kotlin DSL) | JVM 原生语言，与 Java 生态无缝集成 |
| **ArkTS** | DevEco Studio CLI | ohpm | hvigor | 鸿蒙原生语言，需 HarmonyOS SDK |
| **mise** | `brew install mise` | 多语言版本管理 | - | 统一替代 asdf/nvm/pyenv，可选方案 |

### 7.2 构建工具

| 工具 | 安装 | 用途 | 选型理由 |
|------|------|------|----------|
| **CMake** | `brew install cmake` | C/C++ 跨平台构建 | 事实标准，支持 Ninja/Make/Xcode 多种生成器 |
| **Ninja** | `brew install ninja` | 高性能增量构建 | 比 Make 更快，CMake 默认推荐后端 |
| **Maven** | `brew install maven` | Java 项目构建与依赖管理 | Java 生态最广泛的构建工具 |
| **Gradle** | `brew install gradle` | JVM 多语言构建 (Java/Kotlin) | Kotlin DSL 支持，Android/Spring 官方推荐 |
| **make** | 系统内置 (Xcode CLT) | 通用构建自动化 | POSIX 标准，所有平台内置 |

### 7.3 ArkTS / HarmonyOS 开发

由于 HarmonyOS 工具链依赖 IDE（DevEco Studio），不完全符合终端闭环原则，此处列出 CLI 替代方案：

| 工具 | 安装 | 用途 |
|------|------|------|
| **ohpm** | 随 DevEco Studio 安装，路径在 `~/Library/Huawei/ohpm/bin` | HarmonyOS 包管理器（类 npm） |
| **hvigor** | 随 DevEco Studio 安装 | HarmonyOS 构建工具（类 Gradle） |
| **hdc** | 随 DevEco Studio 安装 | HarmonyOS 设备调试桥（类 adb） |

> **建议**：终端开发使用 Neovim + hvigor CLI，调试/预览使用 DevEco Studio 图形界面。

### 7.4 推荐语言环境初始化

```bash
# Java (Temurin JDK)
brew install --cask temurin
brew install maven gradle

# C/C++
brew install cmake ninja

# Kotlin
brew install kotlin

# TypeScript (全局)
npm install -g typescript

# Python 环境原则
# 避免 pip 全局安装包，统一通过 conda 环境隔离
# 首次使用需先执行: conda init zsh
brew install ruff                        # Python 极速 Linter + Formatter
conda create -n py-dev python=3.13 -y     # 通用开发
conda create -n ai-learn python=3.13 -y   # AI 学习（见第 9 节）
# Open WebUI 推荐通过 Docker 部署（见第 8 节）

# Rust（优先 brew，回退 curl）
brew install rustup && rustup-init -y || \
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
```

> **备选方案**：如果需要在多个项目间管理不同的语言运行时版本，可考虑 `brew install mise`（统一替代 asdf/nvm/pyenv）。

---

## 8. 容器化

| 工具 | 用途 | 安装 | 选型理由 |
|------|------|------|----------|
| **Colima** | 容器运行时（Docker 替代） | `brew install colima` | Go，极简二进制，macOS/Linux 统一，无需 Docker Desktop |
| **Docker CLI** | Docker 客户端 | `brew install docker` | 与 Colima 启动的 dockerd 配合，命令完全兼容 |
| **Docker Compose** | 多容器编排 | `brew install docker-compose` | 或使用 `docker compose` 子命令 |
| **lazydocker** | 终端 Docker 管理 TUI | `brew install lazydocker` | Go，TUI 管理容器/镜像/日志/卷 |
| **dive** | 镜像层分析 | `brew install dive` | Go，逐层查看镜像大小变化，定位臃肿层 |

### 8.1 Colima 初始化

```bash
# 启动（默认 2 CPU / 2GB / Docker 引擎）
colima start

# 自定义配置启动
colima start --cpu 4 --memory 8 --disk 60

# 状态查看
colima status
colima list
```

Docker CLI 自动连接 Colima 的 socket，后续 `docker ps` / `docker compose` 等命令开箱即用。

### 8.2 选型说明

| 方案 | 跨平台 | 资源占用 | 推荐场景 |
|------|--------|----------|----------|
| **Colima + Docker CLI** | ✅ macOS/Linux | 低（≈200MB） | 个人本地开发，轻量级首选 |
| Docker Engine | ✅ Linux/WSL2 | 极低 | WSL2 首选（避免嵌套虚拟化） |
| Docker Desktop | ⚠️ Windows 收费 | 高（≈2GB） | 团队标准化环境 |
| OrbStack | ❌ 仅 macOS | 极低 | macOS 追求极致性能 |
| Podman | ✅ | 低 | 无守护进程场景，兼容性略差 |

> **结论**：macOS/Linux 使用 Colima，WSL2 使用 Docker Engine（嵌套虚拟化下 Colima 性能极差）。

---

## 9. AI 学习工具链

| 工具 | 用途 | 安装 | 选型理由 |
|------|------|------|----------|
| **Ollama** | 本地 LLM 运行时 | `brew install ollama` | Go，一行拉模型，API 兼容 OpenAI |
| **Open WebUI** | 本地 ChatGPT 风格聊天 | Docker Compose 部署（推荐） | 对接 Ollama API，RAG/多模型，需容器化环境 |
| **uv** | Python 包管理器 | `brew install uv` | Rust，比 pip 快 10-100x，自带虚拟环境和 lockfile |
| **PyTorch** | 深度学习框架 | 分平台 pip install（见下方） | 工业界主流，动态计算图 |
| **MLX** | Apple Silicon 原生 ML 框架 | `pip install mlx mlx-lm mlx-vlm` | **macOS 独占**，统一内存，零拷贝推理 |
| **HuggingFace CLI** | 模型/数据集下载 | `pip install huggingface-hub` | 全球最大模型仓库 |
| **DVC** | 数据与模型版本管理 | `brew install dvc` | Git for Data，远程存储支持 |
| **MLflow** | 实验追踪与模型注册 | `pip install mlflow` | 最广泛 MLOps 实验管理 |
| **Jupyter Lab** | 交互式数据科学实验 | `pip install jupyterlab` | 标准 Notebook，插件生态丰富 |
| **Marimo** | 响应式 Python Notebook | `pip install marimo` | 自动追踪依赖，确定性执行，`.py` 格式版控 |
| **Aider** | AI 结对编程 | `pip install aider-chat` | 终端原生，多模型，Git 自动提交 |
| **llm** | 终端一键调用大模型 | `pip install llm llm-ollama` | 极简 CLI，多后端插件体系 |

### 9.1 跨平台概述

| 维度 | macOS (Apple Silicon) | Linux (x86_64) | Windows (WSL2) |
|------|-----------------------|----------------|----------------|
| GPU 后端 | **MPS** (Metal Performance Shaders) + **MLX** | **CUDA** (NVIDIA) / **ROCm** (AMD) | **CUDA** (WSL2 直通) |
| PyTorch 加速 | `torch` 默认集成 MPS | `torch --index-url cuXXX` 指定 CUDA 版本 | 同 Linux CUDA |
| 本地推理首选 | MLX (统一内存，零拷贝) | Ollama + CUDA | Ollama + CUDA |
| 不可用工具 | CUDA 系（无 NVIDIA GPU）、bitsandbytes | **MLX**（Apple Silicon 独占） | **MLX**（Apple Silicon 独占） |

> **选型原则**：优先使用各平台原生加速方案（MLX / CUDA），再回退到统一的 Ollama + HuggingFace 流水线。
>
> **备选 Python 环境管理**：uv 已支持完整项目管理（`uv init` / `uv run` / `uv lock`），长远可考虑用 uv 替代 conda 作为 Python 环境管理器。当前仍推荐 conda 以保证 AI/ML 库的二进制兼容性。

### 9.2 PyTorch 分平台安装

```bash
# macOS (MPS 加速，默认内置)
uv pip install torch torchvision torchaudio

# Linux / WSL2 (CUDA 12.x)
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# Linux (仅 CPU，无 NVIDIA GPU 时)
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 9.3 推荐 conda 环境布局（分平台）

**macOS (Apple Silicon)**：
```bash
conda create -n ai-learn python=3.13 -y
conda activate ai-learn

uv pip install torch torchvision torchaudio    # PyTorch MPS (macOS)
uv pip install mlx mlx-lm mlx-vlm             # Apple Silicon 原生推理
uv pip install huggingface-hub jupyterlab marimo
uv pip install mlflow
uv pip install aider-chat llm llm-ollama
```

**Linux / WSL2 (NVIDIA GPU)**：
```bash
conda create -n ai-learn python=3.13 -y
conda activate ai-learn

uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126  # CUDA 12.x
uv pip install bitsandbytes                     # 量化推理（Linux/WSL2 CUDA）
uv pip install huggingface-hub jupyterlab marimo
uv pip install mlflow
uv pip install aider-chat llm llm-ollama
```

**Linux (仅 CPU)**：
```bash
conda create -n ai-learn python=3.13 -y
conda activate ai-learn

uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
uv pip install huggingface-hub jupyterlab marimo
uv pip install mlflow
uv pip install aider-chat llm llm-ollama
```

> **Open WebUI**：推荐通过 Docker Compose 部署（`docker compose -f open-webui up -d`），完整的 RAG/多模型功能依赖容器化环境。`pip install open-webui` 仅安装 Python 包，功能受限。

---

## 10. AI Agent 平台

| 工具 | 用途 | 兼容平台 | 备选 |
|------|------|----------|------|
| **OpenCode** | 主 Agent 平台 | macOS / Linux / WSL2 | — |
| **Claude Code** | 辅助 Agent | 全平台（Node.js） | — |
| **Codex** | 辅助 Agent | 全平台 | — |
| **Antigravity** | 自定义 Agent 工具 | macOS / Linux | — |

| 工具 | 安装方式 | 用途 |
|------|----------|------|
| **OpenCode** | `brew install opencode` | 主 Agent 平台 |
| **Claude Code** | `npm install -g @anthropic-ai/claude-code` | 辅助 Agent |
| **Codex** | 按官方指引 | 辅助 Agent |
| **Antigravity** | 自定义路径 `~/.antigravity/antigravity/bin` | 自定义 Agent 工具 |

---

## 11. 其他 CLI 工具

| 工具 | 用途 | 替代 | 安装 | 选型理由 |
|------|------|------|------|----------|
| **bottom (btm)** | 系统资源监控 | top / htop | `brew install bottom` | Rust，彩色 TUI 资源监控 |
| **eza** | 现代文件列表 | ls | `brew install eza` | Rust，图标/颜色/树状展示 |
| **tokei** | 代码行数统计 | cloc | `brew install tokei` | Rust，比 cloc 快 100x |
| **hyperfine** | 命令行基准测试 | time | `brew install hyperfine` | Rust，统计预热/异常值检测 |
| **dust** | 磁盘使用可视化 | du | `brew install dust` | Rust，树状展示 |
| **procs** | 进程列表查看 | ps | `brew install procs` | Rust，彩色输出 |
| **sd** | 直观的查找替换 | sed | `brew install sd` | Rust，正则替换 |
| **xh** | HTTP 客户端 | httpie / curl | `brew install xh` | Rust，免 Python 依赖 |
| **watchexec** | 文件变更自动执行命令 | watch | `brew install watchexec` | Rust，文件监控+命令执行 |
| **ouch** | 统一解压工具 | tar / unzip / 7z | `brew install ouch` | Rust，免记参数 |
| **gdu** | 磁盘使用分析 TUI | ncdu | `brew install gdu` | Go，比 ncdu 更快 |

---

## 12. 笔记工具链

| 工具 | 用途 | 兼容平台 | 备选 |
|------|------|----------|------|
| **Obsidian** | Markdown 知识库（GUI） | macOS / Linux / Windows | Logseq、Joplin |
| **marksman** | Markdown LSP（补全/链接检查/引用跳转） | macOS / Linux / WSL2 | zk（CLI 工具，侧重 Zettelkasten） |
| **pandoc** | 通用文档格式转换 | macOS / Linux / WSL2 | — |

> **选型原则**：Obsidian 作为知识库核心（本地 Markdown、双向链接、海量插件），Neovim 通过 `obsidian.nvim` 插件实现终端内编辑同一 Vault。`marksman` 提供 Markdown 级别的 LSP 支持。`pandoc` 用于 Markdown ↔ PDF/Word/HTML 转换。

### 12.1 Obsidian + Neovim 集成

| 组件 | 安装方式 | 用途 |
|------|----------|------|
| **Obsidian** | `brew install --cask obsidian` | 图形界面知识库管理（Vault 创建、图谱视图、插件管理） |
| **obsidian.nvim** | LazyVim 插件（`epwalsh/obsidian.nvim`） | Neovim 内编辑 Obsidian Vault，支持日记、模板、自动补全、反向链接 |
| **marksman** | `brew install marksman` | Markdown LSP，提供链接自动补全、Wiki 链接跳转、标题引用 |

obsidian.nvim 配置示例（`~/.config/nvim/lua/plugins/notes.lua`）：
```lua
return {
  {
    "epwalsh/obsidian.nvim",
    version = "*",
    lazy = true,
    ft = "markdown",
    dependencies = { "nvim-lua/plenary.nvim" },
    opts = {
      workspaces = {
        { name = "notes", path = "~/Obsidian/Notes" },
      },
      daily_notes = {
        folder = "daily",
        date_format = "%Y-%m-%d",
      },
      templates = {
        folder = "templates",
      },
    },
  },
}
```

### 12.2 文档转换

| 工具 | 安装 | 用途 |
|------|------|------|
| **pandoc** | `brew install pandoc` | Markdown ↔ PDF/Word/HTML 转换 |
| **basictex** | `brew install --cask basictex` | 轻量 LaTeX 环境（PDF 导出依赖） |

> `pandoc` + `basictex` 组合可实现 `pandoc note.md -o note.pdf` 一键导出。

### 12.3 其他笔记工具（按需安装）

| 工具 | 安装 | 用途 | 选型理由 |
|------|------|------|----------|
| **zk** | `brew install zk` | CLI Zettelkasten 管理 | Go 实现，终端原生的笔记创建/链接/搜索；与 Obsidian 不冲突，互补使用 |
| **nb** | `brew install nb` | CLI 笔记 + 书签管理 | Bash 实现，轻量级，支持加密/同步/Git 版本控制 |

---

## 13. 声明式依赖管理 (Brewfile)

推荐使用 `Brewfile` + `brew bundle` 声明式管理所有依赖，便于版本锁定、复现和审计：

```ruby
# Brewfile — 声明式工具链管理
# 使用方式：brew bundle --file=Brewfile

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
brew "node"
brew "go"
brew "kotlin"
brew "cmake"
brew "ninja"
brew "maven"
brew "gradle"
brew "ruff"
brew "rustup"
cask "miniconda"
cask "temurin"

# === 容器化 ===
brew "colima"
brew "docker"
brew "docker-compose"
brew "lazydocker"
brew "dive"

# === AI ===
brew "ollama"
brew "uv"
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

> 使用 `brew bundle dump` 可从当前已安装工具反向生成 Brewfile。

---

## 14. 一键安装脚本

Agent 在新机器上执行以下命令即可完成整个工具链安装：

```bash
# === 终端 & Shell ===
brew install --cask ghostty
brew install starship zellij

# === 字体 ===
brew install --cask font-jetbrains-mono-nerd-font font-cascadia-mono-nf

# === 输入法 (macOS) ===
brew install --cask squirrel-app
brew tap daipeihust/tap && brew install im-select
brew install --cask cc-switch

# === 编辑器 ===
brew install neovim
brew install --cask visual-studio-code

# === 文件 & 搜索 ===
brew install fd ripgrep bat fzf zoxide yazi
$(brew --prefix)/opt/fzf/install --all --no-bash --no-fish --no-update-rc

# === Git & GitHub ===
brew install git gh lazygit git-delta git-extras act gitleaks
gh extension install dlvhdr/gh-dash

# === 编程语言 ===
brew install node
brew install --cask miniconda
# 将 conda 加入 PATH（miniconda cask 不会自动配置）
eval "$(/opt/homebrew/bin/brew shellenv)"
conda init zsh
brew install --cask temurin      # Java JDK
brew install go                  # Go
brew install kotlin              # Kotlin
brew install cmake ninja         # C/C++ 构建
brew install maven gradle        # JVM 构建
npm install -g typescript
brew install ruff                  # Python linter + formatter
brew install rustup && rustup-init -y || \
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# === 容器化 ===
brew install colima docker docker-compose lazydocker dive
colima start --cpu 4 --memory 8 --disk 60

# === AI 学习 (macOS / Apple Silicon) ===
brew install ollama uv dvc

# AI 学习 conda 环境
conda create -n ai-learn python=3.13 -y
conda run -n ai-learn uv pip install torch torchvision torchaudio      # MPS 加速
conda run -n ai-learn uv pip install mlx mlx-lm mlx-vlm               # Apple Silicon 原生
conda run -n ai-learn uv pip install huggingface-hub jupyterlab marimo mlflow
conda run -n ai-learn uv pip install aider-chat llm llm-ollama
# Open WebUI 推荐通过 Docker 部署: docker compose up open-webui

# === AI 学习 (Linux / WSL2 + NVIDIA GPU) ===
# brew install ollama uv dvc
# brew install fcitx5 fcitx5-rime      # 中文输入法（Linux 原生）
# conda create -n ai-learn python=3.13 -y
# conda run -n ai-learn uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
# conda run -n ai-learn uv pip install bitsandbytes
# conda run -n ai-learn uv pip install huggingface-hub jupyterlab marimo mlflow
# conda run -n ai-learn uv pip install aider-chat llm llm-ollama

# === AI Agent ===
brew install opencode
npm install -g @anthropic-ai/claude-code

# === 其他 CLI ===
brew install bottom eza tokei hyperfine dust procs sd xh watchexec ouch gdu

# === 笔记工具 ===
brew install --cask obsidian
brew install marksman pandoc
# brew install --cask basictex    # PDF 导出依赖（~350MB，按需安装）
# brew install zk nb             # CLI 笔记管理（按需安装）
```

---

## 15. 配置文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| Shell 配置 | `~/.zshrc` | PATH、别名、Starship/Zellij 初始化、Conda hook、FZF 配置 |
| Starship 配置 | `~/.config/starship.toml` | Dracula 主题，模块化 prompt |
| Ghostty 配置 | `~/.config/ghostty/config` | Dracula 主题，**JetBrainsMono Nerd Font 14pt**，透明度 0.92 + 毛玻璃模糊 |
| Zellij 配置 | `~/.config/zellij/config.kdl` | Dracula 主题，透明背景，session-manager 插件 |
| Neovim 配置 | `~/.config/nvim/` | LazyVim v8，dracula.nvim，可选透明背景 |
| Yazi 配置 | `~/.config/yazi/` | `package.toml` 声明插件，`theme.toml` Dracula flavor |
| lazygit 配置 | `~/.config/lazygit/config.yml` | Dracula 主题配色 |
| lazydocker 配置 | `~/.config/lazydocker/config.yml` | Dracula 主题配色 |
| bottom 配置 | `~/.config/bottom/bottom.toml` | Dracula 主题配色 |
| gh-dash 配置 | `~/.config/gh-dash/config.yml` | Dracula 主题配色 |
| gitconfig delta | `~/.gitconfig` | `[delta]` 样式 key 配置 Dracula 色板 |
| VS Code 配置 | `~/Library/Application Support/Code/User/settings.json` | **JetBrainsMono Nerd Font 14pt**，Dracula 扩展 |
| Obsidian Vault | `~/Obsidian/Notes/`（推荐路径） | 本地 Markdown 知识库目录 |
| Obsidian 配置 | `~/Obsidian/Notes/.obsidian/app.json` | **JetBrainsMono Nerd Font 14pt**，Dracula 主题插件 |
| obsidian.nvim | `~/.config/nvim/lua/plugins/notes.lua` | Neovim 集成 Obsidian Vault |
| marksman 配置 | `~/.config/marksman/config.toml` | Markdown LSP 配置 |

> **字体统一说明**：Ghostty、VS Code、Obsidian 均配置 JetBrainsMono Nerd Font 14pt。TUI 工具继承终端字体。Neovim 终端版继承 Ghostty 字体，GUI 版（Neovide）可独立配置。

---

## 16. 一键更新

```bash
# Homebrew 更新所有工具
brew update && brew upgrade && brew upgrade --cask --greedy

# conda 更新
conda update --all -y

# npm 全局包更新
npm update -g

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

| 场景 | macOS | Linux | Windows (WSL2) |
|------|-------|-------|----------------|
| 包管理器 | Homebrew | **Homebrew on Linux** (无 sudo) | Homebrew (WSL2 内) |
| 终端 | Ghostty.app | Ghostty (formula) | Windows Terminal + WSL2 |
| 中文输入法 | Squirrel (Rime) | fcitx5-rime | Windows 侧 weasel (Rime) |
| 输入法切换 | im-select + cc-switch | fcitx5-remote | 不需要 |
| 剪贴板 | pbcopy/pbpaste | xclip (`brew install xclip`) / wl-copy (`brew install wl-clipboard`) | clip.exe |
| 字体注册 | 系统级安装 | `fc-cache -fv` | Windows 侧安装，WSL2 共享 |
| 容器运行时 | **Colima** (Lima VM) | **Colima** (Lima VM) | **Docker Engine** (`sudo apt install docker.io`，不用 Colima） |
| C/C++ 编译器 | Apple Clang (Xcode CLT) | GCC / Clang (`brew install gcc`) | GCC (WSL2 内) |
| JDK | **Temurin** (`brew install --cask temurin`) | **Temurin** (`brew install --cask temurin`) | **Temurin** (`brew install --cask temurin`) |
| ArkTS | DevEco Studio + ohpm/hdc | ❌ 不可用 | ❌ 不可用 |
| Kotlin | `brew install kotlin` | `brew install kotlin` | `brew install kotlin` (WSL2 内) |
| GitHub Actions 本地测试 | `act` (Docker 依赖) | `act` (Docker 依赖) | `act` (Docker 依赖) |
| AI 推理加速 | **MLX** (Apple Silicon 专用) | CUDA (NVIDIA) / ROCm (AMD) | CUDA (WSL2 直通 GPU) |
| LLM 运行时 | Ollama (MPS/MLX) | Ollama (CUDA) | Ollama (CUDA) |
| 笔记 | **Obsidian.app** + marksman | **Obsidian** (AppImage/flatpak) + marksman | Windows 侧 **Obsidian** + WSL2 内 marksman |

---

## 18. 自动化约束

Agent 执行安装时必须遵循：

- 所有安装命令必须带非交互参数（`--yes` / `-y` / `--no-confirm`）
- Linux 上禁止使用 `sudo apt install` / `sudo yum install`，统一用 `brew install` 避开 sudo
- 禁止 `git clone ... && make && make install` 源码编译（Rust 除外）
- 禁止 GUI 安装指引，所有操作在终端内完成
- 创建文件/目录前需先用 `ls` 验证父路径存在
