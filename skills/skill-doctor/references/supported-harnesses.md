# 支持的会话来源

本文件统一说明 `skill-doctor` 支持的会话格式、来源参数和技能目录。执行技能的 Agent 需要具备本地文件访问与 Python 脚本执行能力；下表限定采集器支持的数据来源，不限定执行技能的宿主。

## 启动检查

| 来源 | 采集器标识 | 本地会话存储 |
| --- | --- | --- |
| Warp | `warp` | 以只读方式访问 Warp 会话数据库 |
| Claude Code | `claude` | 项目历史 JSONL |
| Codex | `codex` | Rollout JSONL |
| Pi | `pi` | Pi Agent JSONL，默认位于 `~/.pi/agent/sessions` |
| Grok Build | `grok` | Chat history JSONL，默认位于 `~/.grok/sessions` |
| ZCode | `zcode` | Model-io rollout，默认位于 `~/.zcode/cli/rollout` |

从运行时上下文确认当前宿主的执行能力，不要根据磁盘上的日志推断正在使用哪个宿主。用户明确指定的来源不在表中、无法对应到受支持的格式，或宿主不能运行采集器时，在创建报告目录和读取会话前停止，说明未读取任何会话及需要补充的来源或能力。

## 选择会话来源

- `--harness auto`：默认值，扫描所有本机可用的受支持来源。
- `--harness all`：同样请求全部受支持来源。
- `--harness <采集器标识>`：仅采集表中指定的一种来源。
- 报告只包含一种来源时，`inventory.json` 的 `harness` 使用该来源标识；包含多种来源时使用 `mixed`。

ZCode rollout 当前不提供可用于项目归属的工作目录，因此仅在 `--all-conversations` 模式下纳入评估；按项目筛选时会排除这类会话。仅采集 ZCode 时，需要用 `--skills-dir PATH` 指定技能目录，或用 `--include-global-skills` 纳入全局技能。采集器使用其最后一个非空请求上下文作为会话摘要。

Pi 会话目前不识别子代理身份；Grok Build 带有 `synthetic_reason` 的合成会话始终排除，`--include-subagents` 不会将其纳入。

非标准存储位置可通过以下参数指定：

- `--claude-home PATH`：Claude Code 配置目录。
- `--codex-home PATH`：Codex 主目录。
- `--warp-db PATH`：Warp 数据库路径，可重复传入。
- `--warp-data-dir PATH`：Warp 渠道数据目录。
- `--pi-home PATH`：Pi Agent 主目录，默认 `~/.pi/agent`。
- `--grok-home PATH`：Grok Build 主目录，默认 `~/.grok`。
- `--zcode-home PATH`：ZCode 主目录，默认 `~/.zcode`。

## 技能目录

项目技能从以下位置发现：

- `skills`
- `.agents/skills`
- `.claude/skills`
- `.codex/skills`

添加 `--include-global-skills` 时，还会发现用户主目录下的 `~/.claude/skills`、`~/.agents/skills`，以及配置的 Codex、Pi、Grok Build、ZCode 主目录中的 `skills`。后三者的默认位置分别是 `~/.pi/agent/skills`、`~/.grok/skills` 和 `~/.zcode/skills`。
