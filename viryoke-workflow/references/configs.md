# 配置文件参考

本文档包含阶段 8 需部署的配置文件内容。

---

## 统一主题标准

- **主题**：Dracula (#282a36 背景 / #f8f8f2 文字)
- **字体**：JetBrainsMono Nerd Font 14pt
- **透明度**：opacity=0.92
- **模糊**：blur=true（毛玻璃效果）

---

## 配置文件清单

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

---

## ~/.zshrc

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

---

## ~/.gitconfig（delta 配色）

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

> 必须询问真实 email。GPG/SSH 签名可选追加。

---

## ~/.config/ghostty/config

```
theme = "dracula"
font-family = "JetBrainsMono Nerd Font"
font-size = 14
window-opacity = 0.92
window-blur = true
```

---

## ~/.config/starship.toml

```toml
# Dracula 主题配色
[character]
success_symbol = "[➜](bold green)"
error_symbol = "[➜](bold red)"

[directory]
style = "bold purple"

[git_branch]
style = "bold yellow"

[git_status]
style = "bold red"
```

---

## ~/.config/zellij/config.kdl

```kdl
theme "dracula"
pane_frames {
    transparent_bg true
}
```

---

## VS Code settings.json

**路径：**
- macOS: `~/Library/Application Support/Code/User/settings.json`
- Linux/WSL2: `~/.config/Code/User/settings.json`

```json
{
  "editor.fontFamily": "'JetBrainsMono Nerd Font', 'Cascadia Mono NF', monospace",
  "editor.fontSize": 14,
  "editor.fontLigatures": true,
  "workbench.colorTheme": "Dracula",
  "workbench.fontAliasing": "antialiased"
}
```

---

## Obsidian app.json

**路径：** `<vault>/.obsidian/app.json`

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

---

## ~/.config/opencode/config.toml

```toml
theme = "dracula"
```

---

## TUI 工具 Dracula 配色

各工具配置文件需设置 Dracula 配色，保持视觉一致性：
- lazygit: `~/.config/lazygit/config.yml`
- lazydocker: `~/.config/lazydocker/config.yml`
- bottom: `~/.config/bottom/bottom.toml`
- gh-dash: `~/.config/gh-dash/config.yml`

具体配色参数参考 Dracula 官方文档或 TOOLCHAIN.md §2.2。