import sqlite3
import csv
import os

# FIXED PATHING: This looks up the exact folder this file is sitting in right now
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "countries_database.db")
CSV_NAME = os.path.join(BASE_DIR, "countries.csv")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 1. Rebuild Staging Tier
cursor.execute("DROP TABLE IF EXISTS staging_countries;")
cursor.execute("""
    CREATE TABLE staging_countries (
        country_name TEXT,
        capital TEXT,
        population TEXT,
        area_sq_km TEXT
    );
""")

if os.path.exists(CSV_NAME):
    with open(CSV_NAME, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO staging_countries (country_name, capital, population, area_sq_km)
                VALUES (?, ?, ?, ?);
            """, (row['country_name'], row['capital'], row['population'], row['area_sq_km']))
    print(f"✅ Ingested raw text data into staging_countries.")
else:
    print(f"❌ Error: {CSV_NAME} not found.")

# 2. Rebuild Production Tier WITH Bulletproof Trimming
cursor.execute("DROP TABLE IF EXISTS clean_countries;")
cursor.execute("""
    CREATE TABLE clean_countries AS
    SELECT 
        TRIM(country_name) AS Country,
        TRIM(capital) AS Capital,
        CAST(TRIM(population) AS INTEGER) AS Population,
        CAST(TRIM(area_sq_km) AS REAL) AS Area_Sq_KM,
        
        CASE 
            WHEN CAST(TRIM(area_sq_km) AS REAL) > 0 
            THEN ROUND(CAST(TRIM(population) AS REAL) / CAST(TRIM(area_sq_km) AS REAL), 2)
            ELSE 0 
        END AS Population_Density
    FROM staging_countries
    WHERE country_name IS NOT NULL 
      AND TRIM(country_name) != '' 
      AND TRIM(country_name) != 'None';
""")

print("🚀 Production table 'clean_countries' successfully built with custom metrics!")

conn.commit()
conn.close()
