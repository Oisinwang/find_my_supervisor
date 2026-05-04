from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agents_policy_exists_and_preserves_delete_rule():
    agents = ROOT / "AGENTS.md"
    assert agents.exists()
    text = agents.read_text(encoding="utf-8")
    assert "D:\\rubbish" in text
    assert "requested deletion" in text


def test_readme_defines_skills_route_scope():
    readme = ROOT / "README.md"
    assert readme.exists()
    text = readme.read_text(encoding="utf-8")
    assert "skills route" in text.lower()
    assert "CS/AI" in text
    assert "mathematics" in text.lower()
    assert "985" in text
    assert "CAS/UCAS" in text
    assert "HKU" in text and "CUHK" in text and "HKUST" in text
