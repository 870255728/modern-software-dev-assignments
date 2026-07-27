# Week 5 逐句展示讲稿

> **汇报人私有材料：不要投屏展示。** 本文只用于提示台词、切屏顺序、时间控制和故障备用方案。观众应看到 `docs/WEEK5_PRESENTATION.md` 及其中列出的项目证据文件。

## 使用方法

这份文档用于现场照稿讲解。每个步骤包含三种标记：

- **【操作】**：你在屏幕上做什么。
- **【讲稿】**：可以直接逐字说出的内容。
- **【提示】**：不要念出来，只用于提醒节奏、重点或备用方案。

完整汇报约 **16–20 分钟**。如果只有 10 分钟，可跳过标记为“可压缩”的段落。

---

## 0. 汇报前准备

### 0.1 提前打开的窗口

**【操作】** 提前准备以下窗口，不要现场临时寻找文件：

1. 浏览器：GitHub 上的 `docs/WEEK5_PRESENTATION.md`。
2. 编辑器：`docs/WEEK5_PRESENTATION.md` 的“项目目标”和 `docs/TASKS_ZH.md`。
3. 编辑器：`docs/IMPLEMENTATION_ZH.md`。
4. 编辑器：`docs/AGENT_RULES_ZH.md`。
5. 编辑器：`.warp/workflows/week5-quality-gate.yaml`。
6. 编辑器：`scripts/quality_gate.sh`。
7. 编辑器：`docs/WARP_MULTI_AGENT_PLAYBOOK_ZH.md`。
8. 终端：主仓库 `/root/modern-software-dev-assignments`。
9. 浏览器：`http://localhost:8000`。
10. 浏览器：`http://localhost:8000/docs`。

**【提示】** 如果不方便打开十个窗口，至少准备编辑器、终端、Web UI 和 Swagger 四个窗口。

### 0.2 启动服务

**【操作】** 本地建立 tunnel：

```bash
ssh -L 8000:127.0.0.1:8000 root@190.92.200.190
```

**【操作】** 在远程服务器启动应用：

```bash
cd /root/modern-software-dev-assignments/week5
PYTHONPATH=. /root/miniconda3/envs/cs146s/bin/python -m uvicorn \
  backend.app.main:app --host 127.0.0.1 --port 8000
```

**【提示】** 演示前确认首页和 `/docs` 能打开。预先创建两条 Note 和三个 Action Item，避免现场全部从零输入。

---

## 1. 开场：我要展示什么（约 1 分钟）

**【操作】** 打开 `docs/WEEK5_PRESENTATION.md`，停留在标题和“汇报目标”部分。

**【讲稿 1】**

> 大家好，我今天汇报的是 Week 5：The Modern Terminal。

**【讲稿 2】**

> 这周的重点不是简单地让 AI 帮我补全代码，而是把终端变成一个可以组织、监督和验证 Agent 工作流的开发环境。

**【讲稿 3】**

> 我会展示两个方面：第一，如何通过项目规则和质量门约束 Agent；第二，如何通过 Git worktree 让两个 Agent 在相互隔离的目录中并发工作。

**【讲稿 4】**

> 最后我会现场演示新增功能，并运行完整质量门，证明结果不仅能运行，而且通过了自动化测试、静态检查和格式检查。

**【讲稿 5】**

> 整个流程可以概括成五个阶段：规则约束、worktree 隔离、并发实现、人工集成、自动验证。

**【提示】** 说到五个阶段时，用鼠标指向文档中的粗体流程。

---

## 2. 作业要求与选题（约 1.5 分钟）

### 2.1 展示作业要求

**【操作】** 打开 `docs/WEEK5_PRESENTATION.md`，滚动到“项目目标”。

**【讲稿 1】**

> 作业要求至少选择两个功能任务，并且必须同时使用两类 Warp 能力。

**【讲稿 2】**

> 第一类是 Warp Drive，例如 Saved Prompt、Rule、Workflow 或 MCP；第二类是在不同 Warp tab 中运行并发的多 Agent 工作流。

**【讲稿 3】**

> 除了实现功能，writeup 还必须解释自动化的设计、输入输出、自动化前后对比、自主权限，以及多 Agent 的并发收益和风险。

