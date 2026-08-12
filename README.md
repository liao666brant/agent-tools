# agent-tools

个人 Agent Skills 仓库，符合 [skills.sh](https://skills.sh) 规范。

技能基于 [Anthropic Agent Skills](https://agent-sdk.anthropic.com/skills) 规范编写（目录 + `SKILL.md` frontmatter），兼容 Claude Code、Codex、OpenCode 等支持该规范的 agent。

## 技能列表

| 技能       | 说明                                                              |
| ---------- | ----------------------------------------------------------------- |
| git-commit | 智能 Git 提交：conventional commits、自动语言检测、可指定语言     |
| commit-zh  | 中文 Git 提交：分析变更并生成中文 conventional commit message     |

## 安装

```bash
npx skills add liao666brant/agent-tools -g
```

`skills` CLI 会自动发现仓库 `skills/` 下的所有技能，并按当前 agent 写入对应的用户级 skills 目录（Claude Code、Codex、OpenCode 等），一套技能多端通用。

## 目录结构

```
agent-tools/
├── skills.sh.json          # skills.sh 展示分组配置
└── skills/                 # 技能目录
    ├── git-commit/
    │   └── SKILL.md
    └── commit-zh/
        └── SKILL.md
```

## 添加新技能

1. 在 `skills/` 下新建目录，目录名即技能名（kebab-case）
2. 编写 `SKILL.md`，frontmatter 必须包含 `name` 和 `description`（description 决定触发时机）
3. 按需在技能目录内放脚本、参考文件等，随技能一起安装
