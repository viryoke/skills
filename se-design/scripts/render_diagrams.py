#!/usr/bin/env python3
"""渲染 PlantUML 和 GraphViz DOT 图表为 PNG，用于归档阶段（Phase 5）

使用内置打包工具或系统工具，无需联网。
自动注入 CJK 字体配置，确保中文不乱码。

用法: python3 render_diagrams.py <diagrams_dir>
例如: python3 render_diagrams.py output/diagrams
"""

import os
import sys
import re
import shutil
import subprocess
import glob
import platform

# ─── CJK 字体检测 ───

def detect_cjk_font():
    """检测系统可用的 CJK 字体，返回字体名"""
    plat = platform.system()
    if plat == "Windows":
        candidates = ["Microsoft YaHei", "SimHei", "SimSun"]
    elif plat == "Darwin":
        candidates = ["PingFang SC", "Heiti SC", "STHeiti"]
    else:
        candidates = ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "Droid Sans Fallback"]

    if plat == "Linux" or plat == "Darwin":
        try:
            result = subprocess.run(
                ["fc-list", ":lang=zh", "family"],
                capture_output=True, text=True, timeout=5,
            )
            available = result.stdout
            for font in candidates:
                if font.lower() in available.lower():
                    return font
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    elif plat == "Windows":
        return candidates[0]

    return candidates[0]


def inject_plantuml_font(code, cjk_font):
    """在 PlantUML 源码中注入 CJK 字体配置"""
    font_line = "skinparam defaultFontName " + cjk_font + "\n"
    if "@startuml" in code and "skinparam defaultFontName" not in code:
        code = code.replace("@startuml", "@startuml\n" + font_line, 1)
    return code


def inject_dot_font(code, cjk_font):
    """在 GraphViz DOT 源码中注入 CJK 字体配置（graph+node+edge 三级）"""
    # 替换已知不支持中文的字体名
    for bad_font in ["Helvetica", "Arial", "DejaVu Sans", "Liberation Sans"]:
        code = code.replace('fontname="' + bad_font + '"', 'fontname="' + cjk_font + '"')
    # 如果全局没有 fontname，在首个 digraph/graph 行后注入
    if "fontname=" not in code:
        code = re.sub(
            r"(digraph\s+\w+\s*\{)",
            r'\1\n    graph [fontname="' + cjk_font + '"]; node [fontname="' + cjk_font + '"]; edge [fontname="' + cjk_font + '"];',
            code, count=1,
        )
    return code


# ─── 工具检测 ───

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_platform_dir():
    """获取当前平台的 GraphViz 目录名"""
    system = platform.system().lower()
    if system == "windows":
        return "win64"
    elif system == "darwin":
        return "darwin"
    else:
        return "linux"


