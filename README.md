# TradeMind

TradeMind is a backend-first FinTech analytics platform designed to automate **post-trade analysis** for active traders.

Unlike basic trading journals, TradeMind focuses on **correct accounting, performance diagnostics, and risk visibility** — starting from raw broker trade data.

---

## Core Philosophy

- Backend-first (correctness before UI)
- Broker-agnostic ingestion
- Deterministic analytics (no hidden frontend math)
- Test-driven development
- Docker-friendly local setup

---

## Tech Stack

- **Python** 3.12
- **Django** 6.0
- **PostgreSQL**
- **Docker & Docker Compose**
- **uv** (dependency & venv management)
- **pytest** (testing)
- **Ruff + pre-commit** (linting & formatting)

---

## Current Capabilities ✅

### Trade Ingestion
- Broker-agnostic CSV ingestion pipeline
- Adapter-based normalization layer (Zerodha implemented)
- Validated parsing with explicit error handling
- Fully test-covered ingestion flow

### Trade Accounting
- FIFO trade matching engine
  - Supports partial & full exits
  - Handles multiple buy lots
- Realized trade persistence
- Decimal-safe financial calculations (no floats)

### Analytics & Metrics
- Daily P&L aggregation
- Dashboard summary metrics:
  - Total trades
  - Win count / Loss count
  - Win % / Loss %
  - Net P&L
  - Average win / Average loss
  - Expectancy
- **Equity Curve backend API**
  - Cumulative P&L over time
  - Chronologically ordered
  - Frontend chart–ready output

### Engineering Quality
- Full unit test coverage for:
  - FIFO engine
  - Ingestion pipeline
  - Persistence layer
  - Analytics services
- Clean domain separation:
  - Models
  - DTOs
  - Services
  - Analytics engines
- Dockerized Django + PostgreSQL setup for local development

---

## API Endpoints (Current)

| Endpoint | Description |
|--------|-------------|
| `/dashboard/summary/` | High-level performance metrics |
| `/dashboard/equity-curve/` | Cumulative equity curve data |

All APIs are **read-only**, deterministic, and frontend-ready.

---

## What TradeMind Helps Answer

- Am I actually profitable or just lucky?
- How consistent is my equity growth?
- Where do I give back profits?
- Is my strategy statistically sound?
- What is my real risk profile?

---

## Roadmap (Next)

- Risk & drawdown analytics (max drawdown, profit factor, risk–reward)
- Strategy-level tagging & analytics
- Async CSV ingestion with background workers
- Frontend dashboards (Chart.js / ECharts)
- Multi-user authentication & isolation

---

## Status

🟢 **Active development**
This project is being built incrementally with production-grade practices and transparent progress updates.

---

> TradeMind is intentionally built slow and correct — because trading analytics done wrong is worse than no analytics at all.
