import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# ---------- duty_rate ----------
def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0

def test_prohibited_item_raises():
    with pytest.raises(ValueError):
        duty_rate("narcotics", "US")

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

def test_personal_import_boundary_1000_is_exempt():
    assert total_duty("electronics", 1000, "US", False) == 0

def test_negative_value_raises():
    with pytest.raises(ValueError):
        total_duty("books", -1, "US", False)

def test_negative_gift_value_raises():
    with pytest.raises(ValueError):
        total_duty("books", -50, "US", True)

def test_gift_below_exemption():
    assert total_duty("electronics", 3000, "US", True) == 0

def test_gift_boundary_5000_is_exempt():
    assert total_duty("electronics", 5000, "US", True) == 0

def test_gift_above_exemption_pays_duty_on_excess():
    # taxable value 1000 * 0.15 = 150
    assert total_duty("toys", 6000, "US", True) == pytest.approx(150)

def test_minimum_duty_applied_for_gift():
    assert total_duty("clothing", 5001, "FTA", True) == 50

def test_personal_import_above_1000_electronics_non_fta():
    assert total_duty("electronics", 2000, "US", False) == pytest.approx(400)

def test_personal_import_above_1000_electronics_fta():
    assert total_duty("electronics", 2000, "FTA", False) == pytest.approx(200)

def test_duty_just_above_minimum_not_raised():
    # 1001 * 0.05 = 50.05, which is not below 50
    assert total_duty("clothing", 1001, "FTA", False) == pytest.approx(50.05)

def test_zero_duty_category_above_threshold():
    assert total_duty("books", 2000, "US", False) == 0

def test_prohibited_category_raises_in_total_duty():
    with pytest.raises(ValueError):
        total_duty("weapons", 5000, "US", False)


# ---------- clearance_channel ----------
def test_prohibited_is_refused():
    assert clearance_channel(100, "narcotics", True) == "refuse"

def test_very_high_value_is_inspected():
    assert clearance_channel(100001, "books", True) == "inspect"

def test_value_exactly_100000_with_documents_is_green():
    assert clearance_channel(100000, "books", True) == "green"

def test_high_value_without_documents_is_inspected():
    assert clearance_channel(30000, "books", False) == "inspect"

def test_high_value_with_documents_is_green():
    assert clearance_channel(30000, "books", True) == "green"

def test_value_exactly_20000_without_documents_is_green():
    assert clearance_channel(20000, "books", False) == "green"

def test_low_value_is_green():
    assert clearance_channel(5000, "books", False) == "green"
