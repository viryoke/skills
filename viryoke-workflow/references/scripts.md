# 安装命令参考

本文档包含各阶段的详细安装命令。执行时参考本文档和 toolchain.md。

## 目录

- [阶段 1：终端 & Shell & 字体](#阶段-1终端--shell--字体)
- [阶段 2：输入法 & 编辑器](#阶段-2输入法--编辑器)
- [阶段 3：文件 & 搜索](#阶段-3文件--搜索)
- [阶段 4：Git & GitHub](#阶段-4git--github)
- [阶段 5：编程语言](#阶段-5编程语言)
- [阶段 6：容器化 & AI](#阶段-6容器化--ai)
- [阶段 7：笔记](#阶段-7笔记)
- [阶段 9：验证脚本](#阶段-9验证脚本)

---

## 阶段 1：终端 & Shell & 字体

### macOS

```bash
brew install starship zellij
brew install --cask ghostty font-jetbrains-mono-nerd-font font-cascadia-mono-nf
```

### Linux

```bash
sudo apt install -y zsh curl

# Ghostty（从 GitHub Release 下载 deb）
curl -fsSL https://github.com/ghostty-org/ghostty/releases/latest/download/ghostty_amd64.deb -o /tmp/ghostty.deb
sudo dpkg -i /tmp/ghostty.deb

# JetBrainsMono Nerd Font
mkdir -p ~/.local/share/fonts
curl -fsSL https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.tar.xz -o /tmp/JetBrainsMono.tar.xz
tar -xf /tmp/JetBrainsMono.tar.xz -C ~/.local/share/fonts/
fc-cache -fv

# Starship, Zellij（通过 cargo，Rust 需先安装见阶段 5）
```

> **手动提示：** Linux 执行完字体安装后需 `fc-cache -fv`

---

## 阶段 2：输入法 & 编辑器

### macOS

```bash
brew install --cask squirrel-app
brew tap daipeihust/tap && brew install im-select
# brew install --cask cc-switch  # .pkg cask，提示用户手动安装

brew install neovim
brew install --cask visual-studio-code
code --install-extension dracula-theme.theme-dracula
```

> **手动提示：** `cc-switch` 是 `.pkg` cask，需输入密码。阶段末提示用户手动执行。

### Linux

```bash
sudo apt install -y fcitx5 fcitx5-rime xclip wl-clipboard

# Neovim（apt 版本可能旧，建议用 PPA 或 AppImage）
sudo apt install -y neovim

# VS Code
sudo snap install code --classic
code --install-extension dracula-theme.theme-dracula
```

---

## 阶段 3：文件 & 搜索

### macOS

```bash
brew install fd ripgrep bat fzf zoxide yazi
$(brew --prefix)/opt/fzf/install --all --no-bash --no-fish --no-update-rc
```

### Linux

```bash
# apt 可用工具
sudo apt install -y ripgrep fd-find bat fzf

# cargo 安装（需先安装 Rust，见阶段 5）
cargo install zoxide yazi-fm

# fzf 安装脚本
$(which fzf)/../opt/fzf/install --all --no-bash --no-fish --no-update-rc

# bat 符号链接（Ubuntu 上 bat 二进制名为 batcat）
mkdir -p ~/.local/bin && ln -sf $(which batcat) ~/.local/bin/bat 2>/dev/null || true
# fd 符号链接（Ubuntu 上 fd 二进制名为 fdfind）
ln -sf $(which fdfind) ~/.local/bin/fd 2>/dev/null || true
```

---

## 阶段 4：Git & GitHub

### macOS

```bash
brew install git gh lazygit git-delta git-extras act gitleaks
# gh extension install dlvhdr/gh-dash    # 需 gh auth login
```

### Linux

```bash
sudo apt install -y git gh lazygit git-extras

# cargo 安装
cargo install git-delta

# go install（需先安装 Go，见阶段 5）
go install github.com/nektos/act@latest
go install github.com/gitleaks/gitleaks/v8@latest

# gh extension install dlvhdr/gh-dash    # 需 gh auth login
```

**gitconfig 配置：** 见 `references/configs.md`

> **手动提示：** 需先 `gh auth login`，再执行 `gh extension install dlvhdr/gh-dash`。
> **手动提示：** gitconfig 需询问用户 Git email 后配置。

---

## 阶段 5：编程语言

**安装顺序：** Rust (rustup) → Bun → Pixi → Java → Go/Kotlin → 构建工具 → ruff/uv

### Rust（两平台共通）

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"
```

### macOS

```bash
# Bun
brew install bun

# Pixi + uv
curl -fsSL https://pixi.sh/install.sh | bash
brew install uv

# Java (Temurin)
# brew install --cask temurin    # .pkg cask，提示用户手动安装

# Go / Kotlin / 构建工具
brew install go kotlin cmake ninja maven gradle

# ruff
brew install ruff
```

> **手动提示：** `brew install --cask temurin` 是 `.pkg` cask，阶段末提示用户手动输入密码执行。

### Linux

```bash
# Bun
curl -fsSL https://bun.sh/install | bash

# Pixi + uv
curl -fsSL https://pixi.sh/install.sh | bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Java (OpenJDK)
sudo apt install -y openjdk-21-jdk

# Go
sudo apt install -y golang-go

# Kotlin
sudo snap install kotlin --classic

# 构建工具
sudo apt install -y cmake ninja-build maven gradle

# ruff（cargo 或 pipx）
cargo install ruff
```

### Python 环境（Pixi + uv，替代 conda）

```bash
# 创建通用开发环境
pixi init ~/projects/py-dev && cd ~/projects/py-dev
pixi add python=3.13
pixi run uv pip install ruff

# 创建 AI 学习环境
pixi init ~/projects/ai-learn && cd ~/projects/ai-learn
pixi add python=3.13
# macOS: pixi run uv pip install torch torchvision torchaudio mlx mlx-lm mlx-vlm
# Linux NVIDIA: pixi run uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pixi run uv pip install huggingface-hub jupyterlab marimo mlflow aider-chat llm llm-ollama
```

---

## 阶段 6：容器化 & AI

### macOS

```bash
brew install colima docker docker-compose lazydocker dive
```

> **手动提示：** 执行 `colima start --cpu <n> --memory <n> --disk 60`。

### Linux

```bash
sudo apt install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER

# Go-based Docker 工具
go install github.com/jesseduffield/lazydocker@latest
go install github.com/wagoodman/dive@latest
```

> **手动提示：** 重新登录使 docker 组生效，`sudo systemctl enable --now docker`。

### AI 学习

```bash
# macOS
brew install ollama dvc opencode

# Linux
curl -fsSL https://ollama.com/install.sh | sh
# DVC (pipx)
pipx install dvc
# OpenCode
bun install -g opencode

# Claude Code
bun install -g @anthropic-ai/claude-code
```

### 其他 CLI

```bash
# macOS
brew install bottom eza tokei hyperfine dust procs sd xh watchexec ouch gdu

# Linux（apt 已安装部分，补充 cargo）
sudo apt install -y hyperfine gdu xh
cargo install eza bottom tokei du-dust procs sd-find watchexec-cli ouch
```

---

## 阶段 7：笔记

### macOS

```bash
brew install --cask obsidian
brew install marksman pandoc
# 按需提示用户手动安装：brew install --cask basictex（~350MB，PDF 导出）
```

### Linux

```bash
sudo snap install obsidian --classic
sudo apt install -y pandoc
cargo install marksman
# 按需提示用户手动安装：sudo apt install texlive-latex-base（~350MB，PDF 导出）
```

---

## 阶段 9：验证脚本

按阶段逐项验证，每项输出 ✓/✗ 和失败原因。

### 阶段 0 — 包管理器/网络/权限

```bash
echo "=== 阶段 0: 前置条件 ==="
command -v brew &>/dev/null && echo "  ✓ Homebrew: $(brew --version | head -1)" || \
  command -v apt &>/dev/null && echo "  ✓ apt" || echo "  ✗ 无包管理器"
ping -c1 github.com &>/dev/null && echo "  ✓ 网络 (github.com)" || echo "  ✗ 网络不通"
sudo -n true &>/dev/null && echo "  ✓ sudo 可用" || echo "  ✗ sudo 不可用（部分安装需手动）"
```

### 阶段 1 — 终端/Shell/字体

```bash
echo "=== 阶段 1: 终端 & Shell & 字体 ==="
zsh -n ~/.zshrc 2>&1 && echo "  ✓ zshrc 语法" || echo "  ✗ zshrc 语法错误: $(zsh -n ~/.zshrc 2>&1)"
command -v starship &>/dev/null && echo "  ✓ Starship: $(starship --version)" || echo "  ✗ Starship"
command -v zellij &>/dev/null && echo "  ✓ Zellij: $(zellij --version)" || echo "  ✗ Zellij"
# Ghostty 验证（macOS/Linux 通用）
ghostty +validate-config 2>&1 >/dev/null && echo "  ✓ Ghostty" || \
  [ -d /Applications/Ghostty.app ] && echo "  ✓ Ghostty.app 已安装" || \
  command -v ghostty &>/dev/null && echo "  ✓ Ghostty CLI" || echo "  ✗ Ghostty"
# 字体（跨平台兼容）
system_profiler SPFontsDataType 2>/dev/null | grep -q "JetBrainsMono Nerd Font" && echo "  ✓ JetBrainsMono Nerd Font" || \
  fc-list 2>/dev/null | grep -q "JetBrainsMono" && echo "  ✓ JetBrainsMono Nerd Font" || \
  echo "  ✗ JetBrainsMono Nerd Font 未找到"
```

### 阶段 2 — 编辑器

```bash
echo "=== 阶段 2: 编辑器 ==="
nvim --headless -c 'qall' 2>&1 && echo "  ✓ Neovim: $(nvim --version | head -1)" || echo "  ✗ Neovim"
command -v code &>/dev/null && echo "  ✓ VS Code: $(code --version | head -1)" || echo "  ✗ VS Code"
code --list-extensions 2>/dev/null | grep -q "dracula-theme" && echo "  ✓ VS Code Dracula 主题" || echo "  ✗ Dracula 扩展未装"
```

### 阶段 3 — 文件搜索

```bash
echo "=== 阶段 3: 文件 & 搜索 ==="
for tool in fd rg bat fzf zoxide yazi; do
  command -v $tool &>/dev/null && echo "  ✓ $tool" || echo "  ✗ $tool"
done
```

### 阶段 4 — Git 工具链

```bash
echo "=== 阶段 4: Git & GitHub ==="
command -v git &>/dev/null && echo "  ✓ git: $(git --version)" || echo "  ✗ git"
command -v gh &>/dev/null && echo "  ✓ gh: $(gh --version | head -1)" || echo "  ✗ gh"
gh auth status &>/dev/null && echo "  ✓ gh 已登录" || echo "  ✗ gh 未登录（需 gh auth login）"
command -v delta &>/dev/null && echo "  ✓ delta: $(delta --version)" || echo "  ✗ delta"
command -v lazygit &>/dev/null && echo "  ✓ lazygit" || echo "  ✗ lazygit"
# delta 配色验证
grep -q "delta.*Dracula\|plus-style.*50fa7b" ~/.gitconfig 2>/dev/null && echo "  ✓ delta Dracula 配色" || echo "  ✗ delta 配色未配置"
```

### 阶段 5 — 语言运行时

```bash
echo "=== 阶段 5: 编程语言 ==="
for cmd_ver in "bun --version" "go version" "java --version" "rustc --version" "kotlin -version"; do
  cmd=$(echo "$cmd_ver" | awk '{print $1}')
  ver=$($cmd_ver 2>&1 | head -1) && echo "  ✓ $cmd: $ver" || echo "  ✗ $cmd 未找到"
done
pixi --version &>/dev/null && echo "  ✓ Pixi: $(pixi --version)" || echo "  ✗ Pixi"
uv --version &>/dev/null && echo "  ✓ uv: $(uv --version)" || echo "  ✗ uv"
command -v ruff &>/dev/null && echo "  ✓ ruff: $(ruff --version)" || echo "  ✗ ruff"
python3 --version &>/dev/null && echo "  ✓ python3: $(python3 --version)" || echo "  ✗ python3"
```

### 阶段 6 — 容器 & AI

```bash
echo "=== 阶段 6: 容器化 & AI ==="
docker info >/dev/null 2>&1 && echo "  ✓ Docker 运行中" || echo "  ✗ Docker 未运行"
# macOS Colima
colima status 2>&1 | grep -q "Running" && echo "  ✓ Colima 运行中" || true
# Linux Docker 组
id -nG 2>/dev/null | grep -q docker && echo "  ✓ 用户在 docker 组" || true
# AI 工具
command -v ollama &>/dev/null && echo "  ✓ Ollama: $(ollama --version)" || echo "  ✗ Ollama"
command -v opencode &>/dev/null && echo "  ✓ OpenCode" || echo "  ✗ OpenCode"
command -v claude &>/dev/null && echo "  ✓ Claude Code" || echo "  ✗ Claude Code"
```

### 阶段 7 — 笔记

```bash
echo "=== 阶段 7: 笔记 ==="
# Obsidian（macOS .app / Linux snap）
[ -d /Applications/Obsidian.app ] && echo "  ✓ Obsidian.app" || \
  snap list 2>/dev/null | grep -q obsidian && echo "  ✓ Obsidian snap" || \
  echo "  ✗ Obsidian 未找到"
command -v marksman &>/dev/null && echo "  ✓ marksman" || echo "  ✗ marksman"
command -v pandoc &>/dev/null && echo "  ✓ pandoc: $(pandoc --version | head -1)" || echo "  ✗ pandoc"
```

### 阶段 8 — 配置文件

```bash
echo "=== 阶段 8: 配置文件 ==="
# 配置文件存在性
for cfg in \
  ~/.zshrc \
  ~/.config/starship.toml \
  ~/.config/ghostty/config \
  ~/.config/zellij/config.kdl \
  ~/.config/yazi/theme.toml \
  ~/.config/lazygit/config.yml \
  ~/.config/bottom/bottom.toml; do
  [ -f "$cfg" ] && echo "  ✓ $cfg" || echo "  ✗ $cfg 缺失"
done
# Dracula 主题验证
grep -qi "dracula" ~/.config/ghostty/config 2>/dev/null && echo "  ✓ Ghostty Dracula" || echo "  ✗ Ghostty 主题"
grep -q "window-opacity.*0.92" ~/.config/ghostty/config 2>/dev/null && echo "  ✓ Ghostty 透明度=0.92" || echo "  ✗ 透明度未设置"
grep -q "theme.*dracula" ~/.config/opencode/config.toml 2>/dev/null && echo "  ✓ OpenCode Dracula" || echo "  ✗ OpenCode 主题"
```

### 一键全量验证

```bash
# 合并上述所有阶段验证，一次性运行
# 使用方式：将上述各阶段脚本拼接，或 curl 到此文件执行
echo "全量验证通过数: $(grep -c '✓' <<<以上输出)"
```
