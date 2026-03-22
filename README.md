# DiffSage

An intelligent Git diff analyzer that leverages advanced LLMs to provide deep semantic understanding of code changes.

## 🔥 Key Features

- Semantic change detection beyond simple line diffs
- Security vulnerability analysis in changed code paths
- Architectural impact assessment of changes
- Automated code review suggestions with rationale
- Technical debt tracking across changes
- Integration with major CI/CD platforms

## 🚀 Getting Started

```bash
pip install diffsage
diffsage analyze --repo=/path/to/repo --branch=feature/new-changes
```

## 🔧 Configuration

Create a `diffsage.yaml` in your repo root:

```yaml
model: gpt-5-turbo
ignore_patterns:
  - '*.min.js'
  - 'vendor/*'
rules:
  max_complexity_increase: 5
  required_test_coverage: 0.8
```

## 🔍 How It Works

DiffSage uses a multi-stage pipeline:
1. Extract semantic code representations
2. Compare AST changes with context
3. Apply LLM reasoning for impact analysis
4. Generate human-readable insights

## 🤝 Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📜 License

MIT
