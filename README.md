
# TradeMind

TradeMind is a **broker-agnostic trade analytics backend** designed to automate post-trade analysis for retail traders.
The system ingests raw broker tradebooks (CSV), normalizes them, applies matching logic, and generates **objective performance metrics** such as P&L, win rate, and daily performance.

This project is intentionally **backend-first**. UI and charts will be added later.

---

## Core Goals

* Accept tradebook CSVs from **any broker**
* Normalize inconsistent broker formats into a single domain model
* Perform **FIFO trade matching**
* Persist realized trades and P&L
* Expose analytics suitable for dashboards and charting
* Help traders identify **what works and what doesn’t**

---

## Tech Stack

* **Python 3.12**
* **Django 6.0**
* **PostgreSQL**
* **Docker & Docker Compose**
* **uv** (dependency & environment management)
* **pytest + pytest-django**
* **Ruff + pre-commit**

---

## Architecture Overview

The project follows a **clean, layered backend design**:

### 1. Ingestion Layer

* Broker-specific adapters (e.g. Zerodha)
* Adapter pattern to support new brokers without changing core logic
* Strict normalization into domain DTOs

### 2. Domain Layer

* `TradeDTO` (immutable trade input)
* FIFO matching engine
* Realized trade calculation

### 3. Persistence Layer

* Raw trades stored separately
* Realized trades stored after matching
* Clear separation between input data and derived analytics

### 4. Analytics Layer

* Daily P&L aggregation
* Win / loss classification
* Performance metrics (win %, loss %, net P&L)

---

## Current Features (Implemented)

### ✅ Broker-Agnostic CSV Ingestion

* Zerodha tradebook supported
* Adapter-based normalization
* Handles inconsistent CSV formats

### ✅ FIFO Matching Engine

* Supports partial and full fills
* Generates realized trades
* Fully unit-tested

### ✅ Persistence

* `Trade` model for raw trades
* `RealizedTrade` model for matched trades
* PostgreSQL-backed

### ✅ Performance Metrics

* Daily P&L aggregation
* Winning vs losing trades
* Win percentage & loss percentage

### ✅ Test Coverage

* FIFO engine tests
* Ingestion pipeline tests
* Metrics calculation tests
* Model-level tests

All core business logic is validated using **pytest**.

---

## Local Development

### Prerequisites

* Python 3.12
* Docker & Docker Compose
* uv

### Run Locally (without Docker)

```bash
uv venv
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

---

## Docker Development

### Start Services

```bash
docker compose up -d --build
```

### Run Migrations

```bash
docker compose exec web python manage.py migrate
```

### Run Server

```bash
docker compose exec web python manage.py runserver
```

### Stop Services

```bash
docker compose down
```

---

## Testing

Run all tests locally:

```bash
uv run pytest
```

Tests cover:

* FIFO trade matching
* Ingestion pipeline
* Persistence
* Performance metrics

---

## What’s Next

### 🔜 Backend Dashboard APIs

* Aggregated metrics endpoint
* Time-series P&L data
* Symbol-level performance

### 🔜 Frontend (Later)

* Chart.js / ECharts integration
* CSV upload UI
* Interactive dashboards

### 🔜 Strategy-Level Analysis

* Pattern detection
* Risk metrics
* Mistake identification

---

## Philosophy

TradeMind is built with the belief that:

> **Correct data and correct logic matter more than fancy dashboards.**

The system is designed to be:

* Deterministic
* Testable
* Extensible
* Honest about trading performance
