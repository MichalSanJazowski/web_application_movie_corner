def test_login_logout_flow(client, user):
    resp = client.post("/login", data={"email": "user@example.com", "password": "pass123"}, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Please log in" not in resp.data

    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200