---
name: init-project
description: >
  Initialize or refresh a project's AI context documentation by generating/updating root and module
  AGENTS.md files for Codex/OpenCode, CLAUDE.md files for Claude Code compatibility, and structured
  context indexes such as .ai/index.json and .claude/index.json. Use when the user asks to initialize
  a project, generate project docs, build a project index, document architecture, create CLAUDE.md or
  AGENTS.md, support Codex/OpenCode/Claude project context, organize AI context, scan module structure,
  or says vague phrases like "整理一下这个项目", "了解项目结构", "初始化项目", "生成项目文档", "项目索引",
  "AI 上下文", or "init project".
---

# Init Project — 项目 AI 上下文初始化

为当前项目生成或刷新多 Agent 可用的上下文索引体系：根级/模块级 `AGENTS.md`、Claude Code 兼容用 `CLAUDE.md`、`.ai/index.json`、兼容用 `.claude/index.json`。

`AGENTS.md` 是主入口和公共事实源，必须优先服务 Codex 和 OpenCode；`CLAUDE.md` 只做 Claude Code 兼容壳和 Claude 专属补充，公共规则不要重复写两份。

## 输入

1. 先判断项目根目录，默认使用当前工作目录；如果用户指定路径，则使用用户指定路径。
2. 推断 `project_summary`：
   - 用户提供摘要或项目名时，直接使用并保留原意。
   - 未提供时，从 `package.json`、`README.md`、`pyproject.toml`、`go.mod`、`Cargo.toml`、目录名等高信号文件推断。
3. `target_clients` 默认包含 `codex`、`opencode`、`claude`；用户指定目标工具时按用户指定范围执行。
4. 支持用户额外要求，例如只扫某些模块、只刷新 `AGENTS.md`、继续上次缺口。

## 执行约束

- 只生成或更新文档、`.ai/index.json` 与兼容索引，不要修改业务源码、依赖锁文件或配置。
- 写入前必须读取已有 `AGENTS.md`、`CLAUDE.md`、`.ai/index.json`、`.claude/index.json`。
- 如果目标文件已有人工内容，优先只更新 `<!-- INIT-PROJECT:START -->` 到 `<!-- INIT-PROJECT:END -->` 之间的托管区块。
- 如果目标文件存在但没有托管区块，保留原文，并在合适位置插入新的托管区块；不要整文件覆盖。
- 不要默认创建 `AGENTS.override.md`。Codex 会优先读取 override 文件，乱建这玩意儿会把普通 `AGENTS.md` 架空。
- 不要让 `AGENTS.md` 和 `CLAUDE.md` 各自维护一套公共规则；发现重复或冲突时，把跨工具规则收敛到 `AGENTS.md`，`CLAUDE.md` 通过 `@AGENTS.md` 引用。
- 遵守 `.gitignore`，同时默认跳过 `.git`、`node_modules`、`dist`、`build`、`.next`、`coverage`、缓存目录、锁文件、大型二进制和媒体文件。
- 扫描全局 Claude/Codex/OpenCode 资源时，只写索引摘要和路径，不复制资源正文。

## 扫描流程

1. 获取一次运行时间戳，所有产物使用同一时间。
2. 读取忽略规则：
   - 优先读取项目根 `.gitignore`。
   - 合并默认忽略：`.git/**`、`node_modules/**`、`dist/**`、`build/**`、`.next/**`、`coverage/**`、`__pycache__/**`、`.venv/**`、`*.lock`、`*.log`、二进制和媒体文件。
3. 阶段 A：全仓清点。
   - 优先用 `rg --files` 获取文件清单；不可用时使用文件枚举工具分批列举。
   - 统计文件数、语言占比、目录拓扑。
   - 发现模块候选：`package.json`、`pyproject.toml`、`go.mod`、`Cargo.toml`、`apps/*`、`packages/*`、`services/*`、`cmd/*`、`crates/*`、`src/*`。
4. 阶段 B：模块扫描。
   - 入口与启动：`main.*`、`index.*`、`app.py`、`manage.py`、`cmd/*/main.go`、`src/main.rs`。
   - 对外接口：routes、controllers、api、openapi、proto、GraphQL schema。
   - 依赖与脚本：manifest、配置、启动脚本、Docker 文件。
   - 数据层：ORM 模型、schema、migrations、Prisma、SQL。
   - 测试与质量：`tests/**`、`__tests__/**`、`*.spec.*`、`*_test.go`、lint/type/test 配置。
5. 阶段 C：深度补捞。
   - 如果阶段 B 后无法判断接口、数据模型、测试策略或模块职责，追加分页读取目标目录。
   - 如果遇到时间、上下文或工具上限，先写可用结果，并在缺口里记录下一步补扫目录。

## 期望产物

- 根级 `AGENTS.md`：Codex/OpenCode 可直接读取的项目规则、命令、模块地图、AI 工作指引和资源索引；保持简洁，避免超过 Codex 默认 32 KiB 项目指令预算。
- 模块级 `AGENTS.md`：仅在模块需要更具体规则时生成；Codex 会按目录层级叠加读取，OpenCode 也可通过根级说明或 `opencode.json` instructions 使用。
- 根级 `CLAUDE.md`：Claude Code 兼容入口，默认导入 `@AGENTS.md`，只追加 Claude Code 专属规则。
- 模块级 `CLAUDE.md`：默认不生成；只有模块存在 Claude 专属规则时才生成，并导入同级或根级 `AGENTS.md`。
- `.ai/index.json`：中立结构化索引，记录模块清单、入口/接口/测试/重要路径、覆盖率、忽略统计、缺口清单、截断状态、生成状态。
- `.claude/index.json`：从 `.ai/index.json` 镜像或保留的 Claude 兼容索引。

