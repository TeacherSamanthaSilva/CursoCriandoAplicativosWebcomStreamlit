import os
import streamlit as st
import pandas as pd
import requests

# Garante que os dados estão carregados
if "data" not in st.session_state:
    st.session_state["data"] = pd.read_csv("CLEAN_FIFA23_official_data.csv")

df_data = st.session_state["data"]

# Sidebar - seleção de clube
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtra jogadores do clube
df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

# Dados do jogador selecionado
player_stats = df_data[df_data["Name"] == player].iloc[0]

# --- FOTO LOCAL ---
player_id = str(player_stats["ID"])
photo_path = os.path.join("images", "players", f"{player_id}.png")
st.write(player_stats["Photo"])# mostra o caminho da foto

if os.path.exists(photo_path):
    st.image(photo_path, width=150, caption=player_stats["Name"])
else:
    st.write("📷 Foto não disponível")

# --- INFORMAÇÕES ---
st.title(player_stats["Name"])
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")