### 2.2 展示所选任务

**【操作】** 打开 `docs/TASKS_ZH.md`，分别定位“任务 3”和“任务 4”。

**【讲稿 4】**

> 我选择的第一个任务是 Task 3，难度是 medium：为 Notes 增加完整的更新和删除接口，并在前端实现乐观 UI 更新和失败回滚。

**【讲稿 5】**

> 第二个任务是 Task 4，同样是 medium：为 Action Items 增加完成状态筛选，以及具有事务语义的批量完成接口。

**【讲稿 6】**

> 我选择这两个任务，是因为它们在后端 API 层面相对独立，适合并行；但它们又会共同修改 schema 和前端文件，所以可以真实观察多 Agent 集成时的冲突风险。

**【提示】** 最后一句是选题理由，必须讲出来，它能自然引出 worktree。

---

## 3. 原始项目架构（约 1.5 分钟）

**【操作】** 打开 `docs/IMPLEMENTATION_ZH.md`，展示 Mermaid 架构图。

**【讲稿 1】**

> 这是项目的整体架构。它是一个很小但完整的全栈应用。

**【讲稿 2】**

> 浏览器端使用原生 JavaScript，没有 Node 构建链；前端通过 JSON HTTP 请求调用 FastAPI。

**【讲稿 3】**

> FastAPI Router 负责接口，Pydantic 负责请求校验，SQLAlchemy 负责数据库会话和事务，最终数据存储在 SQLite。

**【讲稿 4】**

> 测试使用 pytest 和 FastAPI TestClient。每个测试都会使用独立的临时 SQLite 数据库，因此不会依赖演示环境中的 `data/app.db`。

**【讲稿 5】**

> 在这个架构中，Warp 的角色不是替代 FastAPI 或 pytest，而是把开发步骤、权限约束和质量检查组织成一个可重复的入口。

### 3.1 说明初始基线

**【讲稿 6】**

> 开始修改前，项目只有 3 个测试通过，并且存在 4 条 FastAPI 和 Pydantic 的弃用警告。

**【讲稿 7】**

> 最终项目增加到 20 个测试，并且通过兼容性清理消除了这些警告。

---

## 4. Automation A：Agent 项目规则（约 2 分钟）

### 4.1 为什么需要规则

**【操作】** 打开 `docs/AGENT_RULES_ZH.md`，依次指向“项目结构”“测试规范”和“Agent 权限边界”。

**【讲稿 1】**

> 第一个自动化组件是项目 Rule。屏幕上是 `AGENTS.md` 的中文等价摘要；英文原件仍保存在仓库根目录。它不是某一个具体任务的 Prompt，而是所有 Agent 都必须遵守的项目规则。

**【讲稿 2】**

> 我把不会随任务变化的信息写进 Rule，例如目录结构、运行测试的方法、Black 和 Ruff 的格式要求，以及 Git 提交规范。

**【讲稿 3】**

> 这样做的好处是，我不需要在每个任务 Prompt 中重复解释整个仓库，Agent 可以把更多上下文用于当前任务。

### 4.2 指出关键规则

**【操作】** 滚动到 `Agent-Specific Instructions`。

**【讲稿 4】**

> 第一条关键规则是只能修改 `week5/`，避免 Agent 影响其他周的作业。

**【讲稿 5】**

> 第二条规则是先检查现有行为，再做最小修改，并且不能覆盖用户已有的无关改动。

**【讲稿 6】**

> 第三条规则是并发 Agent 必须使用独立分支或 Git worktree。

**【讲稿 7】**

> 最后一条是 Agent 只能完成自己的功能提交，最终合并和推送必须留给监督者。

### 4.3 权限设计

**【讲稿 8】**

> 这体现了我采用的自主策略：允许 Agent 在任务目录中读取、编辑和运行测试，但不允许它自行扩大作用范围、删除文件、合并分支或推送。

**【讲稿 9】**

> 换句话说，Agent 可以执行工程步骤，但最终接受权仍然在人。

---

## 5. Automation A：Warp Quality Gate（约 2.5 分钟）

### 5.1 展示 Workflow

**【操作】** 打开 `.warp/workflows/week5-quality-gate.yaml`。

