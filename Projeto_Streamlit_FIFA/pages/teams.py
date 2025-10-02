import os
import streamlit as st
import pandas as pd

# ⚠️ Se já tiver set_page_config no Home.py, remova daqui
st.set_page_config(
    page_title="Teams",
    page_icon="⚽",
    layout="wide"
)

# Garante que os dados estão carregados
if "data" not in st.session_state:
    st.session_state["data"] = pd.read_csv("CLEAN_FIFA23_official_data.csv")

df_data = st.session_state["data"]

# Sidebar - seleção de clube
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

# Filtra jogadores do clube
df_club = df_data[df_data["Club"] == club].set_index("Name")

# --- ESCUDO DO CLUBE (local) ---
# Os arquivos foram salvos em images/clubs/{nome_do_clube}.png
safe_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in club)
club_logo_path = os.path.join("images", "clubs", f"{safe_name}.png")
st.write(df_club.iloc[0]["Club Logo"])  # exibe a URL do CDN


if os.path.exists(club_logo_path):
    st.image(club_logo_path, width=120)
else:
    st.write("🏳️ Escudo não disponível")

# --- INFORMAÇÕES DO CLUBE ---
st.title(club)
st.markdown(f"**Número de jogadores:** {len(df_club)}")
st.markdown(f"**Média de idade:** {df_club['Age'].mean():.1f}")
st.markdown(f"**Média de overall:** {df_club['Overall'].mean():.1f}")
st.markdown(f"**Valor total de mercado:** £ {df_club['Value(£)'].sum():,}")

st.divider()

# --- LISTA DE JOGADORES ---
columns = [
    "Age", "Photo", "Flag", "Overall", "Value(£)", "Wage(£)", "Joined",
    "Height(cm.)", "Weight(lbs.)", "Contract Valid Until", "Release Clause(£)"
]

st.subheader("Jogadores do clube")
st.dataframe(
    df_club[columns],
    column_config={
        "Overall": st.column_config.ProgressColumn(
            "Overall", format="%d", min_value=0, max_value=100
        ),
        "Wage(£)": st.column_config.ProgressColumn(
            "Weekly Wage", format="£%f",
            min_value=0, max_value=df_club["Wage(£)"].max()
        ),
        "Photo": st.column_config.ImageColumn("Player"),
        "Flag": st.column_config.ImageColumn("Country"),
    },
    use_container_width=True
)