def find_plantuml_cmd():
    """检测 PlantUML（Homebrew openjdk → 系统 java → 系统 plantuml）"""
    bundled_jar = os.path.join(SCRIPTS_DIR, "plantuml.jar")
    java_cmd = None

    # 优先检测 Homebrew openjdk（macOS 上 /usr/bin/java 可能是 stub）
    homebrew_paths = [
        "/opt/homebrew/opt/openjdk/bin/java",       # Apple Silicon
        "/usr/local/opt/openjdk/bin/java",           # Intel Mac
    ]
    for path in homebrew_paths:
        if os.path.isfile(path):
            try:
                result = subprocess.run(
                    [path, "-version"],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    java_cmd = path
                    break
            except (subprocess.TimeoutExpired, OSError):
                pass

    # 如果 Homebrew openjdk 不可用，检测系统 java
    if not java_cmd:
        sys_java = shutil.which("java")
        if sys_java:
            try:
                result = subprocess.run(
                    [sys_java, "-version"],
                    capture_output=True, text=True, timeout=5,
                )
                if result.returncode == 0:
                    java_cmd = sys_java
            except (subprocess.TimeoutExpired, OSError):
                pass

    if os.path.isfile(bundled_jar) and java_cmd:
        return [java_cmd, "-jar", bundled_jar]
    if not java_cmd and os.path.isfile(bundled_jar):
        print("[提示] PlantUML 渲染需要 Java，当前不可用")
        print("  macOS: brew install openjdk")
        print("  Linux: sudo apt-get install default-jre")
    if shutil.which("plantuml"):
        return ["plantuml"]
    return None


def find_dot_cmd():
    """检测 GraphViz dot（内置 → 系统），返回 [cmd, renderer_flag]"""
    plat = _get_platform_dir()
    if plat == "win64":
        bundled_dot = os.path.join(SCRIPTS_DIR, "graphviz", plat, "bin", "dot.exe")
    else:
        bundled_dot = os.path.join(SCRIPTS_DIR, "graphviz", plat, "bin", "dot")
    # 平台专用渲染器：macOS 用 quartz（Core Text 支持 CJK），Linux 用 cairo（Pango 支持 CJK）
    renderer_flag = {"darwin": "-Tpng:quartz", "linux": "-Tpng:cairo", "win64": "-Tpng"}.get(plat, "-Tpng")
    if os.path.isfile(bundled_dot):
        return [bundled_dot, renderer_flag]
    if shutil.which("dot"):
        return ["dot", renderer_flag]
    return None


# ─── 本地渲染 ───

def render_plantuml_local(cmd, puml_files, output_dir):
    """使用本地 PlantUML 渲染（自动注入 CJK 字体，绝对路径避免嵌套目录）"""
    cjk_font = detect_cjk_font()
    print("使用本地 PlantUML: " + " ".join(cmd) + " (CJK字体: " + cjk_font + ")")
    abs_output_dir = os.path.abspath(output_dir)
    for puml_file in puml_files:
        print("  本地渲染: " + puml_file)
        # 读取源码，注入字体配置，写入临时文件渲染
        with open(puml_file, "r", encoding="utf-8") as f:
            code = f.read()
        code = inject_plantuml_font(code, cjk_font)
        # 写入带字体配置的临时文件（使用绝对路径避免 PlantUML 路径嵌套）
        tmp_path = os.path.abspath(puml_file) + ".cjk"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(code)
        result = subprocess.run(
            cmd + ["-tpng", "-o", abs_output_dir, tmp_path],
            capture_output=True, text=True,
        )
        os.remove(tmp_path)
        if result.returncode != 0:
            print("[错误] 本地渲染失败: " + puml_file)
            print("  " + result.stderr.strip())
            return False
    return True


def render_graphviz_local(cmd, dot_files, output_dir):
    """使用本地 GraphViz dot 渲染（自动注入 CJK 字体，平台专用渲染器）"""
    cjk_font = detect_cjk_font()
    # cmd = [dot_binary, renderer_flag]，如 ["dot", "-Tpng:quartz"]
    print("使用本地 GraphViz: " + cmd[0] + " 渲染器: " + cmd[1] + " (CJK字体: " + cjk_font + ")")
    for dot_file in dot_files:
        basename = os.path.splitext(os.path.basename(dot_file))[0]
        png_path = os.path.join(output_dir, basename + ".png")
        print("  本地渲染: " + dot_file + " -> " + png_path)
        # 读取源码，注入字体配置，写入临时文件渲染
        with open(dot_file, "r", encoding="utf-8") as f:
            code = f.read()
        code = inject_dot_font(code, cjk_font)
        tmp_path = dot_file + ".cjk"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(code)
        result = subprocess.run(
            cmd + [tmp_path, "-o", png_path],
            capture_output=True, text=True,
        )
        os.remove(tmp_path)
        if result.returncode != 0:
            print("[错误] 本地渲染失败: " + dot_file)
            print("  " + result.stderr.strip())
            return False
    return True


# ─── 主逻辑 ───

def render_with_fallback(label, source_files, output_dir,
                         local_cmd_fn, local_render_fn):
    """渲染入口：内置工具 → 系统工具 → 保留源码"""
    print("=== 渲染 " + label + " 图表 ===")
    if not source_files:
        print("未找到 " + label + " 源文件")
        return True

    local_cmd = local_cmd_fn()
    if local_cmd:
        if local_render_fn(local_cmd, source_files, output_dir):
            print(label + ": 渲染成功 (" + local_cmd[0] + ")")
            return True

    print("[提示] " + label + " 渲染不可用，源文件保留在文档中")
    if label == "GraphViz":
        print("  Mac: brew install graphviz")
        print("  Linux: sudo apt-get install graphviz")
    elif label == "PlantUML":
        print("  需要安装 Java (JRE)")
    return False


# ─── Main ───

def main():
    diagrams_dir = sys.argv[1] if len(sys.argv) >= 2 else "output/diagrams"
    src_dir = os.path.dirname(diagrams_dir) or "output"
    os.makedirs(diagrams_dir, exist_ok=True)

    # 搜索源文件（在 src_dir 和 diagrams_dir 中递归查找，去重）
    puml_files = set()
    for base in [src_dir, diagrams_dir]:
        puml_files.update(glob.glob(os.path.join(base, "**", "*.puml"), recursive=True))
        puml_files.update(glob.glob(os.path.join(base, "**", "*.plantuml"), recursive=True))
    puml_files = sorted(puml_files)

    dot_files = set()
    for base in [src_dir, diagrams_dir]:
        dot_files.update(glob.glob(os.path.join(base, "**", "*.dot"), recursive=True))
        dot_files.update(glob.glob(os.path.join(base, "**", "*.gv"), recursive=True))
    dot_files = sorted(dot_files)

    plantuml_ok = render_with_fallback(
        "PlantUML", puml_files, diagrams_dir,
        find_plantuml_cmd, render_plantuml_local,
    )
    print("")
    graphviz_ok = render_with_fallback(
        "GraphViz", dot_files, diagrams_dir,
        find_dot_cmd, render_graphviz_local,
    )

    # ─── 摘要 ───
    print("")
    print("=== 渲染摘要 ===")
    print("PNG 文件目录: " + diagrams_dir)
    png_files = glob.glob(os.path.join(diagrams_dir, "*.png"))
    if png_files:
        for f in sorted(png_files):
            print("  " + os.path.basename(f) + " (" + str(os.path.getsize(f)) + " bytes)")
    else:
        print("(暂无 PNG 文件)")

    if not plantuml_ok or not graphviz_ok:
        print("")
        print("[提示] 部分图表未渲染为 PNG，源码保留在 Markdown 中，可后续手动渲染")


if __name__ == "__main__":
    main()