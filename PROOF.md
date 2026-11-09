# skilldoctor proof

Captured 2026-11-09 13:26 PST.

Fresh-venv install: `pip install .` succeeded and `skilldoctor --version` printed `skilldoctor 0.1.1`.

Tests: 18 passed in 0.03s

## lint of a typo-ridden skill (expect errors)
```
error: typo-field: field 'allowed_tools' is not in the Agent Skills spec; did you mean allowed-tools? (/tmp/ai-tools-proof/skilldoctor/tidy-notes/SKILL.md)
warning: weak-description: description is vague or short; agents pick skills from this field and a line like 'Helps with writing.' often never triggers. Say what it does and when to use it. (/tmp/ai-tools-proof/skilldoctor/tidy-notes/SKILL.md)
1 error(s), 1 warning(s)
exit: 2
```
