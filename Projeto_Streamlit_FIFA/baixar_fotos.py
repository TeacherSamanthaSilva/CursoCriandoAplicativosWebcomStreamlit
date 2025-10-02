import os
import pandas as pd
import requests
from tqdm import tqdm  # barra de progresso (pip install tqdm)

# Caminho do dataset
CSV_PATH = "Projeto_Streamlit_FIFA\datasets\CLEAN_FIFA23_official_data.csv"

# Pasta onde as imagens serão salvas
OUTPUT_DIR = "images/players"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Carrega o dataset
df = pd.read_csv(CSV_PATH)

# Itera sobre os IDs dos jogadores
for player_id in tqdm(df["ID"].unique(), desc="Baixando fotos"):
    player_id = str(player_id)
    url = f"https://cdn.sofifa.net/players/{player_id[:3]}/{player_id[3:]}/23_60.png"
    output_path = os.path.join(OUTPUT_DIR, f"{player_id}.png")

    # Pula se já baixado
    if os.path.exists(output_path):
        continue

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(r.content)
        else:
            print(f"❌ Erro {r.status_code} para {url}")
    except Exception as e:
        print(f"⚠️ Falha ao baixar {url}: {e}")
