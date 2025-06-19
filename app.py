
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# Title
st.title("Haraz-5 Well Log Interactive Explorer")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Haraz_5_clustered_with_Vshale_Porosity.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
depth_min = st.sidebar.slider("Min Depth", float(df['DEPTH'].min()), float(df['DEPTH'].max()), float(df['DEPTH'].min()))
depth_max = st.sidebar.slider("Max Depth", float(df['DEPTH'].min()), float(df['DEPTH'].max()), float(df['DEPTH'].max()))
selected_clusters = st.sidebar.multiselect("Select Clusters", sorted(df['Cluster'].unique()), sorted(df['Cluster'].unique()))

# Apply filters
df_filtered = df[(df['DEPTH'] >= depth_min) & (df['DEPTH'] <= depth_max)]
if selected_clusters:
    df_filtered = df_filtered[df_filtered['Cluster'].isin(selected_clusters)]

# Multi-track plot
st.subheader("Multi-track Log Visualization")
tracks = ['GR', 'RHOB', 'NPHI', 'Vshale', 'Porosity']
fig = go.Figure()
for i, track in enumerate(tracks):
    fig.add_trace(go.Scatter(x=df_filtered[track], y=df_filtered['DEPTH'], mode='lines', name=track, yaxis='y'))
fig.update_layout(height=700, yaxis=dict(autorange='reversed'), title="Log Tracks vs Depth")
st.plotly_chart(fig)

# Cluster summary stats
st.subheader("Cluster-wise Lithology Statistics")
st.write(df_filtered.groupby("Cluster")[['Porosity', 'Vshale']].describe())

# Hydrocarbon zone prediction (simplified example)
st.subheader("Hydrocarbon Zone Estimation")
hc_conditions = (df_filtered['Porosity'] > 0.15) & (df_filtered['Vshale'] < 0.4)
df_filtered['HC_Zone'] = np.where(hc_conditions, 'Hydrocarbon', 'Non-HC')
st.write(df_filtered[['DEPTH', 'Porosity', 'Vshale', 'HC_Zone']].head(10))

# Display result
st.success("Use the filters in the sidebar to explore zones of interest.")
