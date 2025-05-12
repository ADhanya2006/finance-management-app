# supabase_client.py
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://pfgbsstvlwcseckewnti.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBmZ2Jzc3R2bHdjc2Vja2V3bnRpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDcwMzk1MjcsImV4cCI6MjA2MjYxNTUyN30.s6939uIOyWyp6Fs1jYwgBiBHBOqd6-Tpgirzvn-InXk")  

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
