"""
UI Helpers Module - PODES 2024
Modul untuk komponen UI dan visualisasi Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def display_kpi_cards(df, kpi_indicators):
    """
    Menampilkan KPI cards dalam grid
    """
    # Hitung nilai KPI
    kpi_values = {}
    for indicator in kpi_indicators:
        if indicator in df.columns:
            kpi_values[indicator] = df[indicator].mean() * 100
        else:
            kpi_values[indicator] = 0
    
    # Display dalam grid 2x5 atau sesuaikan dengan jumlah indikator
    num_cols = min(5, len(kpi_indicators))
    cols = st.columns(num_cols)
    
    for i, (indicator, value) in enumerate(kpi_values.items()):
        col_idx = i % num_cols
        
        with cols[col_idx]:
            # Format nama indikator
            indicator_name = indicator.replace('_', ' ').title()
            
            # Tentukan emoji berdasarkan jenis indikator
            emoji = get_indicator_emoji(indicator)
            
            # Tentukan warna berdasarkan nilai
            if value >= 75:
                delta_color = "normal"
            elif value >= 50:
                delta_color = "off"
            else:
                delta_color = "inverse"
            
            st.metric(
                label=f"{emoji} {indicator_name}",
                value=f"{value:.1f}%",
                help=f"Persentase desa dengan {indicator_name.lower()}"
            )

def get_indicator_emoji(indicator):
    """
    Mengembalikan emoji yang sesuai untuk indikator
    """
    emoji_map = {
        'has_tps3r': '🗑️',
        'has_bank_sampah': '🏦',
        'air_layak': '💧',
        'jamban_layak': '🚻',
        'ada_bencana': '⚠️',
        'sistem_peringatan': '📢',
        'jalan_aspal': '🛤️',
        'ada_angkutan': '🚌',
        'internet_4g': '📶',
        'kantor_online': '💻'
    }
    return emoji_map.get(indicator, '📊')

def create_distribution_chart(df, column, title):
    """
    Membuat chart distribusi untuk kolom tertentu dengan dark mode
    """
    if column not in df.columns:
        st.warning(f"Kolom {column} tidak ditemukan")
        return
    
    # Hitung distribusi
    dist = df[column].value_counts().reset_index()
    dist.columns = ['Kategori', 'Jumlah']
    
    # Chart pie dengan warna yang kontras
    fig = px.pie(
        dist,
        values='Jumlah',
        names='Kategori',
        title=title,
        color_discrete_sequence=['#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa']
    )
    
    # Update layout untuk dark mode
    fig.update_layout(
        title_font_color='#f8fafc',
        legend_font_color='#d1d5db',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_heatmap(df, indicators, group_by='NAMA_KEC'):
    """
    Membuat heatmap indikator per grup (kecamatan) dengan dark mode
    """
    if group_by not in df.columns:
        st.warning(f"Kolom {group_by} tidak ditemukan")
        return
    
    # Agregasi per grup
    agg_data = df.groupby(group_by)[indicators].mean()
    
    # Heatmap dengan color scale yang cocok untuk dark mode
    fig = px.imshow(
        agg_data.T,
        aspect="auto",
        title=f"Heatmap Indikator per {group_by.replace('_', ' ').title()}",
        labels=dict(x=group_by.replace('_', ' ').title(), y="Indikator", color="Nilai"),
        color_continuous_scale="viridis"  # Color scale yang lebih baik untuk dark mode
    )
    
    # Update layout untuk dark mode
    fig.update_layout(
        title_font_color='#f8fafc',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#d1d5db')),
        yaxis=dict(tickfont=dict(color='#d1d5db')),
        coloraxis_colorbar=dict(tickfont=dict(color='#d1d5db'))
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_ranking_table(df, score_column='skor_komposit', top_n=10):
    """
    Membuat tabel ranking desa
    """
    if score_column not in df.columns:
        st.warning(f"Kolom {score_column} tidak ditemukan")
        return
    
    # Sort dan ambil top N
    top_desa = df.nlargest(top_n, score_column)
    
    # Format untuk display
    display_cols = ['NAMA_DESA', 'NAMA_KEC', score_column]
    if all(col in df.columns for col in display_cols):
        ranking_df = top_desa[display_cols].reset_index(drop=True)
        ranking_df.index += 1  # Start from 1
        
        st.dataframe(ranking_df, use_container_width=True)
    else:
        st.warning("Kolom yang diperlukan untuk ranking tidak tersedia")

def display_status_badge(value, thresholds=[25, 50, 75]):
    """
    Menampilkan badge status berdasarkan nilai dengan emoji kontras
    """
    if value >= thresholds[2]:
        return "🟢 Sangat Baik"
    elif value >= thresholds[1]:
        return "🟡 Baik"  
    elif value >= thresholds[0]:
        return "🟠 Perlu Perhatian"
    else:
        return "🔴 Prioritas"

def create_comparison_chart(data, title="Perbandingan"):
    """
    Membuat chart perbandingan dengan dark mode
    """
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=['Kategori', 'Nilai'])
    else:
        df = data
    
    fig = px.bar(
        df,
        x='Kategori',
        y='Nilai',
        title=title,
        color='Nilai',
        color_continuous_scale='viridis'  # Better for dark mode
    )
    
    # Update layout untuk dark mode
    fig.update_layout(
        title_font_color='#f8fafc',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(color='#d1d5db')),
        yaxis=dict(tickfont=dict(color='#d1d5db')),
        coloraxis_colorbar=dict(tickfont=dict(color='#d1d5db'))
    )
    
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

def create_indicator_panel(df, desa_name, indicators):
    """
    Membuat panel indikator untuk desa tertentu
    """
    desa_data = df[df['NAMA_DESA'] == desa_name]
    
    if desa_data.empty:
        st.error(f"Data untuk desa {desa_name} tidak ditemukan")
        return
    
    desa_row = desa_data.iloc[0]
    
    # Display indikator dalam ekspander
    for indicator in indicators:
        if indicator in desa_row:
            value = desa_row[indicator]
            status = "✅ Ya" if value == 1 else "❌ Tidak"
            
            with st.expander(f"{get_indicator_emoji(indicator)} {indicator.replace('_', ' ').title()}"):
                st.write(f"Status: {status}")
                st.write(f"Nilai: {value}")

def format_number(number, decimal_places=1):
    """
    Format angka dengan pemisah ribuan
    """
    return f"{number:,.{decimal_places}f}"

def create_gauge_chart(value, title, max_value=100):
    """
    Membuat gauge chart untuk menampilkan persentase dengan dark mode
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'color': '#f8fafc'}},
        delta = {'reference': max_value/2},
        gauge = {
            'axis': {'range': [None, max_value], 'tickfont': {'color': '#d1d5db'}},
            'bar': {'color': "#60a5fa"},  # Blue yang lebih terang
            'steps': [
                {'range': [0, max_value/4], 'color': "#374151"},      # Gray gelap
                {'range': [max_value/4, max_value/2], 'color': "#4b5563"},  # Gray medium
                {'range': [max_value/2, 3*max_value/4], 'color': "#fbbf24"}, # Yellow terang
                {'range': [3*max_value/4, max_value], 'color': "#34d399"}    # Green terang
            ],
            'threshold': {
                'line': {'color': "#f87171", 'width': 4},  # Red yang lebih terang
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    # Update layout untuk dark mode
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc')
    )
    st.plotly_chart(fig, use_container_width=True)
