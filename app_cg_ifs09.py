import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="IFS-09 CG Calculator", layout="wide")

st.title("🏎️ Calculador de Centro de Gravedad - Formula Student IFS-09")
st.markdown("Herramienta interactiva para el cálculo dinámico de CG y reparto de pesos.")

# --- DATOS BASE PRECARGADOS (IFS-09) ---
if "components" not in st.session_state:
    st.session_state.components = [
        # CHASSIS
        {"Categoria": "CHASSIS", "Componente": "Chassis weight", "Masa": 34.06765, "Qty": 1, "X": 1159.0, "Y": 404.2, "Activo": True},
        {"Categoria": "CHASSIS", "Componente": "Asientos, arneses, cortafuegos", "Masa": 5.2, "Qty": 1, "X": 850.0, "Y": 300.0, "Activo": True},
        {"Categoria": "CHASSIS", "Componente": "Atenuador de impactos + placa anti-intrusión", "Masa": 2.0, "Qty": 1, "X": 2300.0, "Y": 200.0, "Activo": True},
        # ELECTRONICS
        {"Categoria": "ELECTRONICS", "Componente": "LV Battery", "Masa": 5.0, "Qty": 1, "X": 510.0, "Y": 410.0, "Activo": True},
        {"Categoria": "ELECTRONICS", "Componente": "ACU (Acumulador)", "Masa": 60.0, "Qty": 1, "X": 429.0, "Y": 219.0, "Activo": True},
        {"Categoria": "ELECTRONICS", "Componente": "DV ECU", "Masa": 1.5, "Qty": 1, "X": 510.0, "Y": 410.0, "Activo": True},
        {"Categoria": "ELECTRONICS", "Componente": "Estimate wiring", "Masa": 2.0, "Qty": 1, "X": 812.0, "Y": 300.0, "Activo": True},
        # TRACTIVE SYSTEM
        {"Categoria": "TRACTIVE SYSTEM", "Componente": "Engine weight (each)", "Masa": 3.7, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "TRACTIVE SYSTEM", "Componente": "Planetary gears (each)", "Masa": 0.38, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "TRACTIVE SYSTEM", "Componente": "Inverter module", "Masa": 1.1, "Qty": 1, "X": 510.0, "Y": 250.0, "Activo": True},
        {"Categoria": "TRACTIVE SYSTEM", "Componente": "Cárteres, Palieres y Trípodes", "Masa": 7.6, "Qty": 1, "X": 0.0, "Y": 203.2, "Activo": True},
        # BRAKES & STEERING
        {"Categoria": "BRAKES & STEERING", "Componente": "Pedals total", "Masa": 4.0, "Qty": 1, "X": 2054.5, "Y": 246.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Steering axle", "Masa": 2.0, "Qty": 1, "X": 1563.0, "Y": 340.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Steering rack", "Masa": 0.68, "Qty": 1, "X": 1563.0, "Y": 180.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Hidraulic lines", "Masa": 2.0, "Qty": 1, "X": 812.0, "Y": 100.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Hidraulic pumps", "Masa": 1.5, "Qty": 1, "X": 2054.5, "Y": 150.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Front Brake calipers (each)", "Masa": 0.5, "Qty": 2, "X": 1624.0, "Y": 203.2, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Rear Brake calipers (each)", "Masa": 0.4, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "EBS", "Masa": 2.5, "Qty": 1, "X": 1150.0, "Y": 360.0, "Activo": True},
        # WHEELS
        {"Categoria": "WHEELS", "Componente": "Rear Rubbers weight (each) & Rear Wheel rim weight (each)", "Masa": 5.67, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "WHEELS", "Componente": "Front Rubbers weight (each) & Front Wheel rim weight (each)", "Masa": 5.67, "Qty": 2, "X": 1624.0, "Y": 203.2, "Activo": True},
        {"Categoria": "WHEELS", "Componente": "Rear Rotor mass (each)", "Masa": 0.378, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "WHEELS", "Componente": "Front Rotor mass (each)", "Masa": 0.378, "Qty": 2, "X": 1624.0, "Y": 203.2, "Activo": True},
        # SUSPENSION
        {"Categoria": "SUSPENSION", "Componente": "Rear Push", "Masa": 0.125, "Qty": 2, "X": 0.0, "Y": 250.0, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Trapecio trasero 1", "Masa": 0.3, "Qty": 2, "X": 0.0, "Y": 281.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Trapecio trasero 2", "Masa": 0.3, "Qty": 2, "X": 0.0, "Y": 121.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Front Push", "Masa": 0.06, "Qty": 2, "X": 1624.0, "Y": 250.0, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Trapecio delantero 1", "Masa": 0.185, "Qty": 2, "X": 1624.0, "Y": 281.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Trapecio delantero 2", "Masa": 0.185, "Qty": 2, "X": 1624.0, "Y": 121.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Antiroll trasera", "Masa": 0.51, "Qty": 1, "X": -160.0, "Y": 341.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Antiroll delantera", "Masa": 0.17, "Qty": 1, "X": 1624.0, "Y": 530.0, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Front Steering knuckle (each)", "Masa": 0.63546, "Qty": 2, "X": 1624.0, "Y": 203.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Mangueta+Buje+Rod. Trasero (each)", "Masa": 2.7, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Buje delantero (cada uno)", "Masa": 1.0, "Qty": 2, "X": 1624.0, "Y": 203.2, "Activo": True},
        {"Categoria": "SUSPENSION", "Componente": "Front Bearings (each)", "Masa": 0.375, "Qty": 2, "X": 1624.0, "Y": 203.2, "Activo": True},
        # AERO KIT (REDISTRIBUIDO: TOTAL = 16.0 kg)
        {"Categoria": "AERO KIT", "Componente": "Front Aero Weight", "Masa": 4.5, "Qty": 1, "X": 1624.0, "Y": 210.0, "Activo": True},
        {"Categoria": "AERO KIT", "Componente": "Rear Aero Weight (PDF)", "Masa": 6.0, "Qty": 1, "X": 180.0, "Y": 715.0, "Activo": True},
        {"Categoria": "AERO KIT", "Componente": "Side Wings (each)", "Masa": 2.75, "Qty": 2, "X": 820.0, "Y": 170.0, "Activo": True},
        # COOLING 
        {"Categoria": "COOLING", "Componente": "Circuito completo", "Masa": 3.8, "Qty": 1, "X": 480.0, "Y": 230.0, "Activo": True},
        # HARDWARE
        {"Categoria": "HARDWARE", "Componente": "Tornillería general y casquillos", "Masa": 5.0, "Qty": 1, "X": 800.0, "Y": 250.0, "Activo": True}
    ]

