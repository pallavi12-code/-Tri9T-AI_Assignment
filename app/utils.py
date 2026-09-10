"""Small helpers shared by parsing and tests."""


def create_heading(title: str, level: int) -> dict[str, int | str]:
    return {"title": title, "level": level}


def create_sample_document() -> list[dict[str, int | str]]:
    return [
        create_heading("Introduction", 1),
        create_heading("Background", 2),
        create_heading("Conclusion", 1),
    ]
