# CLAUDE.md — DAT System 项目总结

## 项目概述

DAT System（Divergent Association Task）是一个发散性思维测试系统，通过计算 10 个名词之间的语义距离来客观评估用户的发散性思维能力。

基于论文：Ding, G., He, Y., Yi, K., & Li, S. (2024). *Thinking Skills and Creativity, 52*, 101503.
论文链接：https://doi.org/10.1016/j.tsc.2024.101503

- **原始项目**：Django 4.2 单体应用，前后端不分离
- **改造后**：FastAPI + 纯静态前端 + CLI 入口
- **仓库**：https://github.com/HYW2023-s/dat_system
- **作者**：HYW2023-s (He Yiwei, 广州大学教育学院)

---

## 技术架构

| 层次 | 技术栈 |
|------|--------|
| CLI | Typer + Rich |
| Web 框架 | FastAPI + Uvicorn |
| 数据库 | SQLite + SQLAlchemy (async) + aiosqlite |
| 认证 | JWT (python-jose) + bcrypt |
| 前端 | 纯 HTML/CSS/JS + ECharts + Phosphor Icons |
| 算法 | Gensim (Word2Vec) + NumPy + scikit-learn + scipy |
| API 客户端 | httpx (async) |
| 可视化 | ECharts（前端交互式热力图） |
| i18n | 自研轻量 JS 字典 + Python 后端辅助模块 |

---

## 项目结构（新版本）

```
dat_system/
├── cli.py                      # CLI 入口（4 个命令）
├── backend/                    # FastAPI 后端
│   ├── main.py                 # 应用入口 + 静态文件路由
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库引擎
│   ├── models.py               # SQLAlchemy 模型（6 张表）
│   ├── i18n.py                 # 后端翻译辅助
│   ├── routers/
│   │   ├── auth.py             # 认证路由（登录/注册/改密）
│   │   ├── dat.py              # DAT 核心路由（计算/查询/热力图）
│   │   ├── admin.py            # 管理路由（用户/分析/搜索/导出）
│   │   ├── export.py           # 数据导出（CSV/Excel）
│   │   └── models_api.py       # 模型配置路由
│   ├── services/
│   │   ├── embedding.py        # 多模型 Embedding 服务
│   │   ├── dat_calculator.py   # DAT 算法（向量化优化）
│   │   └── vector_cache.py     # 向量缓存
│   └── utils/
│       └── visualization.py    # 热力图（matplotlib 后备）
├── frontend/
│   ├── css/style.css           # 全局样式（暖白学术风格）
│   ├── js/
│   │   ├── api.js              # API 客户端 + JWT + 导航栏
│   │   └── i18n.js             # 翻译引擎（~200 对键值）
│   └── pages/                  # 12 个 HTML 页面
├── models/                     # 模型文件（软链接）
├── data/                       # 数据库文件（gitignore）
└── README.md / README_EN.md    # 双语文档
```

---

## 已实现功能

### 第一阶段：基础改造
- [x] **CLI 模式**：4 个命令 — `start`、`export`、`deploy`、`admin reset-password`
- [x] **前后端分离**：FastAPI 替代 Django，纯静态前端
- [x] **SQLite 数据库**：6 张表，SQLAlchemy async ORM
- [x] **JWT 认证**：登录/注册/修改密码，管理员权限控制
- [x] **DAT 算法优化**：模型常驻内存 + 矩阵批量计算余弦距离
- [x] **前端重设计**：暖白学术风格，PingFang SC 字体，琥珀铜强调色
- [x] **交互式热力图**：ECharts 渲染，蓝红渐变，鼠标悬停提示
- [x] **数据分析**：6 项统计 + 4 个图表（柱状图/箱型图/密度/累积分布）

