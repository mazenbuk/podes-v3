"""
📊 Overview - Dashboard Ringkasan Seluruh Desa
Halaman untuk melihat ringkasan indikator dengan filter kecamatan
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Setup path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import modules
from loader import load_podes_data, load_indicators_catalog, get_kecamatan_list, get_desa_list
from indicators import calculate_all_indicators, get_kpi_indicators
from ui_helpers import display_kpi_cards, create_distribution_chart, create_heatmap, create_ranking_table, display_status_badge

def get_indicator_emoji(indicator):
    """
    Mengembalikan emoji yang sesuai untuk setiap indikator
    """
    emoji_map = {
        # Prioritas Urgent
        'has_tps3r': '♻️',
        'ada_poskesdes': '�',
        'air_layak': '💧',
        'sistem_peringatan': '�',
        
        # Indikator Sedang
        'ada_apotek': '�',
        'ada_angkutan': '�',
        
        # Indikator Baik
        'ada_bidan': '�‍⚕️',
        'internet_4g': '📡',
        'kantor_online': '🌐',
        
        # Legacy indicators (jika masih ada)
        'has_bank_sampah': '�',
        'jamban_layak': '🚽',
        'jalan_aspal': '🛣️',
        'ada_bencana': '⚠️',
        'ada_pustu': '🏥',
        'ada_tbm': '📚'
    }
    return emoji_map.get(indicator, '📊')

def display_kpi_cards_concrete(df, kpi_indicators):
    """
    Menampilkan KPI cards dengan angka konkrit
    """
    # Hitung nilai KPI
    total_desa = len(df)
    kpi_values = {}
    
    for indicator in kpi_indicators:
        if indicator in df.columns:
            count_ada = int(df[indicator].sum())
            kpi_values[indicator] = count_ada
        else:
            kpi_values[indicator] = 0
    
    # Display dalam grid
    num_cols = min(3, len(kpi_indicators))
    cols = st.columns(num_cols)
    
    for i, (indicator, count) in enumerate(kpi_values.items()):
        col_idx = i % num_cols
        
        with cols[col_idx]:
            # Format nama indikator
            indicator_name = indicator.replace('_', ' ').title()
            
            # Tentukan emoji berdasarkan jenis indikator
            emoji = get_indicator_emoji(indicator)
            
            # Hitung persentase untuk delta
            percentage = (count / total_desa * 100) if total_desa > 0 else 0
            
            st.metric(
                label=f"{emoji} {indicator_name}",
                value=f"{count} desa",
                delta=f"{percentage:.1f}% dari {total_desa} desa",
                help=f"Jumlah desa yang memiliki {indicator_name.lower()}"
            )

# Page config
st.set_page_config(
    page_title="Overview - Data Desa Dalam Genggaman",
    page_icon="📊",
    layout="wide"
)

# Custom CSS untuk dark mode dengan kontras tinggi
st.markdown("""
<style>
    /* Dark mode dengan kontras tinggi */
    .main .block-container {
        color: #f8fafc;
        font-weight: 500;
        background-color: transparent;
    }
    
    /* Metric cards untuk dark mode */
    .metric-card {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        color: #f9fafb;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #60a5fa;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        border: 1px solid #6b7280;
    }
    
    .metric-card h3, .metric-card h4 {
        color: #f9fafb !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        color: #d1d5db !important;
        font-weight: 600;
        font-size: 1.1em;
        line-height: 1.5;
    }
    
    /* Insight boxes untuk dark mode */
    .insight-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        color: #f1f5f9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #60a5fa;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.4);
        border: 1px solid #4f46e5;
    }
    
    .insight-box h3, .insight-box h4 {
        color: #ddd6fe !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .insight-box p, .insight-box li {
        color: #e0e7ff !important;
        font-weight: 500;
        line-height: 1.6;
    }
    
    /* Streamlit elements */
    .stSelectbox label, .stMarkdown p {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    
    /* Chart titles dan labels untuk dark mode */
    .plotly .main-svg text {
        fill: #f8fafc !important;
        font-weight: 600;
    }
    
    /* Table styling untuk dark mode */
    .dataframe {
        color: #f8fafc !important;
        font-weight: 500;
    }
    
    .dataframe th {
        background-color: #374151 !important;
        color: #f9fafb !important;
        font-weight: 700;
    }
    
    .dataframe td {
        color: #d1d5db !important;
        font-weight: 500;
    }
    
    /* Sidebar text untuk dark mode */
    .css-1d391kg, .css-1d391kg p {
        color: #f8fafc !important;
        font-weight: 600;
    }
    
    /* Priority indicators dengan warna lebih terang */
    .priority-urgent {
        color: #f87171 !important;
        font-weight: 700;
    }
    
    .priority-medium {
        color: #fbbf24 !important;
        font-weight: 600;
    }
    
    .priority-good {
        color: #34d399 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.title("📊 Overview Dashboard")
    st.markdown("**Analisis komprehensif kondisi desa di Kota Batu berdasarkan PODES 2024**")
    
    # Load data
    with st.spinner("⏳ Memuat data..."):
        df = load_podes_data()
        catalog = load_indicators_catalog()
    
    if df.empty:
        st.error("❌ Data tidak dapat dimuat")
        st.stop()
    
    # Hitung indikator
    df_with_indicators = calculate_all_indicators(df)
    kpi_indicators = get_kpi_indicators()
    
    # === PRIORITAS URGENT METRICS ===
    st.markdown("### 🚨 Indikator Prioritas Urgent")
    st.markdown("**4 indikator yang memerlukan perhatian segera**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'has_tps3r' in df_with_indicators.columns:
            tps3r_count = int(df_with_indicators['has_tps3r'].sum())
            urgent_count = 24 - tps3r_count
            st.metric(
                "♻️ Desa Tanpa TPS3R",
                f"{urgent_count} desa",
                delta=f"{urgent_count/24*100:.1f}% - SANGAT URGENT",
                delta_color="inverse",
                help="Tempat Pengolahan Sampah 3R - 20 desa masih belum memiliki"
            )
        else:
            st.metric("♻️ TPS3R", "N/A")
    
    with col2:
        if 'ada_poskesdes' in df_with_indicators.columns:
            poskesdes_count = int(df_with_indicators['ada_poskesdes'].sum())
            urgent_count = 24 - poskesdes_count
            st.metric(
                "🏥 Desa Tanpa Poskesdes",
                f"{urgent_count} desa",
                delta=f"{urgent_count/24*100:.1f}% - SANGAT URGENT",
                delta_color="inverse",
                help="Pos Kesehatan Desa - 18 desa masih belum memiliki"
            )
        else:
            st.metric("🏥 Poskesdes", "N/A")
    
    with col3:
        if 'air_layak' in df_with_indicators.columns:
            air_count = int(df_with_indicators['air_layak'].sum())
            urgent_count = 24 - air_count
            st.metric(
                "💧 Air Tidak Layak",
                f"{urgent_count} desa",
                delta=f"{urgent_count/24*100:.1f}% - URGENT",
                delta_color="inverse",
                help="Akses air bersih layak minum - 16 desa masih belum memiliki"
            )
        else:
            st.metric("💧 Air Layak", "N/A")
    
    with col4:
        if 'sistem_peringatan' in df_with_indicators.columns:
            peringatan_count = int(df_with_indicators['sistem_peringatan'].sum())
            urgent_count = 24 - peringatan_count
            st.metric(
                "⚠️ Tanpa Sistem Peringatan",
                f"{urgent_count} desa",
                delta=f"{urgent_count/24*100:.1f}% - URGENT",
                delta_color="inverse",
                help="Sistem peringatan dini bencana - 12 desa masih belum memiliki"
            )
        else:
            st.metric("⚠️ Sistem Peringatan", "N/A")
    
    # === ANALISIS PRIORITAS ===
    st.markdown("### 🎯 Analisis Prioritas")
    
    st.error("""
    **🔴 SANGAT URGENT - Prioritas Tertinggi:**
    
    1. **♻️ TPS3R (Tempat Pengolahan Sampah 3R)**: Hanya **4 dari 24 desa** (16.7%)
       - 20 desa belum memiliki fasilitas pengolahan sampah yang memadai
       - Dampak: Pencemaran lingkungan dan masalah kesehatan
    
    2. **🏥 Poskesdes (Pos Kesehatan Desa)**: Hanya **6 dari 24 desa** (25.0%)
       - 18 desa belum memiliki fasilitas kesehatan dasar
       - Dampak: Akses kesehatan terbatas, terutama untuk ibu hamil dan balita
    """)
    
    st.warning("""
    **🟡 URGENT - Perlu Ditingkatkan:**
    
    3. **💧 Air Layak Minum**: Hanya **8 dari 24 desa** (33.3%)
       - 16 desa belum memiliki akses air bersih layak minum
       - Dampak: Risiko penyakit waterborne dan masalah kesehatan
    
    4. **🚨 Sistem Peringatan Dini**: **12 dari 24 desa** (50.0%)
       - 12 desa masih belum memiliki sistem peringatan bencana
       - Dampak: Kerentanan terhadap bencana alam
    """)
    
    st.success("""
    **✅ KONDISI BAIK - Sudah Optimal:**
    
    - **👩‍⚕️ Praktik Bidan**: 23/24 desa (95.8%) - Akses persalinan sudah sangat baik
    - **📡 Internet 4G**: 24/24 desa (100%) - Konektivitas digital sudah optimal
    - **🌐 Kantor Online**: 24/24 desa (100%) - Pelayanan digital sudah tersedia
    - **🏦 Bank Sampah**: 24/24 desa (100%) - Program sudah merata
    - **🚽 Jamban Layak**: 24/24 desa (100%) - Sanitasi sudah memadai  
    - **🛣️ Jalan Aspal**: 24/24 desa (100%) - Infrastruktur jalan sudah baik
    """)
    
    # === SEPARATOR ===
    st.markdown("---")
    
    # Sidebar Filter
    st.sidebar.markdown("### 🎛️ Filter Data")
    
    # Filter Kecamatan
    kecamatan_options = ["Semua Kecamatan"] + get_kecamatan_list(df)
    selected_kecamatan = st.sidebar.selectbox(
        "📍 Pilih Kecamatan:",
        kecamatan_options,
        index=0
    )
    
    # Filter data
    if selected_kecamatan == "Semua Kecamatan":
        df_filtered = df_with_indicators.copy()
        filter_info = "Semua desa di Kota Batu"
    else:
        df_filtered = df_with_indicators[df_with_indicators['NAMA_KEC'] == selected_kecamatan].copy()
        filter_info = f"Desa di Kecamatan {selected_kecamatan}"
    
    # Info filter
    st.sidebar.info(f"""
    **Data yang ditampilkan:**  
    {filter_info}  
    
    **Jumlah desa:** {len(df_filtered)}
    """)
    
    # === KPI CARDS ===
    st.markdown("### 📈 Detail Indikator per Kecamatan")
    st.markdown(f"**Filter: {filter_info}**")
    
    # Tampilkan KPI cards dengan angka konkrit
    display_kpi_cards_concrete(df_filtered, kpi_indicators)
    
    # === INFORMASI PENDUKUNG ===
    st.markdown("### 📊 Informasi Pendukung")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏘️ Ringkasan Per Kecamatan")
        if selected_kecamatan == "Semua Kecamatan":
            kec_summary = df_filtered.groupby('NAMA_KEC').agg({
                'NAMA_DESA': 'count'
            }).round(1)
            kec_summary.columns = ['Jumlah Desa']
            st.dataframe(kec_summary, use_container_width=True)
        else:
            # Detail desa dalam kecamatan terpilih
            desa_list = df_filtered['NAMA_DESA'].tolist()
            st.markdown(f"**Desa di {selected_kecamatan}:**")
            for i, desa in enumerate(desa_list, 1):
                st.markdown(f"{i}. {desa}")
    
    with col2:
        st.markdown("#### 📈 Status Capaian")
        total_desa = len(df_filtered)
        
        # Hitung status untuk setiap indikator
        status_data = []
        for indicator in kpi_indicators:
            if indicator in df_filtered.columns:
                count_ada = int(df_filtered[indicator].sum())
                count_tidak = total_desa - count_ada
                indicator_name = indicator.replace('_', ' ').title()
                
                status_data.append({
                    'Indikator': indicator_name,
                    'Ada': count_ada,
                    'Tidak Ada': count_tidak,
                    'Persentase': f"{(count_ada/total_desa*100):.1f}%"
                })
        
        status_df = pd.DataFrame(status_data)
        st.dataframe(status_df, use_container_width=True)

if __name__ == "__main__":
    main()
