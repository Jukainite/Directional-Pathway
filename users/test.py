from supabase import create_client, Client
import ast
url="https://zilpepysnqvfkpylfumn.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppbHBlcHlzbnF2ZmtweWxmdW1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwNjA2NzAsImV4cCI6MjAzMjYzNjY3MH0.yhOVyH2Ulk2Uhnulyu8FxkKS5zYfqgy1W_vRIGkQ300"
supabase = create_client(url, key)

string = "['dsp11', 'dsp12']"
voucher_ids = ast.literal_eval(string)
for voucher_id in voucher_ids:
    response =supabase.table('voucher').delete().eq('voucher_id', voucher_id).execute()

    print(response)