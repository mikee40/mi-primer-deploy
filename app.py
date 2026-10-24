import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="Dashboard Gourmet Insight",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARGA DE DATOS OPTIMIZADA
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Asegurar formato de fecha para análisis temporales si se requiere
        if 'Fecha_Hora' in df.columns:
            df['Fecha_Hora'] = pd.to_datetime(df['Fecha_Hora'])
        return df
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo en la ruta especificada: '{file_path}'")
        st.stop()

df = load_data("data/datos.csv")

# 3. ENCABEZADO LLAMATIVO Y EMOCIONANTE
st.title("☕ Espresso & Data Analytics Dashboard")
st.subheader("Transformando granos de café en insights interactivos y alta rentabilidad ✨")
st.markdown("---")

# 4. BARRA LATERAL (SIDEBAR) - FILTROS INTERACTIVOS
st.sidebar.header("🎯 Filtros de Segmentación")

# Filtro Dropdown (Multiselect) - Producto
productos_disponibles = sorted(df['Producto'].unique())
productos_seleccionados = st.sidebar.multiselect(
    "Selecciona los Productos:",
    options=productos_disponibles,
    default=productos_disponibles
)

# Filtro Checkbox - Canal de Venta
canales_disponibles = df['Canal_Venta'].unique()
st.sidebar.markdown("**Canales de Venta:**")
canales_seleccionados = []
for canal in canales_disponibles:
    if st.sidebar.checkbox(canal, value=True, key=f"chk_{canal}"):
        canales_seleccionados.append(canal)

# Aplicación estricta de filtros sobre el DataFrame original
df_filtrado = df[
    (df['Producto'].isin(productos_seleccionados)) & 
    (df['Canal_Venta'].isin(canales_seleccionados))
]

# 5. VISTA PREVIA INTERACTIVA DEL DATAFRAME
if st.checkbox("🔍 Mostrar vista previa de los datos filtrados", value=False):
    st.markdown("### 📊 Muestra de Transacciones Activas")
    # Mostramos las primeras 8 filas de manera interactiva
    st.dataframe(df_filtrado.head(8), use_container_width=True)
    st.caption(f"Mostrando 8 de {len(df_filtrado)} filas que coinciden con los criterios de filtrado.")

# 6. MÉTRICAS CLAVE (KPIs rápidos para contexto del dashboard)
st.markdown("### 📈 Rendimiento General")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Ventas Totales", f"${df_filtrado['Total_Ventas'].sum():,.2f}")
with kpi2:
    st.metric("Margen Neto Promedio", f"${df_filtrado['Ganancia_Neta'].mean():,.2f}")
with kpi3:
    st.metric("Satisfacción Promedio", f"⭐ {df_filtrado['Satisfaccion_Cliente'].mean():,.2f} / 5.0")

st.markdown("---")

# 7. SECCIÓN DE GRÁFICOS ALTAMENTE INTERACTIVOS (PLOTLY EXPRESS)
# Distribución en columnas para balancear el peso visual
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Top Productos por Ingresos Generados")
    # Gráfico 1: Barras horizontales
    fig_barras = px.bar(
        df_filtrado.groupby('Producto', as_index=False)['Total_Ventas'].sum().sort_values(by='Total_Ventas'),
        x='Total_Ventas',
        y='Producto',
        orientation='h',
        labels={'Total_Ventas': 'Ingresos ($)', 'Producto': 'Categoría'},
        color='Total_Ventas',
        color_continuous_scale='YlOrBr', # Paleta de colores cálidos estilo café
        template='plotly_white'
    )
    fig_barras.update_layout(showlegend=False, margin=dict(l=20, r=20, t=10, b=20))
    st.plotly_chart(fig_barras, use_container_width=True)

with col2:
    st.markdown("#### 💳 Preferencia de Métodos de Pago")
    # Gráfico 2: Circular (Donut Chart)
    fig_donut = px.pie(
        df_filtrado,
        names='Metodo_Pago',
        values='Total_Ventas',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.YlOrBr_r,
        template='plotly_white'
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    fig_donut.update_layout(margin=dict(l=20, r=20, t=10, b=20))
    st.plotly_chart(fig_donut, use_container_width=True)

# Fila inferior para un gráfico extendido
st.markdown("#### 📉 Distribución de la Satisfacción del Cliente")
# Gráfico 3: Histograma
fig_hist = px.histogram(
    df_filtrado,
    x='Satisfaccion_Cliente',
    nbins=15,
    labels={'Satisfaccion_Cliente': 'Puntaje de Satisfacción (1-5)', 'count': 'Número de Clientes'},
    color_discrete_sequence=['#8B4513'], # Tono café premium uniforme
    marginal='box', # Agrega un diagrama de caja superior para análisis estadístico completo
    template='plotly_white'
)
fig_hist.update_layout(bargap=0.05, margin=dict(l=20, r=20, t=10, b=20))
st.plotly_chart(fig_hist, use_container_width=True)
