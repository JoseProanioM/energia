import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
@st.cache_data
def load_data():
    # Replace with the path to your dataset
    data = pd.read_csv("https://raw.githubusercontent.com/JoseProanioM/energia/refs/heads/main/data/predicci%C3%B3n_energ%C3%ADa.csv", parse_dates=["Periodo"])
    return data

# Load data
df_extended = load_data()

# Streamlit App Layout
st.title("Predicción de Oferta y Demanda de Energía")

# Year slicer
min_year = df_extended['Periodo'].dt.year.min()
max_year = df_extended['Periodo'].dt.year.max()
selected_years = st.slider(
    "Selecciona el Rango de Años", 
    min_value=min_year, 
    max_value=max_year, 
    value=(min_year, max_year)
)

# Filter data based on selected years
df_filtered = df_extended[
    (df_extended['Periodo'].dt.year >= selected_years[0]) & 
    (df_extended['Periodo'].dt.year <= selected_years[1])
]

# Dropdown filter for prediction type
prediction_options = ["ARIMA", "Random Walk", "VAR", "Combinada"]
selected_prediction = st.selectbox("Select Prediction Type:", prediction_options)

# Plotting function
def plot_predictions(df, prediction_type):
    fig = go.Figure()

    # Original data for Demand
    fig.add_trace(go.Scatter(
        x=df['Periodo'], 
        y=df['demanda'], 
        mode='lines', 
        name='Serie Original - Demanda', 
        line=dict(color='#002A5C')
    ))

    # Original data for Production
    fig.add_trace(go.Scatter(
        x=df['Periodo'], 
        y=df['producción'], 
        mode='lines', 
        name='Serie Original - Oferta', 
        line=dict(color='#017DC3')
    ))

    # Add prediction traces based on selected type
    if prediction_type == "ARIMA":
        # Demand ARIMA Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['ARIMA_Demanda'], 
            mode='lines', 
            name='ARIMA - Demanda', 
            line=dict(color='green', dash='dash')
        ))
        
        # Confidence Interval for Demand
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['ARIMA_Demanda_Upper80'].tolist() + df['ARIMA_Demanda_Lower80'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(0, 255, 0, 0.2)',
            line=dict(color='rgba(0, 255, 0, 0)'),
            name='CI - 80%'
        ))
        
        # Production ARIMA Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['ARIMA_Produccion'], 
            mode='lines', 
            name='ARIMA - Producción', 
            line=dict(color='red', dash='dash')
        ))
        
        # Confidence Interval for Production
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['ARIMA_Produccion_Upper80'].tolist() + df['ARIMA_Produccion_Lower80'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.2)',
            line=dict(color='rgba(255, 0, 0, 0)'),
            name='CI - 80%'
        ))

    elif prediction_type == "Random Walk":
        # Demand Random Walk Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['RW_Demanda'], 
            mode='lines', 
            name='RW - Demanda', 
            line=dict(color='purple', dash='dot')
        ))
        
        # Confidence Interval for Demand
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['RW_Demanda_Upper80'].tolist() + df['RW_Demanda_Lower80'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(128, 0, 128, 0.2)',
            line=dict(color='rgba(128, 0, 128, 0)'),
            name='CI - 80%'
        ))
        
        # Production Random Walk Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['RW_Produccion'], 
            mode='lines', 
            name='RW - Producción', 
            line=dict(color='orange', dash='dot')
        ))
        
        # Confidence Interval for Production
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['RW_Produccion_Upper80'].tolist() + df['RW_Produccion_Lower80'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(255, 165, 0, 0.2)',
            line=dict(color='rgba(255, 165, 0, 0)'),
            name='CI - 80%'
        ))

    elif prediction_type == "VAR":
        # Demand VAR Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['VAR_Demanda'], 
            mode='lines', 
            name='VAR - Demanda', 
            line=dict(color='brown', dash='dashdot')
        ))
        
        # Confidence Interval for Demand
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['VAR_Demanda_Upper80'].tolist() + df['VAR_Demanda_Lower80'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(165, 42, 42, 0.2)',
            line=dict(color='rgba(165, 42, 42, 0)'),
            name='CI - 80%'
        ))
        
        # Production VAR Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['VAR_Produccion'], 
            mode='lines', 
            name='VAR - Producción', 
            line=dict(color='pink', dash='dashdot')
        ))
        
        # Confidence Interval for Production
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['VAR_Produccion_Upper80'].tolist() + df['VAR_Produccion_Lower80'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(255, 192, 203, 0.2)',
            line=dict(color='rgba(255, 192, 203, 0)'),
            name='CI - 80%'
        ))

    elif prediction_type == "Combinada":
        # Combined Demand Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['Combined_Forecast_Demanda'], 
            mode='lines', 
            name='Combinada - Demanda', 
            line=dict(color='navy', dash='longdash')
        ))
        
        # Confidence Interval for Demand
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['Combined_Upper80_Demanda'].tolist() + df['Combined_Lower80_Demanda'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(0, 0, 128, 0.2)',
            line=dict(color='rgba(0, 0, 128, 0)'),
            name='CI - 80%'
        ))
        
        # Combined Production Prediction with Confidence Intervals
        fig.add_trace(go.Scatter(
            x=df['Periodo'], 
            y=df['Combined_Forecast_Produccion'], 
            mode='lines', 
            name='Combinada - Producción', 
            line=dict(color='teal', dash='longdash')
        ))
        
        # Confidence Interval for Production
        fig.add_trace(go.Scatter(
            x=df['Periodo'].tolist() + df['Periodo'][::-1].tolist(),
            y=df['Combined_Upper80_Produccion'].tolist() + df['Combined_Lower80_Produccion'][::-1].tolist(),
            fill='toself',
            fillcolor='rgba(0, 128, 128, 0.2)',
            line=dict(color='rgba(0, 128, 128, 0)'),
            name='CI - 80%'
        ))

    fig.update_layout(
    title=f"Predicción {prediction_type} para la Demanda y Producción de Electricidad",
    xaxis_title="Period",
    yaxis_title="Value",
    template="plotly_white",
    showlegend=False  # This line removes the legend
)

    return fig

# Display plot with filtered data
st.plotly_chart(plot_predictions(df_filtered, selected_prediction))
