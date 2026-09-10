from fastapi.testclient import TestClient

from app.main import app



client = TestClient(app)



def test_home():

    response = client.get("/")


    assert response.status_code == 200


    assert response.json()["status"] == "running"


def test_parse_returns_headings_and_validation():
    response = client.post(
        "/api/parse",
        json={"text": "INTRODUCTION\n\n3. Details"},
    )

    assert response.status_code == 200
    assert response.json()["headings"] == [
        {"title": "INTRODUCTION", "level": 1},
        {"title": "Details", "level": 1},
    ]


def test_upload_rejects_non_pdf():
    response = client.post(
        "/api/upload",
        files={"file": ("notes.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 415


def test_versions_are_persisted_and_compared():
    first = client.post(
        "/api/versions",
        json={"document_id": "api-test", "content": "INTRODUCTION"},
    )
    second = client.post(
        "/api/versions",
        json={"document_id": "api-test", "content": "INTRODUCTION\nCONCLUSION"},
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["version"] == first.json()["version"] + 1

    comparison = client.post(
        "/api/compare",
        params={"document_id": "api-test", "old_version": 1, "new_version": 2},
    )
    assert comparison.status_code == 200
    assert comparison.json()["added"] == ["CONCLUSION"]
