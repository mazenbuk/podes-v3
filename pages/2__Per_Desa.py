"""
🏷️ Per Desa - Dashboard Visual Profil Desa
Modern visual dashboard untuk analisis mendalam per desa dengan chart yang relevan untuk data binary
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys

# Setup path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import modules
from loader import load_podes_data, get_kecamatan_list, get_desa_list
from indicators import calculate_all_indicators, get_kpi_indicators

# Page config
st.set_page_config(
    page_title="Profil Visual Desa - PODES 2024",
    page_icon="🏘️",
    layout="wide"
)

# Enhanced CSS Styling for High Contrast Dark Mode
st.markdown("""
<style>
    /* Global dark background and high contrast text */
    .main .block-container {
        padding-top: 1rem;
        color: #ffffff !important;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        min-height: 100vh;
    }
    
    /* Override all Streamlit default colors */
    .stMarkdown, .stMarkdown p, .stMarkdown div, 
    .stSelectbox label, .stSelectbox div, 
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #ffffff !important;
    }
    
    /* Selectbox styling for better visibility */
    .stSelectbox > div > div {
        background-color: #374151 !important;
        color: #ffffff !important;
        border: 2px solid #60a5fa !important;
    }
    
    .stSelectbox option {
        background-color: #374151 !important;
        color: #ffffff !important;
    }
    
    .village-hero {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: #ffffff;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        border: 2px solid #60a5fa;
    }
    
    .village-hero h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #ffffff !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.8);
    }
    
    .village-hero p {
        font-size: 1.4rem;
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    .metric-modern {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
        border: 2px solid #60a5fa;
        margin-bottom: 1.5rem;
    }
    
    .metric-modern h3 {
        color: #ffffff !important;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .metric-modern p {
        color: #e2e8f0 !important;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .chart-container {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
        border: 2px solid #60a5fa;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #34d399;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    }
    
    .insight-card h4 {
        color: #ffffff !important;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .insight-card p {
        color: #e2e8f0 !important;
        line-height: 1.8;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .status-good { color: #22c55e !important; font-weight: 700; font-size: 1.1rem; }
    .status-warning { color: #f59e0b !important; font-weight: 700; font-size: 1.1rem; }
    .status-critical { color: #ef4444 !important; font-weight: 700; font-size: 1.1rem; }
    
    /* Force white text on all elements */
    * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

def create_chart_header(title, icon="📊"):
    """Helper function untuk membuat header chart yang konsisten"""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); 
                padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;
                border: 2px solid #60a5fa; text-align: center;">
        <h3 style="color: #ffffff; margin: 0; font-size: 1.4rem; font-weight: 700;">
            {icon} {title}
        </h3>
    </div>
    """, unsafe_allow_html=True)

def create_facility_status_cards(village_data, village_name):
    """Buat status cards menggunakan Streamlit native components"""
    indicators = get_kpi_indicators()
    
    # Mapping indikator ke nama yang lebih readable
    indicator_names = {
        'has_tps3r': 'TPS 3R',
        'has_bank_sampah': 'Bank Sampah', 
        'air_layak': 'Air Layak',
        'jamban_layak': 'Jamban Layak',
        'ada_bencana': 'Rawan Bencana',
        'sistem_peringatan': 'Sistem Peringatan',
        'jalan_aspal': 'Jalan Aspal',
        'ada_angkutan': 'Angkutan Umum',
        'internet_4g': 'Internet 4G',
        'kantor_online': 'Kantor Online',
        'ada_poskesdes': 'Poskesdes',
        'ada_bidan': 'Bidan Desa',
        'ada_pustu': 'Pustu',
        'ada_apotek': 'Apotek',
        'ada_tbm': 'Taman Bacaan'
    }
    
    # Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); 
                padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;
                border: 2px solid #60a5fa; text-align: center;">
        <h3 style="color: #ffffff; margin: 0; font-size: 1.4rem; font-weight: 700;">
            📊 Status Fasilitas Desa {village_name}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Buat grid dengan columns Streamlit
    num_cols = 3
    cols = st.columns(num_cols)
    
    for i, indicator in enumerate(indicators):
        col_idx = i % num_cols
        status = village_data.get(indicator, 0)
        name = indicator_names.get(indicator, indicator.replace('_', ' ').title())
        
        with cols[col_idx]:
            if status == 1:
                st.success(f"✅ **{name}**\n\n**TERSEDIA**")
            else:
                st.error(f"❌ **{name}**\n\n**TIDAK ADA**")

def create_comparison_radar_chart(village_data, df_with_indicators, selected_kecamatan, village_name):
    """Buat radar chart untuk perbandingan dengan angka konkrit desa"""
    indicators = get_kpi_indicators()
    
    # Hitung jumlah desa yang memiliki fasilitas
    kec_data = df_with_indicators[df_with_indicators['NAMA_KEC'] == selected_kecamatan]
    city_data = df_with_indicators
    
    # Data perbandingan (angka konkrit)
    village_scores = [1 if village_data.get(ind, 0) == 1 else 0 for ind in indicators]
    kec_counts = [int(kec_data[ind].sum()) for ind in indicators]
    city_counts = [int(city_data[ind].sum()) for ind in indicators]
    
    indicator_labels = [ind.replace('_', ' ').title() for ind in indicators]
    
    fig = go.Figure()
    
    # Village data (1 or 0)
    fig.add_trace(go.Scatterpolar(
        r=village_scores,
        theta=indicator_labels,
        fill='toself',
        name=f'{village_name} (Ada/Tidak)',
        fillcolor='rgba(34, 197, 94, 0.4)',  # Hijau terang dan transparan
        line=dict(color='#22c55e', width=4),
        hovertemplate='<b>%{theta}</b><br>Status: %{customdata}<extra></extra>',
        customdata=['Ada' if x == 1 else 'Tidak Ada' for x in village_scores]
    ))
    
    # Kecamatan counts (normalize to 0-1 scale for radar)
    kec_max = len(kec_data)
    kec_normalized = [count / kec_max for count in kec_counts]
    fig.add_trace(go.Scatterpolar(
        r=kec_normalized,
        theta=indicator_labels,
        fill='toself',
        name=f'Kecamatan {selected_kecamatan}',
        fillcolor='rgba(245, 158, 11, 0.3)',  # Kuning terang
        line=dict(color='#f59e0b', width=3),
        hovertemplate='<b>%{theta}</b><br>Jumlah desa: %{customdata}<extra></extra>',
        customdata=[f'{count}/{kec_max} desa' for count in kec_counts]
    ))
    
    # City counts (normalize to 0-1 scale for radar)
    city_max = len(city_data)
    city_normalized = [count / city_max for count in city_counts]
    fig.add_trace(go.Scatterpolar(
        r=city_normalized,
        theta=indicator_labels,
        fill='toself',
        name='Kota Batu',
        fillcolor='rgba(59, 130, 246, 0.3)',  # Biru terang
        line=dict(color='#3b82f6', width=3),
        hovertemplate='<b>%{theta}</b><br>Jumlah desa: %{customdata}<extra></extra>',
        customdata=[f'{count}/{city_max} desa' for count in city_counts]
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                ticktext=['0', '1/4', '1/2', '3/4', 'Semua'],
                gridcolor='#ffffff',  # Grid putih untuk kontras
                tickfont=dict(color='#ffffff', size=12)  # Tick label putih
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#ffffff')  # Label angular putih
            )
        ),
        title=None,  # Hapus title dari chart
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color='#ffffff', size=12)  # Legend text putih terang
        ),
        height=420,  # Kurangi height karena tidak ada title
        paper_bgcolor='rgba(0,0,0,0)'  # Transparent background
    )
    
    return fig

def create_priority_donut_chart(village_data, df_with_indicators):
    """Buat donut chart untuk prioritas pembangunan berdasarkan angka konkrit"""
    indicators = get_kpi_indicators()
    
    # Kategorisasi berdasarkan status dan prioritas
    categories = {
        'Sudah Tersedia': 0,
        'Prioritas Tinggi': 0,
        'Prioritas Sedang': 0,
        'Prioritas Rendah': 0
    }
    
    total_villages = len(df_with_indicators)
    
    for indicator in indicators:
        village_status = village_data.get(indicator, 0)
        # Hitung berapa desa di kota yang memiliki fasilitas ini
        villages_with_facility = int(df_with_indicators[indicator].sum())
        
        if village_status == 1:
            categories['Sudah Tersedia'] += 1
        elif villages_with_facility > (total_villages * 0.75):  # Lebih dari 75% desa memiliki
            categories['Prioritas Tinggi'] += 1
        elif villages_with_facility > (total_villages * 0.5):   # Lebih dari 50% desa memiliki
            categories['Prioritas Sedang'] += 1
        else:
            categories['Prioritas Rendah'] += 1
    
    # Warna yang sangat kontras untuk dark mode
    colors = ['#22c55e', '#ef4444', '#f59e0b', '#6b7280']  # Hijau terang, Merah terang, Kuning terang, Abu
    
    fig = go.Figure(data=[go.Pie(
        labels=list(categories.keys()),
        values=list(categories.values()),
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=3)),  # Border putih
        textinfo='label+percent',
        textfont=dict(size=14, color='#ffffff'),  # Text putih pada pie
        hovertemplate='<b>%{label}</b><br>Jumlah: %{value} fasilitas<br>Persentase: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=None,  # Hapus title dari chart
        annotations=[dict(
            text='Total<br>Fasilitas', 
            x=0.5, y=0.5, 
            font_size=16, 
            font_color='#ffffff', 
            showarrow=False
        )],
        height=350,  # Kurangi height karena tidak ada title
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        margin=dict(l=20, r=20, t=20, b=20),  # Margin yang seragam
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color='#ffffff', size=11)
        )
    )
    
    return fig

def create_kecamatan_comparison_chart(village_data, df_with_indicators, selected_kecamatan, village_name):
    """Buat chart perbandingan dengan desa lain di kecamatan yang sama"""
    indicators = get_kpi_indicators()
    
    # Data desa di kecamatan yang sama
    kec_villages = df_with_indicators[df_with_indicators['NAMA_KEC'] == selected_kecamatan]
    
    # Hitung total fasilitas per desa
    village_scores = []
    village_names = []
    
    for _, village in kec_villages.iterrows():
        total_facilities = sum([village.get(ind, 0) for ind in indicators])
        village_scores.append(total_facilities)
        village_names.append(village['NAMA_DESA'])
    
    # Highlight desa yang dipilih dengan warna yang sangat kontras
    colors = ['#22c55e' if name == village_name else '#6b7280' for name in village_names]  # Hijau terang vs abu gelap
    
    fig = go.Figure(data=[
        go.Bar(
            x=village_names,
            y=village_scores,
            marker=dict(color=colors, line=dict(color='#ffffff', width=2)),  # Border putih
            text=village_scores,
            textposition='outside',
            textfont=dict(color='#ffffff', size=14),  # Text putih terang
            hovertemplate='<b>%{x}</b><br>Total Fasilitas: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=None,  # Hapus title dari chart
        xaxis=dict(
            title=dict(text="Desa", font=dict(color='#ffffff')),  # Axis title putih
            tickfont=dict(color='#ffffff', size=12),   # Tick label putih
            tickangle=45
        ),
        yaxis=dict(
            title=dict(text="Jumlah Fasilitas", font=dict(color='#ffffff')),  # Axis title putih  
            tickfont=dict(color='#ffffff', size=12),   # Tick label putih
            range=[0, len(indicators) + 1]
        ),
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        height=350  # Kurangi height karena tidak ada title
    )
    
    return fig

def generate_smart_insights(village_data, df_with_indicators, village_name, kecamatan):
    """Generate insights otomatis berdasarkan data konkrit"""
    indicators = get_kpi_indicators()
    insights = []
    
    # Hitung statistik
    village_facilities = sum([village_data.get(ind, 0) for ind in indicators])
    total_facilities = len(indicators)
    coverage_pct = (village_facilities / total_facilities) * 100
    
    # Insight utama
    if coverage_pct >= 80:
        insights.append(f"🌟 **Excellent!** {village_name} memiliki {village_facilities}/{total_facilities} fasilitas ({coverage_pct:.1f}%). Desa ini termasuk sangat lengkap fasilitasnya.")
    elif coverage_pct >= 60:
        insights.append(f"✅ **Baik!** {village_name} memiliki {village_facilities}/{total_facilities} fasilitas ({coverage_pct:.1f}%). Perlu sedikit peningkatan.")
    elif coverage_pct >= 40:
        insights.append(f"⚠️ **Perhatian!** {village_name} memiliki {village_facilities}/{total_facilities} fasilitas ({coverage_pct:.1f}%). Perlu pengembangan lebih lanjut.")
    else:
        insights.append(f"🔴 **Prioritas!** {village_name} memiliki {village_facilities}/{total_facilities} fasilitas ({coverage_pct:.1f}%). Perlu pembangunan intensif.")
    
    # Analisis komparatif menggunakan data konkrit
    missing_priorities = []
    available_facilities = []
    total_villages = len(df_with_indicators)
    
    for indicator in indicators:
        village_status = village_data.get(indicator, 0)
        villages_with_facility = int(df_with_indicators[indicator].sum())
        facility_name = indicator.replace('_', ' ').title()
        
        if village_status == 1:
            available_facilities.append(facility_name)
        elif villages_with_facility > (total_villages * 0.6):  # Jika lebih dari 60% desa lain punya
            missing_priorities.append(f"{facility_name} ({villages_with_facility}/{total_villages} desa memiliki)")
    
    if available_facilities:
        insights.append(f"💪 **Kekuatan:** Fasilitas yang sudah tersedia: {', '.join(available_facilities[:3])}{'...' if len(available_facilities) > 3 else ''}")
    
    if missing_priorities:
        insights.append(f"🎯 **Rekomendasi Prioritas:** {missing_priorities[0]}")
        if len(missing_priorities) > 1:
            insights.append(f"📋 **Fokus Selanjutnya:** {', '.join(missing_priorities[1:3])}")
    
    return insights

def main():
    # Load data
    with st.spinner("⏳ Memuat data..."):
        df = load_podes_data()
        
    if df.empty:
        st.error("❌ Data tidak dapat dimuat")
        st.stop()
    
    df_with_indicators = calculate_all_indicators(df)
    
    # === HERO SECTION ===
    st.markdown("""
    <div class="village-hero">
        <h1>🏘️ Profil Visual Desa</h1>
        <p>Dashboard interaktif untuk analisis mendalam fasilitas dan infrastruktur desa</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === SELEKSI DESA ===
    col1, col2 = st.columns([1, 1])
    
    with col1:
        kecamatan_list = get_kecamatan_list(df)
        selected_kecamatan = st.selectbox(
            "📍 Pilih Kecamatan:",
            kecamatan_list,
            help="Pilih kecamatan untuk melihat daftar desa"
        )
    
    with col2:
        desa_list = get_desa_list(df, selected_kecamatan)
        selected_desa = st.selectbox(
            "🏘️ Pilih Desa:",
            desa_list,
            help="Pilih desa untuk analisis detail"
        )
    
    # Get data
    village_data = df_with_indicators[
        (df_with_indicators['NAMA_KEC'] == selected_kecamatan) & 
        (df_with_indicators['NAMA_DESA'] == selected_desa)
    ].iloc[0]
    
    kec_avg = df_with_indicators[df_with_indicators['NAMA_KEC'] == selected_kecamatan][get_kpi_indicators()].mean()
    city_avg = df_with_indicators[get_kpi_indicators()].mean()
    
    # === METRICS OVERVIEW ===
    st.markdown("### 📊 Ringkasan Cepat")
    
    col1, col2 = st.columns(2)
    
    indicators = get_kpi_indicators()
    total_facilities = len(indicators)
    available_facilities = sum([village_data.get(ind, 0) for ind in indicators])
    coverage_pct = (available_facilities / total_facilities) * 100
    
    with col1:
        st.markdown(f"""
        <div class="metric-modern">
            <h3>🏗️ Total Fasilitas</h3>
            <p>{available_facilities}/{total_facilities}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-modern">
            <h3>📈 Cakupan</h3>
            <p>{coverage_pct:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # === VISUALISASI UTAMA ===
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Status Cards untuk data binary
        create_facility_status_cards(village_data, selected_desa)
    
    with col2:
        # Header untuk donut chart
        create_chart_header("Prioritas Pembangunan Fasilitas", "🎯")
        priority_chart = create_priority_donut_chart(village_data, df_with_indicators)
        st.plotly_chart(priority_chart, use_container_width=True, config={'displayModeBar': False})
    
    # === CHART PERBANDINGAN ===
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Header untuk radar chart
        create_chart_header(f"Perbandingan {selected_desa} dengan Desa Lain", "🎯")
        radar_chart = create_comparison_radar_chart(village_data, df_with_indicators, selected_kecamatan, selected_desa)
        st.plotly_chart(radar_chart, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        # Header untuk comparison chart
        create_chart_header(f"Perbandingan dengan Desa Lain di Kecamatan {selected_kecamatan}", "📈")
        kec_comparison_chart = create_kecamatan_comparison_chart(village_data, df_with_indicators, selected_kecamatan, selected_desa)
        st.plotly_chart(kec_comparison_chart, use_container_width=True, config={'displayModeBar': False})
    
    # === SMART INSIGHTS ===
    st.markdown("### 🔍 Analisis & Rekomendasi")
    
    insights = generate_smart_insights(village_data, df_with_indicators, selected_desa, selected_kecamatan)
    
    for i, insight in enumerate(insights):
        st.markdown(f"""
        <div class="insight-card">
            <h4>Insight {i+1}</h4>
            <p>{insight}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # === DOWNLOAD SECTION ===
    st.markdown("### 📥 Export Data")
    
    # Prepare export data
    export_data = {
        'Desa': selected_desa,
        'Kecamatan': selected_kecamatan,
        'Total_Fasilitas': f"{available_facilities}/{total_facilities}",
        'Cakupan_Persen': f"{coverage_pct:.1f}%"
    }
    
    for indicator in indicators:
        export_data[indicator.replace('_', ' ').title()] = "Ada" if village_data.get(indicator, 0) == 1 else "Tidak Ada"
    
    export_df = pd.DataFrame([export_data])
    csv = export_df.to_csv(index=False)
    
    st.download_button(
        label="📊 Download Profil Desa (CSV)",
        data=csv,
        file_name=f"profil_visual_{selected_desa.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
