# Agent Skills Collection

Personal collection of agent skills for AI-assisted development workflows.

## Skills

### self-learning

通用自学系统。输入 `/learn <topic>` 启动智能学习流程。

**核心特性：**
- 科普性整体介绍：用通俗语言讲故事，串联各阶段知识点
- 全局知识图谱：结构化展示知识依赖关系
- 知识体系由浅入深：基础→原理→进阶→实战→融会贯通→前沿
- 动态图谱更新：每阶段完成后补充新发现的概念

**安装：** 将 `self-learning/` 目录复制到你的 skills 目录（如 `~/.agents/skills/`）

### viryoke-workflow

快速初始化完整的开发环境工作流。

**触发场景：**
- 用户提到"初始化环境"、"搭建开发环境"、"新机器配置"
- 用户要求按 TOOLCHAIN.md 配置工具链

**覆盖平台：** macOS / Linux / WSL2

**安装：** 将 `viryoke-workflow/` 目录复制到你的 skills 目录

## Installation

```bash
# Clone this repo
git clone https://github.com/viryoke/skills.git

# Copy skills to your agent's skills directory
cp -r skills/self-learning ~/.agents/skills/
cp -r skills/viryoke-workflow ~/.agents/skills/
```

## License

MIT