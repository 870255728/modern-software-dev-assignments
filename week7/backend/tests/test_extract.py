import pytest

from backend.app.services.extract import extract_action_items


def test_extracts_supported_action_patterns_in_source_order():
    text = """
    Meeting summary
    - TODO: write tests
    * ACTION ITEM: review PR
    1. Next step: deploy staging
    + FIXME: handle empty input
    - [ ] Update the README
    - @maya: confirm the launch date
    We need to notify support
    Please archive the old dashboard
    Ship it!
    """.strip()

    assert extract_action_items(text) == [
        "TODO: write tests",
        "ACTION ITEM: review PR",
        "Next step: deploy staging",
        "FIXME: handle empty input",
        "[ ] Update the README",
        "@maya: confirm the launch date",
        "We need to notify support",
        "Please archive the old dashboard",
        "Ship it!",
    ]


def test_ignores_completed_tasks_and_non_actionable_notes():
    text = """
    - [x] Already shipped
    - [X] Also complete
    This is background context.
    The team discussed deployment.
    """.strip()

    assert extract_action_items(text) == []


def test_deduplicates_case_insensitively_after_cleaning_bullets():
    text = """
    - TODO: Write tests
    * todo: write tests
    """.strip()

    assert extract_action_items(text) == ["TODO: Write tests"]


@pytest.mark.parametrize(
    "text",
    [
        "",
        "\n\n",
        "- TODO:",
        "- [ ]",
        "@owner:",
        "We should to",
    ],
)
def test_does_not_emit_empty_or_incomplete_actions(text):
    assert extract_action_items(text) == []
