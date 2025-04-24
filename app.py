import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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

# choix multiple
#event_types = df["event_type"].dropna().unique()
#selected_types = st.multiselect("Sélectionnez un ou plusieurs types d'événements :", sorted(event_types), default=["earthquake"])
#filtered_df = df[df["event_type"].isin(selected_types)]


# filtrage et agrégation
filtered_df = df[df["event_type"] == event_type]
tweet_counts = filtered_df.groupby("year").size()


# affichage du graphique
fig, ax = plt.subplots(figsize=(10, 5))
tweet_counts.plot(kind="bar", stacked=True, ax=ax)

ax.set_xlabel("Année")
ax.set_ylabel("Nombre de tweets")
ax.set_title(f"Évolution des tweets pour : {event_type}")

ax.set_xticks(range(len(tweet_counts)))
ax.set_xticklabels(tweet_counts.index, rotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()

# affichage dans Streamlit
st.pyplot(fig)





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