**【讲稿 1】**

> 第二个组件是一个参数化的 Warp YAML Workflow，名称是 Week 5 Quality Gate。

**【讲稿 2】**

> 它有两个输入：Week 5 的绝对路径，以及要运行的 pytest 测试范围。

**【讲稿 3】**

> 默认测试范围是整个 `backend/tests`，但也可以替换成单个测试文件或 selector，用于更快的局部反馈。

**【讲稿 4】**

> Workflow 本身保持很薄，只负责切换到正确目录并调用辅助脚本。

### 5.2 展示脚本

**【操作】** 打开 `scripts/quality_gate.sh`。

**【讲稿 5】**

> 真正的验证逻辑在这个 Shell 脚本中。

**【操作】** 指向 `set -euo pipefail`。

**【讲稿 6】**

> `set -euo pipefail` 保证任何命令失败、未定义变量或管道失败都会中止流程，避免后面的成功输出掩盖前面的错误。

**【操作】** 指向 `WEEK5_DIR` 和 `PYTHON_BIN`。

**【讲稿 7】**

> 脚本从自身路径解析 Week 5 目录，并明确使用 `cs146s` 环境中的 Python，因此不会依赖调用者当前在哪个目录或 PATH 是否正确。

**【操作】** 指向四个质量检查命令。

**【讲稿 8】**

> 第一层 pytest 验证业务行为；第二层 Ruff 检查静态问题；第三层 Black 检查格式；第四层 `git diff --check` 捕获空白和冲突标记问题。

**【讲稿 9】**

> 这四层关注不同风险，任何一层都不能完全替代其他层。

### 5.3 Before vs. After

**【讲稿 10】**

> 自动化之前，我必须记住四条命令，并确认自己在正确的 Conda 环境和目录中。

**【讲稿 11】**

> 自动化之后，一个入口就能执行同一套标准，而且这个脚本不仅能在 Warp 中运行，也能直接用于 SSH 或 CI。

**【讲稿 12】**

> 实际集成中，20 个测试已经全部通过，但 Ruff 仍然发现 import 排序问题。这个例子说明，测试通过不等于整个工程质量门通过。

---

## 6. Automation B：两个 Agent 的任务划分（约 2 分钟）

**【操作】** 打开 `docs/WARP_MULTI_AGENT_PLAYBOOK_ZH.md`，显示两个中文任务 Prompt。

**【讲稿 1】**

> 第二类自动化是多 Agent 工作流。我没有给两个 Agent 一个模糊的共同目标，而是明确划分任务所有权。

**【讲稿 2】**

> Agent A 只负责 Notes CRUD，包括 PUT、DELETE、校验、乐观 UI 和相关测试。

**【讲稿 3】**

> Agent B 只负责 Action Items 筛选和批量完成，包括事务回滚、筛选 UI、复选框和测试。

**【讲稿 4】**

> 两个 Prompt 都明确要求：只修改当前 worktree 的 `week5/`，运行完整质量门，检查 diff，创建自己的 feature commit，但不能 merge 或 push。

**【讲稿 5】**

> 这种任务合约让 Agent 的输入、输出和完成条件都可以比较，也减少了范围漂移。

---

## 7. Git worktree 隔离与提交历史（约 2.5 分钟）

### 7.1 展示 worktree

**【操作】** 在终端运行：

```bash
git -C /root/modern-software-dev-assignments worktree list
```

**【讲稿 1】**

> 这里可以看到三个工作目录。

**【讲稿 2】**

> 主目录对应 `xyp`，只负责集成；`week5-task3` 对应 Notes Agent；`week5-task4` 对应 Action Items Agent。

**【讲稿 3】**

> Worktree 的重点不是多开一个终端，而是让不同分支拥有独立的文件系统状态。

**【讲稿 4】**

> 如果两个普通 tab 共享同一 checkout，它们同时编辑 `app.js` 时可能覆盖彼此；使用 worktree 后，它们只会在最终 merge 时显式相遇。

### 7.2 展示提交图

**【操作】** 运行：

```bash
git -C /root/modern-software-dev-assignments \
  log --graph --oneline --decorate -12
```

**【讲稿 5】**

