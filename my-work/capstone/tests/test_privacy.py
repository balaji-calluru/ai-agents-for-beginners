"""Privacy regression tests for the customer-scoped tools. No model calls, so they are free and fast.

    python -m pytest my-work/capstone/tests -q      (from the repo root, with the .venv active)
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # make `tools` and `data` importable

import tools  # noqa: E402
from data.seed import seed  # noqa: E402


@pytest.fixture(scope="module")
def db(tmp_path_factory):
    return seed(tmp_path_factory.mktemp("db") / "shop.db")  # throwaway copy, never the real shop.db


def call(db, customer_id, tool_index, order_id):
    return tools.make_tools(customer_id, db_path=db)[tool_index].func(order_id)


LOOKUP, WARRANTY = 0, 1


def test_customer_sees_own_order(db):
    assert "Turbo RC Car" in call(db, 1, LOOKUP, "A-1001")


def test_order_id_is_normalised(db):
    assert "Turbo RC Car" in call(db, 1, LOOKUP, "  a-1001 ")


@pytest.mark.parametrize("tool_index", [LOOKUP, WARRANTY])
def test_other_customers_order_is_hidden(db, tool_index):
    reply = call(db, 1, tool_index, "B-2001")  # B-2001 belongs to customer 2
    assert "No order" in reply and "Castle Block Set" not in reply


def test_foreign_order_looks_identical_to_missing_order(db):
    foreign = call(db, 1, LOOKUP, "B-2001").replace("B-2001", "X")
    missing = call(db, 1, LOOKUP, "Z-9999").replace("Z-9999", "X")
    assert foreign == missing  # a snooper can't tell which order ids exist


@pytest.mark.parametrize("payload", ["A-1001' OR '1'='1", "x' OR customer_id=2 --", "'; DROP TABLE orders; --"])
def test_sql_injection_returns_nothing(db, payload):
    assert "No order" in call(db, 1, LOOKUP, payload)
    assert "Turbo RC Car" in call(db, 1, LOOKUP, "A-1001")  # table still intact


def test_warranty_in_and_out_of_range(db):
    assert "UNDER WARRANTY" in call(db, 1, WARRANTY, "A-1001")  # 12 months from 2026-03-06
    assert "OUT OF WARRANTY" in call(db, 2, WARRANTY, "B-2002")  # 6 months from 2026-02-05


def test_warranty_not_started_before_delivery(db):
    assert "not been delivered" in call(db, 1, WARRANTY, "A-1003")
