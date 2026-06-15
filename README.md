# DAT System v2.0

> 📖 [English version](README_EN.md)

Divergent Association Task（发散性思维测试）系统 — 通过计算词汇之间的语义距离，客观测量发散性思维能力。

> 📄 **论文**：[Using the divergent association task to measure divergent thinking in Chinese elementary school students](https://doi.org/10.1016/j.tsc.2024.101503)  
> Ding, G., He, Y., Yi, K., & Li, S. (2024). *Thinking Skills and Creativity, 52*, 101503.  
> https://doi.org/10.1016/j.tsc.2024.101503

---

## 快速开始

### 1. 环境要求

- Python >= 3.10
- 操作系统：macOS / Windows / Linux

### 2. 安装

```bash
# 克隆项目
git clone https://github.com/HYW2023-s/dat_system.git
cd dat_system

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate     # macOS / Linux
# .venv\Scripts\activate      # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 下载模型文件

腾讯 AI 实验室 Word2Vec 模型官方下载链接已失效。可通过百度网盘下载（**仅限学术用途**）：

> 链接: https://pan.baidu.com/s/15UETBSiae9yQr4FPN62V9g?pwd=yrxa  
> 提取码: yrxa

下载后将以下文件放入项目 `models/` 目录：
- `w2v.wv`
- `w2v.wv.vectors.npy`

### 4. 启动

安装完成后，有两种方式启动系统：

#### 方式一：使用 CLI 命令（推荐）

```bash
# 确保虚拟环境已激活（命令行前有 (.venv) 标识）
# 如果没有，先执行：
source .venv/bin/activate     # macOS / Linux
# .venv\Scripts\activate      # Windows

# 启动服务
python cli.py start

# 或者安装为系统命令后直接用 dat
pip install -e .
dat start
```

`pip install -e .` 会将 `dat` 命令注册到当前虚拟环境，之后在虚拟环境激活状态下可直接使用 `dat` 开头的所有命令，无需每次输入 `python cli.py`。

#### 方式二：直接启动

```bash
# 确保虚拟环境已激活
source .venv/bin/activate

# 直接使用 uvicorn 启动
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

#### 指定端口

```bash
dat start --port 8080              # CLI 方式
python -m uvicorn backend.main:app --port 8080   # 直接启动
```

### 5. 登录

打开浏览器访问 `http://localhost:8000`，使用默认管理员账号：

| 用户名 | 密码 |
|--------|------|
| `admin` | `123456` |

**首次登录后请立即修改密码。**

---

## CLI 命令

> **前提**：CLI 命令需要在虚拟环境激活状态下使用。  
> 首次使用前建议执行 `pip install -e .` 注册 `dat` 命令，之后在终端输入 `dat` 即可。  
> 如果没有注册，可以用 `python cli.py` 替代 `dat`，效果相同。

### 启动服务

```bash
# 默认启动（http://localhost:8000）
dat start

# 指定端口
dat start --port 8080

# 允许局域网内其他设备访问
dat start --host 0.0.0.0 --port 8080
```

启动后在浏览器打开 `http://localhost:8000` 即可使用。

### 导出实验数据

```bash
# 导出为 CSV（默认格式），保存到 ./export 目录
dat export

# 导出为 Excel
dat export --format xlsx

# 指定输出目录
dat export --output ~/Desktop/dat_data
```

导出文件包含所有用户的作答记录：ID、用户名、时间、10个词汇、DAT得分、有效词数、作答耗时。

### 修改密码

```bash
# 重置管理员密码为默认值 123456
dat admin reset-password

# 重置指定用户的密码
dat admin reset-password --username student01 --password 新密码
```

### 生产部署

```bash
# 部署到 80 端口（需要 root 权限）
dat deploy

# 部署到指定端口（非 1024 以下端口不需要 root）
dat deploy --port 8080
```

生产模式与 `start` 的区别：绑定 `0.0.0.0`（允许外部访问），关闭访问日志，只输出警告级别日志。

### 查看帮助

```bash
dat --help                  # 查看所有命令
dat start --help            # 查看某个命令的选项
dat admin --help            # 查看子命令
```

---

## 功能说明

### 语言切换

系统支持中文 / English 切换，右上角点击 `EN` / `中文` 按钮即可切换界面语言。

### DAT 发散性思维测试

1. **输入词汇**：在限定时间（默认 4 分钟）内输入 10 个尽可能不相关的名词
2. **自动计算**：系统使用 Word2Vec 词向量计算词汇之间的语义距离
3. **查看结果**：获得 DAT 得分、超越百分比、交互式语义距离热力图

#### 测试规则

- 词汇之间的差异越大，得分越高
- 必须输入**名词**，不要输入动词、形容词或其他词性
- 不在词库中的词汇会被自动跳过
- 至少需要 **5 个有效词汇**才能生成热力图

### 多模型支持

系统支持多种 Embedding 模型，可在管理面板中切换：

| 模型 | 维度 | 运行方式 | 说明 |
|------|------|----------|------|
| Tencent Word2Vec | 200 | 本地 | 默认模型，无需网络 |
| OpenAI text-embedding-3-small | 1536 | API | 需提供 API Key |
| OpenAI text-embedding-3-large | 3072 | API | 需提供 API Key |
| 硅基流动 BGE-large-zh-v1.5 | 1024 | API | 需提供 API Key |
| 硅基流动 Qwen3-Embedding-4B | 2560 | API | 需提供 API Key |
| 阿里百炼 text-embedding-v4 | 1024 | API | 需提供 API Key |
| **自定义模型** | 任意 | API | OpenAI 兼容格式即可 |

切换模型后，通过 API 获取的词向量会**自动缓存**到本地数据库，相同词语不会重复请求。

### 管理员功能

- **数据分析**：查看所有用户的得分统计分析（均值、方差、分布图、箱型图）
- **用户管理**：通过 Excel 批量导入用户账号
- **任务配置**：调整测试限制时间
- **数据导出**：导出全部作答记录为 CSV 或 Excel
- **模型配置**：切换 Embedding 模型、设置 API Key
- **密码管理**：修改管理员和用户密码

---

## API 文档

启动服务后访问 `http://localhost:8000/docs` 查看完整的 Swagger API 文档。

### 主要接口

#### 认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 用户登录，返回 JWT |
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/change-password` | 修改密码 |
| GET | `/api/auth/me` | 获取当前用户信息 |

#### DAT 测试

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/dat/test-config` | 获取测试配置（含时间限制） |
| POST | `/api/dat/calculate` | 提交词汇，计算 DAT 得分 |
| GET | `/api/dat/results` | 查询作答记录列表（分页） |
| GET | `/api/dat/result/{id}` | 查看单条记录详情 |
| GET | `/api/dat/result/{id}/heatmap-data` | 获取热力图矩阵数据 |
| GET | `/api/dat/limited-time` | 获取当前限制时间 |

#### 管理功能

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/analysis` | 数据分析（统计数据 + 分布） |
| POST | `/api/admin/upload-users` | 批量上传用户（Excel） |
| PUT | `/api/admin/task-time` | 修改测试限制时间 |
| POST | `/api/admin/reset-password` | 重置指定用户密码 |
| GET | `/api/admin/search` | 按用户名搜索作答记录 |
| GET | `/api/admin/users` | 列出所有用户 |
| GET | `/api/admin/export` | 导出数据（CSV） |

#### 模型配置

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/models` | 列出可用模型和当前模型 |
| POST | `/api/models/switch` | 切换当前使用的模型 |
| POST | `/api/models/apikey` | 设置/更新 API Key |
| GET | `/api/models/cache-stats` | 查看向量缓存统计 |

#### 数据导出

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/export/csv` | 导出 CSV |
| GET | `/api/export/xlsx` | 导出 Excel |

---

## 项目结构

```
dat_system/
├── cli.py                      # CLI 入口 (Typer + Rich)
├── backend/                    # FastAPI 后端
│   ├── main.py                 # 应用入口 + 生命周期管理
│   ├── config.py               # 配置管理
│   ├── database.py             # SQLite + SQLAlchemy (async)
│   ├── models.py               # 数据模型（5 张表）
│   ├── routers/
│   │   ├── auth.py             # 认证路由
│   │   ├── dat.py              # DAT 核心路由
│   │   ├── admin.py            # 管理功能路由
│   │   ├── export.py           # 数据导出路由
│   │   └── models_api.py       # 模型配置路由
│   ├── services/
│   │   ├── embedding.py        # 多模型 Embedding 服务
│   │   ├── dat_calculator.py   # DAT 算法（向量化优化）
│   │   └── vector_cache.py     # 向量缓存服务
│   └── utils/
│       └── visualization.py    # 热力图生成（后备方案）
├── frontend/                   # 纯静态前端
│   ├── index.html
│   ├── css/style.css           # 全局样式（暖白学术风格）
│   ├── js/api.js               # API 客户端 + JWT 认证
│   └── pages/
│       ├── login.html          # 登录页
│       ├── register.html       # 注册页
│       ├── introduction.html   # 任务介绍
│       ├── test.html           # DAT 测试页
│       ├── results.html        # 结果查询（分页 + 搜索）
│       ├── result-detail.html  # 结果详情（ECharts 热力图）
│       ├── analysis.html       # 数据分析（ECharts 图表）
│       ├── model-config.html   # 模型配置
│       └── admin/
│           ├── dashboard.html  # 管理面板
│           ├── upload-user.html # 批量上传用户
│           └── task-config.html # 任务时间配置
├── models/                     # 模型文件目录
│   ├── w2v.wv                  # Word2Vec 模型（软链接）
│   └── SIMHEI.TTF              # 中文字体
├── data/                       # 运行时数据
│   └── dat.db                  # SQLite 数据库
├── pyproject.toml              # 项目元数据
├── requirements.txt            # Python 依赖
└── README.md
```

---

## 架构说明

### 设计理念

- **模型常驻内存**：Word2Vec 模型在服务启动时加载，整个生命周期复用
- **向量化计算**：使用 sklearn 批量计算余弦相似度矩阵，替代双重循环
- **异步架构**：FastAPI + aiosqlite，多个用户同时计算不互相阻塞
- **向量缓存**：API 模型获取的词向量自动存入 SQLite，避免重复调用
- **CLI 优先**：所有操作都可通过命令行完成，无需手动管理进程

### 数据库

使用 SQLite，数据文件位于 `data/dat.db`，包含以下表：

| 表名 | 说明 |
|------|------|
| `user` | 用户账号 |
| `dat_test` | DAT 测试记录 |
| `answer_log` | 作答行为日志 |
| `spend_time` | 作答耗时记录 |
| `task_time` | 任务时间配置 |
| `embedding_cache` | 词向量缓存 |

---

## 论文引用

如果您在研究中使用了本系统，请引用：

> Ding, G., He, Y., Yi, K., & Li, S. (2024). Using the divergent association task to measure divergent thinking in Chinese elementary school students. *Thinking Skills and Creativity, 52*, 101503. https://doi.org/10.1016/j.tsc.2024.101503

---

## 技术栈

| 层次 | 技术 |
|------|------|
| CLI | Typer + Rich |
| Web 框架 | FastAPI + Uvicorn |
| 数据库 | SQLite + SQLAlchemy (async) + aiosqlite |
| 认证 | JWT (python-jose) + bcrypt |
| 前端 | HTML/CSS/JS + ECharts + Phosphor Icons |
| 算法 | Gensim (Word2Vec) + NumPy + scikit-learn |
| API 客户端 | httpx (async) |
| 可视化 | ECharts (前端交互式热力图) |
| 导出 | openpyxl (xlsx) + csv |

---

## License

MIT License。模型文件仅限学术用途。
