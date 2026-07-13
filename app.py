# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------
# Configuración de la página
# -------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Vehículos",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Estilos CSS
# -------------------------------------------------
st.markdown("""
<style>
.main{
    background-color:#0f172a;
}

.block-container{
    padding-top:1rem;
}

h1{
    color:#ff4b4b;
}

h2,h3{
    color:white;
}

[data-testid="stSidebar"]{
    background:#111827;
}

div[data-testid="metric-container"]{
    background:#1e293b;
    border:1px solid #374151;
    padding:15px;
    border-radius:12px;
}

.stButton>button{
    background-color:#ef4444;
    color:white;
    border-radius:10px;
}

.stCheckbox label{
    font-size:16px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Cargar datos
# -------------------------------------------------


@st.cache_data
def cargar_datos():
    df = pd.read_csv(
        "C:\\Users\\hilary\\OneDrive\\Escritorio\\PF_7_edit\\Proyecto7_anuncios_venta_de_coches.-\\vehicles_us.csv")
    return df


car_data = cargar_datos()

# -------------------------------------------------
# Limpieza básica
# -------------------------------------------------
car_data["date_posted"] = pd.to_datetime(
    car_data["date_posted"],
    errors="coerce"
)

# -------------------------------------------------
# Título
# -------------------------------------------------
st.title("🚗🔥 Dashboard Interactivo de Venta de Vehículos")
st.header("📊 Explora, filtra y descubre tendencias del mercado automotriz")
st.markdown(
    """
Bienvenido al panel interactivo.

Utiliza los filtros del menú lateral para explorar el conjunto de datos de vehículos usados.
"""
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("⚙️ Filtros")

# Año
anios = sorted(car_data["model_year"].dropna().unique())

anio = st.sidebar.multiselect(
    "📅 Año del modelo",
    anios,
    default=anios
)

# Tipo

tipos = sorted(car_data["type"].dropna().unique())

tipo = st.sidebar.multiselect(
    "🚙 Tipo de vehículo",
    tipos,
    default=tipos
)

# Combustible

combustible = st.sidebar.multiselect(
    "⛽ Combustible",
    sorted(car_data["fuel"].dropna().unique()),
    default=sorted(car_data["fuel"].dropna().unique())
)

# Transmisión

trans = st.sidebar.multiselect(
    "⚙️ Transmisión",
    sorted(car_data["transmission"].dropna().unique()),
    default=sorted(car_data["transmission"].dropna().unique())
)

# Precio

precio = st.sidebar.slider(
    "💲 Precio",
    int(car_data["price"].min()),
    int(car_data["price"].max()),
    (
        int(car_data["price"].min()),
        int(car_data["price"].max())
    )
)

# -------------------------------------------------
# Aplicar filtros
# -------------------------------------------------
df = car_data[
    (car_data["model_year"].isin(anio)) &
    (car_data["type"].isin(tipo)) &
    (car_data["fuel"].isin(combustible)) &
    (car_data["transmission"].isin(trans)) &
    (car_data["price"].between(precio[0], precio[1]))
]

# -------------------------------------------------
# Métricas
# -------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("🚘 Vehículos", len(df))
c2.metric("💰 Precio promedio", f"${df['price'].mean():,.0f}")
c3.metric("🛣️ Odómetro promedio", f"{df['odometer'].mean():,.0f}")
c4.metric("📆 Año promedio", f"{df['model_year'].mean():.0f}")

st.divider()

# -------------------------------------------------
# Vista previa
# -------------------------------------------------
if st.checkbox("👀 Mostrar vista previa del DataFrame"):
    st.dataframe(
        df.head(10),
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# Checkbox Histograma (graph_objects)
# -------------------------------------------------
if st.checkbox("📈 Mostrar histograma (Graph Objects)"):

    st.write("### Distribución del Odómetro")

    fig = go.Figure(
        data=[
            go.Histogram(
                x=df["odometer"],
                marker_color="#ef4444"
            )
        ]
    )

    fig.update_layout(
        title="Distribución del Odómetro",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------
# Checkbox Scatter (graph_objects)
# -------------------------------------------------
if st.checkbox("🔵 Mostrar gráfico de dispersión (Graph Objects)"):

    st.write("### Relación entre Odómetro y Precio")

    fig = go.Figure(
        data=[
            go.Scatter(
                x=df["odometer"],
                y=df["price"],
                mode="markers",
                marker=dict(
                    color="#38bdf8",
                    size=8,
                    opacity=0.7
                )
            )
        ]
    )

    fig.update_layout(
        title="Relación entre Odómetro y Precio",
        template="plotly_dark",
        xaxis_title="Odómetro",
        yaxis_title="Precio"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# Plotly Express
# -------------------------------------------------

col1, col2 = st.columns(2)

# -------------------------------------------------
# Gráfico de Barras
# -------------------------------------------------
with col1:

    conteo = (
        df["type"]
        .value_counts()
        .reset_index()
    )

    conteo.columns = ["Tipo", "Cantidad"]

    fig_bar = px.bar(
        conteo,
        x="Cantidad",
        y="Tipo",
        orientation="h",
        color="Cantidad",
        color_continuous_scale="Turbo",
        title="🚙 Vehículos por Tipo"
    )

    fig_bar.update_layout(
        template="plotly_dark",
        title_x=0.5
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# -------------------------------------------------
# Pie Chart
# -------------------------------------------------
with col2:

    combustible_df = (
        df["fuel"]
        .value_counts()
        .reset_index()
    )

    combustible_df.columns = [
        "Combustible",
        "Cantidad"
    ]

    fig_pie = px.pie(
        combustible_df,
        values="Cantidad",
        names="Combustible",
        hole=.55,
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="⛽ Distribución del Combustible"
    )

    fig_pie.update_layout(
        template="plotly_dark",
        title_x=0.5
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# -------------------------------------------------
# Histograma Plotly Express
# -------------------------------------------------
fig_hist = px.histogram(
    df,
    x="price",
    nbins=40,
    color="condition",
    color_discrete_sequence=px.colors.qualitative.Bold,
    title="💰 Distribución de Precios"
)

fig_hist.update_layout(
    template="plotly_dark",
    title_x=0.5
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# -------------------------------------------------
# Scatter Plot Plotly Express
# -------------------------------------------------
fig_scatter = px.scatter(
    df,
    x="odometer",
    y="price",
    color="type",
    size="days_listed",
    hover_data=[
        "model",
        "condition",
        "fuel",
        "transmission"
    ],
    title="🚘 Precio vs Odómetro",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_scatter.update_layout(
    template="plotly_dark",
    title_x=0.5
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# -------------------------------------------------
# Box Plot adicional
# -------------------------------------------------
fig_box = px.box(
    df,
    x="condition",
    y="price",
    color="condition",
    title="📦 Precio por Condición",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_box.update_layout(
    template="plotly_dark",
    title_x=0.5
)

st.plotly_chart(
    fig_box,
    use_container_width=True
)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")

st.markdown(
    """
### 🚀 Dashboard desarrollado con

- 🐍 Python
- ⚡ Streamlit
- 📊 Plotly Express
- 📈 Plotly Graph Objects
- 🐼 Pandas

Este panel es completamente interactivo y todos los gráficos se actualizan automáticamente al modificar los filtros del menú lateral.
"""
)
