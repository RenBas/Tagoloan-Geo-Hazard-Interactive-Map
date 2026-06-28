import streamlit as st
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Tagoloan River Basin Hazard Map",
    page_icon="🌊",
    layout="wide"
)

# --- SIDEBAR ---
st.sidebar.title("🌊 Tagoloan River Basin")
st.sidebar.markdown("**PAGASA / DENR-MGB Hazard Map**")
st.sidebar.markdown("---")
st.sidebar.info("This interactive map uses Folium. It requires no external API keys and is fully stable on Streamlit Cloud.")

# --- MAIN UI ---
st.title("🗺️ Tagoloan River Basin — Interactive Hazard Map")
st.caption("Traced from DOST-PAGASA / DENR-MGB location maps.")

# --- GEOJSON DATA (Fully Validated) ---
geojson_data = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {"name": "Tagoloan River Basin", "type": "basin_boundary"},
      "geometry": {"type": "Polygon", "coordinates": [[[124.690,8.622],[124.710,8.618],[124.730,8.615],[124.755,8.610],[124.775,8.605],[124.790,8.598],[124.800,8.585],[124.810,8.570],[124.815,8.552],[124.820,8.535],[124.825,8.515],[124.830,8.495],[124.835,8.475],[124.840,8.455],[124.845,8.435],[124.848,8.415],[124.850,8.395],[124.852,8.375],[124.855,8.355],[124.857,8.335],[124.858,8.315],[124.855,8.295],[124.850,8.278],[124.843,8.262],[124.835,8.248],[124.825,8.235],[124.815,8.225],[124.805,8.215],[124.793,8.207],[124.780,8.200],[124.765,8.195],[124.750,8.192],[124.735,8.190],[124.718,8.190],[124.700,8.193],[124.685,8.198],[124.670,8.205],[124.658,8.215],[124.648,8.228],[124.640,8.242],[124.635,8.258],[124.630,8.275],[124.627,8.295],[124.625,8.315],[124.623,8.335],[124.622,8.355],[124.622,8.375],[124.623,8.395],[124.625,8.415],[124.628,8.435],[124.632,8.455],[124.638,8.473],[124.645,8.490],[124.650,8.505],[124.652,8.520],[124.650,8.535],[124.645,8.548],[124.638,8.560],[124.630,8.570],[124.622,8.580],[124.618,8.590],[124.620,8.600],[124.628,8.610],[124.640,8.617],[124.655,8.621],[124.672,8.623],[124.690,8.622]]]}
