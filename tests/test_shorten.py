from http import HTTPStatus

from fastapi.testclient import TestClient


def test_shorten_url(client: TestClient):
    payload = {"url": "https://www.python.org/"}
    response = client.post("/api/shorten", json=payload)

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert "short_url" in data
    assert data["original_url"] == "https://www.python.org/"
    assert data["message"] == "URL encurtada com sucesso!"


def test_list_urls(client: TestClient):
    client.post("/api/shorten", json={"url": "https://www.python.org/"})
    client.post("/api/shorten", json={"url": "https://fastapi.tiangolo.com/"})

    response = client.get("/api/links")

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["original_url"] == "https://www.python.org/"
    assert data[1]["original_url"] == "https://fastapi.tiangolo.com/"


def test_redirect_url(client: TestClient):
    payload = {"url": "https://www.python.org/"}
    create_res = client.post("/api/shorten", json=payload)
    short_url = create_res.json()["short_url"]
    short_id = short_url.split("/")[-1]

    response = client.get(f"/{short_id}", follow_redirects=False)

    assert response.status_code in (HTTPStatus.FOUND, HTTPStatus.TEMPORARY_REDIRECT)
    assert response.headers["location"] == "https://www.python.org/"


def test_get_url_stats(client: TestClient):
    payload = {"url": "https://www.python.org/"}
    create_res = client.post("/api/shorten", json=payload)
    short_url = create_res.json()["short_url"]
    short_id = short_url.split("/")[-1]

    response = client.get(f"/api/stats/{short_id}")

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["original_url"] == "https://www.python.org/"
    assert data["short_url"] == short_url
    assert data["total_accesses"] == 0
    assert data["top_referrers"] == {}
    assert data["unique_visitors"] == 0
    assert data["recent_accesses"] == []
