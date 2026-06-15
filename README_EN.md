# DAT System v2.0

> 📖 [中文版本](README.md)

The Divergent Association Task (DAT) system — objectively measures divergent thinking ability through semantic distance computation between words.

Based on the paper [Using the divergent association task to measure divergent thinking in Chinese elementary school students](https://doi.org/10.1016/j.tsc.2024.101503) (Ding, G., He, Y., Yi, K., & Li, S., 2024, *Thinking Skills and Creativity, 52*, 101503).

---

## Quick Start

### 1. Prerequisites

- Python >= 3.10
- OS: macOS / Windows / Linux

### 2. Installation

```bash
git clone https://github.com/HYW2023-s/dat_system.git
cd dat_system

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate     # macOS / Linux
# .venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Download Model Files

The official Tencent AI Lab Word2Vec model download link is no longer available. You can download via Baidu Netdisk (**academic use only**):

> Link: https://pan.baidu.com/s/15UETBSiae9yQr4FPN62V9g?pwd=yrxa  
> Passcode: yrxa

After downloading, place these files in the `models/` directory:
- `w2v.wv`
- `w2v.wv.vectors.npy`

### 4. Launch

Two ways to start:

#### Using CLI (recommended)

```bash
# Make sure virtual environment is activated
source .venv/bin/activate     # macOS / Linux
# .venv\Scripts\activate      # Windows

# Start the service
python cli.py start

# Or install the dat command first
pip install -e .
dat start
```

`pip install -e .` registers the `dat` command in your virtual environment. After that, you can use all `dat` commands directly.

#### Direct start

```bash
source .venv/bin/activate
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

#### Custom port

```bash
dat start --port 8080
python -m uvicorn backend.main:app --port 8080
```

### 5. Login

Open `http://localhost:8000` in your browser. Default admin credentials:

| Username | Password |
|----------|----------|
| `admin` | `123456` |

**Change the password immediately after first login.**

---

## CLI Commands

> **Prerequisite**: CLI commands require an active virtual environment.  
> Run `pip install -e .` first to register the `dat` command, then type `dat` in terminal.  
> If not registered, use `python cli.py` instead of `dat`.

### Start Service

```bash
dat start                                 # Default http://localhost:8000
dat start --port 8080                     # Custom port
dat start --host 0.0.0.0 --port 8080      # Allow LAN access
```

### Export Data

```bash
dat export                                # Export as CSV
dat export --format xlsx                  # Export as Excel
dat export --output ~/Desktop/dat_data    # Custom output directory
```

Exported columns: ID, Username, Time, 10 words, DAT Score, Effective Word Count, Time Spent.

### Reset Password

```bash
dat admin reset-password                  # Reset admin password to 123456
dat admin reset-password --username user --password newpwd
```

### Production Deploy

```bash
dat deploy                                # Deploy to port 80
dat deploy --port 8080
```

Production mode differs from `start` by binding `0.0.0.0` (external access) and reducing log verbosity.

### Help

```bash
dat --help
dat start --help
dat admin --help
```

---

## Features

### DAT Test

1. **Enter words**: Enter 10 nouns that are as unrelated to each other as possible, within the time limit (default 4 minutes)
2. **Auto calculation**: The system uses Word2Vec embeddings to compute semantic distances between words
3. **View results**: Get your DAT score, percentile ranking, and interactive semantic distance heatmap

#### Test Rules

- The greater the difference between words, the higher the score
- Enter **nouns only** — no verbs, adjectives, or other parts of speech
- Words not in the vocabulary are automatically skipped
- At least **5 valid words** are required for heatmap generation

### Multi-Model Support

Multiple embedding models are supported and can be switched in the admin panel:

| Model | Dimension | Type | Notes |
|-------|-----------|------|-------|
| Tencent Word2Vec | 200 | Local | Default model, no network needed |
| Aliyun text-embedding-v4 | 1024 | API | Requires API Key |
| OpenAI text-embedding-3-small | 1536 | API | Requires API Key |
| OpenAI text-embedding-3-large | 3072 | API | Requires API Key |
| SiliconFlow BGE-large-zh | 1024 | API | Requires API Key |
| SiliconFlow Qwen3-Embedding-4B | 2560 | API | Requires API Key |
| **Custom** | Any | API | OpenAI-compatible endpoints |

Vectors fetched via API are **automatically cached** in the local database. The same word is never requested twice.

### Admin Features

- **Data Analysis**: View statistical analysis of all user scores (mean, variance, distribution chart, box plot)
- **User Management**: Batch import users via Excel file
- **Task Configuration**: Adjust test time limit
- **Data Export**: Export all test records as CSV or Excel
- **Model Configuration**: Switch embedding models, set API Keys
- **Password Management**: Change admin and user passwords

---

## API Documentation

Visit `http://localhost:8000/docs` for the full Swagger API documentation.

### Key Endpoints

#### Authentication

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | Login, returns JWT |
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/change-password` | Change password |
| GET | `/api/auth/me` | Get current user info |

#### DAT Test

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/dat/test-config` | Get test configuration |
| POST | `/api/dat/calculate` | Submit words, get DAT score |
| GET | `/api/dat/results` | List test records (paginated) |
| GET | `/api/dat/result/{id}` | Get record detail |
| GET | `/api/dat/result/{id}/heatmap-data` | Get heatmap matrix data |
| GET | `/api/dat/limited-time` | Get current time limit |

#### Admin

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/admin/analysis` | Statistical analysis |
| POST | `/api/admin/upload-users` | Batch upload users (Excel) |
| PUT | `/api/admin/task-time` | Update time limit |
| POST | `/api/admin/reset-password` | Reset user password |
| GET | `/api/admin/search` | Search records by username |
| GET | `/api/admin/users` | List all users |

#### Model Configuration

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/models` | List models and active model |
| GET | `/api/models/templates` | List built-in templates |
| POST | `/api/models/activate` | Activate a model with API key |
| POST | `/api/models/switch` | Switch active model |
| POST | `/api/models/custom` | Add custom model |
| POST | `/api/models/delete` | Remove a model |
| GET | `/api/models/cache-stats` | Cache statistics |

#### Export

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/export/csv` | Export CSV |
| GET | `/api/export/xlsx` | Export Excel |

---

## Project Structure

```
dat_system/
├── cli.py                      # CLI entry (Typer + Rich)
├── backend/                    # FastAPI backend
│   ├── main.py                 # App entry + lifecycle
│   ├── config.py               # Configuration
│   ├── database.py             # SQLite + SQLAlchemy (async)
│   ├── models.py               # Data models (6 tables)
│   ├── i18n.py                 # Backend translations
│   ├── routers/
│   │   ├── auth.py             # Auth routes
│   │   ├── dat.py              # DAT core routes
│   │   ├── admin.py            # Admin routes
│   │   ├── export.py           # Export routes
│   │   └── models_api.py       # Model config routes
│   ├── services/
│   │   ├── embedding.py        # Multi-model embedding
│   │   ├── dat_calculator.py   # DAT algorithm
│   │   └── vector_cache.py     # Vector cache
│   └── utils/
│       └── visualization.py    # Heatmap generation (fallback)
├── frontend/                   # Static frontend
│   ├── index.html
│   ├── css/style.css           # Global styles
│   ├── js/
│   │   ├── api.js              # API client + auth
│   │   └── i18n.js             # i18n engine
│   └── pages/                  # Pages
│       ├── login.html
│       ├── register.html
│       ├── introduction.html
│       ├── test.html           # DAT test page
│       ├── results.html        # Results list
│       ├── result-detail.html  # Result detail + heatmap
│       ├── analysis.html       # Data analysis
│       ├── model-config.html   # Model config
│       └── admin/
│           ├── dashboard.html
│           ├── upload-user.html
│           └── task-config.html
├── models/                     # Model files
├── data/                       # Database (dat.db)
├── pyproject.toml
├── requirements.txt
├── README.md                   # Chinese README
└── README_EN.md                # English README
```

---

## Architecture

### Design Principles

- **Model stays in memory**: Word2Vec loaded once at startup, reused across all requests
- **Vectorized computation**: sklearn batch cosine similarity instead of double loops
- **Async architecture**: FastAPI + aiosqlite, concurrent users don't block each other
- **Vector caching**: API embeddings automatically cached in SQLite
- **CLI-first**: All operations available via command line
- **i18n**: Chinese/English toggle, persisted in localStorage

### Database

SQLite, data file at `data/dat.db`:

| Table | Purpose |
|-------|---------|
| `user` | User accounts |
| `dat_test` | DAT test records |
| `answer_log` | Answer behavior log |
| `spend_time` | Time spent records |
| `task_time` | Task time configuration |
| `embedding_cache` | Word vector cache |

---

## Citation

If you use this system in your research, please cite:

> Ding, G., He, Y., Yi, K., & Li, S. (2024). Using the divergent association task to measure divergent thinking in Chinese elementary school students. *Thinking Skills and Creativity, 52*, 101503. https://doi.org/10.1016/j.tsc.2024.101503

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| CLI | Typer + Rich |
| Web Framework | FastAPI + Uvicorn |
| Database | SQLite + SQLAlchemy (async) + aiosqlite |
| Auth | JWT (python-jose) + bcrypt |
| Frontend | HTML/CSS/JS + ECharts + Phosphor Icons |
| NLP | Gensim (Word2Vec) + NumPy + scikit-learn |
| API Client | httpx (async) |
| Visualization | ECharts (interactive heatmap) |
| Export | openpyxl (xlsx) + csv |

---

## License

MIT License. Model files are for academic use only.
