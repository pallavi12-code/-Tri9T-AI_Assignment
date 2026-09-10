"""Text and PDF heading extraction."""

from __future__ import annotations

import re


class DocumentParser:
    """Extract headings from plain text using conservative heuristics."""

    _numbered_heading = re.compile(r"^(?P<number>\d+(?:\.\d+)*)[.)]?\s+(?P<title>.+)$")

    def extract_headings(self, text: str) -> list[dict[str, int | str]]:
        headings: list[dict[str, int | str]] = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            match = self._numbered_heading.match(line)
            if match:
                level = min(match.group("number").count(".") + 1, 6)
                title = match.group("title").strip()
            elif self._is_heading(line):
                level = 1
                title = line
            else:
                continue

            headings.append({"title": title, "level": level})
        return headings

    @staticmethod
    def _is_heading(line: str) -> bool:
        words = line.split()
        return (
            len(line) <= 120
            and len(words) <= 12
            and not line.endswith((".", ",", ";", ":"))
            and (line.isupper() or line.istitle())
        )