### 第二阶段：多模型支持
- [x] **多 Embedding 模型**：Word2Vec + OpenAI + 硅基流动 + 阿里百炼 + 自定义
- [x] **向量缓存**：API 词向量存入 SQLite，避免重复调用
- [x] **模型切换**：前端管理面板一键切换
- [x] **自定义模型**：用户输入 URL/模型名/维度/API Key

### 额外增强
- [x] **中英文切换**：Navbar 按钮，localStorage 持久化，~200 字符串全覆盖
- [x] **双语 README**：README.md + README_EN.md
- [x] **数据导出**：CLI + Web API 双通道，CSV/Excel 格式
- [x] **批量上传用户**：Excel 文件导入
- [x] **任务时间配置**：动态调整测试限时

---

## CLI 命令速查

```bash
# 安装
pip install -r requirements.txt
pip install -e .     # 注册 dat 命令

# 启动
dat start                        # http://localhost:8000
dat start --port 8080
dat deploy                       # 生产模式，0.0.0.0:80

# 导出
dat export                       # CSV
dat export --format xlsx
dat export --output ~/Desktop/

# 密码
dat admin reset-password
dat admin reset-password --username user --password newpwd
```

---

## API 端点（共 22 个）

### 认证
- `POST /api/auth/login` — 登录
- `POST /api/auth/register` — 注册
- `POST /api/auth/change-password` — 改密
- `GET /api/auth/me` — 当前用户

### DAT 测试
- `GET /api/dat/test-config` — 测试配置
- `POST /api/dat/calculate` — 提交词汇计算
- `GET /api/dat/results` — 记录列表（分页）
- `GET /api/dat/result/{id}` — 记录详情
- `GET /api/dat/result/{id}/heatmap-data` — 热力图矩阵
- `GET /api/dat/limited-time` — 时间限制

### 管理
- `GET /api/admin/analysis` — 数据分析
- `POST /api/admin/upload-users` — 批量上传
- `PUT /api/admin/task-time` — 修改限时
- `POST /api/admin/reset-password` — 重置密码
- `GET /api/admin/search` — 搜索记录
- `GET /api/admin/users` — 用户列表
- `GET /api/admin/export` — 导出数据

### 模型配置
- `GET /api/models` — 模型列表
- `GET /api/models/templates` — 内置模板
- `POST /api/models/activate` — 激活模型
- `POST /api/models/switch` — 切换模型
- `POST /api/models/custom` — 添加自定义
- `POST /api/models/delete` — 移除模型
- `GET /api/models/cache-stats` — 缓存统计

### 导出
- `GET /api/export/csv` — CSV 导出
- `GET /api/export/xlsx` — Excel 导出

---

## 支持模型

| 模型 | 维度 | 类型 |
|------|------|------|
| Tencent Word2Vec | 200 | 本地，默认 |
| OpenAI text-embedding-3-small | 1536 | API |
| OpenAI text-embedding-3-large | 3072 | API |
| 硅基流动 BGE-large-zh-v1.5 | 1024 | API |
| 硅基流动 Qwen3-Embedding-4B | 2560 | API |
| 阿里百炼 text-embedding-v4 | 1024 | API |
| 自定义模型 | 任意 | API（OpenAI 兼容） |

---

## 已知注意事项

1. **模型文件**：Word2Vec 模型（`w2v.wv`）需下载后放在 `models/` 目录，百度网盘链接见 README
2. **字体**：热力图（matplotlib 后备方案）自动检测系统字体，无需额外安装
3. **代理**：Git push 需 `git config --local http.version HTTP/1.1`（代理兼容性）
4. **服务端口**：默认 8000，启动前确保端口未被占用
5. **Python 版本**：需要 >= 3.10（gensim 兼容性）

---

## 项目统计

- **提交数**：25 commits
- **文件数**：128 files
- **后端代码**：~2,500 行 Python
- **前端代码**：~1,300 行 HTML/CSS/JS
- **i18n 覆盖**：~200 个翻译键值对

---

## License

MIT License. 模型文件仅限学术用途。
