# Web Scraping & Relational SQL Pipeline: Global Country Metrics

A production-grade ELT (Extract, Load, Transform) data engineering pipeline built to scrape, clean, and normalise global country demographics from an unformatted web sandbox into a structured relational database tier optimized for downstream business intelligence analytics within Power BI.

---

## 📈 Pipeline Architecture

The data travels through a robust two-tier structural staging and optimization architecture:

```text
  Live Website (HTML) 
         │
         ▼  [ Scrapy Asynchronous Engine ]
   countries.csv (Raw Text Staging File)
         │
         ▼  [ Python sqlite3 Absolute Path Ingestion ]
   staging_countries (SQL Raw String Table)
         │
         ▼  [ SQL Transform: TRIM, CAST, Defensive Case-Guard Math ]
   clean_countries (Normalized Production Table)
         │
         ▼  
   countries_database.db ➔ Imported into Power BI for Map Analytics
```

---

## 🛠️ Data Engineering Core Phases

### Phase 1: Web Scraping & Ingestion
The asynchronous scraper (`country_spider.py`) bypasses root-domain structural redirects by targeting exact directory routes.
* **Target Isolation:** Uses Scrapy's structural document parsing tree to loop across independent `div.country` layout grids.
* **Nested Node Resolution:** Utilises advanced spacing text selectors (`h3.country-name ::text`) to exhaustively capture loose string content alongside nested elements (such as flag icon sub-tags) without dropping character values.

### Phase 2: Relational SQL Ingestion & Staging
A database connector script (`sql_stage.py`) links directly into a transactional SQLite instance. To guarantee pipeline reproducibility across varying system paths, the runtime environment dynamically computes absolute folder directories via Python's `os` library.
1. **Staging Tier (`staging_countries`):** An append-safe repository that isolates raw, variable text fields directly from the CSV stream.
2. **Production Tier (`clean_countries`):** An optimized analytical table generated via schema transformations.

### Phase 3: Data Cleansing & Metric Engineering
The production layer executes targeted SQL transformations to scrub out raw layout imperfections before presentation:
* **Structural Type Casting:** Employs `CAST(TRIM(population) AS INTEGER)` and `CAST(TRIM(area_sq_km) AS REAL)` to force flat text blocks into queryable mathematical datatypes.
* **Calculated Metric Engineering:** Computes a custom **Population Density** metric, embedding a conditional `CASE` block logic to protect the database engine from division-by-zero application crashes:
  ```sql
  CASE 
      WHEN CAST(TRIM(area_sq_km) AS REAL) > 0 
      THEN ROUND(CAST(TRIM(population) AS REAL) / CAST(TRIM(area_sq_km) AS REAL), 2)
      ELSE 0 
  END AS Population_Density
  ```
* **Validation Guardrails:** Filters out empty, corrupt, or missing web entries natively using a `WHERE country_name IS NOT NULL` validation loop.

---

## 🚀 Execution & Verification Instructions

### 1. Initialize Project Dependencies
Ensure all matching runtime framework components are established locally:
```bash
pip3 install -r requirements.txt
```

### 2. Execute Web Crawling Engine
Extract the live records directly into a localized raw staging file (overwriting outdated files via the capital `-O` flag):
```bash
python3 -m scrapy runspider country_spider.py -O countries.csv
```

### 3. Run the SQL Pipeline Engine
Ingest raw records, run type modifications, and compile calculated columns into the database:
```bash
python3 sql_stage.py
```

### 4. Direct Terminal Verification
Log into the server file directly from the command prompt to execute immediate diagnostics:
```bash
sqlite3 countries_database.db
```
```sql
.mode table
.headers on
SELECT Country, Capital, Population, Area_Sq_KM, Population_Density FROM clean_countries LIMIT 5;
```
