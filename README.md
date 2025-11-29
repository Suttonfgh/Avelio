# Avelio MVP - Architecture Guard

## 🎯 What is Avelio?

**Avelio** is an **Early Warning System** and **Architectural Guard** designed to oversee code contributed by AI agents and developers.

### The Problem
Typical AI agents excel at tactical tasks (writing functions, fixing bugs) but often ignore the strategic consequences of their actions, leading to:
- Unseen technical debt
- Integration errors
- API mismatches between frontend and backend

### Avelio's Mission
To convert invisible architectural risk into a **visible warning** during the Pull Request stage.

### MVP Focus
**API Contract Integrity** - Ensuring that backend code changes (models) are properly reflected in the API contract file (`openapi.yaml`).

---

## 🚀 Installation

```bash
pip install -r requirements.txt
```

---

## 📖 Usage

```bash
python src/avelio_core.py --old-commit <commit-hash> --new-commit <commit-hash>
```

---

## 🧩 Architecture

### Module 1: AST Parser (`ast_parser.py`)
- Accepts Git Diff and transforms it into structured JSON
- Detects `RENAME` and `DELETE` operations in Python models
- Uses Python's built-in `ast` module for syntax tree analysis

### Module 2: Contract Validator (`contract_validator.py`)
- Compares AST changes against OpenAPI contract
- Detects violations (missing updates in contract)
- Returns detailed violation reports

### Module 3: Entry Point (`avelio_core.py`)
- Orchestrates the analysis workflow
- Provides CI/CD-ready output
- Returns appropriate exit codes

---

## 🧪 Testing

Example target project is included in `/target_project/` for testing purposes.

---

## 📝 License

MIT License
