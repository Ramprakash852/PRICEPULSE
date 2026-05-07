# PricePulse — Competitor Price Intelligence Platform

## Overview

PricePulse is an automated competitor price intelligence platform designed to help businesses monitor product pricing trends, availability, and ratings from publicly available competitor marketplaces.

The system collects raw product data through automated web scraping with retry logic and user-agent headers, cleans and standardizes the data with comprehensive quality metrics, stores it in a PostgreSQL database with historical price tracking, and exposes business-ready insights through a professionally-designed REST API and an interactive dashboard with real-time visualizations.

This project demonstrates a complete production-ready end-to-end data engineering pipeline including:

* automated data collection with resilience
* data cleaning and transformation with quality validation
* database integration with historical tracking
* professional API development with response models
* comprehensive scheduling and automation with logging
* interactive dashboard visualization with real-time analytics
* cloud-ready architecture

---

# Problem Statement

Businesses frequently need access to competitor pricing and product intelligence to:

* monitor market trends
* track pricing changes
* identify high-performing products
* improve pricing strategies
* support market research decisions

However, this data is often fragmented and unavailable in structured form.

PricePulse solves this by building an automated pipeline that continuously collects, processes, and delivers competitor product data in a usable format with historical tracking capabilities.

---

# Features

## Automated Web Scraping

* Multi-page product scraping using Playwright
* Pagination handling with retry logic (3 attempts per page)
* Graceful failure handling with detailed logging
* Missing field handling
* Realistic User-Agent headers to avoid detection
* Timestamp tracking for data lineage

---

## Data Cleaning Pipeline

* Schema validation (ensures required columns exist)
* Duplicate removal with tracking
* Price normalization
* Missing value handling
* Rating standardization
* Data quality metrics reporting
* Output in both CSV and JSON formats

---

## PostgreSQL Database Integration

* Structured product storage with unique constraints
* Persistent historical records
* ORM-based database interaction using SQLAlchemy
* **NEW: Price history tracking** - stores all price snapshots for trend analysis
* **NEW: Created timestamp** - tracks when data was recorded
* Automatic migration tools for schema updates

---

## FastAPI Backend

REST API endpoints for:

* `/health` - Health check (production best practice)
* `/products` - Retrieve all products with timestamps
* `/top-rated` - Filter products by rating
* `/search?name=query` - Full-text search functionality
* `/top-discounts` - Sort by lowest prices (configurable limit)
* `/products/{id}/price-history` - Historical price tracking and trends

**Features:**
* Pydantic response models for type safety
* Automatic Swagger documentation at `/docs`
* Query parameter validation
* Professional error handling
* Session management
* Comprehensive logging

---

## Automation

* Scheduled pipeline execution using APScheduler (every 6 hours)
* Fully automated scrape → clean → store workflow
* **NEW: Detailed pipeline logging** to `logs/pipeline.log`
* **NEW: Run history tracking** in `logs/pipeline_runs.json`
* Success/failure tracking for each component
* Automatic retry on failure with detailed error reporting

---

## Interactive Dashboard

Streamlit dashboard with:

* **Metrics Cards**: Total products, average price, highest rating, lowest price
* **Interactive Charts**: 
  - Price distribution histogram
  - Rating distribution bar chart
  - Price vs Rating scatter plot
  - Best discounts bar chart
* **Sidebar Filters**:
  - Auto-refresh interval selector
  - Minimum rating filter
  - Price range slider
  - Show/hide unavailable products toggle
* **Real-time Data**: Cached with configurable TTL
* **Detailed Tables**: All products, top-rated, best discounts
* Professional layout with visual hierarchy

---

# Tech Stack

| Layer           | Technology               |
| --------------- | ------------------------ |
| Scraping        | Playwright               |
| Data Processing | Pandas                   |
| Backend API     | FastAPI                  |
| Database        | PostgreSQL               |
| ORM             | SQLAlchemy               |
| Automation      | APScheduler              |
| Dashboard       | Streamlit + Plotly       |
| Logging         | Python logging module    |
| Deployment      | Render + Neon PostgreSQL |

---

# Project Architecture

![Architecture Diagram](app/public/Architecture.png)

```
          Playwright Scraper
         (with retry logic)
                    ↓
             Raw CSV Dataset
          (with timestamps)
                    ↓
          Data Cleaning Pipeline
      (schema validation + metrics)
                    ↓
        Cleaned CSV + JSON Data
                    ↓
              PostgreSQL DB
         (with price history)
                    ↓
         FastAPI Backend
      (with response models)
                    ↓
        Streamlit Dashboard
     (interactive + real-time)
```

