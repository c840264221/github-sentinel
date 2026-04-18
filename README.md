# 🚀 GitHub Sentinel

> An AI-powered GitHub monitoring agent for developers and teams.

GitHub Sentinel is an open-source tool that helps developers and project managers automatically track updates from subscribed GitHub repositories and receive structured reports.

---

## ✨ Features (v0.0.1)

* 📦 Subscribe to GitHub repositories
* 🔄 Daily scheduled update checks
* 📊 Basic event aggregation
* 📢 Console-based notifications
* 🧱 Modular and extensible architecture


## 📂 Project Structure
---

```text
app/
├── core/ # Core infrastructure
│ ├── config.py # Configuration management
│ ├── command_handler.py # CLI command parsing/handling
│ └── scheduler.py # Background scheduler (multi-threaded)

├── data/ # Data access layer
│ ├── github_client.py # GitHub API client (fetch issues/PRs)
│ └── subscriptions.json # Persistent storage for subscribed repositories

├── domain/ # Domain models (currently unused / reserved)
│ └── models.py

├── interfaces/ # Interface layer
│ └── cli/
│ └── run.py # CLI entry for triggering workflows

├── services/ # Business logic layer
│ ├── report_generator.py # Generate raw Markdown reports
│ └── llm/ # LLM integration layer
│ ├── base.py # LLM abstract interface
│ ├── factory.py # LLM client factory
│ └── ollama_client.py # Ollama-based local LLM implementation

├── reports/ # Generated reports (ignored by Git)
│ ├── raw/ # Raw data reports
│ └── processed/ # LLM summarized reports

├── storage/ # Persistence logic
│ └── repository.py # Manage subscriptions (add/remove/list)

├── main.py # Application entry point (scheduler + CLI loop)

data/ # (optional external data dir, if used)
tests/ # Test cases

.env # Environment variables
.gitignore # Git ignore rules
README.md # Project documentation
requirements.txt # Python dependencies
LICENSE # License
```

---

## ⚙️ Installation

```bash
git clone https://github.com/YOUR_USERNAME/github-sentinel.git
cd github-sentinel
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

Set your GitHub token:

```bash
export GITHUB_TOKEN=your_token_here
```

Windows:

```bash
set GITHUB_TOKEN=your_token_here
```

---

## ▶️ Usage

```bash
python app/main.py
```

---

## 🧠 Roadmap

### v0.1

* SQLite support
* CLI subscription management
* Deduplication

### v0.2

* Email notifications
* Markdown reports
* Event filtering

### v1.0

* AI-generated summaries
* Intelligent alerts
* Multi-repo aggregation

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit PRs.

---

## 📄 License

MIT License