> Notes Agent 的交付提交是 `59c3a4c`，它在自己的分支上通过了 15 个测试。

**【讲稿 6】**

> Action Items Agent 的交付提交是 `afd9a76`，它在自己的分支上通过了 8 个测试。

**【讲稿 7】**

> 监督者首先合并 Action Items，再合并 Notes，最后在集成分支上运行完整的 20 个测试。

### 7.3 真实冲突

**【操作】** 打开 `writeup_zh.md`，定位 Automation B 的 “角色、协调、收益、风险与失败”。

**【讲稿 8】**

> 第一次合并没有冲突。第二次合并在 `backend/app/schemas.py` 和 `frontend/styles.css` 出现了真实冲突。

**【讲稿 9】**

> 这个冲突不是 worktree 失败，而是 worktree 正确地把并发风险推迟到一个明确、可审查的集成点。

**【讲稿 10】**

> 我没有简单选择 ours 或 theirs，而是合并两边的 Pydantic import 和模型，并保留 Notes 与 Action Items 两组 CSS 规则。

**【讲稿 11】**

> 解决冲突之后，我重新运行全部测试和静态检查，最终 20 个测试通过。

---

## 8. 功能演示：Notes CRUD（约 2 分钟）

**【操作】** 切换到 `http://localhost:8000`。

### 8.1 创建

**【操作】** 输入标题和内容，点击 Add。

**【讲稿 1】**

> 首先创建一条 Note。前端调用原有的 POST 接口，成功后重新加载列表。

### 8.2 编辑与乐观更新

**【操作】** 点击 Edit，修改标题和内容，点击 Save。

**【讲稿 2】**

> Task 3 新增了 PUT 接口和编辑 UI。

**【讲稿 3】**

> 点击 Save 后，前端先更新本地 `notesState` 并重新渲染，然后才等待服务器响应，这就是乐观更新。

**【讲稿 4】**

> 如果请求失败，catch 分支会把原始 Note 放回 state、重新渲染，并显示错误信息。

### 8.3 删除与回滚

**【操作】** 点击 Delete。

**【讲稿 5】**

> 删除采用相同策略：先从本地列表移除，再请求 DELETE 接口；如果失败，就恢复之前保存的完整列表。

### 8.4 校验

**【操作】** 切换到 `/docs`，找到 Notes POST 或 PUT，提交空标题。

**【讲稿 6】**

> Pydantic 对标题设置了 1 到 200 字符的限制，对正文设置了 1 到 10000 字符的限制。

**【讲稿 7】**

> 因为空标题不满足 schema，所以 FastAPI 在进入业务逻辑前直接返回 422。

---

## 9. 功能演示：Action Items（约 2.5 分钟）

**【操作】** 回到首页，确保有三个 Action Item。

### 9.1 筛选

**【操作】** 依次点击 All、Open、Completed。

**【讲稿 1】**

> Task 4 为 GET `/action-items/` 增加了可选的 `completed` 布尔查询参数。

**【讲稿 2】**

> 不传参数时返回全部；传 false 返回未完成项；传 true 返回已完成项。

**【讲稿 3】**

> 前端的三个按钮只是改变当前 filter，然后重新请求 API，不是在浏览器中伪造筛选结果。

### 9.2 批量完成

**【操作】** 选择两个未完成项，点击 Complete selected。

**【讲稿 4】**

> 每个未完成事项都有复选框，选择状态保存在 `selectedActionIds` 中。

**【讲稿 5】**

> 点击批量完成后，前端把 ID 列表发送到 `/action-items/bulk-complete`。

**【讲稿 6】**

> 后端先查询所有 ID，计算缺失 ID；只有完整集合验证通过之后，才修改任何一行。

**【讲稿 7】**

> 因此如果请求中混入一个不存在的 ID，接口返回 404，并且其他合法 ID 不会被部分完成。

### 9.3 事务回滚演示

**【操作】** 在 Swagger 的 bulk-complete 中提交一个有效 ID 和 `999999`，然后重新 GET。

**【讲稿 8】**

> 这里故意混入一个不存在的 ID。

**【讲稿 9】**

