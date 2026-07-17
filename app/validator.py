"""
Validation utilities for parsed document structures.

Handles:
- duplicate heading detection
- heading hierarchy validation
- skipped heading levels
- document structure warnings
"""


class DocumentValidator:

    def __init__(self):
        self.errors = []
        self.warnings = []


    def validate(self, headings):
        """
        Main validation entry point.

        headings format:

        [
            {
                "title": "Introduction",
                "level": 1
            }
        ]

        """

        self.errors = []
        self.warnings = []

        self.check_duplicates(headings)
        self.check_heading_levels(headings)

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }


    def check_duplicates(self, headings):
        """
        Detect duplicate headings.

        Example:

        Introduction
        Introduction

        """

        seen = set()


        for heading in headings:

            title = heading["title"].strip().lower()

            if title in seen:

                self.warnings.append(
                    f"Duplicate heading detected: {heading['title']}"
                )

            else:
                seen.add(title)



    def check_heading_levels(self, headings):
        """
        Detect skipped heading levels.

        Example:

        H1
          H2
            H3

        Valid


        H1
            H3

        Invalid because H2 skipped.
        """


        previous_level = 0


        for heading in headings:

            current_level = heading["level"]


            if current_level > previous_level + 1:

                self.warnings.append(
                    f"Skipped heading level before "
                    f"{heading['title']} "
                    f"(H{current_level})"
                )


            previous_level = current_level



    def has_duplicate(self, headings, title):
        """
        Helper used in unit tests.
        """

        count = 0


        for heading in headings:

            if heading["title"].lower() == title.lower():
                count += 1


        return count > 1
