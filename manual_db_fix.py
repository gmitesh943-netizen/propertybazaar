import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_db():
    with connection.cursor() as cursor:
        # Create Builder table
        print("Creating properties_builder table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties_builder (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar(255) NOT NULL,
                logo varchar(100) NOT NULL,
                description text NOT NULL,
                stat1_value varchar(50) NOT NULL,
                stat1_label varchar(100) NOT NULL,
                stat2_value varchar(50) NOT NULL,
                stat2_label varchar(100) NOT NULL,
                leader_name varchar(255) NOT NULL,
                leader_designation varchar(255) NOT NULL,
                leader_image varchar(100) NOT NULL,
                created_at datetime NOT NULL
            );
        """)
        
        # Check if builder_id exists in properties_property
        cursor.execute("PRAGMA table_info(properties_property);")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'builder_id' not in columns:
            print("Adding builder_id column to properties_property...")
            cursor.execute("ALTER TABLE properties_property ADD COLUMN builder_id bigint REFERENCES properties_builder(id);")
            print("Column added successfully.")
        else:
            print("builder_id column already exists.")

if __name__ == "__main__":
    try:
        fix_db()
        print("Database fix complete.")
    except Exception as e:
        print(f"Error fixing database: {e}")