> 返回结果会列出缺失 ID。再次获取列表后，原来的合法事项仍然保持未完成，这证明批量操作没有产生部分更新。

---

## 10. 最终质量门（约 1.5 分钟）

**【操作】** 在终端运行：

```bash
cd /root/modern-software-dev-assignments/week5
bash scripts/quality_gate.sh backend/tests
```

**【讲稿 1】**

> 功能演示只能证明几个示例路径，最终完成标准仍然是自动化质量门。

**【操作】** 等待输出 `20 passed`。

**【讲稿 2】**

> 这里可以看到 20 个测试全部通过。

**【操作】** 指向 `All checks passed!` 和 `Quality gate passed.`。

**【讲稿 3】**

> 随后的 Ruff、Black 和 Git whitespace 检查也全部通过。

**【讲稿 4】**

> 与初始的 3 个测试相比，新增测试覆盖了更新、删除、404、参数验证、筛选、批量成功、非法 ID 和事务回滚。

---

## 11. Warp 额度限制的说明（约 30 秒）

**【操作】** 打开 `docs/warp/EVIDENCE_ZH.md`。

**【讲稿 1】**

> 本机已经安装 Warp，但账户没有可用的付费 Agent 额度，因此没有生成公开的 Warp Agent Session URL。

**【讲稿 2】**

> 我没有虚构分享链接，而是把可复现证据版本化：包括 YAML Workflow、Project Rule、完整 Agent Prompt、两个 worktree、feature commit、merge commit 和最终质量门。

**【讲稿 3】**

> 其他人可以按照 playbook 重新创建相同工作流；额度限制是本次实验环境的一项明确限制。

**【提示】** 不要说“两个 Warp Agent 已经真实运行并产生 Session”，因为没有对应链接或截图。

---

## 12. 总结（约 1 分钟）

**【操作】** 回到 `docs/WEEK5_PRESENTATION.md` 的“工程结论”。

**【讲稿 1】**

> 这次实验让我看到，多 Agent 的价值不仅是速度，更重要的是任务所有权和失败隔离。

**【讲稿 2】**

> Worktree 解决并发文件覆盖，测试验证业务语义，质量门统一完成标准，而最终 diff review 和冲突处理仍由人负责。

**【讲稿 3】**

> Agent 可以自动执行工程步骤，但“什么结果可以被接受”必须由可重复的验证和人工判断共同决定。

**【讲稿 4】**

> 我认为这也是现代终端最大的变化：开发者从逐条输入命令，转向设计上下文、权限、任务边界和反馈循环。

**【讲稿 5】**

> 我的汇报到这里，谢谢大家，下面可以提问。

---

## 13. 常见提问的逐句回答

### 13.1 为什么不用一个 Agent？

> 两个任务在 API 层面相对独立，适合并发。拆分以后，每个 Agent 的上下文更聚焦，提交更小，也更容易确定问题属于哪个任务。代价是共享前端文件会在集成时产生冲突，因此仍然需要监督者。

### 13.2 为什么不用两个普通 terminal tab？

> 普通 tab 只隔离终端进程，不隔离文件系统。两个 Agent 如果进入同一个 checkout，同时修改 `app.js`，后写入的一方可能覆盖前一方。Git worktree 同时隔离目录和分支，让冲突只在显式 merge 时发生。

### 13.3 为什么不用数据库事务中的 rollback 显式调用？

> 本次实现采用“先验证完整集合，再修改任何 ORM 对象”的策略。只要发现缺失 ID，就在变更前抛出 404，因此不会产生需要回滚的部分更新。数据库依赖层同时在异常时执行 session rollback，提供第二层保护。

### 13.4 乐观 UI 有什么风险？

> 乐观 UI 提高响应速度，但要求保存旧状态。如果请求失败却没有回滚，界面就会与服务器不一致。本次更新保存原始 Note，删除保存完整旧列表，并在 catch 中恢复和显示错误。

### 13.5 为什么最终是 20 个测试？

> 初始项目有 3 个测试。Notes 分支增加了更新、删除、404 和多组 validation 测试；Action Items 分支增加了筛选、非法筛选、批量成功、输入校验和事务回滚测试。合并后完整套件共有 20 个测试。

### 13.6 并发是否真的节省时间？

