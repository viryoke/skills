---
name: viryoke-workflow
description: >
  快速初始化完整的开发环境工作流。触发场景：
  - 用户提到"初始化环境"、"搭建开发环境"、"setup workflow"、"新机器配置"、"装工具"
  - 用户要求按 TOOLCHAIN.md 配置工具链
  
  覆盖 macOS / Linux / WSL2 三平台，幂等跳过已安装工具，支持 dry-run 模式。
  基于 TOOLCHAIN.md 定义的完整工具链：终端、字体、编辑器、Git、编程语言、容器、AI、笔记。
---

# Viryoke Workflow Setup

按 TOOLCHAIN.md 在新机器上快速搭建完整开发环境。

## 核心原则

- **幂等安装**：安装前检查是否已存在，已装则跳过
- **平台感知**：自动检测 macOS / Linux / WSL2，选择对应指令
- **批量安装**：同阶段 formula/cask 合并为一条 `brew install`
- **非交互**：所有命令带 `-y` / `--yes` / `--no-confirm`
- **零 sudo**：仅 Homebrew 安装和 `.pkg` cask 需 sudo
- **Dry-run**：可先列出完整操作清单，确认后再执行

## cask sudo 分类

| 类型 | 示例 | sudo |
|------|------|------|
| `.app` cask | ghostty, visual-studio-code | 否 |
| `.pkg` cask | squirrel-app, temurin, cc-switch | **是** |
| 字体 cask | font-jetbrains-mono-nerd-font | 否 |

> `.pkg` cask 在非交互终端无法完成，跳过并加入手动安装列表。

## 加载参考文档

```
references/TOOLCHAIN.md
```

TOOLCHAIN.md 是权威参考，执行过程中随时查阅，不要凭记忆执行。

## 执行流程

9 个阶段顺序执行，每阶段完成后报告结果（含耗时）。预估总耗时 20-35 分钟。

### 阶段 0：平台检测与前置检查（~1 分钟）

1. **检测平台**：
   ```bash
   uname -s   # Darwin=macOS, Linux=Linux
   uname -m   # arm64=Apple Silicon, x86_64=Intel
   grep -qi microsoft /proc/version 2>/dev/null && echo "WSL2" || echo "Native"
   ```

2. **网络连通性**：
   ```bash
   for host in github.com pypi.org raw.githubusercontent.com; do
     curl -sI --connect-timeout 5 "https://$host" >/dev/null 2>&1 \
       && echo "  ✓ $host" || echo "  ✗ $host 不可达"
   done
   ```
   > 不可达时提示配置镜像（清华/中科大 Homebrew 镜像）。

3. **安装策略**：
   - **macOS**：确认 Xcode CLI + Homebrew
   - **Linux**：确认 Homebrew on Linux（先装 build-essential）
   - **WSL2**：按 Linux 策略（容器用 Docker Engine 而非 Colima）

4. **前置检查**（macOS）：
   - `sudo -n true 2>/dev/null` 失败 → `.pkg` cask 标记为手动
   - `gh auth status` 未登录 → `gh extension install` 标记为手动
   - `conda tos accept 2>/dev/null || true` → 预接受 ToS

5. **汇报**：平台、架构、Homebrew、sudo、网络状态 → 询问用户是否继续。

6. **Dry-run**：若用户要求，列出全部阶段工具清单，确认后再执行。

### 阶段 1：终端 & Shell & 字体（~2 分钟）

```bash
brew install starship zellij
brew install --cask ghostty font-jetbrains-mono-nerd-font font-cascadia-mono-nf
```

幂等检查：`brew list --formula <name>` / `brew list --cask <name>`。Linux 字体装后需 `fc-cache -fv`。

### 阶段 2：输入法 & 编辑器（~2 分钟）

**输入法**：
- macOS: squirrel-app + `brew tap daipeihust/tap && brew install im-select` + cc-switch
- Linux: fcitx5, fcitx5-rime
- WSL2: 跳过（Windows 侧装 weasel）

**编辑器**：neovim, visual-studio-code

```bash
code --install-extension dracula-theme.theme-dracula
```

**剪贴板（仅 Linux）**：`brew install xclip`（X11）或 `brew install wl-clipboard`（Wayland）。Neovim `+clipboard` 依赖。

### 阶段 3：文件 & 搜索（~1 分钟）

```bash
brew install fd ripgrep bat fzf zoxide yazi
$(brew --prefix)/opt/fzf/install --all --no-bash --no-fish --no-update-rc
```

### 阶段 4：Git & GitHub（~1 分钟）

```bash
brew install git gh lazygit git-delta git-extras act gitleaks
gh extension install dlvhdr/gh-dash    # 需 gh auth login
```

