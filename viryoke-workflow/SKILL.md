---
name: viryoke-workflow
description: 快速初始化完整的开发环境工作流。当用户提到新机器、换电脑、重装系统、搭建环境、setup、装开发工具、配置终端、安装工具链，或暗示缺少某些 CLI 工具时触发。即使用户只是问某个工具怎么装，也应先执行工作流确认整体环境状态。覆盖 macOS/Linux，幂等跳过已安装项，支持 dry-run 模式。
---

# Viryoke Workflow Setup

## 核心原则

| 原则 | 说明 |
|------|------|
| 幂等安装 | 安装前检查是否已存在，已存在则跳过 |
| 平台最优 | macOS/Linux 各自选择该生态最佳工具，不强制统一 |
| 批量安装 | 同阶段工具合并一条命令，减少网络往返 |
| 非交互 | 所有命令带 `-y` / `--yes` / `--no-confirm` |
| Dry-run | 先列出完整操作清单，确认后再执行 |

---

## 阶段编排理由

阶段顺序按依赖链编排，前一阶段是后一阶段的先决条件：
- **阶段 0（前置）** → 包管理器和编译链是所有后续安装的基石
- **阶段 1（终端）** → 先装好界面，后续命令才有可见载体
- **阶段 2（编辑器）** → 随即装好编辑环境，方便后续查看/编辑配置
- **阶段 3（文件）** → fd/rg/fzf 是后续阶段的效率工具（如 fzf 补全依赖安装）
- **阶段 4（Git）** → 版本控制是开发基础设施，早装以尽早配置 gitconfig
- **阶段 5（语言）** → Rust 最先（cargo 后续阶段大量使用），Pixi + uv 替代 conda（更快、声明式）
- **阶段 6（容器 & AI）** → 依赖语言工具链就绪
- **阶段 7（笔记）** → 最后装辅助工具
- **阶段 8（配置）** → 所有工具就绪后统一部署主题配置
- **阶段 9（验证）** → 全链路验证，确保环境可用

工具选型理由详见 `references/toolchain.md`（流行度 > 跨平台 > 性能 > 实时性 > 趋势）。

## 参考文档

| 文档 | 用途 |
|------|------|
| `references/toolchain.md` | 工具选型定义（权威参考） |
| `references/scripts.md` | 详细安装命令 |
| `references/configs.md` | 配置文件内容 |

执行时查阅 toolchain.md，不要凭记忆执行。

---

## 执行流程

10 个阶段顺序执行，预计 20-35 分钟。每阶段完成后报告结果，末了提示需用户手动执行的命令。

### 阶段 0：平台检测与前置检查

确认平台、网络、包管理器/编译链状态，识别需手动安装的项目。

```bash
uname -s   # Darwin=macOS, Linux=Linux
uname -m   # arm64=Apple Silicon, x86_64=Intel
```

检查网络连通性（github.com / pypi.org / raw.githubusercontent.com），`sudo -n true` 判断 sudo 是否可用，`gh auth status` 判断 GitHub 登录状态。

**平台策略：**
| 平台 | 包管理器 | 编译链 | 容器 |
|------|----------|--------|------|
| macOS | Homebrew | Xcode CLI | Colima |
| Linux | apt + cargo + curl/snap | build-essential | Docker Engine (apt) |

**需手动执行：** 该阶段无手动命令。

---

### 阶段 1：终端 & Shell & 字体

安装终端模拟器、Shell 提示符、复用器、Nerd Font 字体。

| 平台 | 终端 | 安装方式 |
|------|------|----------|
| macOS | Ghostty | `brew install --cask ghostty` |
| Linux | Ghostty | GitHub Release (deb/AppImage) 或 flatpak |

Starship、Zellij：macOS 用 brew，Linux 用 cargo。
JetBrainsMono Nerd Font：macOS 用 brew cask，Linux 下载到 `~/.local/share/fonts/` 后 `fc-cache -fv`。

**需手动执行（仅 Linux）：** `fc-cache -fv`

---

### 阶段 2：输入法 & 编辑器

| 平台 | 输入法 | 剪贴板 |
|------|--------|--------|
| macOS | Squirrel + im-select + cc-switch | 系统内置 pbcopy/pbpaste |
| Linux | fcitx5 + fcitx5-rime (apt) | xclip (X11) 或 wl-clipboard (Wayland) |

编辑器：Neovim + VS Code。macOS 用 brew，Linux 用 apt/snap。

**需手动执行 (macOS)：** `brew install --cask cc-switch` 涉及 `.pkg` 安装，需输入密码

---

### 阶段 3：文件 & 搜索

fd、ripgrep、bat、fzf、zoxide、yazi。macOS 用 brew，Linux 用 apt + cargo。

**需手动执行：** 无。

---

### 阶段 4：Git & GitHub

git、gh、lazygit、git-delta、git-extras、act、gitleaks、gh-dash。配置 gitconfig（含 delta Dracula 配色）。

