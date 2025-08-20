def test_movie_rank_requires_login(client):
    resp = client.get("/movie_rank")
    assert resp.status_code in (302, 401, 403)