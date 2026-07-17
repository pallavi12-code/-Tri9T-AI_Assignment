from app.parser import DocumentParser



def test_parser():

    parser = DocumentParser()


    text = """
INTRODUCTION

Overview:

"""


    result = parser.extract_headings(text)


    assert len(result) > 0
