# Phase 执行细节

本文件为 SE Design Skill 的各 Phase 详细执行指导。当 SKILL.md 中指示"参考 phase_details"时，读取对应 Phase 章节。

---

## Phase 3: IR→SR Decomposition 执行细节

### Step 3.1: 结构化 IR 输出

基于 Phase 2 的交互结果，填充设计资产表（参考 `assets/requirement_analysis_spec.md` 模版「4.1 结构化IR」章节）：

```markdown
## 结构化IR设计资产

| 设计资产 | 内容 | owner |
|----------|------|-------|
| IR标识 | [IR-版本-序号] | MKT |
| 名称 | [需求名称] | MKT |
| 描述 | [完整描述] | MKT |
| RR标识 | [关联RR] | MKT |
| 优先级 | [P0/P1/P2/P3] | MKT |
| Who | [利益相关方] | SE,MKT |
| What | [功能范围] | SE |
| Why | [业务驱动力] | SE |
| When | [时间约束/目标TR] | SE |
| Where | [部署环境] | SE |
| How | [方案方向] | SE |
| How much | [资源估算] | SE |
| 类别 | [功能类别] | SE |
| 场景列表 | [场景编号列表] | SE |
```

### Step 3.2: 系统上下文建模

使用 ASCII 字符图生成系统上下文图（参考 `references/diagram_guide.md` 中 ASCII 部分）：

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  终端用户     │────>│  目标系统         │────>│  外部系统A    │
│  (User)      │ 使用 │  (TargetSystem)  │ API │  (ExtSysA)   │
└──────────────┘     └──────────────────┘     └──────────────┘
                           │
                           │ IPC
                           v
                     ┌──────────────┐
                     │  外部系统B    │
                     │  (ExtSysB)   │
                     └──────────────┘
```

### Step 3.3: IR→SR 分解

**SR 分解规则**：
- 每个 SR 必须满足 **INVEST** 原则（Independent, Negotiable, Valuable, Estimable, Small, Testable）
- SR 编号规则：`SR-[IR编号]-[序号]`，例如 `SR-IR001-001`
- 每个 SR 必须关联至少一个验收标准
- 每个 SR 必须可追溯到其来源 IR（零遗漏）

**分解方法**：
- 按 **功能维度** 分解：每个独立功能点对应一个 SR
- 按 **场景维度** 分解：每个核心场景对应一个 SR
- 按 **DFX维度** 分解：关键非功能需求独立成 SR
- 避免将多个不相关功能合并到同一 SR 中

**SR 列表格式**：

```markdown
## SR 列表

