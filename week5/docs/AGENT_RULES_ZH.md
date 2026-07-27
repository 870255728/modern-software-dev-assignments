# Agent 项目规则

## 项目结构

Week 5 是一个小型 FastAPI 应用。后端位于 `backend/app/`：`main.py` 配置应用，`routers/` 定义接口，`models.py` 保存 SQLAlchemy 模型，`schemas.py` 定义 Pydantic 合约，`services/` 保存领域逻辑。测试位于 `backend/tests/`。无构建依赖的浏览器界面位于 `frontend/`，SQLite 数据位于 `data/`。

## 开发与验证命令

在 `week5/` 中使用：

- `make run`：启动本地 Uvicorn 服务。
- `make test`：运行 pytest 测试。
- `make format`：使用 Black 格式化并应用 Ruff 安全修复。
- `make lint`：只检查 Ruff，不修改文件。
- `bash scripts/quality_gate.sh backend/tests`：运行完整统一质量门。

## 代码规范

Python 使用四空格缩进、`snake_case` 函数与变量、`PascalCase` 模型类，并遵循 Black 的 100 字符行宽。JavaScript 保持无依赖，使用两空格缩进和 `camelCase`。REST 路径应清晰表达资源，例如 `/action-items/{item_id}`。

## 测试规范

测试文件命名为 `test_<功能>.py`，测试函数命名为 `test_<行为>`。每个接口变更都应覆盖成功、校验失败和资源不存在。测试必须使用 `backend/tests/conftest.py` 的临时数据库，不依赖 `data/app.db`。

## Agent 权限边界

- 只修改 `week5/` 中与任务相关的文件。
- 编辑前检查现有行为，保留无关用户改动。
- 新增行为必须增加测试，不得隐藏失败检查。
- 并发工作必须使用独立分支或 Git worktree。
- 每个 Agent 应检查自己的 diff 并创建聚焦提交。
- 合并、冲突解决和远程 push 由监督者负责。

英文规范原件为仓库根目录的 `AGENTS.md`；本文是用于中文说明的等价摘要。
