import datetime
from decimal import Decimal
import sys
import os
import requests
from unittest.mock import MagicMock, patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from data.question import (
    create_view_completed_orders,
    create_view_electronics_products,
    total_spending_per_customer,
    order_details_with_total,
    get_customer_who_bought_most_expensive_product,
    get_order_status_descriptions,
    get_products_above_average_price,
    get_customer_categories,
    get_recent_customers,
    get_most_ordered_product,
    get_product_price_categories,
)


def test_create_view_completed_orders():
    result = create_view_completed_orders()
    assert result is None 

def test_create_view_electronics_products():
    result = create_view_electronics_products()
    assert result is None 

def test_total_spending_per_customer():
    result = total_spending_per_customer()
    assert result is not None
    assert isinstance(result, list)

def test_order_details_with_total():
    result = order_details_with_total()
    assert result is not None
    assert isinstance(result, list)

def test_get_customer_who_bought_most_expensive_product():
    result = get_customer_who_bought_most_expensive_product()
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0], tuple)


def test_get_order_status_descriptions():
    result = get_order_status_descriptions()
    assert isinstance(result, list)
    if result:
        assert len(result[0]) == 3  # order_id, status, status_description


def test_get_products_above_average_price():
    result = get_products_above_average_price()
    assert isinstance(result, list)
    if result:
        assert len(result[0]) == 2  # product_name, price


def test_get_customer_categories():
    result = get_customer_categories()
    assert isinstance(result, list)
    if result:
        assert len(result[0]) == 2  # full_name, customer_category


def test_get_recent_customers():
    result = get_recent_customers()
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0][0], str)  # sadece isim geliyor


def test_get_most_ordered_product():
    result = get_most_ordered_product()
    assert isinstance(result, list)
    if result:
        assert isinstance(result[0][0], str)  # ürün adı


def test_get_product_price_categories():
    result = get_product_price_categories()
    assert isinstance(result, list)
    if result:
        assert len(result[0]) == 3  # product_name, price, price_category

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")


class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://edugen-backend-487d2168bc6c.herokuapp.com/projectLog/"
    payload = {
        "user_id": 403,
        "project_id": 37,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()