| 序号 | IR编号 | IR描述 | SR编号 | SR标题 | SR描述 | 类别 | 验收标准 | 关联功能 |
| ---- | ------ | ------ | ------ | ------ | ------ | ---- | -------- | -------- |
```

### Step 3.4: 需求追踪矩阵生成

使用 ASCII 字符图生成 IR→SR 追踪矩阵图（参考 `references/diagram_guide.md` 中 ASCII 部分）。

### Step 3.5: 功能性需求分析

使用 ASCII 用例图表达功能需求场景（参考 `references/diagram_guide.md` 中 ASCII 用例图示例）。

### Step 3.6: DFX 非功能性需求分析

按需分析以下 DFX 维度（即使结论为"不适用"也需说明），维度清单与 `assets/requirement_analysis_spec.md` 模板对齐：

| DFX维度 | 分析内容 | 输出格式 |
|---------|---------|---------|
| 定界定位 | 系统边界、定位精度 | 表格 |
| 可靠性/可用性 | 可用性等级、容错策略 | 表格 + ASCII状态图 |
| 安全韧性隐私 | 权限、加密、隐私合规 | 表格 |
| 生命周期 | 交付、升级、退役策略 | 表格 |
| 漏洞 | 已知漏洞、修复计划 | 表格 |
| 可服务性 | 诊断、运维、升级 | 表格 |
| 可测试性 | 测试策略、验收标准 | 表格 |
| 功能安全 | 安全等级、失效模式 | FMEA表格 |
| 合规性 | 法规遵从 | 表格 |
| 本地遵从 | 数据本地化、本地法规 | 表格 |
| 开发者资料开发 | SDK、文档、示例 | 表格 |
| 伦理&AI治理 | AI伦理、治理框架 | 表格 |
| 其他DFX | 上述未覆盖的特殊维度 | 表格 |

### Step 3.7: 需求分析说明书生成

基于 `assets/requirement_analysis_spec.md` 模版，填充所有章节，生成完整的《需求分析说明书》。

---

## Phase 4: SR→AR Design 执行细节

### Step 4.1: 单个 SR 方案设计

对每个 SR，展示以下内容：

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Phase 4: SR→AR Design — SR-[编号]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### SR-[编号]: [SR标题]

#### 1. 需求点厘清

| 需求维度 | 内容 |
|---------|------|
| 输入 | [数据/事件/触发条件] |
| 输出 | [结果/状态变更/副作用] |
| 前置条件 | [必须满足的前提] |
| 后置条件 | [执行后的系统状态] |
| 约束条件 | [性能/安全/可靠性约束] |
| 验收标准 | AC-1: [标准]; AC-2: [标准] |

#### 2. 方案设计细节

**2.1 架构策略**（ADR记录）

| ADR字段 | 内容 |
|---------|------|
| ADR编号 | ADR-[SR编号]-[序号] |
| 决策标题 | [架构决策标题] |
| 状态 | [提议/已决定/已替代] |
| 背景 | [为什么需要做这个决策] |
| 决策 | [选择了什么方案] |
| 候选方案 | [方案A/方案B/方案C对比] |
| 理由 | [选择依据] |

**2.2 4+1 视图（按需选用）**

| 视图 | 是否使用 | 图表类型 | 交互展示方式 |
|------|---------|---------|-------------|
| 场景视图 | [使用/跳过] | [Use Case/Flowchart] | [ASCII] |
| 逻辑视图 | [使用/跳过] | [Class/ER] | [ASCII] |
| 过程视图 | [使用/跳过] | [Sequence/Activity] | [ASCII] |
| 开发视图 | [使用/跳过] | [Component/Package] | [ASCII] |
| 物理视图 | [使用/跳过] | [Deployment] | [ASCII] |

**2.3 接口契约（设计级）**

| 接口类型 | 名称 | 方向 | 描述 |
|---------|------|------|------|
| 提供接口 | [接口名] | 对外提供 | [功能描述] |
| 调用接口 | [接口名] | 对外调用 | [功能描述] |
| 进程间通信 | [IPC名] | 内部通信 | [通信机制] |

**2.4 DFX 设计要点**

| DFX维度 | 设计要点 |
|---------|---------|
| 可靠性 | [容错策略/降级方案] |
| 安全性 | [权限设计/加密策略] |
| 可测试性 | [测试策略/验证点] |
| 性能 | [性能目标/优化策略] |
| 可扩展性 | [模块化/隔离设计] |

#### 3. SR→AR 分配

| SR编号 | AR编号 | 分配目标（子系统/模块） | 分配说明 |
|--------|--------|----------------------|---------|
| SR-IR001-001 | AR-IR001-001-01 | [子系统X] | [分配说明] |

#### 4. 依赖关系

[使用 ASCII 字符图展示依赖关系图]
```

### Step 4.2: 4+1 视图选择指南

4+1 视图不是必须全部使用，根据 SR 特征按需选择：

