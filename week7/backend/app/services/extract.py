import re

PREFIX_PATTERN = re.compile(
    r"^(?:todo|action(?:\s+item)?|next\s+step|fixme)\s*:\s*\S",
    re.IGNORECASE,
)
OPEN_CHECKBOX_PATTERN = re.compile(r"^\[\s\]\s+\S")
COMPLETED_CHECKBOX_PATTERN = re.compile(r"^\[[xX]\]\s+")
ASSIGNEE_PATTERN = re.compile(r"^@\w+(?:[-.]\w+)*\s*:\s*\S")
DIRECTIVE_PATTERN = re.compile(
    r"^(?:please\s+|remember\s+to\s+|we\s+(?:need|must|should)\s+to\s+|"
    r"(?:i|you|they)\s+(?:need|must|should)\s+to\s+)\S",
    re.IGNORECASE,
)
BULLET_PATTERN = re.compile(r"^(?:[-*+]|\d+[.)])\s+")


def _clean_line(raw_line: str) -> str:
    line = raw_line.strip()
    line = BULLET_PATTERN.sub("", line)
    return line.strip()


def _is_actionable(line: str) -> bool:
    if COMPLETED_CHECKBOX_PATTERN.match(line):
        return False
    return bool(
        PREFIX_PATTERN.match(line)
        or OPEN_CHECKBOX_PATTERN.match(line)
        or ASSIGNEE_PATTERN.match(line)
        or DIRECTIVE_PATTERN.match(line)
        or line.endswith("!")
    )


def extract_action_items(text: str) -> list[str]:
    """Extract actionable lines while preserving their useful context.

    Supported forms include explicit labels, unchecked Markdown tasks,
    assignee-prefixed tasks, directive language, and emphatic lines. Completed
    Markdown tasks are ignored and duplicate actions are removed.
    """
    results: list[str] = []
    seen: set[str] = set()

    for raw_line in text.splitlines():
        line = _clean_line(raw_line)
        if not line or not _is_actionable(line):
            continue

        normalized = line.casefold()
        if normalized in seen:
            continue
        seen.add(normalized)
        results.append(line)

    return results
