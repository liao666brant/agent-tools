# Agent Skill 编写最佳实践

创建和维护通用 Agent Skill 时使用本参考。规则不依赖特定 Agent 或安装目录。

## 目录

- [渐进式披露](#渐进式披露)
- [编写有效描述](#编写有效描述)
- [精简原则](#精简原则)
- [代码示例格式](#代码示例格式)
- [工作流与简单指令](#工作流与简单指令)
- [常见反模式](#常见反模式)
- [命名约定](#命名约定)
- [迭代 Skill](#迭代-skill)

## 渐进式披露

Skill 分三层加载内容：

1. **元数据。** `name` 和 `description` 用于发现，通常始终可见。
2. **`SKILL.md` 正文。** 只有 Skill 触发后才加载。
3. **参考文件。** 仅在当前任务需要时加载。

### 何时使用参考文件

尽量让 `SKILL.md` 保持在 150 至 200 行以内。内容变长时，选择真正适合当前任务的拆分方式。

**高层指南配直接引用**

```markdown
## 高级功能

- 详细配置见 [references/config.md](references/config.md)
- API 说明见 [references/api.md](references/api.md)
- 完整示例见 [references/examples.md](references/examples.md)
```

**按独立领域组织**

```text
skill-name/
├── SKILL.md
└── references/
    ├── domain-a.md
    ├── domain-b.md
    └── domain-c.md
```

处理 `domain-a` 时只加载对应文件，不要顺带读取其他领域。

**基础说明内联，条件细节外置**

```markdown
## 基本用法

直接写主路径。

高级配置见 [references/advanced.md](references/advanced.md)。
```

参考文件只保持一层深度，由 `SKILL.md` 直接链接。不要让参考文件继续充当路由器。超过 100 行的参考文件应提供目录。

## 编写有效描述

Agent 通过 `description` 判断是否加载 Skill，因此描述必须可区分。

1. **写具体并包含关键词。**
   - 好：`为代码变更添加功能开关并更新对应测试。`
   - 差：`帮助处理功能。`
2. **同时写清能力和触发场景。**
   - 能力：`编写、改进并运行 Rust 单元测试。`
   - 场景：`适用于修改 Rust 测试或用户提到 cargo test 时。`
3. **直接陈述动作。**
   - 好：`添加功能开关以控制代码路径。`
   - 差：`我可以帮你添加功能开关。`
   - 差：`你可以使用本 Skill 添加功能开关。`
4. **加入真正参与发现的词。** 使用目标文件、命令、格式或领域名，而不是堆积同义词。
5. **只添加有价值的边界。** 当两个 Skill 容易混淆时说明排除项；不要把描述写成完整功能清单。

## 精简原则

Skill 与系统指令、会话历史和其他 Skill 共享上下文。每段文字都应证明自己的价值。

逐项询问：

- Agent 是否真的需要这段解释？
- 这是普通能力，还是无法从任务和代码恢复的约束？
- 这段内容是否会改变决策或避免真实错误？

**精简示例：**

````markdown
## 提取 PDF 文本

使用 pdfplumber：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

不要先解释 PDF 是什么、有哪些库、为什么文件常见，再进入真正步骤。Agent 已经知道这些常识。依赖选择若没有项目证据，也不要写成“推荐”。

## 代码示例格式

### 标注语言

所有代码围栏都应标注语言：

```rust
pub fn example() {
    println!("始终标注语言");
}
```

```bash
cargo nextest run --workspace
```

### 匹配任务形状

工作流型 Skill 可以使用前后对比：

````markdown
### 修改前

```rust
if FeatureFlag::YourFeature.is_enabled() {
    run_new_behavior();
} else {
    run_old_behavior();
}
```

### 修改后

```rust
run_new_behavior();
```
````

命令示例给出完整参数：

```bash
cargo clippy --workspace --all-targets --all-features --tests -- -D warnings
```

只有参数含义不明显且会影响结果时才解释。优先选择能从命令本身读懂的写法。

## 工作流与简单指令

### 何时使用工作流

顺序会影响结果时使用编号步骤：

```markdown
1. 分析表单结构。
2. 创建字段映射。
3. 验证映射。
4. 填写表单。
5. 检查输出。
```

只有复杂流程确实需要跨步骤追踪时才加入清单。不要给三步小任务附带状态模板。

### 何时使用简单指令

直接任务应直接说明目标：

````markdown
## 添加功能开关

在 `app/Cargo.toml` 中添加：

```toml
[features]
your_feature_name = []
```

再用项目现有的运行时检查保护新路径。
````

## 常见反模式

### Windows 风格路径

通用仓库路径使用正斜杠：

- 好：`scripts/helper.py`、`references/guide.md`
- 差：`scripts\helper.py`、`references\guide.md`

只有指令明确针对 Windows 原生路径时才使用反斜杠。

### 模糊描述

- 差：`帮助处理文档。`
- 好：`从 PDF 提取文本和表格，并填写 PDF 表单。`

### 过多选项

不要无差别罗列工具：

- 差：`可以使用 pypdf、pdfplumber、PyMuPDF 或其他库。`
- 好：根据目标仓库已有依赖和输入类型选一个主路径；只有扫描件需要 OCR 等真实分支时再说明替代方案。

### 易过期信息

不要把日期、当前版本或临时迁移状态写成长期规则。

- 差：`2025 年 8 月前使用旧 API。`
- 好：说明如何从权威配置或官方文档查询当前方法；若必须兼容旧路径，写明可检测的条件。

### 术语不一致

同一概念只使用一个名称。不要在同一文档中混用“API 端点”“URL”“API 路由”和“路径”，除非它们确实代表不同对象。

### 解释常识

- 差：`Git 是一种跟踪文件变化的版本控制系统。`
- 好：`使用 git --no-pager diff 查看不经分页器处理的差异。`

### 过度组织

不是每个 Skill 都需要“概述、最佳实践、示例、FAQ”四套章节。

- 简单 Skill：标题和直接指令。
- 中等 Skill：范围、主路径和必要约束。
- 复杂 Skill：入口路由加按需参考资料。

### 无证据的绝对规则

不要把一次故障、个人偏好或某个仓库的约定推广到所有项目。先确认规则是否属于平台不变量、目标仓库约束，或仅是本次任务选择。

### 未授权的副作用

创建或更新 Skill 不等于获准安装、暂存、提交、推送、发布、创建外部资源或修改用户级配置。把这些动作留在用户明确授权的范围内。

## 命名约定

名称应使用小写字母、数字和连字符，并与目录名一致。优先选择短且可发现的动作名称。

可用形式：

- 动作型：`process-pdfs`、`analyze-spreadsheets`
- 名词短语：`pdf-processing`、`spreadsheet-analysis`
- 维护型：`update-skill`、`review-code`

避免：

- 模糊名称：`helper`、`utils`、`tools`
- 过于宽泛：`documents`、`data`、`files`
- 只有内部团队才能理解的缩写

## 迭代 Skill

根据实际使用改进 Skill：

1. 观察 Agent 在哪里成功、犹豫或反复试错。
2. 找出缺失、模糊或导致误触发的信息。
3. 只修改能解决该问题的描述或章节。
4. 用相似的真实请求验证行为是否改善。

保持每次迭代聚焦。不要预先添加未经验证的规则，也不要为了一个示例累积永久例外。
