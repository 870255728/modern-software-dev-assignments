# Warp 证据索引

本文索引仓库中真实、可复现的 Week 5 证据。由于本地 Warp 账户没有可用的付费 Agent 额度，因此没有公开 Agent Session 链接或并发 Agent 截图。

## 自动化 A：Warp Drive 与项目规则

| 证据 | 位置或结果 |
| --- | --- |
| 英文 Project Rule 原件 | `week5/AGENTS.md` |
| 中文规则说明 | `week5/docs/AGENT_RULES_ZH.md` |
| Warp Workflow | `week5/.warp/workflows/week5-quality-gate.yaml` |
| 质量门脚本 | `week5/scripts/quality_gate.sh` |
| Saved Prompt 模板 | `week5/docs/warp/QUALITY_GATE_PROMPT.md` |
| Saved Prompt 分享链接 | 未生成；可使用版本化模板复现 |
| 最终结果 | `20 passed`，Ruff、Black、Git 检查通过 |

## 自动化 B：隔离工作区

| 角色 | 分支 | Worktree | 可审计结果 |
| --- | --- | --- | --- |
| Supervisor | `xyp` | `/root/modern-software-dev-assignments` | 最终合并历史 |
| Notes 工作单元 | `week5-task3` | `/root/worktrees/week5-task3` | `59c3a4c`；无公开 Session URL |
| Action Items 工作单元 | `week5-task4` | `/root/worktrees/week5-task4` | `afd9a76`；无公开 Session URL |

第一次 feature merge 为干净合并；第二次在 `backend/app/schemas.py` 和 `frontend/styles.css` 中产生并解决真实冲突。

## 证据可用性

| 证据 | 状态 |
| --- | --- |
| 并发 Warp Agent 标签页 | 未生成；付费 Agent 额度不可用 |
| Notes 功能结果 | feature commit 与隔离测试结果可复现 |
| Action Items 功能结果 | feature commit 与隔离测试结果可复现 |
| 集成结果 | 合并历史、冲突文件和最终质量门可复现 |

## 复现命令

```bash
cd /root/modern-software-dev-assignments/week5
bash scripts/quality_gate.sh backend/tests
git log --oneline --decorate --graph -10
git status --short
```
