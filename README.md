# Restaurant Production Tracker

Streamlit app for real-time kitchen production tracking - simple, effective, production-ready.

[![Streamlit](https://img.shields.io/badge/Streamlit-Powered-brightgreen)](https://streamlit.io)

## Problem Statement

Restaurants use sophisticated software for billing, inventory, and orders. However, tracking daily food production - what each cook prepares, quantities, and timing - remains manual.

This creates blind spots:
- No visibility into kitchen output
- No historical analytics for staffing/ingredients
- Difficult to audit production across shifts

## Solution

A simple web app where:
- Cooks log production entries (restricted to their categories)
- Admins view, edit, delete entries/users, and gain insights
- Live sync - all changes reflect instantly
- Advanced analytics with charts, forecasts, heatmaps

Built for immediate real-world use - deployed and working from day one.

## Features

- Role-based login (Cook/Admin)
- Category-restricted production logging
- Admin user management (CRUD roles/categories)
- Production entries CRUD (view/edit/delete per cook or bulk)
- History & Analytics (filters, CSV export, monthly summaries)
- Advanced Analytics Dashboard
  - KPIs (total, avg/day, top item/category/cook)
  - Interactive Plotly charts (trends, stacked areas, bars, histograms, heatmaps)
  - Today/Yesterday growth, 7-day MA forecast
- Minimalist theme (professional, clean UI)
- Real-time updates, caching, smooth navigation

## Tech Stack

| Frontend | Backend | Data | Analytics |
|----------|---------|------|-----------|
| Streamlit | Python | Pandas, JSON/CSV | Plotly |

- Zero-setup deployment
- Responsive wide layout
- Cached analytics (300s TTL)

## Quick Start

1. **Clone & Install**
```bash
git clone https://github.com/maitreyeeraneee/restaurant_production_tracker.git
cd restaurant_production_tracker
pip install -r requirements.txt
```

2. **Run**
```bash
streamlit run matamaal_production.py
```

3. **Open** `http://localhost:8501`

Data persists in `users.json` & `production_data.csv`.

## Real-World Impact

- Instant deployment - solved production tracking Day 1
- Kitchen visibility - admins see exactly what cooks produce
- Actionable insights - staffing, peak hours, trends
- Scalable - multi-cook, multi-category support

## Personal Note

Built this for my father, a restaurant manager frustrated with manual production tracking. 

What started as a simple problem turned into a polished system with advanced analytics. It was genuinely fun solving something practical that works immediately in production.

## Conclusion

Small scope, big impact. A clean, intuitive tool that bridges the gap between kitchen operations and data insights.

Perfect example of targeted problem-solving - identify a gap, build the minimal effective solution, iterate to excellence.

---
Open to collaboration or similar real-world projects.


