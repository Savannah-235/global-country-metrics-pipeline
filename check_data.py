import sqlite3

DB_NAME = "countries_database.db"

# Connect to the database directly
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print("--- 🔍 CHECKING DATABASE SCHEMAS ---")

# 1. Check what tables actually exist inside this specific file
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables found inside the file: {tables}")

# 2. If clean_countries exists, try to print the top rows directly
if ('clean_countries',) in tables:
    print("\n--- 📊 CLEAN COUNTRIES TOP 5 DATA ---")
    cursor.execute("SELECT Country, Capital, Population, Population_Density FROM clean_countries LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
else:
    print("\n❌ Table 'clean_countries' does not exist in this database file instance.")

conn.close()