---

# Project Structure

```
pricepulse/
│
├── app/
│   ├── api/
│   │   ├── main.py (API endpoints + health check)
│   │   └── schemas.py (Pydantic response models)
│   │
│   ├── scraper/
│   │   ├── scraper.py (with retry logic + logging)
│   │   └── raw_data.csv
│   │
│   ├── cleaning/
│   │   ├── clean_data.py (with quality metrics)
│   │   ├── cleaned_data.csv
│   │   └── cleaned_data.json
│   │
│   ├── database/
│   │   ├── models.py (with price history)
│   │   ├── db.py
│   │   ├── insert_data.py (with price tracking)
│   │   ├── migrate.py (schema migration tool)
│   │   └── quick_fix.py (auto-migration utility)
│   │
│   ├── scheduler/
│   │   ├── scheduler.py (with detailed logging)
│   │   ├── view_runs.py (run history viewer)
│   │   ├── start_scheduler.py (startup script)
│   │   └── README.md (scheduler documentation)
│   │
│   ├── utils/
│   │   └── logger.py (centralized logging)
│   │
│   └── dashboard/
│       └── dashboard.py (interactive + charts)
│
├── logs/
│   ├── pipeline.log (execution logs)
│   └── pipeline_runs.json (run history)
│
├── tests/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-github-repo-url>

cd pricepulse
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Playwright Browser

```bash
playwright install
```

---

# PostgreSQL Setup

## Create Database

```sql
CREATE DATABASE pricepulse;
```

---

## Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/pricepulse
```

Replace:

* `postgres` - your PostgreSQL username
* `password` - your PostgreSQL password
* `localhost:5432` - your database server (if different)

# Database Migration

If you have an existing database with an outdated schema:

```bash
python app/database/quick_fix.py
```

Choose Option 1 to auto-migrate (adds missing columns and tables without deleting data).

---

# Running the Project

---

## Step 1 — Run Scraper

```bash
python app/scraper/scraper.py
```

Output:
* `app/scraper/raw_data.csv` - Raw product data
* Console logs with retry attempts and timestamps

---

## Step 2 — Run Data Cleaning Pipeline

```bash
python app/cleaning/clean_data.py
```

Output:
* `app/cleaning/cleaned_data.csv` - Cleaned data
* `app/cleaning/cleaned_data.json` - JSON format
* Console logs with data quality metrics

---

## Step 3 — Create Database Tables

```bash
python app/database/models.py
```

This creates:
* `products` table (with created_at and unique constraints)
* `price_history` table (for historical tracking)

---

## Step 4 — Insert Data into PostgreSQL

```bash
python -m app.database.insert_data
```

Output:
* Data inserted into database
* Price snapshots recorded
* Console logs with insert summary

---

## Step 5 — Run FastAPI Backend

```bash
uvicorn app.api.main:app --reload
```

API Base URL:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Step 6 — Run Dashboard

```bash
streamlit run app/dashboard/dashboard.py
```

Dashboard URL:

```
http://localhost:8501
```

---

## Step 7 — Run Automated Scheduler

```bash
python app/scheduler/start_scheduler.py
```

Or directly:

```bash
python app/scheduler/scheduler.py
```

This automates (every 6 hours):
* Scraping
* Cleaning
* Database updates

**View run history:**

```bash
python app/scheduler/view_runs.py
```

---

# API Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Welcome message | Welcome JSON |
| `/health` | GET | Health check | Status message |
| `/products` | GET | All products | Array of ProductResponse |
| `/top-rated` | GET | Rated 4+ stars | Array of ProductResponse |
| `/search?name=query` | GET | Search by name | SearchResponse with results |
| `/top-discounts?limit=10` | GET | Lowest prices | Array of ProductResponse |
| `/products/{id}/price-history` | GET | Price trends | ProductDetailResponse |

---

## Data Cleaning Decisions

| Problem             | Solution                    |
| ------------------- | --------------------------- |
| Duplicate records   | Removed using Pandas        |
| Currency formatting | Standardized to float       |
| Missing values      | Filled with "Unknown"       |
| Rating text values  | Converted to numeric scores |
| Data freshness      | Timestamps added for tracking |
| Data quality        | Metrics logged and reported |

---

# Automation Workflow

