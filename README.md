# parking-metrics-automation

🚗 **Parking Metrics Automation** is a cloud-based ETL pipeline designed to automate the extraction, transformation, and loading of operational and financial indicators for rotation parking facilities managed by Sagulpa. This project processes diverse documents and datasets stored in Google Cloud Storage, transforming them into consolidated metrics and KPIs loaded into BigQuery for business analytics and reporting.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Setup and Deployment](#setup-and-deployment)
- [Author](#author)

---

## Project Overview

The manual process of producing monthly reports for Sagulpa’s rotation parking was labor-intensive, error-prone, and difficult to maintain. This ETL pipeline was developed as part of a Bachelor’s Degree Final Project to:

- **Automate data ingestion** from Excel, CSV, and PDF files.
- **Process and transform** parking metrics such as occupancy, revenue, and operational data.
- **Centralize data storage** in Google BigQuery.
- **Enable reliable and timely reporting** through BI dashboards.

---

## Features

✅ Automatic download and organization of raw files from Google Cloud Storage.  
✅ Parsing of:
- Excel workbooks with multiple sheets
- PDF reports
- CSV data exports

✅ Calculation of:
- Occupancy levels by hour and day type (weekday, weekend)
- Financial metrics (revenues, operations) for multiple parking facilities
- Advanced KPIs such as rotation indices, occupancy indices, average stay times, revenue per space, etc.

✅ Loading of all metrics into Google BigQuery for further analysis and dashboarding.

✅ Cloud-native solution supporting scalability, security, and automation.

---

## Architecture

The pipeline follows these key steps:

1. **Router process:**
   - Scans the GCS inbox folder for new files.
   - Classifies files and moves them to specific folders in the data lake.
   - Deletes previous versions of documents where needed.

2. **Processes:**
   - Each process extracts metrics from one or more data sources:
     - Financial reports
     - Occupancy logs
     - Filtered reports
     - Abonados and Rotación (subscriptions vs rotation data)
     - Specialized reports like Rincón statistics

3. **Aggregation:**
   - All events collected from the different processes are merged into a single list of metric events.

4. **Loading:**
   - Events are inserted into a BigQuery table (`events`).

5. **Dashboarding:**
   - Metrics can be consumed by BI tools (e.g. Looker Studio, Power BI, etc.) for visualization.

---

## Technologies Used

- **Python 3.9+**
- Google Cloud Platform:
  - Google Cloud Storage
  - Google BigQuery
- pandas for data processing
- openpyxl for Excel manipulations
- PyPDF2 for PDF parsing

---

## Project Structure

```

parking-metrics-automation/
│
├── main.py                 # Pipeline entrypoint
├── current\_month.py        # Calculates current and previous periods
├── router.py               # GCS router process for file organization
│
├── gcp/
│   ├── paths.py            # GCP paths and BigQuery table references
│   └── utils.py            # Utilities for reading files, GCS, BigQuery
│
├── processes/
│   ├── abonados\_en\_banco.py
│   ├── abonados\_lpa\_y\_qr.py
│   ├── abonados\_y\_rotacion.py
│   ├── informes\_filtrados.py
│   ├── recaudacion.py
│   ├── rincon\_estadisticas.py
│   ├── ocupacion.py
│   └── ratios.py
│
└── README.md

````

---

## How It Works

The pipeline is executed by running:

```python
from main import entry_point

entry_point(request)
````

Or, if deploying as a Cloud Function:

```bash
gcloud functions deploy parking-metrics-automation \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point entry_point
```

### Flow:

* The **router** script scans the inbox in GCS and moves files to proper destinations.
* Each module under `processes/` reads specific files:

  * e.g. financial Excel files, occupancy CSVs, filtered PDF reports.
* Metrics are extracted as lists of “events” in the format:

  ```python
  [parking_id, {"metric_name": metric_value}]
  ```
* The **ratios.py** process calculates additional derived KPIs.
* All metrics are loaded into BigQuery as rows in the `events` table.

---

## Setup and Deployment

### Prerequisites

* Python 3.9+
* Google Cloud SDK installed and authenticated
* BigQuery dataset and tables created
* GCS buckets set up:

  * inbox
  * datalake folders for documents

### Install dependencies

```bash
pip install -r requirements.txt
```

*(Create the `requirements.txt` as needed. Libraries include pandas, google-cloud-storage, google-cloud-bigquery, openpyxl, PyPDF2, etc.)*

### Environment

Set environment variables or adjust `paths.py`:

* `PROJECT_ID`
* Bucket names
* Dataset/table names

---

## Author

👤 **Pablo Medina Sosa**
Bachelor’s Degree in Data Science and Engineering
University of Las Palmas de Gran Canaria

---

*This repository is part of the Bachelor’s Thesis titled:
“Design and Implementation of a Big Data Architecture in the Cloud for the Processing of Management Indicators of Rotation Parking Lots at Sagulpa.”*
