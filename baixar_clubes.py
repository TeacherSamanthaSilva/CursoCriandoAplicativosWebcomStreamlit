import os
import pandas as pd
import requests
from tqdm import tqdm  # pip install tqdm

# Caminho do dataset
CSV_PATH = "Projeto_Streamlit_FIFA\datasets\CLEAN_FIFA23_official_data.csv"

# Pasta onde os escudos serão salvos
OUTPUT_DIR = "images/clubs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Carrega o dataset
df = pd.read_csv(CSV_PATH)

# Alguns datasets FIFA já têm a coluna "Club Logo"
if "Club Logo" not in df.columns:
    raise ValueError("O dataset não contém a coluna 'Club Logo'.")

# Itera sobre os clubes únicos
for club, logo_url in tqdm(df[["Club", "Club Logo"]].drop_duplicates().values, desc="Baixando escudos"):
    if pd.isna(logo_url):
        continue

    # Nome do arquivo (substitui caracteres inválidos)
    safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in club)
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.png")

    # Pula se já baixado
    if os.path.exists(output_path):
        continue

    try:
        r = requests.get(logo_url, timeout=10)
        if r.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(r.content)
        else:
            print(f"❌ Erro {r.status_code} para {club}")
    except Exception as e:
        print(f"⚠️ Falha ao baixar {club}: {e}")
