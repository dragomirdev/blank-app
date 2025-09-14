import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import requests

st.set_page_config(page_title="UAP Sightings by Month", layout="wide")
st.title("🛸 Monthly UAP Sightings Around the World")



# Load data
df = pd.read_csv("uap_sightings_monthly.csv")

# Month selection
months = sorted(df["Month"].unique())
selected_month = st.selectbox("Select Month", months)

# Filter data by selected month
df_month = df[df["Month"] == selected_month]

# ---- Map with Red Dots ----
st.subheader(f"🌍 UAP Sightings Map - {selected_month}")
fig_map = px.scatter_geo(
    df_month,
    lat="Latitude",
    lon="Longitude",
    hover_name="Country",
    size="Sightings",
    size_max=20,
    color_discrete_sequence=["red"]
)
fig_map.update_geos(projection_type="natural earth")
st.plotly_chart(fig_map, use_container_width=True)

# ---- Bar Chart ----
st.subheader(f"📊 UAP Sightings by Country - {selected_month}")
fig_bar = px.bar(
    df_month.sort_values(by="Sightings", ascending=False),
    x="Country",
    y="Sightings",
    color="Country",
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig_bar, use_container_width=True)


# Youtube Video

st.title("USA Pentagon UAP Video 1")
st.video("https://www.youtube.com/watch?v=VUrTsrhVce4")

st.title("USA Pentagon UAP Video 2")
st.video("https://www.youtube.com/watch?v=LN22jK34usA")

st.title("USA Pentagon UAP Video 3")
st.video("https://www.youtube.com/watch?v=lWLZgnmRDs4")


st.set_page_config(page_title="Visitor Country Tracker")

st.title("🌐 Live Country Visitor Tracker")

# --- Session Setup ---
if "country_counts" not in st.session_state:
    st.session_state.country_counts = {}

# --- Geolocation Lookup ---
@st.cache_data(show_spinner=False)
def get_geo_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": data.get("ip", "Unknown"),
                "country": data.get("country", "Unknown"),
                "city": data.get("city", "Unknown")
            }
    except:
        return {"ip": "Unavailable", "country": "Unknown", "city": "Unknown"}

geo = get_geo_info()
country = geo["country"]

# --- Update Country Count ---
if country not in st.session_state.country_counts:
    st.session_state.country_counts[country] = 1
else:
    st.session_state.country_counts[country] += 1

# --- Display Visitor Info ---
st.subheader("👤 Current Visitor Info")
st.write(f"**IP Address:** `{geo['ip']}`")
st.write(f"**Country:** `{country}`")
st.write(f"**City:** `{geo['city']}`")

# --- Create Bar Chart from Country Counts ---
st.subheader("📊 Total Visits by Country (Current Session)")
df = pd.DataFrame({
    "Country": list(st.session_state.country_counts.keys()),
    "Visits": list(st.session_state.country_counts.values())
}).sort_values("Visits", ascending=False)

fig = px.bar(df, x="Country", y="Visits", color="Country", title="Country Visit Count")
st.plotly_chart(fig, use_container_width=True)

# --- Optional Raw Data View ---
with st.expander("🔍 Show Raw Data"):
    st.dataframe(df)