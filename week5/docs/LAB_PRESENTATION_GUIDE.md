# 实验室汇报指南：用 Warp 完成 Week 5

## 汇报目标

建议控制在 12-15 分钟。主线不是“AI 帮我写了多少代码”，而是：**把一个模糊开发任务变成可约束、可并行、可验证、可复现的 Agent 工作流。**

## 时间安排与讲稿

### 1. 问题与目标（1 分钟）

> 这次作业要求我在一个 FastAPI + SQLite + 静态前端项目中完成至少两个任务，同时使用 Warp Drive 自动化和 Warp 多 Agent。我选择了两个 medium 任务：Notes 完整 CRUD，以及 Action Items 过滤和事务性批量完成。

指出手工流程的三个痛点：重复执行检查、并行修改互相覆盖、Agent 成功声明缺少独立验证。

### 2. 基线与约束（2 分钟）

展示 `AGENTS.md`，重点解释：只改 `week5/`、保持 API 兼容、每个新行为必须有测试、禁止 Agent 自行 merge/push。展示改动前 `3 passed` 的基线。

> 规则负责约束“Agent 应该怎样工作”，不是描述某一个具体任务。这样两个 Agent 会共享同一套工程标准。

### 3. Automation A：质量门（2 分钟）

展示 Warp Drive 中的 **Week 5 Quality Gate** 和三个参数。运行后解释四层检查：pytest 验证行为、Ruff 检查静态问题、Black 检查格式、`git diff --check` 捕获空白错误。

> 自动化前，我需要记住并逐条执行命令；自动化后，一个可参数化入口给出一致结果。默认 report 模式只读，因此适合作为监督步骤。

### 4. Automation B：并行 Agent（3 分钟）

展示两个同时运行的 Warp tab，以及 `git worktree list`：

```text
xyp             -> integration
week5-task3     -> Notes Agent
week5-task4     -> Action Items Agent
```

> 两个 Agent 各自拥有独立工作目录和分支，因此并发写文件不会互相覆盖。它们都会修改前端，这会把风险推迟到一次明确、可审核的集成，而不是产生隐蔽的数据竞争。

展示两个提交和合并记录。若出现过冲突，说明如何同时保留 Notes 与 Action Items UI；若没有冲突，不要声称发生过。

### 5. 功能演示（3 分钟）

按以下顺序现场操作：

1. 创建 Note，编辑标题/内容，再删除。
2. 说明 UI 先更新，网络失败时会回滚。
3. 创建三个 Action Item，完成其中一个。
4. 切换 All/Open/Completed。
5. 选择多个未完成项并批量完成。
6. 打开 `/docs` 展示新增 API 和 Pydantic schema。

演示事务性语义时，可以在 Swagger 中提交一个存在 ID 与一个不存在 ID，随后 GET 列表，证明存在 ID 没被部分更新。

### 6. 结果、风险和反思（2 分钟）

展示最终测试数量和质量门 PASS。总结：并行缩短了独立实现阶段，但没有消灭集成成本；worktree 解决文件覆盖，测试解决行为回归，人工 diff review 解决 Agent “看似完成”的风险。

明确局限：SSH 下 Warp 使用终端命令读写远端文件，原生远程索引、文件树和 diff 能力有限；因此本次工作流把 Git diff 和测试结果作为主要监督界面。

## 推荐现场窗口

提前打开并命名：

1. `Warp - Integration`：主分支、Quality Gate。
2. `Warp - Task 3`：Notes Agent 对话。
3. `Warp - Task 4`：Action Items Agent 对话。
4. 浏览器 UI。
5. 浏览器 `/docs`。

不要现场重新安装依赖或临时创建 worktree。演示前运行一次质量门，并准备截图作为网络或模型不可用时的备用证据。

## 常见提问

**为什么不用一个 Agent 完成所有任务？** 任务的 API 代码相互独立，适合并行；分离上下文也减少提示词污染。

**为什么还需要人工监督？** Agent 能执行步骤，但无法替代对事务语义、API 兼容性和合并结果的责任判断。

**为什么选择 worktree 而不是两个普通 tab？** 普通 tab 共享同一工作目录，并发写同一文件可能覆盖；worktree 将文件状态和分支同时隔离。

**自动化是否真正可复用？** 是。YAML Workflow 参数化了目录和测试范围，脚本从自身位置解析项目目录，也可以只运行单个测试文件。

**最大的失败风险是什么？** 两个 Agent 同时修改 `frontend/app.js`。解决方案是独立提交、主分支显式合并、完整质量门和手工 UI 验收。

## 汇报前检查

- 把真实 Warp Prompt 分享链接填入 `writeup.md`。
- 截图两个 Agent 并发、两个提交、最终 PASS。
- 将个人姓名、SUNet ID 和真实耗时填入 writeup。
- 确认前端演示数据已准备，SSH tunnel 正常。
- 确认远程分支已推送，GitHub collaborators 已添加。
