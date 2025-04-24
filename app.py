import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.title("Évolution des tweets par type d'événement")

# chargement des fichiers CSV
@st.cache_data

def load_data():
    is_about_df = pd.read_csv("is_about_clean.csv")
    event_df = pd.read_csv("Event_clean.csv")
    tweet_df = pd.read_csv("Tweet_clean.csv")

    # nettoyage des types
    is_about_df["event_id"] = pd.to_numeric(is_about_df["event_id"], errors="coerce")
    event_df["node_id"] = pd.to_numeric(event_df["node_id"], errors="coerce")
    is_about_df["tweet_id"] = pd.to_numeric(is_about_df["tweet_id"], errors="coerce")
    tweet_df["tweet_id"] = pd.to_numeric(tweet_df["tweet_id"], errors="coerce")

    # renommage pour fusion
    event_df = event_df.rename(columns={"event_id": "real_event_id", "node_id": "event_id"})

    # fusions
    merged_df = is_about_df.merge(event_df, on="event_id", how="left")
    merged_df = merged_df.merge(tweet_df, on="tweet_id", how="left")

    # conversion de date
    merged_df["created_at"] = pd.to_datetime(merged_df["created_at"], errors="coerce")
    merged_df["year"] = merged_df["created_at"].dt.year

    return merged_df

df = load_data()







# liste des types d’événements disponibles
event_types = df["event_type"].dropna().unique()
event_type = st.selectbox("Choisissez un type d'événement :", sorted(event_types))


# filtrage et agrégation
filtered_df = df[df["event_type"] == event_type]
#tweet_counts = filtered_df.groupby("year").size()


# affichage google colab
#fig, ax = plt.subplots(figsize=(10, 5))
#tweet_counts.plot(kind="bar", stacked=True, ax=ax)

#ax.set_xlabel("Année")
#ax.set_ylabel("Nombre de tweets")
#ax.set_title(f"Évolution des tweets pour : {event_type}")

#ax.set_xticks(range(len(tweet_counts)))
#ax.set_xticklabels(tweet_counts.index, rotation=45)
#ax.grid(axis="y", linestyle="--", alpha=0.7)

#plt.tight_layout()

# affichage dans Streamlit
#st.pyplot(fig)





# plotly

# filtrage et agrégation
tweet_counts_df = filtered_df.groupby("year").size().reset_index(name="tweet_count")
tweet_counts_df["event_type"] = event_type  # ajoute la colonne event_type pour l'affichage


fig = px.bar(
    tweet_counts_df,
    x="year",
    y="tweet_count",
    color="event_type",
    barmode="group",
    labels={"year": "Année", "tweet_count": "Nombre de tweets", "event_type": "Type d'événement"},
    title="Nombre de tweets par année et type d'événement",
    template="plotly_white"
)

#fig.update_layout(xaxis_tickangle=-45)

fig.update_traces(marker_color='skyblue', hovertemplate='%{y} tweets en %{x}')
fig.update_layout(dragmode='pan', hovermode='x unified')


st.plotly_chart(fig, use_container_width=True)






# Calcul du nombre de tweets par type d'événement et par année
tweet_counts = df.groupby(["event_type", "year"]).size().unstack(fill_value=0)

# Création de traces empilées pour chaque type d'événement
fig = go.Figure()

for event_type in tweet_counts.index:
    fig.add_trace(go.Bar(
        x=tweet_counts.columns,
        y=tweet_counts.loc[event_type],
        name=event_type,
        hovertemplate="Année : %{x}<br>Nombre de tweets : %{y}<extra></extra>"
    ))

# Mise à jour de la mise en page pour un affichage interactif
fig.update_layout(
    barmode="stack",  # Barres empilées
    title="Évolution des tweets par type d'événement",
    xaxis_title="Année",
    yaxis_title="Nombre de tweets",
    xaxis_tickangle=-45,
    template="plotly_white",  # Thème plus épuré
    hovermode="x unified",  # Afficher les infos pour toutes les barres de la même année
    legend_title="Type d'événement",
    legend=dict(x=1.05, y=1),  # Déplace la légende en dehors du graphique
    margin=dict(r=50, t=50, b=50, l=50)  # Ajoute de l'espace pour la légende
)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig, use_container_width=True)







# Calcul du nombre de tweets par type d'événement et par année
tweet_counts = df.groupby(["event_type", "year"]).size().reset_index(name='tweet_count')

# Création d'un tableau pivot
pivot_df = tweet_counts.pivot_table(index='year', columns='event_type', values='tweet_count', aggfunc='sum', fill_value=0)

# Création de la figure avec Plotly
fig = go.Figure()

# Ajouter une ligne pour chaque type d'événement
for event_type in pivot_df.columns:
    fig.add_trace(go.Scatter(
        x=pivot_df.index,
        y=pivot_df[event_type],
        mode='lines+markers',  # 'lines+markers' pour lignes et points
        name=event_type,
        hovertemplate="Année : %{x}<br>Nombre de tweets : %{y}<extra></extra>"
    ))

# Mise à jour de la mise en page pour un affichage interactif
fig.update_layout(
    title="Évolution des tweets par type d'événement",
    xaxis_title="Année",
    yaxis_title="Nombre de tweets",
    xaxis_tickangle=-45,
    template="plotly_white",  # Thème plus épuré
    hovermode="x unified",  # Afficher les infos pour toutes les lignes de la même année
    legend_title="Type d'événement",
    legend=dict(x=1.05, y=1),  # Déplace la légende en dehors du graphique
    margin=dict(r=50, t=50, b=50, l=50),  # Ajoute de l'espace pour la légende
    showlegend=True
)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig, use_container_width=True)