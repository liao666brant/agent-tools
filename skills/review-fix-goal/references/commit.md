# 内建中文提交与推送

全部有效 finding 已关闭且验证通过后，展示最终 `git status`、拟提交文件、diff 摘要和当前分支，取得对准确提交方案的明确确认。推送在提交后的门禁中单独确认；当前会话已准确确认同一方案时不重复询问，用户及更高优先级指令始终优先。仅调用本技能不替代尚未取得的提交或推送确认。

确认后确定目标文件和 hunk。同文件混有范围外改动时，可安全分离则使用能隔离目标、保留工作树及范围外 index 状态的部分提交方式；仅在无法安全分离时保留现场并询问。不得对混合 hunk 执行整路径 `git add` 或 `git commit --only`。

排除 `.env`、凭据、私钥或其他疑似敏感文件，禁止 `git add .` 和 `git add -A`。仅当目标路径全部变化均属于本次确认范围时，才用显式路径 `git add -- <目标路径>`，并以 `git diff --check HEAD -- <目标路径>`、`git diff HEAD -- <目标路径>` 和 `git status --short` 复核内容。部分提交则检查隔离后实际待提交的 diff 和空白问题。目标 diff 为空时停止；提交前出现的新变化也必须重新核对范围。

整文件提交可使用 `git commit --only -m <message> -- <目标路径>`，使其他路径原有暂存继续留在 index。`--only` 读取目标文件的工作树内容，不提供 hunk 隔离；部分提交使用其已核实的隔离方式，不能再退回整路径命令。所有路径和值都作为独立参数传递，不拼接未经解析的输入。

提交信息使用中文 Conventional Commit：

```text
<type>[(scope)]: <中文祈使句摘要>

- <可选的意图或原因，最多三条>
```

`type` 和可选 `scope` 使用英文；`type` 从 `feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`build`、`ci`、`chore`、`revert` 中选择；摘要不超过 72 个字符且不加句号。破坏性变更使用 `!` 和 `BREAKING CHANGE:`，issue 引用放在 footer。不得修改 Git 配置、跳过 hooks 或自动 amend。

提交成功后，核对新提交 SHA、实际内容及范围外 index 状态，从同一 fixed point 审查共同祖先到 `HEAD` 的已提交 diff，并确认本次目标变更没有遗留的暂存、未暂存或未跟踪变化。若 hooks 改变了内容或发现新的有效 finding，不得推送，回到复核或修复循环；下一次提交前重新确认准确方案，已准确覆盖同一方案的确认不重复取得。

## 推送门禁

最终审查全部有效 finding 已关闭后，确定目标 remote 和远端分支；有 upstream 时使用其 remote/ref，新分支优先使用判断默认分支时的 remote，其次使用唯一 remote。remote 或目标分支不明确时询问用户。先 `git fetch <remote>` 刷新远端引用，再确定比较基线：目标远端分支存在时使用其 remote-tracking ref；新远端分支使用该 remote 的默认分支 ref。

确认比较基线是 `HEAD` 的祖先，否则停止。随后展示 `git log --oneline <remote-base>..HEAD --` 和对应 diff 摘要，将完整待推送提交列表与最终审查覆盖的提交及目标记录逐项核对；任何任务开始前已存在但未纳入本目标的提交，以及其他未审查或范围外提交，都必须阻止推送。不要自动 rebase 或 cherry-pick；如需迁移目标提交，先说明风险并取得明确确认，再从远端基线创建干净分支，迁移后重新执行最终审查和本门禁。待推送列表为空时不推送。

仅在待推送提交全部属于本目标后，展示准确的 remote、source ref、destination ref 和普通 `git push` 命令，按当前环境规则取得推送方案的明确确认；当前会话已准确确认同一方案时不重复询问，更高优先级指令始终优先。禁止 force push。推送成功后，读取远端目标 ref 确认其 SHA 与本次 `HEAD` 一致，再完成持久 goal 或任务清单。
