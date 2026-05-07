# PricePulse — Competitor Price Intelligence Platform

## Overview

PricePulse is an automated competitor price intelligence platform designed to help businesses monitor product pricing trends, availability, and ratings from publicly available competitor marketplaces.

The system collects raw product data through automated web scraping, cleans and standardizes the data, stores it in a PostgreSQL database, and exposes business-ready insights through REST APIs and an interactive dashboard.

This project demonstrates a complete end-to-end data engineering pipeline including:

* automated data collection
* data cleaning and transformation
* database integration
* API development
* scheduling and automation
* dashboard visualization
* cloud deployment

---

# Problem Statement

Businesses frequently need access to competitor pricing and product intelligence to:

* monitor market trends
* track pricing changes
* identify high-performing products
* improve pricing strategies
* support market research decisions

However, this data is often fragmented and unavailable in structured form.

PricePulse solves this by building an automated pipeline that continuously collects, processes, and delivers competitor product data in a usable format.

---

# Features

## Automated Web Scraping

* Multi-page product scraping using Playwright
* Pagination handling
* Graceful failure handling
* Missing field handling

---

## Data Cleaning Pipeline

* Duplicate removal
* Price normalization
* Missing value handling
* Rating standardization

---

## PostgreSQL Database Integration

* Structured product storage
* Persistent historical records
* ORM-based database interaction using SQLAlchemy

---

## FastAPI Backend

REST API endpoints for:

* product retrieval
* top-rated products
* business insights

---

## Automation

* Scheduled pipeline execution using APScheduler
* Fully automated scrape → clean → store workflow

---

## Interactive Dashboard

Streamlit dashboard for:

* product visualization
* search/filtering
* pricing insights
* rating analysis

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
| Dashboard       | Streamlit                |
| Deployment      | Render + Neon PostgreSQL |

---

# Project Architecture

```
          Playwright Scraper
                    ↓
             Raw CSV Dataset
                    ↓
          Data Cleaning Pipeline
                    ↓
             Cleaned CSV Data
                    ↓
              PostgreSQL DB
                    ↓
              FastAPI Backend
                    ↓
           Streamlit Dashboard
```

---

# Project Structure

```
pricepulse/
│
├── app/
│   ├── api/
│   │   └── main.py
│   │
│   ├── scraper/
│   │   ├── scraper.py
│   │   └── raw_data.csv
│   │
│   ├── cleaning/
│   │   ├── clean_data.py
│   │   └── cleaned_data.csv
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── models.py
│   │   └── insert_data.py
│   │
│   ├── scheduler/
│   │   └── scheduler.py
│   │
│   └── dashboard/
│       └── dashboard.py
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

* username
* password

with your PostgreSQL credentials.

---

# Running the Project

---

## Step 1 — Run Scraper

```bash
python app/scraper/scraper.py
```

---

## Step 2 — Run Data Cleaning Pipeline

```bash
python app/cleaning/clean_data.py
```

---

## Step 3 — Create Database Tables

```bash
python app/database/models.py
```

---

## Step 4 — Insert Data into PostgreSQL

```bash
python -m app.database.insert_data
```

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
python app/scheduler/scheduler.py
```

This automates:

* scraping
* cleaning
* database updates

---

# API Endpoints

| Endpoint     | Description                    |
| ------------ | ------------------------------ |
| `/`          | Health check                   |
| `/products`  | Retrieve all products          |
| `/top-rated` | Retrieve highly rated products |

---

# Data Cleaning Decisions

| Problem             | Solution                    |
| ------------------- | --------------------------- |
| Duplicate records   | Removed using Pandas        |
| Currency formatting | Standardized to float       |
| Missing values      | Filled with placeholders    |
| Rating text values  | Converted to numeric scores |

---

# Automation Workflow

The APScheduler service automatically:

1. runs the scraper
2. cleans raw data
3. updates PostgreSQL database

This ensures the system remains continuously updated without manual intervention.

---

# Deployment

## Backend Deployment

* Render

## Database Hosting

* Neon PostgreSQL

---

# Business Value

PricePulse demonstrates how businesses can:

* monitor competitor pricing
* analyze market trends
* identify high-performing products
* automate competitor intelligence collection

---

# Future Improvements

Potential future enhancements:

* historical price tracking
* email alerts for price drops
* AI-based price trend prediction
* advanced analytics dashboard
* Docker containerization
* cloud scheduler integration

---

# Challenges Faced

* Handling pagination reliably
* Cleaning inconsistent scraped data
* Preventing duplicate database entries
* Automating the full pipeline
* Ensuring deployment compatibility

---

# Key Engineering Decisions

| Decision    | Reason                               |
| ----------- | ------------------------------------ |
| FastAPI     | Lightweight and fast backend         |
| PostgreSQL  | Production-ready relational database |
| Playwright  | Reliable dynamic scraping            |
| Streamlit   | Rapid dashboard development          |
| APScheduler | Lightweight automation solution      |

---

# Assignment Requirements Coverage

| Requirement             | Status |
| ----------------------- | ------ |
| Scraper                 | ✅      |
| Pagination Handling     | ✅      |
| Missing Fields Handling | ✅      |
| Failure Handling        | ✅      |
| Data Cleaning           | ✅      |
| Database Storage        | ✅      |
| Automation              | ✅      |
| Deployment              | ✅      |
| Dynamic Interface       | ✅      |

---

# Author

Bhukya Ramprakash

---

# License

This project was developed as part of a Data Engineering Internship assignment for educational and evaluation purposes.
