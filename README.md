# skilldoctor

Lint an Agent Skill (`SKILL.md`) against the public
[Agent Skills specification](https://agentskills.io/specification). Catch the
failures that otherwise go silent: a typo in frontmatter, a file named
`skill.md` on Linux, a directory name that does not match `name`, or a
description so vague that the agent never triggers the skill.

## Install

Python 3.10 or later.

From a checkout:

```bash
python3 -m pip install .
python3 -m pip install -e ".[dev]"  # optional, for tests
skilldoctor path/to/skill
```

Or without installing:

```bash
PYTHONPATH=. python3 -m skilldoctor path/to/skill
```

## 30-second example

```bash
mkdir -p tidy-notes
cat > tidy-notes/SKILL.md << 'EOF'
---
name: tidy-notes
description: Helps with writing.
allowed_tools: Bash
---

Tidy the notes.
EOF

skilldoctor ./tidy-notes
```

You should see an error that `allowed_tools` should be `allowed-tools`, a
warning that the description is too vague to trigger, and a non-zero exit.

Exit codes: `0` clean, `1` warnings only, `2` errors.

## Credit

Field names and constraints follow the public Agent Skills specification
(fetched 9 Nov 2026). The typo and trigger-quality checks were motivated by
public reports of silent frontmatter failures and of vague descriptions that
never loaded. No linter source was copied.

## Limits

- The frontmatter parser is intentionally small: a flat YAML map plus one level of nested `metadata:` keys. It is not a full YAML parser.
- Field names and length limits follow the public Agent Skills specification as fetched on 9 Nov 2026. The spec may change.
- A clean report means the file matches those checks, not that the skill is safe to run. Use skillguard for a static security pass.

From GitHub you can also install with:

```bash
python3 -m pip install git+https://github.com/perron/skilldoctor.git
```

This package is not published to PyPI.

## License

MIT. See `LICENSE`. Please read `SECURITY.md` before filing a vulnerability report.
