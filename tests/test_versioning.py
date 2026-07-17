from app.versioning import VersionManager



def test_version_compare():


    manager = VersionManager()


    old = [

        {
            "title":"Intro",
            "level":1
        }

    ]


    new = [

        {
            "title":"Intro",
            "level":1
        },

        {
            "title":"Conclusion",
            "level":2
        }

    ]


    result = manager.compare(
        old,
        new
    )


    assert "Conclusion" in result["added"]