| 视图 | 使用时机 | 交互展示 | 何时跳过 |
|------|---------|---------|---------|
| **场景视图** | 多角色交互的 SR | ASCII 用例图 | 单一角色、简单场景 |
| **逻辑视图** | 涉及复杂业务实体关系的 SR | ASCII 类图 | 无新增实体 |
| **过程视图** | 涉及异步/并发/多模块交互的 SR | ASCII 时序图 | 同步简单流程 |
| **开发视图** | 涉及多模块协作、新增部件的 SR | ASCII 组件图 | 单模块内部修改 |
| **物理视图** | 涉及多设备/多进程部署的 SR | ASCII 部署图 | 单设备单进程 |

### Step 4.3: 全部 SR 设计完成后生成依赖关系总图

所有 SR 方案设计完成后，使用 ASCII 字符图生成完整的 SR→AR 依赖关系总图（参考 `references/diagram_guide.md` 中 ASCII 部分）。

---

## Phase 5: Archiving 执行细节

### Step 5.1: 文档生成（Markdown + 自动生成 Docx）

生成 Markdown 文件后，**自动调用** `scripts/convert_docx.py` 产出对应的 Docx 文件（图表自动渲染为 PNG 嵌入），无需用户手动执行转换命令。

**输出物清单**：

| 序号 | 文档名称 | Markdown 文件 | Docx 文件（自动生成） | 说明 |
|------|---------|---------------|----------------------|------|
| 1 | 需求分析说明书 | `output/requirement_analysis_spec_[IR编号].md` | `output/requirement_analysis_spec_[IR编号].docx` | IR→SR 全链路文档 |
| 2~N | 功能设计说明书 | `output/functional_design_spec_SR-[编号].md` | `output/functional_design_spec_SR-[编号].docx` | 每个 SR 一份（SR→AR） |

**每份功能设计说明书必须包含的关键章节**：

1. **功能概述**：含架构总览图（PlantUML 组件图）
2. **增量 SR 清单**：本说明书对应的 SR
3. **需求点厘清**：输入/输出/前置/后置/约束/验收标准
4. **方案设计细节**：ADR + 4+1 视图 + 接口契约 + DFX 设计要点
5. **SR→AR 分配表**：分配需求与目标子系统
6. **依赖关系图**：GraphViz DOT
7. **FMEA 分析**：故障模式与影响分析表
8. **周边依赖关系**：网络/SDK/平台依赖

### Step 5.2: Docx 自动转换与图表渲染

Markdown 文件生成完毕后，**SE 自动执行**以下命令产出 Docx：

```bash
# 自动执行：Markdown → Docx，图表自动渲染嵌入
python3 scripts/convert_docx.py output
```

**图表渲染策略**（convert_docx.py 内置）：
1. 内置打包工具（scripts/plantuml.jar, scripts/graphviz/{platform}/）→ 优先使用
2. 系统工具（plantuml / dot / mmdc in PATH）→ 如已安装则使用
3. 源码文本 → 都不可用时，代码块以文本形式保留在 Docx 中

**CJK 字体**：渲染脚本自动检测系统 CJK 字体并注入配置（PlantUML: skinparam defaultFontName; DOT: graph+node+edge fontname），确保中文不乱码。macOS 使用 `-Tpng:quartz` 渲染器（Core Text），Linux 使用 `-Tpng:cairo`（Pango）。

> 如需单独渲染图表源文件（.puml / .dot）为 PNG，可使用 `scripts/render_diagrams.py`（可选工具）。

### Step 5.3: 归档目录结构

```
output/
├── requirement_analysis_spec_IR001.md      # 图表源码内嵌（PlantUML/DOT代码块）
├── requirement_analysis_spec_IR001.docx    # 图表渲染为PNG嵌入
├── functional_design_spec_SR-IR001-001.md
├── functional_design_spec_SR-IR001-001.docx
├── functional_design_spec_SR-IR001-002.md
├── functional_design_spec_SR-IR001-002.docx
└── diagrams/
    ├── IR001_usecase.png                   # 自动渲染缓存
    ├── IR001_traceability.png
    ├── SR-IR001-001_component.png
    └── SR-IR001-001_dependency.png
```