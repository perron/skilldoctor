from pathlib import Path
import json
import skilldoctor.cli as sd


def write(path: Path, name="demo-skill", desc="Extracts release notes from merged PRs. Use when the user asks for a changelog.", extra="", body="# Demo\n\nSteps here.\n", filename="SKILL.md"):
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = f"---\nname: {name}\ndescription: {desc}\n{extra}---\n\n{body}"
    path.write_text(fm, encoding="utf-8")
    return path


def test_clean_skill(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md")
    assert sd.main([str(folder)]) == 0
    assert "clean" in capsys.readouterr().out


def test_filename_case(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "skill.md")
    assert sd.main([str(folder / "skill.md")]) == 2
    out = capsys.readouterr().out
    assert "filename-case" in out


def test_typo_allowed_tools(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md", extra="allowed_tools: Bash\n")
    assert sd.main([str(folder)]) == 2
    out = capsys.readouterr().out
    assert "allowed-tools" in out
    assert "typo-field" in out


def test_weak_and_name_mismatch(tmp_path, capsys):
    folder = tmp_path / "other"
    write(folder / "SKILL.md", name="demo-skill", desc="Helps with writing.")
    code = sd.main([str(folder), "--json"])
    assert code == 2
    data = json.loads(capsys.readouterr().out)
    codes = {f["code"] for f in data["findings"]}
    assert "name-mismatch" in codes
    assert "weak-description" in codes


def test_invalid_name(tmp_path, capsys):
    folder = tmp_path / "PDF-Processing"
    write(folder / "SKILL.md", name="PDF-Processing", desc="Processes PDF files into text. Use when the user mentions a PDF.")
    assert sd.main([str(folder)]) == 2
    assert "invalid-name" in capsys.readouterr().out


def test_missing_frontmatter(tmp_path, capsys):
    path = tmp_path / "x" / "SKILL.md"
    path.parent.mkdir()
    path.write_text("# just a file\n")
    assert sd.main([str(path)]) == 2
    assert "frontmatter-missing" in capsys.readouterr().out
