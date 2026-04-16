# Warehouse Management System

A lightweight, modern,and performant Warehouse & Inventory Management System built with the Frappe Framework.
Designed for **X Electronics**, this app provides full stock tracking with a **stateless Stock Ledger** approach.

## Overview

A simple yet powerful warehouse management system that supports:

- Accurate inventory tracking
- Moving Average valuation
- Real-time stock movements
- Clean audit trail via stateless ledger
- Insightful reports (Stock Ledger + Stock Balance)

---

## Key Features

### 1. Product Management

- Create and manage electronic products/items.
- Support for basic fields (Item Code, Name, Valuation Method = Moving Average).

### 2. Warehouse Management

- Tree structure (e.g., Main Store → Shelf A → Bin 01).
- Unlimited nesting.

### 3. Stock Operations

- Full support for Receipt, Consumption, and Transfer.
- Automatic creation of Stock Ledger Entries on submit.
- Automatic deletion on cancellation.

### 4. Valuation Method

- Moving Average Valuation.
- Calculated efficiently using a single optimized SQL query.

### 5. Reports

**Stock Ledger** - Detailed line-by-line history of all stock movements.
**Stock Balance** - Current quantity + valuation as of any date (with grouping).

### 6. Test Coverage

- Unit tests for all core functionality (e.g. stock entry logic, validations).
- Basic unit tests for reports to ensure accurate aggregation and filtering.

---

## Architecture

### Core DocTypes

| DocType            | Type           | Purpose                                                      | Key Fields                                                                                       |
| ------------------ | -------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Product            | Document       | Defines stockable items in the system                        | `item_code`, `item_name`, `uom`, `valuation_rate`, `description`                                 |
| Warehouse          | Tree DocType   | warehouse/locations (supports nesting)                       | `warehouse_name`, `warehouse_type`, `is_group`                                                   |
| Stock Entry        | Submittable    | User-facing document for Receipt, Issue, and Transfer        | `type`, `from_warehouse`, `to_warehouse`, `items (child table)`                                  |
| Stock Entry Item   | Child          | Item in the stock entry                                      | `item`, `quantity`, `valuation_rate`                                                             |
| Stock Ledger Entry | System (Child) | Stateless audit trail — created on submit, deleted on cancel | `item`, `warehouse`, `quantity`, `incoming_rate`, `valuation_rate`, `voucher_no`, `voucher_type` |

### Stateless Stock Ledger

Unlike ERPNext’s traditional approach (which updates stock in multiple places), this system uses a stateless design:

- Every stock movement creates a Stock Ledger Entry (immutable record).
- Stock balances and valuation are calculated on the fly using SQL queries.

Every time new stock is received, the valuation rate is recalculated:

```py
new_rate = (existing_qty × current_rate + incoming_qty × incoming_rate)
           ÷ (existing_qty + incoming_qty)
```

**Advantages:**

- Easier debugging and auditing
- No “stock reconciliation” nightmares
- Better performance for reports
- Simpler cancellation logic (just delete ledger entries)

This simplifies valuation, cancellation, and querying compared to the standard ERPNext approach.

### Stock Entry Types

#### Receipt

Goods arriving into a warehouse.
Increases stock.
Requires `to_warehouse` and `incoming_rate`.

#### Issue / Consume

Goods consumed or issued out.
Decreases stock.
Requires `from_warehouse`.
Uses current moving average rate.

#### Transfer

Moves stock between warehouses.
Requires both `from_warehouse` and `to_warehouse`.

### Ledger lifecycle

User creates Stock Entry → Submit → Hook fires create_ledger_entries() → SLE rows created

User cancels Stock Entry → Hook fires delete_ledger_entries() → SLE rows deleted

### Reports

#### Stock Ledger report

Line-by-line movement history per item.
Filterable by item, warehouse, and date range.
Shows qty in/out, balance qty, and valuation rate per transaction.

#### Stock Balance report

Point-in-time snapshot of stock.
Filter by date to get balance quantities and values.
Supports grouping by warehouse or item.

---

## Developer Guide

### Project Setup

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

Install as Frappe app.

```sh
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/kunnoh/x_electronics.git --branch main
bench install-app x_electronics
```

Add app to the **site**.

```sh
bench --site [yoursite] install-app x_electronics
```

Enable developer mode + server scripts.

```sh
bench --site [yoursite] set-config developer_mode 1
bench --site [yoursite] set-config enable_server_script 1
```

### Dev Loop

After modifying a **DocType**.

```sh
bench migrate           # apply schema changes
bench build             # rebuild JS assets if form changed
```

After modifying Python (hooks, controllers).

```sh
bench restart           # picks up Python changes in worker/web
```

Quick backend testing via bench execute.

```sh
bench --site xelectronics.local execute \
  xelectronics.stock_ledger.stock_ledger.get_moving_average_rate \
  --kwargs '{"item_code":"ITEM-001","warehouse":"Main Warehouse - XE"}'
```

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.

### License

mit