配置 gitconfig（TOOLCHAIN.md §6.1）：
```bash
git config --global user.name "viryoke"
git config --global user.email "<USER_EMAIL>"     # ⚠️ 必须询问用户
git config --global core.editor "nvim"
git config --global init.defaultBranch "main"
git config --global pull.rebase true
git config --global core.pager "delta"
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global delta.side-by-side true
git config --global delta.light false
git config --global delta.plus-style "syntax #50fa7b"
git config --global delta.minus-style "syntax #ff5555"
git config --global delta.commit-decoration-style "#50fa7b bold box"
git config --global delta.file-style "#bd93f9 bold"
git config --global delta.hunk-header-style "#ff79c6 bold"
git config --global delta.line-numbers-minus-style "#ff5555"
git config --global delta.line-numbers-plus-style "#50fa7b"
git config --global merge.conflictstyle zdiff3
```

> 必须询问真实 email。GPG/SSH 签名可选追加 `commit.gpgsign true` + `gpg.format ssh`。

### 阶段 5：编程语言（~3 分钟）

按 TOOLCHAIN.md §7 安装，注意顺序：

- **Node.js**: `brew install node`（在 bat 之后安装，避免 llhttp 冲突）
- **Miniconda**: `brew install --cask miniconda` → `conda init zsh` → `conda tos accept 2>/dev/null || true`
- **Java**: `brew install --cask temurin`（.pkg，需 sudo）
- **Go/Kotlin**: `brew install go kotlin`
- **C/C++ 构建**: `brew install cmake ninja maven gradle`
- **Rust**: `brew install rustup && rustup-init -y`，失败回退 `curl ... | sh -s -- -y`
- **TypeScript**: `npm install -g typescript`
- **ruff**: `brew install ruff`

```bash
conda create -n py-dev python=3.13 -y
conda create -n ai-learn python=3.13 -y
```

### 阶段 6：容器化 & AI 工具（~5 分钟）

**容器（macOS/Linux，非 WSL2）**：
```bash
brew install colima docker docker-compose lazydocker dive
# 动态分配资源
TOTAL_MEM_GB=$(sysctl -n hw.memsize 2>/dev/null | awk '{print int($1/1073741824)}' \
  || free -g 2>/dev/null | awk '/^Mem:/{print $2}')
COLIMA_MEM=$(( TOTAL_MEM_GB / 2 > 8 ? 8 : TOTAL_MEM_GB / 2 ))
COLIMA_CPU=$(( $(nproc 2>/dev/null || sysctl -n hw.ncpu) / 2 ))
colima start --cpu "${COLIMA_CPU:-2}" --memory "${COLIMA_MEM:-4}" --disk 60
```

**容器（WSL2，不用 Colima）**：
```bash
sudo apt-get update -y && sudo apt-get install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER && brew install lazydocker dive
```

**AI 学习**：
```bash
brew install ollama uv dvc
```

conda 环境内安装（macOS Apple Silicon）：
```bash
conda run -n ai-learn uv pip install --timeout 600 torch torchvision torchaudio
conda run -n ai-learn uv pip install mlx mlx-lm mlx-vlm
conda run -n ai-learn uv pip install huggingface-hub jupyterlab marimo mlflow
conda run -n ai-learn uv pip install aider-chat llm llm-ollama || \
  conda run -n ai-learn pip install --no-deps aider-chat llm llm-ollama
```

Linux/WSL2 NVIDIA：加 `--index-url https://download.pytorch.org/whl/cu126`。

**AI Agent**：`brew install opencode` / `npm install -g @anthropic-ai/claude-code`

**其他 CLI**：
```bash
brew install bottom eza tokei hyperfine dust procs sd xh watchexec ouch gdu
```

### 阶段 7：笔记工具链（~1 分钟）

```bash
brew install --cask obsidian
brew install marksman pandoc
# 按需：brew install --cask basictex / brew install zk nb
```

### 阶段 8：配置文件部署

