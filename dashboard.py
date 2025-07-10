import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# @st.cache_data
def load_gold_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gold_path = os.path.join(script_dir, "data", "gold")
    
    data = {}
    
    dm_customers_path = os.path.join(gold_path, "dm_customers")
    ft_orders_path = os.path.join(gold_path, "ft_orders")
    
    try:
        if os.path.exists(dm_customers_path):
            data['dm_customers'] = pd.read_parquet(dm_customers_path)
        
        if os.path.exists(ft_orders_path):
            data['ft_orders'] = pd.read_parquet(ft_orders_path)
            
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return {}
    
    return data

def create_kpi_cards(data):
    if 'ft_orders' not in data:
        st.warning("Dados da tabela fato não encontrados")
        return
    
    ft_orders = data['ft_orders']
    
    total_orders = len(ft_orders)
    total_revenue = ft_orders['price'].sum()
    avg_order_value = ft_orders['price'].mean()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total de Pedidos",
            value=f"{total_orders:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Receita Total",
            value=f"R$ {total_revenue:,.2f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Ticket Médio",
            value=f"R$ {avg_order_value:.2f}",
            delta=None
        )

def create_temporal_analysis(data):
    if 'ft_orders' not in data:
        return
    
    ft_orders = data['ft_orders']
    
    yearly_data = ft_orders.groupby('order_purchase_year').agg({
        'order_id': 'count',
        'price': 'sum'
    }).reset_index()
    yearly_data.columns = ['Ano', 'Total_Pedidos', 'Receita_Total']
    
    fig_yearly = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Pedidos por Ano', 'Receita por Ano'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig_yearly.add_trace(
        go.Bar(
            x=yearly_data['Ano'], 
            y=yearly_data['Total_Pedidos'], 
            name='Pedidos',
            marker_color='#636EFA'
        ),
        row=1, col=1
    )
    
    fig_yearly.add_trace(
        go.Bar(
            x=yearly_data['Ano'], 
            y=yearly_data['Receita_Total'], 
            name='Receita',
            marker_color='#EF553B'
        ),
        row=1, col=2
    )
    
    fig_yearly.update_layout(height=400, showlegend=False)
    fig_yearly.update_yaxes(title_text="Número de Pedidos", row=1, col=1)
    fig_yearly.update_yaxes(title_text="Receita (R$)", row=1, col=2)
    
    st.plotly_chart(fig_yearly, use_container_width=True)
    
    monthly_data = ft_orders.groupby(['order_purchase_year', 'order_purchase_month']).agg({
        'order_id': 'count'
    }).reset_index()
    
    monthly_data['Periodo'] = monthly_data['order_purchase_year'].astype(str) + '-' + monthly_data['order_purchase_month'].astype(str).str.zfill(2)
    
    fig_monthly = px.line(
        monthly_data, 
        x='Periodo', 
        y='order_id',
        title='Evolução Mensal de Pedidos',
        labels={'order_id': 'Número de Pedidos', 'Periodo': 'Período'},
        line_shape='spline'
    )
    fig_monthly.update_xaxes(tickangle=45)
    fig_monthly.update_traces(line_color='#00CC96', line_width=3)
    st.plotly_chart(fig_monthly, use_container_width=True)

def create_geographic_analysis(data):
    if 'ft_orders' not in data or 'dm_customers' not in data:
        st.warning("Dados necessários para análise geográfica não encontrados")
        return
    
    ft_orders = data['ft_orders']
    dm_customers = data['dm_customers']

    orders_with_location = ft_orders.merge(dm_customers, on='customer_id', how='left')
    
    state_analysis = orders_with_location.groupby('customer_state').agg({
        'order_id': 'count',
        'price': 'sum'
    }).reset_index().sort_values('price', ascending=False)
    state_analysis.columns = ['Estado', 'Total_Pedidos', 'Receita_Total']
    
    top_10_states = state_analysis.head(10)
    col1, col2 = st.columns(2)
    
    with col1:
        fig_state_orders = px.bar(
            top_10_states,
            x='Estado',
            y='Total_Pedidos',
            title='Top 10 Estados - Pedidos',
            labels={'Total_Pedidos': 'Número de Pedidos'},
            color='Total_Pedidos',
            color_continuous_scale='Blues'
        )
        fig_state_orders.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_state_orders, use_container_width=True)
    
    with col2:
        fig_state_revenue = px.bar(
            top_10_states,
            x='Estado',
            y='Receita_Total',
            title='Top 10 Estados - Receita',
            labels={'Receita_Total': 'Receita (R$)'},
            color='Receita_Total',
            color_continuous_scale='Reds'
        )
        fig_state_revenue.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_state_revenue, use_container_width=True)

def main():
    st.title("🛒 E-commerce Dashboard")
    st.markdown("*Dashboard focado nos principais indicadores de performance*")
    st.markdown("---")
    
    data = load_gold_data()
    
    if not data:
        st.error("Não foi possível carregar os dados. Verifique se a camada gold foi criada.")
        return
    
    with st.sidebar:
        st.header("Informações")
        
        st.markdown("### Dados Carregados")
        for table_name, df in data.items():
            st.text(f"{table_name}: {len(df)} registros")
        
        st.markdown("### Última Atualização")
        st.text(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        st.markdown("---")
        st.markdown("📊 **Dashboard**")
    
    st.header("📊 KPIs Principais")
    create_kpi_cards(data)
    
    st.markdown("---")
    
    st.header("📅 Análise Temporal")
    create_temporal_analysis(data)
    
    st.markdown("---")
    
    st.header("🗺️ Top 10 Estados")
    create_geographic_analysis(data)
    
    st.markdown("---")
    st.markdown("*Dashboard - Dados do DataLake (Camada Gold)*")

if __name__ == "__main__":
    main()
