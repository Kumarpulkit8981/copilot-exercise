from pathlib import Path


def test_activity_cards_render_participants_section():
    app_js = Path(__file__).resolve().parents[1] / "src" / "static" / "app.js"
    contents = app_js.read_text()

    assert "Participants" in contents
    assert "participants-list" in contents
    assert "details.participants" in contents
