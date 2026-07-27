# Week 5 汇报运行手册

> **汇报人私有材料：不要投屏展示。** 本文只用于控制顺序、执行命令和核对现场状态；观众版材料为 [`WEEK5_PRESENTATION.md`](WEEK5_PRESENTATION.md)。

## 一句话主线

> 我没有把任务简单地交给一个 Agent，而是把开发过程设计成“规则约束、worktree 隔离、并发实现、质量门验证、人工集成”的可复现工作流。

建议汇报 12-15 分钟。按照下表依次打开文件，不需要现场临时寻找材料。

| 时间 | 讲解主题 | 展示的文件或命令 | 要证明的结论 |
| --- | --- | --- | --- |
| 0:00-1:00 | 作业目标和选题 | `docs/WEEK5_PRESENTATION.md`、`docs/TASKS_ZH.md` | 选了任务 3、任务 4，均为中等难度 |
| 1:00-2:30 | 原始架构 | `docs/IMPLEMENTATION_ZH.md` 的 Mermaid 图 | 前端、FastAPI、Pydantic、SQLAlchemy、SQLite 的调用关系 |
| 2:30-4:30 | Automation A | `docs/AGENT_RULES_ZH.md`、`.warp/workflows/week5-quality-gate.yaml`、`scripts/quality_gate.sh` | Rule 约束 Agent；Workflow 统一验证标准 |
| 4:30-7:30 | Automation B | `docs/WARP_MULTI_AGENT_PLAYBOOK_ZH.md`、`git worktree list` | 两个工作单元在独立 worktree 中隔离，不会互相覆盖 |
| 7:30-9:00 | 冲突与人工监督 | `git log --graph`、`writeup_zh.md` 的 B.d | 隔离不等于零冲突；schema/CSS 需要人工合并 |
| 9:00-12:00 | 功能演示 | Web UI、`/docs` | Notes CRUD/回滚；Action 筛选/批量完成/事务回滚 |
| 12:00-13:30 | 质量结果 | `bash scripts/quality_gate.sh backend/tests` | 20 tests + Ruff + Black + whitespace 全通过 |
| 13:30-15:00 | 反思和问答 | `docs/LAB_PRESENTATION_GUIDE.md` | 并发收益、风险、SSH 限制和人工责任 |

## 开场讲稿

> 这次作业关注的不是单纯用 AI 生成代码，而是如何把终端变成可监督的 Agent 开发环境。我选择了两个中等难度任务：Notes 完整 CRUD，以及 Action Items 筛选和事务性批量完成。我的核心设计是让两个任务并发，但不共享工作目录；再用统一质量门把结果收敛到主分支。

## Automation A 讲稿与展示

先打开 `docs/AGENT_RULES_ZH.md`，指出四条规则：只改 `week5/`、新增行为必须测试、并发 Agent 使用独立 worktree、Agent 不得自行 merge/push。

再打开 `.warp/workflows/week5-quality-gate.yaml` 和 `scripts/quality_gate.sh`：

> YAML 文件提供 Warp 中可搜索、可参数化的入口；Shell 脚本承载真正的验证逻辑，因此同一套规则也能用于 SSH 或 CI。质量门依次执行 pytest、Ruff、Black 和 Git whitespace 检查，任何一步失败都会立即停止。

现场运行：

```bash
cd /root/modern-software-dev-assignments/week5
bash scripts/quality_gate.sh backend/tests
```

结果应为 `20 passed`，随后 Ruff、Black 和 Git 检查全部通过。

## Automation B 讲稿与展示

先运行：

```bash
git -C /root/modern-software-dev-assignments worktree list
git -C /root/modern-software-dev-assignments \
  log --graph --oneline --decorate -12
```

指向三个角色：

- `xyp`：监督者和集成分支。
- `week5-task3`：Notes Agent，commit `59c3a4c`，隔离测试 15 passed。
- `week5-task4`：Action Agent，commit `afd9a76`，隔离测试 8 passed。

讲稿：

> Worktree 同时隔离分支和文件状态。两个 Agent 都会修改前端，如果只开两个普通 tab，它们可能覆盖彼此；worktree 把风险转化成一次显式、可审查的合并。第一次合并是干净的，第二次在 `schemas.py` 和 `styles.css` 发生冲突。我保留两边的模型和样式，再运行完整质量门，最终 20 个测试通过。

## 功能演示步骤

通过 SSH tunnel 启动服务：

```bash
ssh -L 8000:127.0.0.1:8000 root@190.92.200.190
cd /root/modern-software-dev-assignments/week5
PYTHONPATH=. /root/miniconda3/envs/cs146s/bin/python -m uvicorn \
  backend.app.main:app --host 127.0.0.1 --port 8000
```

浏览器打开 `http://localhost:8000` 和 `http://localhost:8000/docs`，按顺序演示：

1. 创建 Note。
2. 编辑 Note，说明 UI 先更新，请求失败时恢复原值。
3. 删除 Note，说明失败时恢复列表。
4. 创建三个 Action Item，单独完成一个。
5. 切换 All、Open、Completed。
6. 选择两个未完成项并批量完成。
7. 在 Swagger 调用 bulk-complete，混入一个不存在的 ID；再次 GET，说明合法 ID 没有被部分更新。

## 结尾讲稿

> 这次实验说明，并发 Agent 的价值不只是速度，而是任务所有权和失败隔离。Worktree 解决文件覆盖，测试验证业务语义，质量门统一完成标准，而最终的 diff review 和冲突处理仍由人负责。最大的经验是：Agent 可以自动执行工程步骤，但“什么结果可以被接受”必须由可重复的验证和人工判断共同决定。

## 汇报时使用的文档清单

- 提交报告：`writeup.md`；中文讲解参考：`writeup_zh.md`。
- 逐分钟演示顺序：`docs/REPORT_RUNBOOK.md`。
- 完整中文讲稿与问答：`docs/LAB_PRESENTATION_GUIDE.md`。
- 架构和 API 语义：`docs/IMPLEMENTATION_ZH.md`。
- 两个工作单元的完整 Prompt：`docs/WARP_MULTI_AGENT_PLAYBOOK_ZH.md`。
- 质量门 Prompt：`docs/warp/QUALITY_GATE_PROMPT.md`。
- 可复现实验证据：`docs/warp/EVIDENCE_ZH.md`。
