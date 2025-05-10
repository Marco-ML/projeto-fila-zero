from supabase import create_client, Client

# Substitua pelos seus dados reais
url = "https://wjelqoiakkyljdxupmyf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndqZWxxb2lha2t5bGpkeHVwbXlmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY5MTIyMjQsImV4cCI6MjA2MjQ4ODIyNH0.tVkJdo_6Tu2blnfgSiBdaoYM5b2635nYuaR5MzRiRGo"
supabase: Client = create_client(url, key)

# Função para buscar dados da tabela
def buscar_dados():
    response = supabase.table("alunos").select("*").execute()
    return response

print(buscar_dados())
