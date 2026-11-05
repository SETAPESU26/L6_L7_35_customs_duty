import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# ---------- duty_rate ----------
def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0

def test_prohibited_item_raises():
    with pytest.raises(ValueError):
        duty_rate("weapons", "US")

def test_electronics_fta():
    assert duty_rate("electronics", "FTA") == 0.10

def test_electronics_non_fta():
    assert duty_rate("electronics", "US") == 0.20

def test_clothing_fta():
    assert duty_rate("clothing", "FTA") == 0.05

def test_clothing_non_fta():
    assert duty_rate("clothing", "US") == 0.12

def test_other_category_default_rate():
    assert duty_rate("toys", "US") == 0.15


# ---------- total_duty ----------
def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0

def test_negative_value_raises():
    with pytest.raises(ValueError):
        total_duty("books", -1, "US", False)

def test_gift_below_exemption():
    assert total_duty("electronics", 3000, "US", True) == 0

def test_minimum_duty_applied():
    # gift of 5001 -> taxable value 1 -> duty 0.05 -> raised to minimum 50
    assert total_duty("clothing", 5001, "FTA", True) == 50


# ---------- clearance_channel ----------
def test_prohibited_is_refused():
    assert clearance_channel(100, "narcotics", True) == "refuse"

def test_very_high_value_is_inspected():
    assert clearance_channel(150000, "books", True) == "inspect"

def test_high_value_without_documents_is_inspected():
    assert clearance_channel(30000, "books", False) == "inspect"

def test_low_value_is_green():
    assert clearance_channel(5000, "books", True) == "green"
