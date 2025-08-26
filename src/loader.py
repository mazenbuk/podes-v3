"""
Data Loader Module - PODES 2024
Modul untuk memuat data dan katalog indikator
"""

import pandas as pd
import streamlit as st
from pathlib import Path

# Path data
DATA_PATH = Path(__file__).parent.parent / "data" / "raw"

@st.cache_data
def load_podes_data():
    """
    Memuat data PODES 2024 dari CSV dan agregasi per desa
    Returns: DataFrame
    """
    try:
        file_path = DATA_PATH / "master_podes_desa.csv"
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # Pastikan kolom yang diperlukan ada
        required_cols = ['IDDESA', 'NAMA_DESA', 'NAMA_KEC']
        for col in required_cols:
            if col not in df.columns:
                st.warning(f"Kolom {col} tidak ditemukan dalam data")
        
        # Agregasi data per desa (karena data berisi duplikasi per RT/RW)
        # Grup by desa dan ambil data yang konsisten
        groupby_cols = ['NAMA_DESA', 'NAMA_KEC', 'NAMA_KAB', 'NAMA_PROV']
        
        # Kolom numerik untuk di-aggregate (ambil modus/yang paling sering)
        numeric_cols = [col for col in df.columns if col.startswith('R') and col not in groupby_cols]
        
        # Aggregate dengan mengambil modus (nilai yang paling sering muncul)
        agg_dict = {}
        for col in numeric_cols:
            if col in df.columns:
                agg_dict[col] = lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]
        
        # Tambahkan IDDESA (ambil yang pertama)
        agg_dict['IDDESA'] = 'first'
        
        df_aggregated = df.groupby(groupby_cols).agg(agg_dict).reset_index()
        
        # Info untuk user
        st.sidebar.success(f"""
        ✅ Data berhasil dimuat:
        - Data asli: {len(df)} rows
        - Data per desa: {len(df_aggregated)} desa
        """)
        
        return df_aggregated
        
    except Exception as e:
        st.error(f"Error loading PODES data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_indicators_catalog():
    """
    Memuat katalog indikator dari CSV
    Returns: DataFrame
    """
    try:
        file_path = Path(__file__).parent.parent / "indicators_catalog.csv"
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except Exception as e:
        st.warning(f"Katalog indikator tidak dapat dimuat: {str(e)}")
        return pd.DataFrame()

def get_kecamatan_list(df):
    """
    Mendapatkan daftar kecamatan
    """
    if 'NAMA_KEC' in df.columns:
        return sorted(df['NAMA_KEC'].unique().tolist())
    return []

def get_desa_list(df, kecamatan=None):
    """
    Mendapatkan daftar desa berdasarkan kecamatan
    """
    if 'NAMA_DESA' not in df.columns:
        return []
    
    if kecamatan and 'NAMA_KEC' in df.columns:
        filtered_df = df[df['NAMA_KEC'] == kecamatan]
        return sorted(filtered_df['NAMA_DESA'].unique().tolist())
    
    return sorted(df['NAMA_DESA'].unique().tolist())

def get_processed_data():
    """
    Memuat data yang sudah diproses (jika ada)
    """
    try:
        file_path = Path(__file__).parent.parent / "data" / "processed" / "podes_processed.csv"
        if file_path.exists():
            return pd.read_csv(file_path, encoding='utf-8')
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def save_processed_data(df, filename="podes_processed.csv"):
    """
    Menyimpan data yang sudah diproses
    """
    try:
        processed_path = Path(__file__).parent.parent / "data" / "processed"
        processed_path.mkdir(exist_ok=True)
        
        file_path = processed_path / filename
        df.to_csv(file_path, index=False, encoding='utf-8')
        return True
    except Exception as e:
        st.error(f"Error saving processed data: {str(e)}")
        return False
