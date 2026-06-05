import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connected to Supabase successfully!")
        print(f"PostgreSQL version: {version[0]}")
        print(f"Database: {connection.settings_dict['NAME']}")
        print(f"Host: {connection.settings_dict['HOST']}")
except Exception as e:
    print(f"❌ Connection failed: {e}")