The APScheduler service automatically every 6 hours:

1. **Runs the scraper**
   - Fetches latest product data
   - Logs with timestamps
   - Retries on failure

2. **Cleans the data**
   - Validates schema
   - Reports quality metrics
   - Outputs CSV + JSON

3. **Updates PostgreSQL**
   - Inserts new products
   - Records price changes in history
   - Logs insert summary

**Logs stored in:**
* `logs/pipeline.log` - Detailed execution logs
* `logs/pipeline_runs.json` - Structured run history

---

# Monitoring & Logging

## View Scheduler Logs

```bash
# Windows
Get-Content -Path logs/pipeline.log -Wait

# Mac/Linux
tail -f logs/pipeline.log
```

## View Run History

```bash
python app/scheduler/view_runs.py
```

Output includes:
* Recent execution timestamps
* Status of each component
* Success rate statistics
* Total runs and failures

---

# Deployment

## Backend Deployment

* Render
* Heroku
* AWS Lambda

## Database Hosting

* Neon PostgreSQL
* AWS RDS
* Azure Database for PostgreSQL

---

# Business Value

PricePulse demonstrates how businesses can:

* **Monitor competitor pricing** - Track price changes in real-time
* **Analyze market trends** - Identify patterns with historical data
* **Identify high-performing products** - Filter by rating and price
* **Automate intelligence collection** - Scheduled runs without manual intervention
* **Make data-driven decisions** - Visual dashboard with interactive analytics

---

# Production Enhancements Implemented

✅ **Scraper Improvements:**
- User-Agent headers for realism
- Comprehensive logging
- Timestamp tracking
- Retry logic (3 attempts)

✅ **Data Cleaning:**
- Schema validation
- Data quality metrics
- Dual format output (CSV + JSON)

✅ **Database:**
- Created timestamps
- Unique constraints
- Historical price tracking

✅ **API:**
- Health endpoint
- Search functionality
- Sorting/filtering
- Response models (Pydantic)
- Automatic Swagger docs

✅ **Dashboard:**
- Metrics cards
- Interactive charts
- Sidebar filters
- Auto-refresh capability

✅ **Automation:**
- Detailed pipeline logging
- Run history tracking
- Success/failure monitoring
- Migration tools

---

# Future Improvements

Potential enhancements:

* Email alerts on price drops
* AI-based price trend prediction
* Advanced analytics dashboard
* Docker containerization
* Cloud scheduler integration (AWS EventBridge, Azure Functions)
* Database backups and disaster recovery
* API rate limiting
* User authentication

---

# Challenges Faced & Solutions

| Challenge | Solution |
|-----------|----------|
| Handling pagination reliably | Implemented retry logic |
| Cleaning inconsistent data | Schema validation + quality metrics |
| Preventing duplicates | Unique constraints + deduplication |
| Automating full pipeline | APScheduler with comprehensive logging |
| Schema mismatches | Migration tools for safe updates |
| Production logging | Centralized logger with file output |

---

# Key Engineering Decisions

| Decision | Reason | Benefit |
|----------|--------|----------|
| FastAPI | Lightweight and fast | High performance API |
| PostgreSQL | Production-ready relational DB | Reliability and scalability |
| Playwright | Reliable dynamic scraping | Handles JavaScript-heavy sites |
| Streamlit | Rapid dashboard development | Quick visualization iteration |
| APScheduler | Lightweight automation | Simple deployment |
| SQLAlchemy ORM | Type-safe DB interaction | Fewer bugs, better maintainability |
| Pydantic models | Response validation | Better API documentation |
| Centralized logging | Observability | Easy debugging and monitoring |

---

# Assignment Requirements Coverage

| Requirement             | Status | Implementation |
| ----------------------- | ------ | --------------- |
| Scraper                 | ✅      | Playwright with retry logic |
| Pagination Handling     | ✅      | Automatic page iteration |
| Missing Fields Handling | ✅      | Schema validation + filling |
| Failure Handling        | ✅      | Try-catch + retry logic |
| Data Cleaning           | ✅      | Quality metrics + CSV/JSON |
| Database Storage        | ✅      | PostgreSQL with history tracking |
| Automation              | ✅      | APScheduler with logging |
| Deployment              | ✅      | Production-ready setup |
| Dynamic Interface       | ✅      | Streamlit dashboard |
| Production Quality      | ✅      | Logging, monitoring, error handling |

---

# Author

Bhukya Ramprakash

---