# --- BARRA LATERAL: CONTROLES RÁPIDOS Y AÑADIR ELEMENTOS ---
st.sidebar.header("⚙️ Parámetros y Filtros")
wheelbase = st.sidebar.number_input("Distancia entre Ejes (Wheelbase) [mm]", value=1624.0, step=1.0)
tire_radius = st.sidebar.number_input("Radio de Rueda [mm]", value=203.2, step=0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("➕ Añadir Elemento Extra")
with st.sidebar.form("new_item_form"):
    new_cat = st.selectbox("Categoría", ["EXTRA", "CHASSIS", "ELECTRONICS", "TRACTIVE SYSTEM", "BRAKES & STEERING", "WHEELS", "SUSPENSION", "AERO KIT", "COOLING", "HARDWARE", "DRIVER"])
    new_name = st.text_input("Nombre Componente", "Piloto (Ejemplo)")
    new_mass = st.number_input("Masa Unitaria [kg]", value=68.0, step=0.5)
    new_qty = st.number_input("Cantidad", value=1, min_value=1)
    new_x = st.number_input("Posición X [mm]", value=1100.0, step=10.0)
    new_y = st.number_input("Posición Y [mm]", value=320.0, step=10.0)
    add_btn = st.form_submit_button("Añadir a la lista")

if add_btn:
    st.session_state.components.append({
        "Categoria": new_cat, "Componente": new_name, "Masa": new_mass, "Qty": new_qty, "X": new_x, "Y": new_y, "Activo": True
    })
    st.sidebar.success(f"¡{new_name} añadido correctamente!")

# --- TABLA DE DATOS INTERACTIVA ---
st.subheader("📋 Inventario de Componentes y Masas")
df_current = pd.DataFrame(st.session_state.components)

# Permite editar cualquier masa o posición directamente en la tabla
edited_df = st.data_editor(
    df_current,
    num_rows="dynamic",
    column_config={
        "Masa": st.column_config.NumberColumn("Masa (kg)", format="%.3f"),
        "X": st.column_config.NumberColumn("X (mm)", format="%.1f"),
        "Y": st.column_config.NumberColumn("Y (mm)", format="%.1f"),
        "Activo": st.column_config.CheckboxColumn("¿Incluir en CG?"),
    },
    use_container_width=True
)

# Recalcular valores según la tabla editada
df_active = edited_df[edited_df["Activo"]].copy()
df_active["Masa_Total"] = df_active["Masa"] * df_active["Qty"]
df_active["Momento_X"] = df_active["Masa_Total"] * df_active["X"]
df_active["Momento_Y"] = df_active["Masa_Total"] * df_active["Y"]

masa_total = df_active["Masa_Total"].sum()
cg_x = df_active["Momento_X"].sum() / masa_total if masa_total > 0 else 0.0
cg_y = df_active["Momento_Y"].sum() / masa_total if masa_total > 0 else 0.0

pct_front = (cg_x / wheelbase) * 100.0
pct_rear = 100.0 - pct_front
peso_front = masa_total * (pct_front / 100.0)
peso_rear = masa_total * (pct_rear / 100.0)

# --- TARJETAS DE RESULTADOS ---
st.markdown("---")
st.subheader("📊 Resultados del Centro de Gravedad")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Masa Total", f"{masa_total:.2f} kg")
col2.metric("Posición X_CG (desde Eje Trasero)", f"{cg_x:.2f} mm")
col3.metric("Posición Y_CG (desde Suelo)", f"{cg_y:.2f} mm")
col4.metric("Reparto (Del / Tras)", f"{pct_front:.1f}% / {pct_rear:.1f}%", f"{peso_front:.1f}kg / {peso_rear:.1f}kg")

# --- REPRESENTACIÓN GRÁFICA DEL COCHE Y CG ---
st.markdown("---")
st.subheader("📐 Representación Gráfica del Monoplaza")

fig = go.Figure()

# Dibujar componentes
cats = df_active["Categoria"].unique()
for cat in cats:
    sub_df = df_active[df_active["Categoria"] == cat]
    fig.add_trace(go.Scatter(
        x=sub_df["X"],
        y=sub_df["Y"],
        mode='markers+text',
        name=cat,
        text=sub_df["Componente"],
        textposition="top center",
        marker=dict(size=np.clip(sub_df["Masa_Total"] * 0.8, 8, 30), opacity=0.7),
        hovertemplate="<b>%{text}</b><br>Masa Total: %{marker.size} kg<br>X: %{x} mm<br>Y: %{y} mm"
    ))

# Dibujar Ruedas (Rear & Front)
fig.add_shape(type="circle", x0=-tire_radius, y0=0, x1=tire_radius, y1=2*tire_radius, line=dict(color="black", width=2, dash="dash"), fillcolor="gray", opacity=0.2)
fig.add_shape(type="circle", x0=wheelbase-tire_radius, y0=0, x1=wheelbase+tire_radius, y1=2*tire_radius, line=dict(color="black", width=2, dash="dash"), fillcolor="gray", opacity=0.2)

# Dibujar Suelo y Ejes
fig.add_shape(type="line", x0=-200, y0=0, x1=wheelbase+300, y1=0, line=dict(color="black", width=3))

# Dibujar CG destacado
fig.add_trace(go.Scatter(
    x=[cg_x], y=[cg_y],
    mode='markers+text',
    name='CENTRO DE GRAVEDAD (CG)',
    marker=dict(size=22, color='red', symbol='x', line=dict(width=3, color='black')),
    text=[f"  CG ({cg_x:.1f}, {cg_y:.1f}) mm"],
    textposition="middle right",
    textfont=dict(size=14, color="red")
))

fig.update_layout(
    title="Distribución de Masas y Posición Relativa del CG (Vista Lateral)",
    xaxis_title="Posición X desde Eje Trasero (mm)",
    yaxis_title="Altura Y desde el Suelo (mm)",
    xaxis=dict(range=[-300, wheelbase + 400]),
    yaxis=dict(range=[-50, 800]),
    height=600,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
