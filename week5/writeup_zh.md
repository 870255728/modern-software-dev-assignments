# 第 5 周作业报告

## 提交信息

姓名：**XYP**

SUNet ID：**[填写你的 SUNet ID]**

所选任务：**任务 3——带乐观 UI 更新的完整 Notes CRUD（中等）**，以及 **任务 4——Action Items 筛选与批量完成（中等）**

完成时间：**约 3.5 小时；提交前请替换为你的实际耗时**

参考资料：[作业说明](assignment.md)、[Warp YAML Workflows](https://docs.warp.dev/terminal/entry/yaml-workflows)、[Warp Rules](https://docs.warp.dev/agent-platform/capabilities/rules)、[Warp Drive Prompts](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/prompts)、[Warp 多 Agent 指南](https://docs.warp.dev/guides/agent-workflows/how-to-run-multiple-ai-coding-agents/)、[Warp 中的 Git worktrees](https://docs.warp.dev/code/git-worktrees)，以及 [Warp SSH 功能支持](https://docs.warp.dev/code/ssh-feature-support)。

> **证据检查点：**提交前，请替换方括号中的 SUNet ID 和 Warp 链接，导出真实的 Warp Drive Prompt，并附上 [`docs/warp/EVIDENCE.md`](docs/warp/EVIDENCE.md) 中列出的截图。本仓库不会把非 Warp 运行冒充为 Warp 使用证据。

## 自动化 A：Warp Drive 质量门与项目规则

### a. 设计：目标、输入、输出和步骤

自动化 A 由三个可复用部分组成：

1. `AGENTS.md` 是项目级 Rule。它要求每个 Agent 只能在 `week5/` 内工作，保持现有行为兼容，为新增功能添加测试，使用隔离的分支或 worktree，检查自己的 diff，并把最终集成和推送留给监督者。
2. `.warp/workflows/week5-quality-gate.yaml` 是参数化的仓库 Workflow。其输入为 Week 5 目录和 pytest 测试范围。它调用 `scripts/quality_gate.sh`，由脚本确定项目目录和 Python 环境，然后以快速失败方式依次执行 pytest、Ruff、Black 和 `git diff --check`。
3. `docs/warp/QUALITY_GATE_PROMPT.md` 中的 Saved Prompt 模板增加了 Agent 审查层。它的 `mode` 输入可选 `report` 或 `fix`，其中 report 模式被有意设计为只读。输出是简洁的 PASS/FAIL 汇总、首个可操作原因以及变更文件列表。

Workflow 和辅助脚本均可重复执行，并支持无交互运行。Warp Drive Prompt 分享链接：**[粘贴真实的 Warp 分享链接]**。

### b. 自动化前后对比

自动化之前，我必须记住四条命令，在正确的环境中逐条运行，分别检查失败原因，而且可能只运行了部分检查就误报成功。自动化之后，一个可搜索的 Warp 入口即可对完整测试套件或单个测试选择器执行同一套质量门。Shell 脚本也可以在 SSH 和 CI 中使用，因此验证策略并不依赖 Warp 界面。

初始基线只有 3 个通过的测试，并伴随 4 条依赖弃用警告。两个功能完成并进行小型兼容性清理后，同一个质量门得到的结果是：**20 个测试通过、Ruff PASS、Black PASS、Git 空白检查 PASS，并且没有警告**。

### c. 自主程度与监督方式

我在每个阶段都采用与任务相匹配的最小权限。审查 Prompt 默认使用只读的 report 模式：可以读取文件、检查 Git 和运行测试，但不能编辑、提交、合并、删除或推送。功能 Agent 只能在分配给自己的 `week5/` worktree 中编辑和执行本地验证。Git 合并和推送始终由人工监督者完成。

在接受每个分支之前，我检查了变更文件列表、接口行为、测试断言和最终 diff。整个流程不需要破坏性命令，也没有启用不受限制的“run until completion”。

### d. 多 Agent 说明

项目 Rule 为两个功能 Agent 提供了相同的完成标准，因此各自的 Prompt 只需要关注任务特有的行为。这减少了重复指令，并使两个 Agent 的完成报告可以直接比较。质量门充当 fan-in 合约：只有四项检查全部通过，分支才可以进入集成阶段。

### e. 实际使用方式及解决的痛点

我分别在未修改的 starter、Action Items 合并后，以及最终 Notes 冲突解决后运行质量门。它在兼容性清理阶段捕获了一个真实的集成问题：虽然 20 个测试全部通过，但 Ruff 仍然拒绝了未排序的 import block。在应用 Ruff 的安全 import 修复并重新运行完整质量门后，所有检查才真正通过。这说明功能测试本身不足以作为完成信号。

## 自动化 B：使用 Git worktree 的并发 Agent 工作流

### a. 设计：目标、输入、输出和步骤

该自动化的目标是在不允许 Agent 相互覆盖文件的前提下，并发完成两个中等难度任务。`scripts/setup_agent_worktrees.sh` 通过 `.warp/workflows/week5-agent-worktrees.yaml` 暴露为 Warp Workflow，用于创建或复用以下工作区：

| 角色 | 分支 | Worktree | 输出 |
| --- | --- | --- | --- |
| Notes Agent | `week5-task3` | `/root/worktrees/week5-task3` | Commit `59c3a4c` |
| Action Agent | `week5-task4` | `/root/worktrees/week5-task4` | Commit `afd9a76` |
| 监督者 | `xyp` | `/root/modern-software-dev-assignments` | 审查后的合并结果与最终质量门 |

Agent A 实现了 `PUT /notes/{id}`、`DELETE /notes/{id}`、带长度限制的 Pydantic 请求模型，以及支持失败回滚的乐观编辑/删除 UI。其隔离分支最终有 15 个测试通过。Agent B 实现了布尔完成状态筛选、缺失 ID 时整体回滚的原子批量完成，以及筛选和批量选择 UI。其隔离分支最终有 8 个测试通过。完整 Warp Prompt 和复现步骤位于 [`docs/WARP_MULTI_AGENT_PLAYBOOK.md`](docs/WARP_MULTI_AGENT_PLAYBOOK.md)。

Warp Agent Session 链接：**Notes [粘贴 URL]**；**Action Items [粘贴 URL]**。

### b. 自动化前后对比

手工方案只能顺序执行：先实现一个任务，重新加载上下文，再实现另一个任务。在同一个 checkout 中打开两个普通终端虽然更快，却不安全，因为两个任务都会修改 `schemas.py`、`app.js`、`index.html` 和 `styles.css`。Worktree 使两个 Agent 可以并发写入和提交，同时保持独立文件状态和可审查的提交历史。

该工作流没有消除集成工作，而是让集成成本变得明确。每个 Agent 先产生聚焦的提交和测试报告，然后监督者再按顺序合并两个分支。

### c. 自主程度与监督方式

每个 Agent 只获得其 worktree 内的文件写入和命令执行权限。它可以检查应用、编辑属于本任务的六个文件、运行 pytest/lint/format 检查，并创建一个功能提交。Prompt 明确禁止修改 `writeup.md`、合并、删除文件和推送。

我通过分支状态、commit hash、测试数量和 diff review 进行监督。只有监督者可以解决冲突并运行集成后的完整测试套件。

### d. 角色、协调、收益、风险与失败

两个任务在 API 层面相互独立，但共享前端和 schema 文件。明确的任务所有权避免了范围漂移，worktree 防止了并发文件覆盖，commit hash 提供了清晰的交接点。第一次合并 Action Items 时没有冲突，并通过了 8 个测试。第二次合并 Notes 时，`backend/app/schemas.py` 和 `frontend/styles.css` 出现了真实冲突。

我没有直接选择某一个分支的版本，而是合并 Pydantic import 和模型，并保留两组 CSS 选择器。`app.js` 和 `index.html` 由 Git 自动合并。冲突解决后，集成质量门通过了全部 20 个测试。

这次冲突是并发带来的主要成本，也是有价值的结果：隔离可以防止意外覆盖，但重叠的设计表面仍然需要人工集成判断。SSH 环境还限制了 Warp 的原生索引、文件树、编辑器和 code-review UI，因此 Agent 使用终端命令和 Git diff 工作；Warpified SSH 仍然支持 Agent 对话和命令执行。

### e. 实际使用方式及解决的痛点

该工作流加速了两个自包含功能的实现，同时把它们的历史和失败域相互隔离。它还形成了可复现的教学材料：其他贡献者可以导入 Workflow，运行可重复执行的 worktree 初始化，把两个任务合约粘贴到不同 Warp tab 中，然后比较两个 Agent 的输出。

最终运行时 smoke test 中，`/`、`/openapi.json`、`/notes/` 和带筛选条件的 `/action-items/` 均返回 HTTP 200；使用合法请求体更新不存在的 Note 时，按预期返回 404。

## 最终结果

- 任务 3 和任务 4 已在后端和原生 JavaScript UI 中完整实现。
- 事务回滚、筛选、CRUD、参数验证和资源不存在行为均有测试覆盖。
- 最终质量门结果：**20 passed**、Ruff PASS、Black PASS、`git diff --check` PASS。
- Warp 自动化定义、辅助脚本、Prompt 模板、多 Agent 操作手册、证据索引、实现指南和实验室汇报指南均已纳入 `week5/` 版本控制。
