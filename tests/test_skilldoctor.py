from pathlib import Path
import json
import pytest
import skilldoctor.cli as sd


def write(path: Path, name="demo-skill", desc="Extracts release notes from merged PRs. Use when the user asks for a changelog.", extra="", body="# Demo\n\nSteps here.\n", filename="SKILL.md"):
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = f"---\nname: {name}\ndescription: {desc}\n{extra}---\n\n{body}"
    path.write_text(fm, encoding="utf-8")
    return path


def test_help_and_version():
    with pytest.raises(SystemExit) as exc:
        sd.main(["--help"])
    assert exc.value.code == 0
    with pytest.raises(SystemExit) as exc:
        sd.main(["--version"])
    assert exc.value.code == 0


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


def test_official_allowed_tools_ok(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md", extra="allowed-tools: Bash\n")
    assert sd.main([str(folder)]) == 0
    assert "clean" in capsys.readouterr().out


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


def test_missing_path(tmp_path, capsys):
    assert sd.main([str(tmp_path / "nope")]) == 1
    assert "path not found" in capsys.readouterr().err


def test_empty_file(tmp_path, capsys):
    path = tmp_path / "demo-skill" / "SKILL.md"
    path.parent.mkdir()
    path.write_text("")
    assert sd.main([str(path)]) == 2
    assert "frontmatter-missing" in capsys.readouterr().out


def test_description_too_long(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md", desc=("Use when processing a very long description. " + ("word " * 400)))
    assert sd.main([str(folder)]) == 2
    assert "description-length" in capsys.readouterr().out


def test_compatibility_too_long(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md", extra="compatibility: " + ("x" * 501) + "\n")
    assert sd.main([str(folder)]) == 2
    assert "compatibility-length" in capsys.readouterr().out


def test_metadata_must_be_mapping(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md", extra="metadata: just-a-string\n")
    assert sd.main([str(folder)]) == 2
    assert "metadata-type" in capsys.readouterr().out


def test_no_when_warning(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(
        folder / "SKILL.md",
        desc="Extracts release notes from merged pull requests and formats a changelog.",
    )
    assert sd.main([str(folder)]) == 1
    assert "no-when" in capsys.readouterr().out


def test_body_long_warning(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    body = "\n".join(f"line {i}" for i in range(501))
    write(folder / "SKILL.md", body=body)
    assert sd.main([str(folder)]) == 1
    assert "body-long" in capsys.readouterr().out


def test_unknown_disable_model_invocation(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md", extra="disable_model_invocation: true\n")
    assert sd.main([str(folder)]) == 2
    assert "unknown-field" in capsys.readouterr().out


def test_empty_directory(tmp_path, capsys):
    folder = tmp_path / "empty"
    folder.mkdir()
    assert sd.main([str(folder)]) == 2
    assert "not-found" in capsys.readouterr().out


def test_unicode_body_clean(tmp_path, capsys):
    folder = tmp_path / "demo-skill"
    write(folder / "SKILL.md", body="# Demo\n\n整理メモ。Emoji ✅\n")
    assert sd.main([str(folder)]) == 0
