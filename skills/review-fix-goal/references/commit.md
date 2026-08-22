# 内建中文提交与推送

审查 clean 且验证通过后，展示最终 `git status`、拟提交文件、diff 摘要和当前分支。按当前环境的危险操作规则，先取得对准确提交范围和 `git commit` 的明确确认；推送在提交后单独确认，触发本技能本身不替代任一确认。

确认后确定本目标的完整文件路径；同一文件中混有范围外改动且无法安全分离时停止并询问用户。排除 `.env`、凭据、私钥或其他疑似敏感文件后，只用显式路径执行 `git add -- <目标路径>`，禁止 `git add .` 和 `git add -A`。紧接着用 `git diff --check HEAD -- <目标路径>`、`git diff HEAD -- <目标路径>` 和 `git status --short` 复核将要提交的准确内容；目标 diff 为空则停止。

使用 `git commit --only -m <message> -- <目标路径>` 提交，使目标路径之外原本已暂存的用户改动继续留在 index 且不进入本次提交。所有路径和值都作为独立参数传递，不拼接未经解析的输入。

提交信息使用中文 Conventional Commit：

```text
<type>[(scope)]: <中文祈使句摘要>

- <可选的意图或原因，最多三条>
```

`type` 和可选 `scope` 使用英文；`type` 从 `feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`build`、`ci`、`chore`、`revert` 中选择；摘要不超过 72 个字符且不加句号。破坏性变更使用 `!` 和 `BREAKING CHANGE:`，issue 引用放在 footer。不得修改 Git 配置、跳过 hooks 或自动 amend。

提交成功后，从同一 fixed point 审查共同祖先到 `HEAD` 的已提交 diff，并确认本目标没有遗留的暂存、未暂存或未跟踪变化。若 hooks 改变了内容或发现新 finding，不得推送；回到修复循环，并在下一次提交前重新确认。

## 推送门禁

最终审查 clean 后，确定目标 remote 和远端分支；有 upstream 时使用其 remote/ref，新分支优先使用判断默认分支时的 remote，其次使用唯一 remote。remote 或目标分支不明确时询问用户。先 `git fetch <remote>` 刷新远端引用，再确定比较基线：目标远端分支存在时使用其 remote-tracking ref；新远端分支使用该 remote 的默认分支 ref。

确认比较基线是 `HEAD` 的祖先，否则停止。随后展示 `git log --oneline <remote-base>..HEAD --` 和对应 diff 摘要，将完整待推送提交列表与最终审查覆盖的提交及目标记录逐项核对；任何任务开始前已存在但未纳入本目标的提交，以及其他未审查或范围外提交，都必须阻止推送。不要自动 rebase 或 cherry-pick；如需迁移目标提交，先说明风险并取得明确确认，再从远端基线创建干净分支，迁移后重新执行最终审查和本门禁。待推送列表为空时不推送。

仅在待推送提交全部属于本目标后，展示准确的 remote、source ref、destination ref 和普通 `git push` 命令，并按当前环境规则再次取得明确确认。禁止 force push。推送成功后才完成持久 goal 或任务清单。
