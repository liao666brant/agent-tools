# skills

个人 Agent Skills 仓库，符合 [skills.sh](https://skills.sh) 规范。

技能基于 [Anthropic Agent Skills](https://agent-sdk.anthropic.com/skills) 规范编写（目录 + `SKILL.md` frontmatter），兼容 Claude Code、Codex、OpenCode 等支持该规范的 agent。

## 技能列表

| 技能          | 说明                                                              |
| ------------- | ----------------------------------------------------------------- |
| git-commit    | 智能 Git 提交：conventional commits、自动语言检测、可指定语言     |
| commit-zh     | 中文 Git 提交：分析变更并生成中文 conventional commit message     |
| image-analyzer | 为当前主模型提供图像理解能力，非多模态模型自动委派 sonnet 读图   |
| code-review | 默认审查未提交改动，也可双轴审查指定基线后的仓库规范与需求实现   |
| review-fix-goal | 自包含的跨宿主审查修复闭环，最终复审清零后中文提交并推送       |
| skill-doctor | 基于本地真实 Agent 会话评估技能效果并生成改进报告 |
| update-skill | 创建或改进通用 Agent Skill 的结构、触发描述与工作流指令 |
| unslop | 清除文本中的 AI 腔、套话和机械结构，保留自然语气与作者个性 |
| show-me | 用精简图示、代码结构草图和 HTML 解释复杂主题 |
| index-project  | 项目 AI 上下文索引：以 AGENTS.md 为唯一事实来源，初始化/增量维护并收敛 CLAUDE.md |
| writing-for-agents | 为 Agent 编写低上下文负担、触发清晰且过程稳定的指令文档 |
| ux-writing | 用户可见文案与文档的清晰度、一致性与时效性检查 |
| scoped-change | 界定变更边界，避免超范围改动与遗漏必要位置 |
| wsl-windows-image | WSL 中读取 Windows 图片：自动转换 /mnt/<盘符>/ 路径并读图            |

## 来源与许可

- `ux-writing`：改编自 [scarletkc/agents 的 ux-writing](https://github.com/scarletkc/agents/tree/main/skills/ux-writing)，原作者 [scarletkc](https://github.com/scarletkc)，遵循 Apache-2.0 许可。
- `scoped-change`：改编自 [scarletkc/agents 的 scoped-change](https://github.com/scarletkc/agents/tree/main/skills/scoped-change)，原作者 [scarletkc](https://github.com/scarletkc)，遵循 Apache-2.0 许可。
- `skill-doctor`：中文化并适配自 [warpdotdev/common-skills 的 skill-doctor](https://github.com/warpdotdev/common-skills/tree/main/.agents/skills/skill-doctor)，原作者 Denver Technologies, Inc.，遵循 MIT 许可。
- `update-skill`：中文化并适配自 [warpdotdev/common-skills 的 update-skill](https://github.com/warpdotdev/common-skills/tree/main/.agents/skills/update-skill)，原作者 Denver Technologies, Inc.，遵循 MIT 许可。
- `unslop`：中文化并适配自 [Cursor plugins 的 pstack/unslop](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop)，原作者 Lauren Tan，遵循 MIT 许可。
- `show-me`：中文化并适配自 [HumanLayer skills 的 show-me](https://github.com/humanlayer/skills/tree/main/plugins/show-me/skills/show-me)，原作者 HumanLayer，遵循 MIT 许可。
- `writing-for-agents`：中文化并适配自 [mattpocock/skills 的 writing-for-agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents)，原作者 Matt Pocock，遵循 MIT 许可。

## 安装

```bash
npx skills add liao666brant/skills -g
```

`skills` CLI 会自动发现仓库 `skills/` 下的所有技能，并按当前 agent 写入对应的用户级 skills 目录（Claude Code、Codex、OpenCode 等），一套技能多端通用。

### 项目推荐安装

以下命令应在目标项目根目录运行；不带 `-g`，因此默认安装到当前项目。

#### 项目上下文

一次安装项目索引与 Agent 文档写作技能：

```bash
npx skills add liao666brant/skills --skill index-project --skill writing-for-agents
```

`index-project` 负责创建和维护项目 AI 上下文索引，`writing-for-agents` 用于编写或改进 Skill、`AGENTS.md` 和 `CLAUDE.md`。

#### 去 AI 味

一次安装文本去 AI 味与用户文案质量检查技能：

```bash
npx skills add liao666brant/skills --skill unslop --skill ux-writing
```

`unslop` 清理 AI 腔、套话和机械结构，`ux-writing` 检查用户可见文案与文档的清晰度、一致性和时效性。

## 目录结构

```
skills/
├── skills.sh.json          # skills.sh 展示分组配置
└── skills/                 # 技能目录
    ├── git-commit/
    │   └── SKILL.md
    ├── commit-zh/
    │   └── SKILL.md
    ├── image-analyzer/
    │   └── SKILL.md
    ├── code-review/
    │   ├── SKILL.md
    │   └── agents/
    │       └── openai.yaml
    ├── review-fix-goal/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── references/          # review.md / commit.md
    ├── skill-doctor/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   ├── assets/
    │   ├── references/
    │   ├── scorers/
    │   └── scripts/
    ├── update-skill/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── references/
    │       └── best-practices.md
    ├── unslop/
    │   ├── SKILL.md
    │   └── agents/
    │       └── openai.yaml
    ├── show-me/
    │   ├── SKILL.md
    │   └── agents/
    │       └── openai.yaml
    ├── index-project/
    │   ├── SKILL.md
    │   └── references/          # first-index.md / incremental-index.md
    ├── writing-for-agents/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── references/
    │       └── skill-mechanics.md
    ├── ux-writing/
    │   └── SKILL.md
    ├── scoped-change/
    │   └── SKILL.md
    └── wsl-windows-image/
        └── SKILL.md
```

## 添加新技能

1. 在 `skills/` 下新建目录，目录名即技能名（kebab-case）
2. 编写 `SKILL.md`，frontmatter 必须包含 `name` 和 `description`（description 决定触发时机）
3. 按需在技能目录内放脚本、参考文件等，随技能一起安装
