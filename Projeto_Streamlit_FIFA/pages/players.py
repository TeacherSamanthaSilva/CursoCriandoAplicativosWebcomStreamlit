import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

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

# --- FOTO DO JOGADOR ---
if pd.notna(player_stats["Photo"]):
    photo_url = str(player_stats["Photo"]).strip()
    st.image(photo_url, width=150)  # garante exibição
else:
    st.write("📷 Foto não disponível")

# --- INFORMAÇÕES BÁSICAS ---
st.title(player_stats["Name"])
st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100:.2f} m")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)']*0.453:.2f} kg")

st.divider()

st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Valor de mercado", value=f"£ {player_stats['Value(£)']:,}")
col2.metric(label="Remuneração semanal", value=f"£ {player_stats['Wage(£)']:,}")
col3.metric(label="Cláusula de rescisão", value=f"£ {player_stats['Release Clause(£)']:,}")
