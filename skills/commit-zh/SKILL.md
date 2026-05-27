---
name: commit-zh
description: '中文 Git 提交技能。分析变更并生成中文 conventional commit message。当用户说"提交"、"commit"、"提交代码"、"提交变更"、"/commit-zh" 时触发。全程主 agent 执行，不使用 subagent。'
---

# 中文 Git 提交

分析暂存/未暂存变更，生成中文 conventional commit message，主 agent 全程执行。

## Conventional Commit 格式

```
<type>[(scope)]: <中文描述>

[可选正文]

[可选脚注]
```

**type/scope 始终英文**，subject/body/footer 中文。

## Commit Types

| Type       | 用途          |
| ---------- | ------------- |
| `feat`     | 新功能        |
| `fix`      | 修复 bug      |
| `docs`     | 文档变更      |
| `style`    | 格式/样式     |
| `refactor` | 重构          |
| `perf`     | 性能优化      |
| `test`     | 测试相关      |
| `build`    | 构建系统/依赖 |
| `ci`       | CI/配置变更   |
| `chore`    | 维护/杂项     |
| `revert`   | 回退提交      |

## 工作流

### 1. 检查仓库状态

```bash
git status --porcelain
```

无变更则停止。

### 2. 分析 Diff

```bash
# 有暂存文件用暂存 diff
git diff --staged

# 无暂存用工作区 diff
git diff
```

### 3. 暂存文件（如需）

无暂存时按逻辑分组暂存：

```bash
git add path/to/file1 path/to/file2
```

- 按逻辑关联分组
- **禁止**暂存可能含密钥的文件（.env、credentials、private keys）
- **禁止** `git add .` / `git add -A`
- 多逻辑单元 → 建议拆分多次提交

### 4. 生成 Commit Message

- **Type**：变更类型（英文）
- **Scope**：目录/模块名（英文，可省略）
- **Subject**：中文摘要，祈使句式，≤72 字符
- **Body**：`- ` 列表解释 why/what，≤3 条，每条 ≤72 字符
- **Footer**：破坏性变更/issue 引用

#### 格式约束

1. Subject ≤72 字符，无句号
2. Body：subject 后空一行，`- ` 开头，说明意图和原因
3. Footer：body 后空一行，git trailer（如 `Closes #123`），破坏性变更用 `BREAKING CHANGE: <描述>` + type 后加 `!`

#### 示例

```text
feat(auth): 添加 OAuth2 登录支持

- 实现 Google 和 GitHub 第三方登录
- 添加用户授权回调处理
- 优化登录状态持久化逻辑

Closes #42
```

```text
feat(api)!: 重新设计认证 API

- 从 session 认证迁移到 JWT
- 更新所有端点签名
- 移除已废弃的登录方式

BREAKING CHANGE: 认证 API 已完全重新设计，所有客户端需更新集成
```

### 5. 执行或建议拆分

- **单一逻辑单元**：直接提交，无需确认
- **多逻辑单元**：建议拆分，等确认后执行

### 6. 执行提交

```bash
git commit -m "$(cat <<'EOF'
<type>[(scope)]: <中文描述>

<body>

<footer>
EOF
)"
```

**禁止自动推送**。仅本地提交，除非用户明确要求。

### 7. 提交后

```bash
git log --oneline -1
```

## 安全协议

- 禁止修改 git config
- 禁止破坏性命令（--force、hard reset）除非用户明确要求
- 禁止跳过 hooks（--no-verify）除非用户明确要求
- 禁止提交含密钥/可能含密钥的文件
- 单一逻辑变更直接提交，多逻辑单元建议拆分后等确认
- 禁止自动推送，仅本地提交
