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
        {"Categoria": "CHASSIS", "Componente": "Impact absorver", "Masa": 2.0, "Qty": 1, "X": 2300.0, "Y": 404.2, "Activo": True},
        # ELECTRONICS
        {"Categoria": "ELECTRONICS", "Componente": "LV Battery", "Masa": 5.0, "Qty": 1, "X": 510.0, "Y": 410.0, "Activo": True},
        {"Categoria": "ELECTRONICS", "Componente": "ACU (Acumulador)", "Masa": 60.0, "Qty": 1, "X": 429.0, "Y": 219.0, "Activo": True},
        {"Categoria": "ELECTRONICS", "Componente": "DV ECU", "Masa": 1.5, "Qty": 1, "X": 510.0, "Y": 410.0, "Activo": True},
        {"Categoria": "ELECTRONICS", "Componente": "Estimate wiring", "Masa": 2.0, "Qty": 1, "X": 812.0, "Y": 300.0, "Activo": True},
        # TRACTIVE SYSTEM
        {"Categoria": "TRACTIVE SYSTEM", "Componente": "Engine weight (each)", "Masa": 3.7, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "TRACTIVE SYSTEM", "Componente": "Planetary gears (each)", "Masa": 0.38, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "TRACTIVE SYSTEM", "Componente": "Inverter module", "Masa": 1.1, "Qty": 1, "X": 510.0, "Y": 250.0, "Activo": True},
        # BRAKES & STEERING
        {"Categoria": "BRAKES & STEERING", "Componente": "Pedals total", "Masa": 4.0, "Qty": 1, "X": 2054.5, "Y": 246.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Steering axle", "Masa": 2.0, "Qty": 1, "X": 1563.0, "Y": 340.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Steering rack", "Masa": 0.68, "Qty": 1, "X": 1563.0, "Y": 180.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Hidraulic lines", "Masa": 2.0, "Qty": 1, "X": 812.0, "Y": 100.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Hidraulic pumps", "Masa": 1.5, "Qty": 1, "X": 2054.5, "Y": 150.0, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Front Brake calipers (each)", "Masa": 0.5, "Qty": 2, "X": 1624.0, "Y": 203.2, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Rear Brake calipers (each)", "Masa": 0.4, "Qty": 2, "X": 0.0, "Y": 203.2, "Activo": True},
        {"Categoria": "BRAKES & STEERING", "Componente": "Volante", "Masa": 1.0, "Qty": 1, "X": 1150.0, "Y": 360.0, "Activo": True},
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
        {"Categoria": "SUSPENSION", "Componente": "Trapecio delantero 2", "Masa": 0.185, "Qty": 2, "X": 1624.0, "Y": 121.2, "Act
