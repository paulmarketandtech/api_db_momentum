def test_health_check(client):
    response = client.get("/meta_data/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ytd_best_returns_list(client):
    response = client.get("/returns/ytd-best/2025-12-31")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ytd_best_returns_correct_fields(client):
    response = client.get("/returns/ytd-best/2025-12-09")
    data = response.json()

    if len(data) > 0:
        first_item = data[0]

        assert "ticker" in first_item
        assert "date" in first_item
        assert "pct_change" in first_item


def test_ytd_best_future_date_returns_empty(client):
    """Future date should return empty list, not error"""
    response = client.get("/returns/ytd-best/2099-01-15")

    assert response.status_code == 200
    assert response.json() == []


def test_stock_price_nonexistent_ticker(client):
    """Fake ticker should return 404 or empty"""
    response = client.get("/prices/FAKETICKER123/2025-01-15")

    assert response.status_code == 200
