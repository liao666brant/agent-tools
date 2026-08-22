# 内建 Code Review

## 审查范围

每轮都审查 fixed point 与 `HEAD` 的共同祖先到当前工作树的完整状态，以同时覆盖已提交、已暂存和未暂存的已跟踪变化；另外逐个读取非忽略的未跟踪文件。下面是 POSIX shell 示例，其他 shell 使用等价参数调用，不照抄变量语法：

```bash
base_commit="$(git rev-parse --verify --end-of-options "${fixed_point}^{commit}")"
merge_base="$(git merge-base "$base_commit" HEAD)"
git log --oneline "${base_commit}..HEAD" --
git status --short
git diff --check "$merge_base" --
git diff --find-renames "$merge_base" --
git ls-files --others --exclude-standard -z
```

固定点解析失败或无法确定共同祖先时停止，不猜测默认分支。用户限定了路径时，对 diff 和未跟踪文件应用同一路径范围。`git diff "$merge_base"` 不包含未跟踪文件；逐个读取这些文件，并在需要时用 `git diff --no-index -- /dev/null "$review_file"` 审查，返回 1 仅表示存在内容差异。

## 证据与标准

先读完整 diff、提交列表和受影响文件上下文，再按需读取调用方、测试和配置；不凭单行 diff 推断行为。需求来源按以下顺序查找：

1. 用户提供的需求文本、路径或链接；
2. 提交信息引用的本地 issue、设计或需求文件；
3. `docs/`、`specs/`、`.scratch/` 及与分支或功能名称相符的本地文档。

再读取根目录及相关子目录的 `AGENTS.md`、`CLAUDE.md`、`CONTRIBUTING.md`、编码规范、README、架构文档和语言工具配置。嵌套规则优先；只把实际读取到的内容当作证据。

分别执行两条审查轴：

- **Standards**：仓库约定、行为边界、错误处理、资源释放、并发、数据完整性、安全、重复和不必要抽象，以及风险所需的测试覆盖。
- **Spec**：逐条核对可用需求，检查缺失、错误、边界偏差和没有需求依据的扩张。无可用需求时跳过，不以猜测替代。

只记录有可验证位置、证据和影响的问题。优先级为 `P0` 严重事故或阻断、`P1` 高概率功能错误、`P2` 合并前应处理的质量问题、`P3` 可选改进。每项记录优先级、位置、根因、证据、最小修复方向和状态；纯风格偏好、自动化已可靠拦截的问题和未复核猜测不是 finding。敏感值只报告类型和位置，不复述内容。
