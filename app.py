import streamlit as st
import folium
from streamlit_folium import st_folium
import copy

st.set_page_config(page_title="Tagoloan River Basin Hazard Map", page_icon="🌊", layout="wide")

# --- LAYOUT: TITLE AND COMPASS ---
col_title, col_compass = st.columns([5, 1])

with col_title:
    st.title("🗺️ Tagoloan River Basin — Interactive Hazard Map")
    st.caption("PAGASA / DENR-MGB Hazard Map. Use the sidebar sliders to align the shaded basin with the actual river.")

with col_compass:
    compass_html = """
    <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="position: relative; width: 110px; height: 110px; border: 2px solid #333; border-radius: 50%; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="position: absolute; top: 8px; left: 50%; transform: translateX(-50%); font-weight: bold; color: #d32f2f; font-size: 13px;">N ▲</div>
            <div style="position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); font-weight: bold; color: #333; font-size: 13px;">S ▼</div>
            <div style="position: absolute; left: 8px; top: 50%; transform: translateY(-50%); font-weight: bold; color: #333; font-size: 13px;">◀ W</div>
            <div style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); font-weight: bold; color: #333; font-size: 13px;">E ▶</div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 8px; height: 8px; background-color: #333; border-radius: 50%;"></div>
        </div>
        <div style="margin-top: 8px; font-size: 11px; text-align: center; color: #555; line-height: 1.2;">
            Shift layer:<br>
            <b>▲ North</b> | <b>▼ South</b><br>
            <b>◀ West</b> | <b>East ▶</b>
        </div>
    </div>
    """
    st.markdown(compass_html, unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR CONTROLS ---
st.sidebar.title("⚙️ Map Controls")
st.sidebar.markdown("---")
st.sidebar.subheader(" Align Map Layer")
st.sidebar.caption("Use your mouse to drag these sliders to align the shaded basin with the actual river on the base map.")

nudge_lon = st.sidebar.slider(
    "East / West (Longitude)", 
    min_value=-0.10, max_value=0.10, value=0.00, step=0.005,
    help="Drag right to move East (▶), left to move West (◀)."
)

nudge_lat = st.sidebar.slider(
    "North / South (Latitude)", 
    min_value=-0.10, max_value=0.10, value=0.00, step=0.005,
    help="Drag up to move North (▲), down to move South (▼)."
)

if st.sidebar.button("🔄 Reset Alignment"):
    nudge_lon = 0.00
    nudge_lat = 0.00

# --- GEOJSON DATA ---
geojson_data = {"type": "FeatureCollection", "features": [
{"type": "Feature", "properties": {"name": "Tagoloan River Basin", "type": "basin_boundary"}, "geometry": {"type": "Polygon", "coordinates": [[[124.690,8.622],[124.710,8.618],[124.730,8.615],[124.755,8.610],[124.775,8.605],[124.790,8.598],[124.800,8.585],[124.810,8.570],[124.815,8.552],[124.820,8.535],[124.825,8.515],[124.830,8.495],[124.835,8.475],[124.840,8.455],[124.845,8.435],[124.848,8.415],[124.850,8.395],[124.852,8.375],[124.855,8.355],[124.857,8.335],[124.858,8.315],[124.855,8.295],[124.850,8.278],[124.843,8.262],[124.835,8.248],[124.825,8.235],[124.815,8.225],[124.805,8.215],[124.793,8.207],[124.780,8.200],[124.765,8.195],[124.750,8.192],[124.735,8.190],[124.718,8.190],[124.700,8.193],[124.685,8.198],[124.670,8.205],[124.658,8.215],[124.648,8.228],[124.640,8.242],[124.635,8.258],[124.630,8.275],[124.627,8.295],[124.625,8.315],[124.623,8.335],[124.622,8.355],[124.622,8.375],[124.623,8.395],[124.625,8.415],[124.628,8.435],[124.632,8.455],[124.638,8.473],[124.645,8.490],[124.650,8.505],[124.652,8.520],[124.650,8.535],[124.645,8.548],[124.638,8.560],[124.630,8.570],[124.622,8.580],[124.618,8.590],[124.620,8.600],[124.628,8.610],[124.640,8.617],[124.655,8.621],[124.672,8.623],[124.690,8.622]]]}},
{"type": "Feature", "properties": {"name": "Flood-prone area — main river corridor", "type": "flood_prone", "hazard_level": "high", "description": "High flood susceptibility along the primary Tagoloan River channel."}, "geometry": {"type": "Polygon", "coordinates": [[[124.710,8.615],[124.718,8.608],[124.715,8.585],[124.712,8.558],[124.708,8.532],[124.706,8.505],[124.702,8.478],[124.700,8.450],[124.698,8.422],[124.696,8.395],[124.694,8.368],[124.692,8.340],[124.690,8.312],[124.688,8.285],[124.686,8.258],[124.684,8.232],[124.682,8.210],[124.676,8.205],[124.672,8.215],[124.674,8.240],[124.676,8.265],[124.678,8.292],[124.680,8.318],[124.682,8.345],[124.684,8.372],[124.686,8.400],[124.688,8.428],[124.690,8.455],[124.692,8.482],[124.696,8.508],[124.700,8.535],[124.704,8.560],[124.708,8.585],[124.710,8.615]]]}},
{"type": "Feature", "properties": {"name": "Flood-prone area — east tributary confluence", "type": "flood_prone", "hazard_level": "high", "description": "Localised flood zone along east tributary near Impasug-Ong."}, "geometry": {"type": "Polygon", "coordinates": [[[124.820,8.508],[124.832,8.500],[124.840,8.488],[124.835,8.472],[124.822,8.465],[124.808,8.470],[124.802,8.482],[124.808,8.498],[124.820,8.508]]]}},
{"type": "Feature", "properties": {"name": "Flood-prone area — lower east sub-basin", "type": "flood_prone", "hazard_level": "high", "description": "Flood-prone lowland confluence zone near Malaybalay approach."}, "geometry": {"type": "Polygon", "coordinates": [[[124.828,8.298],[124.842,8.288],[124.850,8.275],[124.845,8.260],[124.832,8.252],[124.818,8.255],[124.810,8.265],[124.815,8.280],[124.828,8.298]]]}},
{"type": "Feature", "properties": {"name": "Flood-prone area — coastal delta and estuary", "type": "flood_prone", "hazard_level": "very_high", "description": "Estuarine and coastal floodplain. Highest risk zone."}, "geometry": {"type": "Polygon", "coordinates": [[[124.670,8.215],[124.685,8.210],[124.700,8.208],[124.715,8.210],[124.720,8.205],[124.712,8.198],[124.700,8.195],[124.685,8.195],[124.672,8.198],[124.665,8.208],[124.670,8.215]]]}},
{"type": "Feature", "properties": {"name": "Landslide-prone area — basin interior", "type": "landslide_prone", "hazard_level": "high", "description": "High susceptibility to landslides across the basin interior."}, "geometry": {"type": "Polygon", "coordinates": [[[124.698,8.608],[124.718,8.612],[124.738,8.608],[124.758,8.602],[124.778,8.595],[124.795,8.585],[124.808,8.570],[124.815,8.550],[124.820,8.528],[124.822,8.505],[124.820,8.480],[124.815,8.455],[124.812,8.428],[124.814,8.400],[124.818,8.372],[124.820,8.345],[124.818,8.318],[124.812,8.292],[124.805,8.268],[124.795,8.248],[124.782,8.232],[124.768,8.220],[124.752,8.212],[124.735,8.208],[124.718,8.208],[124.702,8.212],[124.688,8.220],[124.675,8.232],[124.665,8.248],[124.658,8.265],[124.655,8.285],[124.654,8.308],[124.655,8.332],[124.658,8.355],[124.662,8.378],[124.668,8.400],[124.674,8.422],[124.678,8.445],[124.680,8.468],[124.679,8.490],[124.676,8.512],[124.672,8.532],[124.670,8.552],[124.672,8.572],[124.680,8.590],[124.690,8.604],[124.698,8.608]]]}},
{"type": "Feature", "properties": {"name": "Tagoloan River — main stem", "type": "river", "stream_order": 1}, "geometry": {"type": "LineString", "coordinates": [[124.748,8.612],[124.745,8.582],[124.748,8.555],[124.752,8.520],[124.748,8.488],[124.742,8.455],[124.738,8.420],[124.735,8.385],[124.730,8.350],[124.726,8.312],[124.722,8.278],[124.718,8.245],[124.712,8.215]]}},
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
]}

# --- NUDGE FUNCTION ---
def nudge_geojson(geojson, d_lon, d_lat):
    nudged = copy.deepcopy(geojson)
    for feature in nudged['features']:
        geom = feature['geometry']
        if geom['type'] == 'Polygon':
            for ring in geom['coordinates']:
                for i, coord in enumerate(ring):
                    ring[i] = [coord[0] + d_lon, coord[1] + d_lat]
        elif geom['type'] == 'LineString':
            for i, coord in enumerate(geom['coordinates']):
                geom['coordinates'][i] = [coord[0] + d_lon, coord[1] + d_lat]
        elif geom['type'] == 'Point':
            geom['coordinates'] = [geom['coordinates'][0] + d_lon, geom['coordinates'][1] + d_lat]
    return nudged

# Apply the interactive nudge
final_geojson = nudge_geojson(geojson_data, nudge_lon, nudge_lat)

# --- CREATE FOLIUM MAP ---
m = folium.Map(location=[8.42, 124.75], zoom_start=10, tiles='CartoDB positron')

folium.GeoJson(
    final_geojson,
    name='Hazard Zones & Rivers',
    style_function=lambda x: {
        'fillColor': '#DC143C' if x['properties'].get('hazard_level') == 'very_high' else 
                     '#FFA500' if x['properties'].get('type') == 'flood_prone' else 
                     '#8B4513' if x['properties'].get('type') == 'landslide_prone' else 
                     'transparent',
        'color': 'black',
        'weight': 1 if x['properties'].get('type') != 'basin_boundary' else 3,
        'fillOpacity': 0.5 if x['properties'].get('type') != 'basin_boundary' else 0
    },
    popup=folium.GeoJsonPopup(fields=['name'])
).add_to(m)

for feature in final_geojson["features"]:
    if feature["geometry"]["type"] == "Point":
        lat = feature["geometry"]["coordinates"][1]
        lon = feature["geometry"]["coordinates"][0]
        name = feature["properties"]["name"]
        stype = feature["properties"]["type"]
        
        if 'raingauge' in stype: color = 'blue'
        elif 'synoptic' in stype: color = 'green'
        else: color = 'red'
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            popup=folium.Popup(name, max_width=200),
            color='white',
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            weight=2
        ).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, width=1200, height=700)
