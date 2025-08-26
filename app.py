"""
Data Desa Dalam Genggaman - PODES 2024
Landing page untuk aplikasi analisis data desa wilayah 3579
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Data Desa Dalam Genggaman - PODES 2024",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk meningkatkan keterbacaan
st.markdown("""
<style>
    /* Improve text readability across the app */
    .main .block-container {
        color: #1a1a1a;
        font-weight: 500;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white !important;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .main-header h1 {
        color: white !important;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95) !important;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .welcome-box {
        background: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        border-left: 6px solid #0ea5e9;
        margin: 2rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .welcome-box h3 {
        color: #1f2937 !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .welcome-box p {
        color: #374151 !important;
        font-weight: 500;
        line-height: 1.7;
        font-size: 1.05em;
    }
    
    .nav-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .nav-card:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    .nav-card h4 {
        color: #1f2937 !important;
        margin-bottom: 0.5rem;
        font-weight: 700;
        font-size: 1.1em;
    }
    .nav-card p {
        color: #374151 !important;
        margin-bottom: 0.5rem;
        line-height: 1.6;
        font-weight: 500;
    }
    .info-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .info-card h4 {
        color: #1f2937 !important;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .info-card p, .info-card li {
        color: #374151 !important;
        line-height: 1.6;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    .info-card ul {
        color: #374151 !important;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Streamlit elements */
    .stMarkdown p {
        color: #1a1a1a !important;
        font-weight: 500;
        line-height: 1.6;
    }
    
    /* Sidebar text */
    .css-1d391kg, .css-1d391kg p {
        color: #1a1a1a !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏘️ Data Desa Dalam Genggaman</h1>
        <h2>PODES 2024 - Wilayah Kota Batu (3579)</h2>
        <p style="font-size: 1.2em;">Analisis Fasilitas Lingkungan, Bencana, Kesehatan & Teknologi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="welcome-box">
        <h3>🎯 Selamat Datang di Dashboard Analisis PODES 2024</h3>
        <p>Aplikasi ini menyediakan analisis komprehensif terhadap kondisi fasilitas dan infrastruktur di 24 desa di Kota Batu berdasarkan data Survei Potensi Desa (PODES) 2024 yang dilakukan oleh Badan Pusat Statistik.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation cards
    st.markdown("### 🧭 Navigasi Halaman")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="nav-card">
            <h4>📊 Overview Dashboard</h4>
            <p><strong>Halaman utama analisis</strong></p>
            <p>• Indikator prioritas urgent<br/>
            • Analisis kondisi desa<br/>
            • Filter per kecamatan<br/>
            • KPI dan insights utama</p>
            <p style="color: #0ea5e9; font-weight: bold;">👈 Mulai dari sini!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="nav-card">
            <h4>🏷️ Profil Per Desa</h4>
            <p><strong>Detail setiap desa</strong></p>
            <p>• Profil lengkap desa<br/>
            • Perbandingan antar desa<br/>
            • Status fasilitas detail<br/>
            • Rekomendasi spesifik</p>
            <p style="color: #6b7280;">Untuk analisis mendalam</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick info
    st.markdown("### ℹ️ Informasi Dataset")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>📊 Cakupan Data</h4>
            <ul>
                <li><strong>24 Desa</strong> di Kota Batu</li>
                <li><strong>3 Kecamatan</strong> (Batu, Bumiaji, Junrejo)</li>
                <li><strong>4 Blok Analisis</strong> (V, VI, VII, X)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Fokus Analisis</h4>
            <ul>
                <li>Fasilitas Lingkungan & Perumahan</li>
                <li>Sistem Peringatan Bencana</li>
                <li>Akses Kesehatan & Transportasi</li>
                <li>Teknologi Informasi & Komunikasi</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <h4>🔍 Fitur Utama</h4>
            <ul>
                <li>Analisis prioritas urgent</li>
                <li>Dashboard interaktif</li>
                <li>Filter dinamis</li>
                <li>Insights actionable</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 1rem;">
        <p><strong>Data Desa Dalam Genggaman</strong> | PODES 2024 | Kota Batu</p>
        <p>Dikembangkan untuk mendukung pengambilan kebijakan berbasis data</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