## AGENTS.md 生成规范

根级 `AGENTS.md` 必须简洁、命令化、适合 Codex/OpenCode 自动读入。托管区块包含：

- 项目快照：一句话说明项目用途和主要技术栈。
- 工作守则：读取范围、禁止事项、提交/分支规则、危险操作确认。
- 常用命令：安装、开发、测试、lint、类型检查、构建。
- 架构地图：核心目录与模块职责，必要时链接到模块级文档。
- 模块规则：指向模块级 `AGENTS.md` 和 `.ai/index.json`，并要求按需读取。
- 资源索引：项目级和相关全局 agent/command/skill 资源简表。
- 变更记录。

控制根级 `AGENTS.md` 体量。Codex 默认项目指令预算约 32 KiB，详细清单放进 `.ai/index.json` 或模块文档，不要把全仓百科硬塞进去。

模块级 `AGENTS.md` 仅在模块需要独立规则时生成。对 Codex 来说，越靠近当前目录的 `AGENTS.md` 会补充根级规则；对 OpenCode 来说，根级 `AGENTS.md` 应明确提示按需读取模块级文件。

如果项目已有 `opencode.json`，读取其中 `instructions` 并在摘要中报告是否覆盖模块级 `AGENTS.md`。不要默认创建或修改 `opencode.json`；如用户明确要求，可建议加入类似 `packages/*/AGENTS.md` 的 instructions glob。

## CLAUDE.md 兼容规范

根级 `CLAUDE.md` 不再承载公共项目规则。默认生成轻量兼容壳：

```markdown
@AGENTS.md

<!-- INIT-PROJECT:START -->
## Claude Code

- Read `AGENTS.md` as the shared project instructions.
- Use `.claude/rules/` only for Claude-specific path-scoped rules.
- Keep shared build, test, style, architecture, and module rules in `AGENTS.md`.
<!-- INIT-PROJECT:END -->
```

规则：

- 如果根级 `CLAUDE.md` 已存在，确保它能读取 `AGENTS.md`：优先插入或保留 `@AGENTS.md`；不要用复制粘贴同步公共内容。
- 如果已有 Claude 专属人工内容，保留在 `## Claude Code` 或托管区块外的原位置。
- 如果已有内容是公共规则，迁移或总结到 `AGENTS.md`，并在摘要中说明。
- 模块级 `CLAUDE.md` 默认不生成。只有模块确实存在 Claude 专属规则时才生成，且第一行必须导入同级 `AGENTS.md`；没有同级 `AGENTS.md` 时导入相对路径的根级 `AGENTS.md`。
- 不要用 `CLAUDE.md` 存放 Mermaid 架构图、模块百科或全仓清单；这些内容放入 `AGENTS.md` 的简表或 `.ai/index.json`。

## 资源扫描

扫描并索引相关资源：

- Claude 项目级：`.claude/agents/**/*.md`、`.claude/commands/**/*.md`、`.claude/skills/**/SKILL.md`
- Claude 全局级：`~/.claude/agents/**/*.md`、`~/.claude/commands/**/*.md`、`~/.claude/skills/**/SKILL.md`
- Claude 插件级：`~/.claude/plugins/cache/**/agents/**/*.md`、`~/.claude/plugins/cache/**/commands/**/*.md`、`~/.claude/plugins/cache/**/skills/**/SKILL.md`
- Codex 项目级：`.codex/agents/**/*.md`、`.codex/commands/**/*.md`、`.codex/skills/**/SKILL.md`
- Codex 全局级：`~/.codex/AGENTS.md`、`~/.codex/agents/**/*.md`、`~/.codex/commands/**/*.md`、`~/.codex/skills/**/SKILL.md`
- Codex 插件级：`~/.codex/plugins/cache/**/agents/**/*.md`、`~/.codex/plugins/cache/**/commands/**/*.md`、`~/.codex/plugins/cache/**/skills/**/SKILL.md`
- OpenCode 项目级：`.opencode/agent/**/*.md`、`.opencode/command/**/*.md`、`opencode.json`
- OpenCode 全局级：`~/.config/opencode/AGENTS.md`、`~/.config/opencode/agent/**/*.md`、`~/.config/opencode/command/**/*.md`、`~/.config/opencode/opencode.json`

只提取 `name`、`description`、工具类型、来源工具和路径。按项目技术栈与目录职责过滤，避免把无关资源全塞进索引。

## 结构化索引

写入 `.ai/index.json` 作为中立索引；同时写入或镜像 `.claude/index.json` 以保持旧流程兼容。至少包含：

- `generated_at`
- `project_summary`
- `project_root`
- `target_clients`
- `modules`
- `coverage`
- `ignored`
- `gaps`
- `truncated`
- `outputs`
- `agents_index`
- `instruction_files`

写入后必须验证 JSON 可解析。

## 完成标准

完成后向用户汇报：

1. 写入或更新了哪些文件。
2. 识别了哪些模块，每个模块一句话职责。
3. `AGENTS.md`、`CLAUDE.md`、`.ai/index.json`、`.claude/index.json` 的创建/更新状态。
4. 扫描覆盖率、跳过目录、主要缺口、是否截断。
5. `.ai/index.json` 和 `.claude/index.json` 是否写入并能被解析。
6. 下一步建议，例如继续补扫的目录或需要用户确认的业务语义。
