# 安装命令参考

本文档包含各阶段的详细安装命令。执行时参考本文档和 TOOLCHAIN.md。

---

## 阶段 1：终端 & Shell & 字体

```bash
brew install starship zellij
brew install --cask ghostty font-jetbrains-mono-nerd-font font-cascadia-mono-nf
```

**幂等检查：**
```bash
brew list --formula <name>   # 检查 formula
brew list --cask <name>      # 检查 cask
```

**Linux 字体：** 安装后执行 `fc-cache -fv`

---

## 阶段 2：输入法 & 编辑器

### macOS 输入法

```bash
brew install --cask squirrel-app
brew tap daipeihust/tap && brew install im-select
brew install --cask cc-switch  # .pkg cask，需 sudo
```

### Linux 输入法

```bash
brew install fcitx5 fcitx5-rime
```

### WSL2 输入法

跳过（Windows 侧装 weasel）

### 编辑器

```bash
brew install neovim
brew install --cask visual-studio-code
code --install-extension dracula-theme.theme-dracula
```

### 剪贴板（仅 Linux）

```bash
brew install xclip           # X11
brew install wl-clipboard    # Wayland
```

---

## 阶段 3：文件 & 搜索

```bash
brew install fd ripgrep bat fzf zoxide yazi
$(brew --prefix)/opt/fzf/install --all --no-bash --no-fish --no-update-rc
```

---

## 阶段 4：Git & GitHub

```bash
brew install git gh lazygit git-delta git-extras act gitleaks
gh extension install dlvhdr/gh-dash    # 需 gh auth login
```

**gitconfig 配置：** 见 `references/configs.md`

---

## 阶段 5：编程语言

**安装顺序（重要）：**
1. Node.js（在 bat 之后安装，避免 llhttp 冲突）
2. Miniconda → `conda init zsh` → `conda tos accept`
3. Java（.pkg cask，需 sudo）
4. Go/Kotlin
5. C/C++ 构建：cmake/ninja/maven/gradle
6. Rust：优先 brew，回退 curl 脚本
7. TypeScript
8. ruff

```bash
brew install node                        # 在 bat 之后
brew install --cask miniconda
conda init zsh
conda tos accept 2>/dev/null || true

brew install --cask temurin              # Java JDK (.pkg)
brew install go kotlin
brew install cmake ninja maven gradle
brew install ruff
npm install -g typescript

brew install rustup && rustup-init -y || \
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
```

**Conda 环境：**
```bash
conda create -n py-dev python=3.13 -y
conda create -n ai-learn python=3.13 -y
```

---

## 阶段 6：容器化 & AI

### macOS/Linux（非 WSL2）

```bash
brew install colima docker docker-compose lazydocker dive

# 动态分配资源
TOTAL_MEM_GB=$(sysctl -n hw.memsize 2>/dev/null | awk '{print int($1/1073741824)}' \
  || free -g 2>/dev/null | awk '/^Mem:/{print $2}')
COLIMA_MEM=$(( TOTAL_MEM_GB / 2 > 8 ? 8 : TOTAL_MEM_GB / 2 ))
COLIMA_CPU=$(( $(nproc 2>/dev/null || sysctl -n hw.ncpu) / 2 ))
colima start --cpu "${COLIMA_CPU:-2}" --memory "${COLIMA_MEM:-4}" --disk 60
```

### WSL2（不用 Colima）

```bash
sudo apt-get update -y && sudo apt-get install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
brew install lazydocker dive
```

### AI 学习

```bash
brew install ollama uv dvc
brew install opencode
npm install -g @anthropic-ai/claude-code
```

**macOS Apple Silicon conda 环境：**
```bash
conda run -n ai-learn uv pip install --timeout 600 torch torchvision torchaudio
conda run -n ai-learn uv pip install mlx mlx-lm mlx-vlm
conda run -n ai-learn uv pip install huggingface-hub jupyterlab marimo mlflow
conda run -n ai-learn uv pip install aider-chat llm llm-ollama || \
  conda run -n ai-learn pip install --no-deps aider-chat llm llm-ollama
```

**Linux/WSL2 NVIDIA：**
```bash
conda run -n ai-learn uv pip install torch torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu126
```

### 其他 CLI

```bash
brew install bottom eza tokei hyperfine dust procs sd xh watchexec ouch gdu
```

---

## 阶段 7：笔记

```bash
brew install --cask obsidian
brew install marksman pandoc
# 按需：brew install --cask basictex / brew install zk nb
```

---

## 阶段 9：验证脚本

### 核心验证（必须通过）

```bash
# Shell 语法
zsh -n ~/.zshrc && echo "zshrc OK" || echo "zshrc 语法错误"

# 工具启动
starship prompt 2>&1 >/dev/null && echo "Starship OK"
nvim --headless -c 'qall' 2>&1 && echo "Neovim OK"
conda info 2>&1 >/dev/null && echo "Conda OK"

# 语言运行时
for cmd_ver in "node --version" "go version" "java --version" "rustc --version" "python3 --version" "kotlin -version"; do
  cmd=$(echo "$cmd_ver" | awk '{print $1}')
  ver=$($cmd_ver 2>&1 | head -1) && echo "  ✓ $cmd: $ver" || echo "  ✗ $cmd 未找到"
done

# Conda 环境
conda env list 2>/dev/null | grep -E "(py-dev|ai-learn)" && echo "Conda 环境 OK"

# 容器（非 WSL2）
colima status 2>&1 | grep -q "Running" && echo "Colima OK"
docker info >/dev/null 2>&1 && echo "Docker OK"

# 关键工具
for tool in starship zellij nvim lazygit fzf zoxide bat eza fd rg yazi gh ollama marksman pandoc opencode; do
  command -v $tool &>/dev/null && echo "  ✓ $tool" || echo "  ✗ $tool"
done
```

### 可选验证

```bash
# Ghostty / Zellij
ghostty +validate-config 2>&1 || echo "Ghostty OK"
timeout 3 zellij options --generate-config 2>&1 >/dev/null && echo "Zellij OK"

# 透明度
grep -q "window-opacity.*0.92" ~/.config/ghostty/config 2>/dev/null && echo "Ghostty 透明度 OK"

# TUI 主题
for cfg in lazygit/config.yml lazydocker/config.yml bottom/bottom.toml gh-dash/config.yml; do
  [ -f ~/.config/$cfg ] && echo "  ✓ $cfg" || echo "  ✗ $cfg 未配置"
done

# 字体
system_profiler SPFontsDataType 2>/dev/null | grep -q "JetBrainsMono Nerd Font" \
  && echo "JetBrainsMono OK" || fc-list 2>/dev/null | grep -q "JetBrainsMono" && echo "JetBrainsMono OK"

# OpenCode 主题
grep -q "theme.*dracula" ~/.config/opencode/config.toml 2>/dev/null && echo "OpenCode Dracula OK"
```