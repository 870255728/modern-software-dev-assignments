# Warp 多 Agent 工作手册

本文记录 Week 5 多工作区流程，使任务边界、权限和验证方式可复现、可审计。

## 前置条件

在本地安装并登录 Warp，通过 SSH 连接服务器：

```bash
ssh root@190.92.200.190
cd /root/modern-software-dev-assignments/week5
```

将 `.warp/workflows/` 中的两个 YAML 文件导入 Warp Drive。`Week 5 Agent Worktrees` Workflow 可重复执行：已有分支或 worktree 会被复用。

## 两个独立工作单元

### 工作单元 A：Notes CRUD

目录：`/root/worktrees/week5-task3/week5`

```text
阅读 AGENTS.md，并完成 docs/TASKS.md 的任务 3。增加 Note 的 PUT 和
DELETE 接口、输入校验、失败回滚的乐观编辑/删除 UI，以及成功、404
和无效输入测试。只修改 week5/。运行质量门、检查 diff，并只提交本
任务。不要合并或推送。
```

### 工作单元 B：Action Items

目录：`/root/worktrees/week5-task4/week5`

```text
阅读 AGENTS.md，并完成 docs/TASKS.md 的任务 4。增加完成状态筛选、
任意 ID 不存在时整体回滚的事务性批量完成、筛选和多选 UI，以及后
端测试。只修改 week5/。运行质量门、检查 diff，并只提交本任务。
不要合并或推送。
```

## 监督与集成

每个工作单元只能修改自己的 worktree、运行本地检查并创建 feature commit。合并和推送由 Supervisor 完成：

```bash
cd /root/modern-software-dev-assignments
git switch xyp
git merge --no-ff week5-task3
git merge --no-ff week5-task4
```

合并时应同时保留 Notes 与 Action Items 的 schema、路由和前端功能。解决冲突后检查完整 diff，并运行 `Week 5 Quality Gate`。

## 审计合约

一次完整执行应保留：

- 每个任务的 Prompt 和最终 commit hash；
- 工作区、分支和权限边界；
- 干净合并或冲突解决记录；
- 最终质量门 PASS 结果；
- Warp 实际生成的 Session 或 Saved Prompt 链接。

普通 shell、Codex 或其他工具的执行记录不等同于 Warp Agent Session。只有 Warp 界面实际生成的证据才能标记为 Warp Agent 证据。

## 本次可复现结果

| 工作单元 | 分支 | 提交 | 隔离验证 |
| --- | --- | --- | --- |
| Notes | `week5-task3` | `59c3a4c` | 15 passed |
| Action Items | `week5-task4` | `afd9a76` | 8 passed |
| 最终集成 | `xyp` | 合并历史 | 20 passed |

由于本地 Warp 账户没有可用的付费 Agent 额度，本次没有生成公开 Warp Agent Session URL；仓库保留的是任务合约、worktree、提交、冲突记录和质量门结果。