> 独立实现阶段可以并行，因此减少等待。但并发不会消灭集成成本。本次 `schemas.py` 和 `styles.css` 的冲突就是额外成本。是否值得并行，取决于任务独立程度和冲突概率。

### 13.7 最大的工程收获是什么？

> 最大收获是把“Agent 说完成了”与“工程上可以接受”分开。真正的完成信号来自聚焦提交、自动测试、静态检查、diff review 和人工集成，而不是 Agent 的自然语言总结。

### 13.8 没有 Warp Agent 额度，为什么还能称为 Warp 自动化？

> 仓库中包含可由 Warp 发现和执行的 YAML Workflow、项目 Rule 和 Saved Prompt 模板，工作流也围绕 Warp tab 与 worktree 设计。但我会明确说明本次没有付费 Agent Session 证据，展示的是可复现定义、执行结果和版本历史，而不是虚构的 Warp 云端运行。

---

## 14. 现场故障备用讲稿

### 14.1 Web UI 打不开

> 现场 SSH tunnel 出现连接问题，我使用已经验证过的 API smoke test 和测试结果作为备用证据。此前 `/`、`/openapi.json`、`/notes/` 和筛选后的 `/action-items/` 均返回 200。

**【操作】** 改为展示 `docs/IMPLEMENTATION_ZH.md` 和测试文件。

### 14.2 质量门现场失败

> 质量门失败本身就是自动化的价值：它阻止我在未满足完成标准时宣称成功。我会先读取第一条失败信息，而不是跳过检查。

**【提示】** 同时展示预先保存的成功输出截图，但不要把旧截图说成刚刚运行的结果。

### 14.3 Warp 无法登录或提示无额度

> Warp 当前账户没有可用 Agent 额度，因此我不会现场触发付费 Agent。这里展示的是已经版本化的 Workflow、Rule、Prompt、worktree 和验证结果。

### 14.4 Swagger 演示数据 ID 不一致

> 这里的 ID 来自当前演示数据库，所以我先通过 GET 获取真实 ID，再构造 bulk-complete 请求。事务语义不依赖某一个固定 ID。

---

## 15. 最终展示文档顺序

严格按照下面顺序切换，汇报会最连贯：

1. `docs/WEEK5_PRESENTATION.md`——标题、作业目标与总体流程。
2. `docs/TASKS_ZH.md`——任务 3、任务 4 与选题理由。
3. `docs/IMPLEMENTATION_ZH.md`——架构图和 API 合约。
4. `docs/AGENT_RULES_ZH.md`——项目规则和权限边界。
5. `.warp/workflows/week5-quality-gate.yaml`——Warp Workflow 参数。
6. `scripts/quality_gate.sh`——四层质量门。
7. `docs/WARP_MULTI_AGENT_PLAYBOOK_ZH.md`——两个中文任务 Prompt。
8. 终端 `git worktree list`——目录和分支隔离。
9. 终端 `git log --graph`——两个 feature commit 与 merge。
10. `writeup_zh.md`——冲突、权限和反思。
11. Web UI——Notes 和 Action Items。
12. Swagger `/docs`——校验和事务失败路径。
13. 终端质量门——20 passed。
14. `docs/warp/EVIDENCE_ZH.md`——证据与额度限制。
15. `docs/WEEK5_PRESENTATION.md` 的“工程结论”——收尾。

`WEEK5_DETAILED_SPEAKER_SCRIPT.md`、`REPORT_RUNBOOK.md` 和 `LAB_PRESENTATION_GUIDE.md` 只供汇报人查看，不属于投屏材料。

## 16. 上台前最后检查

- [ ] 能够在 30 秒内找到每个展示文件。
- [ ] SSH tunnel 和 Uvicorn 已启动。
- [ ] 首页与 Swagger 已加载。
- [ ] 演示数据库准备了 Note 和 Action Item。
- [ ] 终端当前目录正确，没有显示密码或令牌。
- [ ] `git worktree list` 与 Git graph 命令已放入历史记录。
- [ ] 质量门提前运行成功。
- [ ] 准备一张 `20 passed` 备用截图。
- [ ] 明确区分真实证据、可复现定义和未生成的 Warp Session。
