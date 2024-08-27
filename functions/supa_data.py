from supabase import create_client, Client


def get_data(name):
    url="https://zilpepysnqvfkpylfumn.supabase.co"
    key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InppbHBlcHlzbnF2ZmtweWxmdW1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTcwNjA2NzAsImV4cCI6MjAzMjYzNjY3MH0.yhOVyH2Ulk2Uhnulyu8FxkKS5zYfqgy1W_vRIGkQ300"
    supabase = create_client(url, key)

    rows = supabase.table("feature").select("*").eq( "username",name).execute()

    # Assert we pulled real data.
    assert len(rows.data) > 0
    for row in rows.data:
        data = {
                'Thần số học': row['thansohoc'],
                'Sinh trắc học': row['sinhtrachoc'],
                'Nhân tướng học': row['nhantuonghoc'],
        }
    return data
    # print(data[0]['thansohoc'])