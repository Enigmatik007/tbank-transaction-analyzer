from unittest.mock import Mock, patch

import pytest
import requests

from src.api import finance_client


def test_no_api_key(monkeypatch):
    monkeypatch.delenv("TWELVE_DATA_API_KEY", raising=False)
    with pytest.raises(ValueError, match="API key not found"):
        finance_client.get_currency_rates()
    with pytest.raises(ValueError, match="API key not found"):
        finance_client.get_stock_prices()


@patch("src.api.finance_client.requests.get")
def test_get_currency_rates_success(mock_get, monkeypatch):
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "fakekey")
    mock_response = Mock()
    mock_response.json.return_value = {"rate": "75.5"}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    rates = finance_client.get_currency_rates()
    assert isinstance(rates, list)
    assert rates[0]["currency"] == "USD"
    assert isinstance(rates[0]["rate"], float)


@patch("src.api.finance_client.requests.get")
def test_get_stock_prices_success(mock_get, monkeypatch):
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "fakekey")
    mock_response = Mock()
    mock_response.json.return_value = {"price": "150.0"}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    prices = finance_client.get_stock_prices()
    assert isinstance(prices, list)
    assert prices[0]["stock"] == "AAPL"
    assert isinstance(prices[0]["price"], float)


@patch("src.api.finance_client.requests.get")
def test_requests_http_error(mock_get, monkeypatch):
    monkeypatch.setenv("TWELVE_DATA_API_KEY", "fakekey")
    mock_get.side_effect = requests.exceptions.HTTPError("HTTP error")

    with pytest.raises(requests.exceptions.HTTPError):
        finance_client.get_currency_rates()

    with pytest.raises(requests.exceptions.HTTPError):
        finance_client.get_stock_prices()
