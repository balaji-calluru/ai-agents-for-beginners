"""Create the synthetic Awesome Toys Store database (SQLite). Safe to re-run: it rebuilds from scratch.

    python my-work/capstone/data/seed.py

All data is fake. "Today" is pinned (AS_OF) so warranty checks and tests are deterministic.
"""

import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).with_name("shop.db")
AS_OF = date(2026, 11, 11)  # pinned "today" for the demo and the eval set
REFUND_APPROVAL_THRESHOLD = 5.34  # refunds above this need a human (see PROJECT.md)

SCHEMA = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL);
CREATE TABLE products  (sku TEXT PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL,
                        warranty_months INTEGER NOT NULL, description TEXT NOT NULL);
CREATE TABLE orders    (order_id TEXT PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id),
                        sku TEXT NOT NULL REFERENCES products(sku), qty INTEGER NOT NULL, total REAL NOT NULL,
                        status TEXT NOT NULL,            -- processing | shipped | delivered | refunded
                        order_date TEXT NOT NULL, delivered_date TEXT);
CREATE TABLE audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, customer_id INTEGER,
                        action TEXT NOT NULL, detail TEXT NOT NULL);
"""

CUSTOMERS = [(1, "Alice Tan", "alice@example.com"), (2, "Bob Rivera", "bob@example.com"),
             (3, "Chloe Park", "chloe@example.com")]

PRODUCTS = [  # sku, name, price, warranty_months, description
    ("STK-01", "Dino Sticker Pack", 4.99, 3, "50 reusable dinosaur stickers. Ages 3+."),
    ("PZL-02", "Space Puzzle 500pc", 14.50, 12, "500-piece jigsaw of the solar system. Ages 8+."),
    ("RC-03", "Turbo RC Car", 39.99, 12, "Rechargeable 2.4GHz remote-control car. Ages 6+."),
    ("BLK-04", "Castle Block Set", 59.00, 24, "420-piece building set with 4 minifigures. Ages 7+."),
    ("PLH-05", "Cuddly Bear Plush", 19.95, 6, "30cm machine-washable plush bear. All ages."),
    ("DRN-06", "Mini Drone", 79.00, 12, "Beginner drone with 2 spare batteries. Ages 12+."),
]

ORDERS = [  # order_id, customer_id, sku, qty, total, status, order_date, delivered_date
    ("A-1001", 1, "RC-03", 1, 39.99, "delivered", "2026-03-02", "2026-03-06"),   # in warranty
    ("A-1002", 1, "STK-01", 1, 4.99, "delivered", "2026-10-20", "2026-10-24"),   # tiny: under threshold
    ("A-1003", 1, "DRN-06", 1, 79.00, "shipped", "2026-11-08", None),             # not yet delivered
    ("B-2001", 2, "BLK-04", 1, 59.00, "delivered", "2025-06-01", "2025-06-05"),  # in 24-month warranty
    ("B-2002", 2, "PLH-05", 1, 19.95, "delivered", "2026-02-01", "2026-02-05"),  # 6-month warranty expired
    ("C-3001", 3, "PZL-02", 2, 29.00, "delivered", "2026-09-10", "2026-09-14"),  # in warranty
    ("C-3002", 3, "STK-01", 1, 4.99, "processing", "2026-11-10", None),
]


def seed(db_path: Path = DB_PATH) -> Path:
    db_path.unlink(missing_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA)
        conn.executemany("INSERT INTO customers VALUES (?,?,?)", CUSTOMERS)
        conn.executemany("INSERT INTO products VALUES (?,?,?,?,?)", PRODUCTS)
        conn.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?)", ORDERS)
    return db_path


if __name__ == "__main__":
    print(f"Seeded {seed()}")
