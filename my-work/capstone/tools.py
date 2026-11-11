"""Customer-scoped tools for the Awesome Toys support agent.

KEY DESIGN RULE: the customer's identity is bound when the tools are created (make_tools), so
it is never an argument the model can fill in. A customer asking about someone else's order
cannot get it by tricking the prompt: the tool simply has no way to look beyond its own customer.
"""

import sqlite3
from datetime import date
from pathlib import Path
from typing import Annotated

from agent_framework import tool

from data.seed import AS_OF, DB_PATH


def _months_after(start: date, months: int) -> date:
    """Calendar-month addition without extra dependencies (clamps the day, e.g. Jan 31 + 1 month)."""
    month_index = start.month - 1 + months
    year, month = start.year + month_index // 12, month_index % 12 + 1
    day = start.day
    while True:
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1


def _get_owned_order(conn: sqlite3.Connection, customer_id: int, order_id: str) -> sqlite3.Row | None:
    """Return the order row ONLY if it belongs to `customer_id`; otherwise None.

    This is the single choke point for the "never show other customers' data" rule: every tool
    reads orders through here.
    """
    # Both ids are in the WHERE clause, so another customer's row is never loaded at all.
    return conn.execute(
        "SELECT * FROM orders WHERE customer_id = ? AND order_id = ?", (customer_id, order_id)
    ).fetchone()


def make_tools(customer_id: int, db_path: Path = DB_PATH, as_of: date = AS_OF):
    """Build the tool list for ONE signed-in customer."""

    def _connect() -> sqlite3.Connection:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @tool(approval_mode="never_require")
    def lookup_order(order_id: Annotated[str, "The order ID, e.g. A-1001"]) -> str:
        """Look up one of the signed-in customer's orders: product, quantity, total, status and dates."""
        with _connect() as conn:
            row = _get_owned_order(conn, customer_id, order_id.strip().upper())
            if row is None:
                return f"No order {order_id!r} was found on your account."
            product = conn.execute("SELECT name FROM products WHERE sku = ?", (row["sku"],)).fetchone()
        delivered = row["delivered_date"] or "not yet delivered"
        return (
            f"Order {row['order_id']}: {row['qty']} x {product['name']}, total ${row['total']:.2f}, "
            f"status {row['status']}, ordered {row['order_date']}, delivered {delivered}."
        )

    @tool(approval_mode="never_require")
    def check_warranty(order_id: Annotated[str, "The order ID, e.g. A-1001"]) -> str:
        """Check whether one of the signed-in customer's orders is still under warranty."""
        with _connect() as conn:
            row = _get_owned_order(conn, customer_id, order_id.strip().upper())
            if row is None:
                return f"No order {order_id!r} was found on your account."
            product = conn.execute(
                "SELECT name, warranty_months FROM products WHERE sku = ?", (row["sku"],)
            ).fetchone()
        if not row["delivered_date"]:
            return f"Order {row['order_id']} has not been delivered yet, so the warranty has not started."
        expires = _months_after(date.fromisoformat(row["delivered_date"]), product["warranty_months"])
        days_left = (expires - as_of).days
        if days_left >= 0:
            return (
                f"{product['name']} (order {row['order_id']}) is UNDER WARRANTY until {expires} "
                f"({days_left} days left; {product['warranty_months']}-month warranty from delivery)."
            )
        return (
            f"{product['name']} (order {row['order_id']}) is OUT OF WARRANTY: it expired on {expires} "
            f"({-days_left} days ago; {product['warranty_months']}-month warranty from delivery)."
        )

    return [lookup_order, check_warranty]
