"""
Document version management.

Handles:
- creating versions
- comparing versions
- tracking changes
"""


class VersionManager:



    def create_version(
        self,
        old_versions
    ):

        """
        Generates next version number.
        """


        if not old_versions:

            return 1


        latest = max(
            old_versions
        )


        return latest + 1



    def compare(
        self,
        old_headings,
        new_headings
    ):


        old_map = {

            h["title"]:
            h["level"]

            for h in old_headings
        }



        new_map = {

            h["title"]:
            h["level"]

            for h in new_headings
        }



        added = []

        removed = []

        changed = []



        for title in new_map:


            if title not in old_map:

                added.append(title)



            elif old_map[title] != new_map[title]:

                changed.append(
                    title
                )



        for title in old_map:


            if title not in new_map:

                removed.append(title)



        return {

            "added":
            added,


            "removed":
            removed,


            "changed":
            changed

        }v
