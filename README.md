# DAT System v2.0

Divergent Association Task (发散性思维测试) 系统 — 通过语义距离计算测量发散性思维能力。

本系统基于论文 [Using the divergent association task to measure divergent thinking in Chinese elementary school students](https://doi.org/10.1016/j.tsc.2024.101503) (2024, *Thinking Skills and Creativity*) 开发。

---

## 快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/HYW2023-s/dat_system.git
cd dat_system

# 创建虚拟环境（Python >= 3.10）
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 下载模型文件

腾讯 AI 实验室 Word2Vec 模型下载链接已失效，可以通过百度网盘下载（仅限学术用途）：

> 链接: https://pan.baidu.com/s/15UETBSiae9yQr4FPN62V9g?pwd=yrxa
> 提取码: yrxa

下载后将 `w2v.wv` 和 `w2v.wv.vectors.npy` 放入项目 `models/` 目录。

### 3. 启动

```bash
# 启动 Web 服务（默认 http://localhost:8000）
dat start

# 指定端口
dat start --port 8080

# 生产模式部署
dat deploy --port 80
```

### 4. 登录

打开浏览器访问 `http://localhost:8000`，使用默认管理员账号登录：

> 用户名: `admin`
> 密码: `123456`

**首次登录后请立即修改密码。**

---

## CLI 命令

```bash
# 启动服务
dat start                            # 默认端口 8000
dat start --port 8080                # 指定端口
dat start --host 0.0.0.0 --port 8080 # 指定 host 和端口

# 导出实验数据
dat export                           # 导出 CSV
dat export --format xlsx             # 导出 Excel
dat export --output ./export_data    # 指定输出目录

# 修改密码
dat admin reset-password             # 重置管理员密码为 123456
dat admin reset-password --password 新密码 --username 用户名

# 生产部署
dat deploy                           # 部署到 80 端口
dat deploy --port 8080
```

---

## 功能说明

### DAT 发散性思维测试

1. **输入词汇**：在规定时间（默认 4 分钟）内输入 10 个尽可能不相关的名词
2. **自动计算**：系统通过 Word2Vec 词向量计算词汇之间的语义距离
3. **查看结果**：获得 DAT 得分、超越百分比、语义距离热力图

### 管理员功能

- **数据分析**：查看所有用户得分的统计分析和可视化图表
- **用户管理**：批量上传用户（Excel 文件）
- **任务配置**：调整测试限制时间
- **数据导出**：导出所有作答记录为 CSV 或 Excel

---

## API 文档

启动服务后访问 `http://localhost:8000/docs` 查看完整 API 文档。

主要接口：

| 方法  | 路径                    | 说明             |
|-------|------------------------|------------------|
| POST  | `/api/auth/login`       | 用户登录         |
| POST  | `/api/auth/register`    | 用户注册         |
| GET   | `/api/dat/test-config`  | 获取测试配置     |
| POST  | `/api/dat/calculate`   | 提交词汇计算得分  |
| GET   | `/api/dat/results`     | 查询作答记录      |
| GET   | `/api/dat/result/{id}` | 查看记录详情      |
| GET   | `/api/admin/analysis`  | 数据分析（管理员）|
| POST  | `/api/admin/upload-users` | 批量上传用户  |
| GET   | `/api/export/csv`      | 导出 CSV（管理员）|
| GET   | `/api/export/xlsx`     | 导出 Excel（管理员）|

---

## 项目结构

```
dat_system/
├── cli.py                  # CLI 入口 (typer)
├── backend/                # FastAPI 后端
│   ├── main.py             # 应用入口 + 生命周期管理
│   ├── config.py           # 配置管理
│   ├── database.py         # SQLite + SQLAlchemy
│   ├── models.py           # 数据模型
│   ├── routers/
│   │   ├── auth.py         # 认证路由
│   │   ├── dat.py          # DAT 核心路由
│   │   ├── admin.py        # 管理功能路由
│   │   └── export.py       # 数据导出路由
│   ├── services/
│   │   ├── embedding.py    # 词向量加载服务
│   │   └── dat_calculator.py # DAT 算法（向量化优化）
│   └── utils/
│       └── visualization.py # 热力图生成
├── frontend/               # 前端页面
│   ├── index.html
│   ├── css/style.css       # 全局样式
│   ├── js/api.js           # API 客户端 + 认证
│   └── pages/              # 页面
│       ├── login.html
│       ├── test.html       # DAT 测试页
│       ├── results.html    # 结果查询
│       ├── analysis.html   # 数据分析
│       └── admin/          # 管理面板
├── models/                 # 模型文件
│   ├── w2v.wv              # Word2Vec 模型
│   └── SIMHEI.TTF          # 中文字体（热力图）
├── data/                   # 数据库文件 (dat.db)
├── requirements.txt
└── README.md
```

---

## 论文引用

如果您在研究中使用了本系统，请引用：

> Ding, G., He, Y., Yi, K., & Li, S. (2024). Using the divergent association task to measure divergent thinking in Chinese elementary school students. *Thinking Skills and Creativity, 52*, 101503.

---

## 技术栈

| 层次     | 技术                                      |
| -------- | ----------------------------------------- |
| CLI      | Typer + Rich                              |
| Web 框架 | FastAPI + Uvicorn                         |
| 数据库   | SQLite + SQLAlchemy (async)               |
| 认证     | JWT + bcrypt                              |
| 前端     | HTML/CSS/JS + Phosphor Icons + ECharts    |
| 算法     | Gensim (Word2Vec) + NumPy + scikit-learn  |
| 可视化   | Matplotlib                                |

---

## License

MIT License. 模型文件仅限学术用途。
