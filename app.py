import streamlit as st
import plotly.graph_objects as go
import json

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="Tagoloan River Basin Hazard Map",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR UI ---
st.sidebar.title("🌊 Tagoloan River Basin")
st.sidebar.markdown("**PAGASA / DENR-MGB Hazard Map**")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Data Sources:**
*   **Basin Boundary:** DOST-PAGASA
*   **Flood/Landslide Prone Areas:** DENR-MGB
*   **Monitoring Stations:** PAGASA Telemetry Network

**Interactivity:**
*   **Zoom/Pan:** Use mouse or touch
*   **Hover:** Hover over zones or stations for detailed metadata.
*   **3D Tilt:** Click and drag the compass/empty space to tilt the map.
""")

# --- MAIN UI ---
st.title("🗺️ Tagoloan River Basin — Interactive 3D Hazard Map")
st.caption("Traced from DOST-PAGASA / DENR-MGB location maps. Includes basin boundary, flood/landslide-prone areas, river network, and monitoring stations.")

# --- EMBEDDED GEOJSON DATA ---
geojson_data = {
  "type": "FeatureCollection",
  "features": [
    {"type": "Feature", "properties": {"name": "Tagoloan River Basin", "type": "basin_boundary"}, "geometry": {"type": "Polygon", "coordinates": [[[124.690,8.622],[124.710,8.618],[124.730,8.615],[124.755,8.610],[124.775,8.605],[124.790,8.598],[124.800,8.585],[124.810,8.570],[124.815,8.552],[124.820,8.535],[124.825,8.515],[124.830,8.495],[124.835,8.475],[124.840,8.455],[124.845,8.435],[124.848,8.415],[124.850,8.395],[124.852,8.375],[124.855,8.355],[124.857,8.335],[124.858,8.315],[124.855,8.295],[124.850,8.278],[124.843,8.262],[124.835,8.248],[124.825,8.235],[124.815,8.225],[124.805,8.215],[124.793,8.207],[124.780,8.200],[124.765,8.195],[124.750,8.192],[124.735,8.190],[124.718,8.190],[124.700,8.193],[124.685,8.198],[124.670,8.205],[124.658,8.215],[124.648,8.228],[124.640,8.242],[124.635,8.258],[124.630,8.275],[124.627,8.295],[124.625,8.315],[124.623,8.335],[124.622,8.355],[124.622,8.375],[124.623,8.395],[124.625,8.415],[124.628,8.435],[124.632,8.455],[124.638,8.473],[124.645,8.490],[124.650,8.505],[124.652,8.520],[124.650,8.535],[124.645,8.548],[124.638,8.560],[124.630,8.570],[124.622,8.580],[124.618,8.590],[124.620,8.600],[124.628,8.610],[124.640,8.617],[124.655,8.621],[124.672,8.623],[124.690,8.622]]]}},
    {"type": "Feature", "properties": {"name": "Flood-prone area — main river corridor", "type": "flood_prone", "hazard_level": "high", "description": "High flood susceptibility along the primary Tagoloan River channel."}, "geometry": {"type": "Polygon", "coordinates": [[[124.710,8.615],[124.718,8.608],[124.715,8.585],[124.712,8.558],[124.708,8.532],[124.706,8.505],[124.702,8.478],[124.700,8.450],[124.698,8.422],[124.696,8.395],[124.694,8.368],[124.692,8.340],[124.690,8.312],[124.688,8.285],[124.686,8.258],[124.684,8.232],[124.682,8.210],[124.676,8.205],[124.672,8.215],[124.674,8.240],[124.676,8.265],[124.678,8.292],[124.680,8.318],[124.682,8.345],[124.684,8.372],[124.686,8.400],[124.688,8.428],[124.690,8.455],[124.692,8.482],[124.696,8.508],[124.700,8.535],[124.704,8.560],[124.708,8.585],[124.710,8.615]]]}},
    {"type": "Feature", "properties": {"name": "Flood-prone area — east tributary confluence", "type": "flood_prone", "hazard_level": "high", "description": "Localised flood zone along east tributary near Impasug-Ong."}, "geometry": {"type": "Polygon", "coordinates": [[[124.820,8.508],[124.832,8.500],[124.840,8.488],[124.835,8.472],[124.822,8.465],[124.808,8.470],[124.802,8.482],[124.808,8.498],[124.820,8.508]]]}},
    {"type": "Feature", "properties": {"name": "Flood-prone area — lower east sub-basin", "type": "flood_prone", "hazard_level": "high", "description": "Flood-prone lowland confluence zone near Malaybalay approach."}, "geometry": {"type": "Polygon", "coordinates": [[[124.828,8.298],[124.842,8.288],[124.850,8.275],[124.845,8.260],[124.832,8.252],[124.818,8.255],[124.810,8.265],[124.815,8.280],[124.828,8.298]]]}},
    {"type": "Feature", "properties": {"name": "Flood-prone area — coastal delta and estuary", "type": "flood_prone", "hazard_level": "very_high", "description": "Estuarine and coastal floodplain. Highest risk zone — storm surge combined with river flooding."}, "geometry": {"type": "Polygon", "coordinates": [[[124.670,8.215],[124.685,8.210],[124.700,8.208],[124.715,8.210],[124.720,8.205],[124.712,8.198],[124.700,8.195],[124.685,8.195],[124.672,8.198],[124.665,8.208],[124.670,8.215]]]}},
    {"type": "Feature", "properties": {"name": "Landslide-prone area — basin interior", "type": "landslide_prone", "hazard_level": "high", "description": "High susceptibility to landslides across the basin interior. Steep terrain and heavy rainfall."}, "geometry": {"type": "Polygon", "coordinates": [[[124.698,8.608],[124.718,8.612],[124.738,8.608],[124.758,8.602],[124.778,8.595],[124.795,8.585],[124.808,8.570],[124.815,8.550],[124.820,8.528],[124.822,8.505],[124.820,8.480],[124.815,8.455],[124.812,8.428],[124.814,8.400],[124.818,8.372],[124.820,8.345],[124.818,8.318],[124.812,8.292],[124.805,8.268],[124.795,8.248],[124.782,8.232],[124.768,8.220],[124.752,8.212],[124.735,8.208],[124.718,8.208],[124.702,8.212],[124.688,8.220],[124.675,8.232],[124.665,8.248],[124.658,8.265],[124.655,8.285],[124.654,8.308],[124.655,8.332],[124.658,8.355],[124.662,8.378],[124.668,8.400],[124.674,8.422],[124.678,8.445],[124.680,8.468],[124.679,8.490],[124.676,8.512],[124.672,8.532],[124.670,8.552],[124.672,8.572],[124.680,8.590],[124.690,8.604],[124.698,8.608]]]}},
    {"type": "Feature", "properties": {"name": "Tagoloan River — main stem", "type": "river", "stream_order": 1, "length_km": 115}, "geometry": {"type": "LineString", "coordinates": [[124.748,8.612],[124.745,8.582],[124.748,8.555],[124.752,8.520],[124.748,8.488],[124.742,8.455],[124.738,8.420],[124.735,8.385],[124.730,8.350],[124.726,8.312],[124.722,8.278],[124.718,8.245],[124.712,8.215]]}},
    {"type": "Feature", "properties": {"name": "West tributary 1", "type": "river", "stream_order": 2}, "geometry": {"type": "LineString", "coordinates": [[124.638,8.540],[124.655,8.528],[124.675,8.515],[124.698,8.505],[124.718,8.498]]}},
    {"type": "Feature", "properties": {"name": "West tributary 2", "type": "river", "stream_order": 2}, "geometry": {"type": "LineString", "coordinates": [[124.622,8.418],[124.640,8.412],[124.662,8.406],[124.688,8.400],[124.718,8.395]]}},
    {"type": "Feature", "properties": {"name": "East tributary 1", "type": "river", "stream_order": 2}, "geometry": {"type": "LineString", "coordinates": [[124.858,8.575],[124.845,8.552],[124.832,8.528],[124.818,8.505],[124.800,8.480],[124.782,8.460],[124.762,8.445],[124.748,8.438]]}},
    {"type": "Feature", "properties": {"name": "East tributary 2", "type": "river", "stream_order": 2}, "geometry": {"type": "LineString", "coordinates": [[124.855,8.445],[124.840,8.438],[124.820,8.430],[124.800,8.425],[124.780,8.420],[124.760,8.418],[124.745,8.418]]}},
    {"type": "Feature", "properties": {"name": "East tributary 3", "type": "river", "stream_order": 2}, "geometry": {"type": "LineString", "coordinates": [[124.852,8.308],[124.838,8.302],[124.818,8.295],[124.798,8.290],[124.778,8.288],[124.758,8.288],[124.742,8.290]]}},
    {"type": "Feature", "properties": {"name": "Telemetry raingauge — Brgy. San Roque", "type": "telemetry_raingauge", "operator": "PAGASA"}, "geometry": {"type": "Point", "coordinates": [124.728, 8.525]}},
    {"type": "Feature", "properties": {"name": "Telemetry raingauge — San Luis Malit-bog", "type": "telemetry_raingauge", "operator": "PAGASA"}, "geometry": {"type": "Point", "coordinates": [124.818, 8.502]}},
    {"type": "Feature", "properties": {"name": "Telemetry raingauge — Bukidnon lowlands", "type": "telemetry_raingauge", "operator": "PAGASA"}, "geometry": {"type": "Point", "coordinates": [124.758, 8.232]}},
    {"type": "Feature", "properties": {"name": "Telemetry raingauge — Malaybalay approach", "type": "telemetry_raingauge", "operator": "PAGASA"}, "geometry": {"type": "Point", "coordinates": [124.848, 8.238]}},
    {"type": "Feature", "properties": {"name": "Synoptic station — Manolo Fortich", "type": "synoptic_station", "operator": "PAGASA"}, "geometry": {"type": "Point", "coordinates": [124.720, 8.382]}},
    {"type": "Feature", "properties": {"name": "Synoptic station — Brgy. San Vicente", "type": "synoptic_station", "operator": "PAGASA"}, "geometry": {"type": "Point", "coordinates": [124.800, 8.328]}},
    {"type": "Feature", "properties": {"name": "Water level station — Tagoloan bridge", "type": "water_level_station", "operator": "PAGASA", "alert": "1.5m", "critical": "3.5m"}, "geometry": {"type": "Point", "coordinates": [124.708, 8.225]}},
    {"type": "Feature", "properties": {"name": "Water level station — mid-river", "type": "water_level_station", "operator": "PAGASA"}, "geometry": {"type": "Point", "coordinates": [124.840, 8.278]}}
  ]
}

# --- BUILD PLOTLY FIGURE ---
fig = go.Figure()

# Add Polygons
for feature in geojson_data["features"]:
    geom = feature["geometry"]
    props = feature["properties"]
    
    if geom["type"] == "Polygon":
        coords = geom["coordinates"][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        if props["type"] == "basin_boundary":
            color, opacity, line_color, line_width = "rgba(0, 0, 0, 0)", 0, "#333333", 3
        elif props["type"] == "flood_prone":
            if props["hazard_level"] == "very_high":
                color, opacity, line_color, line_width = "rgba(220, 20, 60, 0.5)", 0.5, "#8B0000", 1
            else:
                color, opacity, line_color, line_width = "rgba(255, 165, 0, 0.4)", 0.4, "#8B0000", 1
        elif props["type"] == "landslide_prone":
            color, opacity, line_color, line_width = "rgba(139, 69, 19, 0.4)", 0.4, "#8B4513", 1
            
        fig.add_trace(go.Scattermapbox(
            mode="lines", lon=lons, lat=lats, fill="toself", fillcolor=color, opacity=opacity,
            line=dict(width=line_width, color=line_color), name=props["name"],
            hovertemplate=f"<b>{props['name']}</b><br>Hazard: {props.get('hazard_level', 'N/A')}<br>{props.get('description', '')}<extra></extra>"
        ))

# Add Rivers
for feature in geojson_data["features"]:
    if feature["geometry"]["type"] == "LineString":
        coords = feature["geometry"]["coordinates"]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        props = feature["properties"]
        width = 4 if props.get("stream_order") == 1 else 2
        color = "#0000FF" if props.get("stream_order") == 1 else "#1E90FF"
        
        fig.add_trace(go.Scattermapbox(
            mode="lines", lon=lons, lat=lats, line=dict(width=width, color=color), name=props["name"],
            hovertemplate=f"<b>{props['name']}</b><br>Stream Order: {props.get('stream_order', 'N/A')}<extra></extra>"
        ))

# Add Stations
stations = {
    "telemetry_raingauge": {"color": "#00BFFF", "symbol": "circle", "size": 12, "name": "Telemetry Raingauges"},
    "synoptic_station": {"color": "#32CD32", "symbol": "square", "size": 14, "name": "Synoptic Stations"},
    "water_level_station": {"color": "#9400D3", "symbol": "diamond", "size": 16, "name": "Water Level Stations"}
}

for st_type, style in stations.items():
    lons, lats, names, hover_texts = [], [], [], []
    for feature in geojson_data["features"]:
        if feature["properties"]["type"] == st_type:
            lons.append(feature["geometry"]["coordinates"][0])
            lats.append(feature["geometry"]["coordinates"][1])
            names.append(feature["properties"]["name"])
            text = f"<b>{feature['properties']['name']}</b><br>Operator: {feature['properties'].get('operator', 'N/A')}"
            if "alert" in feature["properties"]:
                text += f"<br>⚠️ Alert: {feature['properties']['alert']} | Critical: {feature['properties']['critical']}"
            hover_texts.append(text)

    fig.add_trace(go.Scattermapbox(
        mode="markers", lon=lons, lat=lats,
        marker=dict(size=style["size"], color=style["color"], symbol=style["symbol"], line=dict(width=2, color="white")),
        name=style["name"], text=names, hovertemplate="%{customdata}<extra></extra>", customdata=hover_texts
    ))

# Mapbox Layout
fig.update_layout(
    mapbox=dict(style="open-street-map", bearing=0, pitch=45, zoom=9, center=dict(lat=8.42, lon=124.75)),
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=700,
    legend=dict(yanchor="bottom", y=0.02, xanchor="right", x=0.98, bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="#333", borderwidth=1),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
)

# --- RENDER IN STREAMLIT ---
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Data visualization generated using DOST-PAGASA and DENR-MGB tracing parameters. Built with Streamlit & Plotly.")
