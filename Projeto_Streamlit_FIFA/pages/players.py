import streamlit as st

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

# Pega o dataframe da sessão
df_data = st.session_state["data"]

# Sidebar - filtro por clube
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Lista jogadores do clube escolhido
df_players = df_data[df_data["Club"] == club]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

# Dados do jogador selecionado
player_stats = df_data[df_data["Name"] == player].iloc[0]

# Cabeçalho com imagens
col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.image(player_stats["Photo"], caption="Jogador", width=120)
with col2:
    st.title(player_stats["Name"])
    st.markdown(f"**Clube:** {player_stats['Club']}")
    st.markdown(f"**Posição:** {player_stats['Position']}")
with col3:
    st.image(player_stats["Club Logo"], caption="Clube", width=80)
    st.image(player_stats["Flag"], caption=player_stats["Nationality"], width=50)

# Estatísticas básicas
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)']/100:.2f} m")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)']*0.453:.1f} kg")
col4.markdown(f"**Pé:** {player_stats['Preferred Foot']}")

st.divider()

# Overall com barra de progresso
st.subheader(f"Overall {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))

# Métricas financeiras
col1, col2, col3 = st.columns(3)
col1.metric(label="Valor de mercado", value=f"£ {player_stats['Value(£)']:,}")
col2.metric(label="Remuneração semanal", value=f"£ {player_stats['Wage(£)']:,}")
col3.metric(label="Cláusula de rescisão", value=f"£ {player_stats['Release Clause(£)']:,}")