**需手动执行：** `gh auth login` 后才能 `gh extension install dlvhdr/gh-dash`

---

### 阶段 5：编程语言

macOS：Bun (brew) / Pixi (curl) / Java Temurin (brew cask) / Go (brew) / Kotlin / CMake / Ninja / Maven / Gradle / Rust (rustup) / ruff / uv (brew)
Linux：Bun (curl) / Pixi (curl) / Java OpenJDK (apt) / Go (apt) / Kotlin (snap) / CMake / Ninja / Maven / Gradle (apt) / Rust (curl) / ruff (cargo/pipx) / uv (curl)

Pixi + uv 替代 conda：用 pixi 创建 Python 环境，uv 安装 pip 包。不需要 conda、Node.js、TypeScript（Bun 内置 TS 支持）。

**安装顺序：** Rust (rustup) → Bun → Pixi → Java → Go/Kotlin → 构建工具 → ruff

**需手动执行 (macOS)：** `brew install --cask temurin` 涉及 `.pkg` 安装，需输入密码

---

### 阶段 6：容器化 & AI

| 平台 | 容器方案 |
|------|----------|
| macOS | Colima + Docker CLI (brew) |
| Linux | Docker Engine (apt install docker.io) |

AI 工具：Ollama、DVC、OpenCode、Claude Code。AI Python 环境分平台：
- macOS Apple Silicon：PyTorch MPS + MLX
- Linux NVIDIA：PyTorch CUDA

**需手动执行 (macOS)：** `colima start` 后 docker 才可用
**需手动执行 (Linux)：** `sudo apt install docker.io docker-compose-v2 && sudo usermod -aG docker $USER`

---

### 阶段 7：笔记工具

Obsidian、marksman、pandoc。macOS 用 brew，Linux 用 snap/cargo/apt。

**需手动执行：** basictex（~350MB）按需提示用户手动安装。

---

### 阶段 8：配置文件部署

部署统一主题的配置文件。标准：Dracula 主题、JetBrainsMono Nerd Font 14pt、opacity=0.92 + blur。配置内容见 `references/configs.md`。

**需手动执行：** 需询问用户 Git email 来配置 gitconfig

---

### 阶段 9：验证（按阶段逐项确认）

**每个阶段的成功标准：**

| 阶段 | 验证目标 | 检查方式 |
|------|---------|---------|
| 0 | 包管理器/网络/sudo | `brew --version`/`apt --version`, `ping -c1 github.com` |
| 1 | 终端+Shell+字体 | `zsh -n ~/.zshrc`, `ghostty +validate-config`, `fc-list | grep JetBrainsMono` |
| 2 | 编辑器 | `nvim --headless +qall`, `code --version` |
| 3 | 文件搜索 | `fd --version`, `rg --version`, `bat --version`, `fzf --version` |
| 4 | Git | `git --version`, `gh auth status`, `delta --version` |
| 5 | 语言运行时 | `bun --version`, `rustc --version`, `go version`, `java --version`, `pixi --version` |
| 6 | 容器+AI | `docker info`, `ollama --version` |
| 7 | 笔记 | `obsidian --version`/`snap list obsidian`, `pandoc --version` |
| 8 | 配置 | 检查各配置文件存在 + Dracula 主题/透明度/字体设置正确 |

完整验证脚本见 `references/scripts.md` §阶段 9。

---

## 平台差异

| 平台 | 包管理器 | 终端 | 容器 | 输入法 |
|------|----------|------|------|--------|
| macOS | Homebrew | Ghostty (cask) | Colima | Squirrel + im-select |
| Linux | apt + cargo + curl/snap | Ghostty (deb/AppImage) | Docker Engine | fcitx5-rime (apt) |

## cask sudo 分类（仅 macOS）

| 类型 | 示例 | sudo |
|------|------|------|
| `.app` cask | ghostty, visual-studio-code | 否 |
| `.pkg` cask | temurin, cc-switch | 是 |
| 字体 cask | font-jetbrains-mono-nerd-font | 否 |

## 错误处理

- 失败不中断，继续执行后续阶段
- 最后汇总失败列表和修复建议
- `.pkg` cask sudo 不可用 → 加入手动安装列表
- gh-dash 失败 → 提示先 `gh auth login`

## 完成报告

```
## 环境初始化完成

### 耗时：阶段 0-9 各 Xs / 总计 Xs
### 已安装 X/Y · 跳过 A · 失败 B

### 失败详情：工具名 → 错误信息 + 修复建议

### 需手动执行：
- (列表每阶段收集的需用户手动操作的命令)

### 后续步骤：
1. source ~/.zshrc 或重启终端
2. Neovim 首次启动自动装 LazyVim 插件
3. macOS: colima start / Linux: sudo systemctl enable docker
4. ollama pull qwen3:latest

### 回滚 (macOS)：brew uninstall <name> / rustup self uninstall
### 回滚 (Linux)：apt remove <name> / cargo uninstall <name> / rustup self uninstall
```
