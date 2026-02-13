
from database.db_connection import get_db_connection

def inspect_db():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database.")
        return

    cur = conn.cursor()
    
    # Test Dashboard Query
    print("\n--- Dashboard Recent Activity (UNION Query) ---")
    try:
        query = """
            SELECT id, 'Image' as type, pollution_level as result, datetime FROM image_results
            UNION ALL
            SELECT id, 'Report' as type, issue_type as result, datetime FROM report_results
            UNION ALL
            SELECT id, 'AQI' as type, CAST(predicted_aqi AS TEXT) as result, datetime FROM aqi_results
            ORDER BY datetime DESC LIMIT 10
        """
        cur.execute(query)
        rows = cur.fetchall()
        if not rows:
            print("No data found.")
        else:
            print(f"Found {len(rows)} rows:")
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Error executing dashboard query: {e}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    inspect_db()