**统一主题标准**：Dracula (#282a36/#f8f8f2) · JetBrainsMono Nerd Font 14pt · opacity=0.92 · blur=true

| 文件 | 路径 | 说明 |
|------|------|------|
| Shell | `~/.zshrc` | PATH、别名、Starship、Zoxide、Conda、FZF |
| Starship | `~/.config/starship.toml` | Dracula 主题 |
| Ghostty | `~/.config/ghostty/config` | Dracula + 14pt + opacity=0.92 + blur |
| Zellij | `~/.config/zellij/config.kdl` | Dracula + 透明背景 |
| Neovim | `~/.config/nvim/` | LazyVim v8 + dracula.nvim |
| Yazi | `~/.config/yazi/` | Dracula flavor |
| lazygit | `~/.config/lazygit/config.yml` | Dracula 配色 |
| lazydocker | `~/.config/lazydocker/config.yml` | Dracula 配色 |
| bottom | `~/.config/bottom/bottom.toml` | Dracula 配色 |
| gh-dash | `~/.config/gh-dash/config.yml` | Dracula 配色 |
| VS Code | settings.json | 14pt + Dracula 扩展 |
| Obsidian | `.obsidian/app.json` | 14pt + Dracula 插件 |
| OpenCode | `~/.config/opencode/config.toml` | `theme = "dracula"` |
| git-delta | `~/.gitconfig` | Dracula 色板（见阶段 4） |

> Claude Code / 其他 Agent：终端内运行，继承 Ghostty 主题与透明度。

若用户提供配置仓库则克隆部署，否则注入最小化 Shell 配置：

```bash
# === Homebrew PATH（兼容全平台）===
eval "$(brew shellenv)"
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

# === Shell 工具 ===
eval "$(starship init zsh)"
eval "$(zoxide init zsh)"

# === 别名 ===
alias ll="ls -la" l="ls -l" ..="cd .." ...="cd ../.."
alias g="git" v="nvim" vi="nvim" vim="nvim" y="yazi"
alias ls="eza --group-directories-first"
alias top="btm 2>/dev/null || top"

# === 主题 ===
export BAT_THEME="Dracula"

# === FZF ===
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
export FZF_DEFAULT_COMMAND="fd --type f --hidden --exclude .git"
export FZF_DEFAULT_OPTS="--color=bg+:#44475a,bg:#282a36,spinner:#f1fa8c,hl:#50fa7b,fg:#f8f8f2,header:#bd93f9,info:#8be9fd,pointer:#ff79c6,marker:#ff79c6,fg+:#f8f8f2,prompt:#bd93f9,hl+:#50fa7b"
```

### 阶段 9：配置验证

**核心验证**（必须全部通过）：

```bash
# Shell 语法
zsh -n ~/.zshrc && echo "zshrc OK" || echo "zshrc 语法错误"

# 工具启动
starship prompt 2>&1 >/dev/null && echo "Starship OK" || echo "Starship 错误"
nvim --headless -c 'qall' 2>&1 && echo "Neovim OK" || echo "Neovim 错误"
conda info 2>&1 >/dev/null && echo "Conda OK" || echo "Conda 错误"

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

# 关键工具可用性
for tool in starship zellij nvim lazygit fzf zoxide bat eza fd rg yazi gh ollama marksman pandoc opencode; do
  command -v $tool &>/dev/null && echo "  ✓ $tool" || echo "  ✗ $tool"
done
```

**可选验证**（配置文件部署后检查）：

```bash
# Ghostty / Zellij 配置
ghostty +validate-config 2>&1 || echo "Ghostty OK"
timeout 3 zellij options --generate-config 2>&1 >/dev/null && echo "Zellij OK"

# 透明度
grep -q "window-opacity.*0.92" ~/.config/ghostty/config 2>/dev/null && echo "Ghostty 透明度 OK"

# TUI 主题（lazygit/lazydocker/bottom/gh-dash）
for cfg in lazygit/config.yml lazydocker/config.yml bottom/bottom.toml gh-dash/config.yml; do
  [ -f ~/.config/$cfg ] && echo "  ✓ $cfg" || echo "  ✗ $cfg 未配置"
done

# 字体
system_profiler SPFontsDataType 2>/dev/null | grep -q "JetBrainsMono Nerd Font" \
  && echo "JetBrainsMono OK" || fc-list 2>/dev/null | grep -q "JetBrainsMono" && echo "JetBrainsMono OK"

# OpenCode 主题
grep -q "theme.*dracula" ~/.config/opencode/config.toml 2>/dev/null && echo "OpenCode Dracula OK"
```

> 验证失败项须报告错误信息和修复方案，不静默跳过。

---

## 平台特殊处理

| 平台 | 要点 |
|------|------|
| **macOS** | Homebrew 在 `/opt/homebrew`(ARM) 或 `/usr/local`(Intel)；Squirrel+im-select |
| **Linux** | Homebrew 在 `/home/linuxbrew`；`fc-cache -fv`；xclip/wl-clipboard；Ghostty 用 formula |
| **WSL2** | Docker Engine 替代 Colima；跳过输入法和字体；推荐 Windows Terminal |

## 执行注意事项

1. **幂等检查**：`brew list` / `command -v`，已存在则跳过
2. **`.pkg` cask**：`sudo -n true` 失败时跳过，加入手动列表
3. **conda**：`conda tos accept || true` → `conda init zsh` → `conda run` 绕过 PATH
4. **Rust**：优先 brew rustup，回退 curl 脚本
5. **gh-dash**：需 `gh auth login`，未登录则跳过
6. **Node/llhttp**：node 在 bat 之后安装，冲突时 `brew reinstall node`
7. **aider-chat**：`uv pip` 失败回退 `pip --no-deps`
8. **Colima**：macOS 需先启动才能用 docker；WSL2 不用 Colima
9. **错误处理**：失败不中断，最后汇总失败列表
10. **版本跟随**：以 TOOLCHAIN.md 为准，不硬编码

## 完成报告

```
## 环境初始化完成

### 耗时：阶段 0-9 各 Xs / 总计 Xs
### 已安装 X/Y · 跳过 A · 失败 B

### 失败详情：工具名 → 错误信息 + 修复建议
### 需手动安装：.pkg cask 列表

### 后续步骤：
1. `source ~/.zshrc` 或重启终端
2. Neovim 首次启动自动装 LazyVim 插件
3. `ollama pull qwen3:latest`
4. Docker Compose 部署 Open WebUI
5. `colima start`

### 回滚：
- `brew uninstall <name>` / `conda env remove -n <name>`
- `rustup self uninstall`
- 全部卸载：Homebrew uninstall 脚本

### 更新：brew update && brew upgrade && brew upgrade --cask --greedy
```
