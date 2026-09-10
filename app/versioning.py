"""Document version numbering and heading comparison."""


class VersionManager:
    """Compare parsed heading structures and calculate next versions."""

    @staticmethod
    def create_version(old_versions: list[int]) -> int:
        return max(old_versions, default=0) + 1

    @staticmethod
    def compare(
        old_headings: list[dict[str, int | str]],
        new_headings: list[dict[str, int | str]],
    ) -> dict[str, list[str]]:
        old_map = {str(item["title"]): item["level"] for item in old_headings}
        new_map = {str(item["title"]): item["level"] for item in new_headings}
        return {
            "added": [title for title in new_map if title not in old_map],
            "removed": [title for title in old_map if title not in new_map],
            "changed": [
                title
                for title in new_map
                if title in old_map and old_map[title] != new_map[title]
            ],
        }
