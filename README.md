# skilldoctor

Lint an Agent Skill (`SKILL.md`) against the public
[Agent Skills specification](https://agentskills.io/specification). Catch the
failures that otherwise go silent: a typo in frontmatter, a file named
`skill.md` on Linux, a directory name that does not match `name`, or a
description so vague that the agent never triggers the skill.

## Install

```bash
python3 -m pip install -e .
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
