"""
Indicators Module - PODES 2024
Modul untuk menghitung indikator dari data PODES
"""

import pandas as pd
import numpy as np

def get_kpi_indicators():
    """
    Mengembalikan daftar indikator KPI utama - fokus pada yang urgent dan meaningful
    """
    return [
        # Prioritas Urgent (Coverage rendah)
        'has_tps3r',        # 16.7% - SANGAT URGENT
        'ada_poskesdes',    # 25.0% - SANGAT URGENT  
        'air_layak',        # 33.3% - URGENT
        'sistem_peringatan', # 50.0% - URGENT
        
        # Indikator Sedang (Perlu Peningkatan)
        'ada_apotek',       # 75.0% - Perlu peningkatan
        'ada_angkutan',     # Transportasi umum
        
        # Indikator Baik (Monitoring)
        'ada_bidan',        # 95.8% - Sangat baik
        'internet_4g',      # 100% - Monitoring
        'kantor_online'     # 100% - Monitoring
    ]

def create_blok_v_indicators(df):
    """
    Menghitung indikator Blok V - Fasilitas Lingkungan & Perumahan
    """
    df = df.copy()
    
    # TPS3R (R504D: 1=Ada digunakan, 2=Ada tidak digunakan, 3=Tidak ada)
    if 'R504D' in df.columns:
        df['has_tps3r'] = (df['R504D'] == 1).astype(int)
    else:
        df['has_tps3r'] = 0
    
    # Bank Sampah (R504E: 1=Ada, 2=Tidak ada)
    if 'R504E' in df.columns:
        df['has_bank_sampah'] = (df['R504E'] == 1).astype(int)
    else:
        df['has_bank_sampah'] = 0
    
    # Air Layak - PDAM atau sumur bor (R508A: 3=PDAM meter, 4=PDAM non-meter, 5=Sumur bor/pompa)
    if 'R508A' in df.columns:
        df['air_layak'] = (df['R508A'].isin([3, 4, 5])).astype(int)  # PDAM, sumur bor/pompa
    else:
        df['air_layak'] = 0
    
    # Jamban Layak - jamban sendiri/bersama (R506A: 1=Jamban sendiri, 2=Jamban bersama, 3=Jamban umum)
    if 'R506A' in df.columns:
        df['jamban_layak'] = (df['R506A'].isin([1, 2])).astype(int)  # Jamban sendiri/bersama
    else:
        df['jamban_layak'] = 0
    
    return df

def create_blok_vi_indicators(df):
    """
    Menghitung indikator Blok VI - Bencana Alam & Mitigasi
    """
    df = df.copy()
    
    # Ada potensi bencana - menggunakan kolom R601AK2 (ada korban bencana)
    if 'R601AK2' in df.columns:
        df['ada_bencana'] = (df['R601AK2'] > 0).astype(int)
    else:
        df['ada_bencana'] = 0
    
    # Sistem Peringatan Dini (R604A: 1=Ada, 2=Tidak ada)
    if 'R604A' in df.columns:
        df['sistem_peringatan'] = (df['R604A'] == 1).astype(int)
    else:
        df['sistem_peringatan'] = 0
    
    return df

def create_blok_vii_indicators(df):
    """
    Menghitung indikator Blok VII - Akses & Transportasi
    """
    df = df.copy()
    
    # Jalan Aspal/Beton (R1001B1: 1=Aspal/beton, 2=Diperkeras/kerikil/batu, 3=Tanah, 4=Lainnya)
    if 'R1001B1' in df.columns:
        df['jalan_aspal'] = (df['R1001B1'] == 1).astype(int)  # Aspal/beton
    else:
        df['jalan_aspal'] = 0
    
    # Ada angkutan umum (R1001C1: 1=Ada dengan trayek tetap, 2=Ada tanpa trayek tetap, 3=Tidak ada)
    if 'R1001C1' in df.columns:
        df['ada_angkutan'] = (df['R1001C1'].isin([1, 2])).astype(int)  # Ada (dengan/tanpa trayek)
    else:
        df['ada_angkutan'] = 0
    
    return df

def create_blok_x_indicators(df):
    """
    Menghitung indikator Blok X - Teknologi Informasi & Komunikasi
    """
    df = df.copy()
    
    # Internet 4G+ (R1005D: 1=5G/4G/LTE, 2=3G/H/H+/EVDO, 3=2.5G/EDGE/GPRS, 4=Tidak ada sinyal internet)
    if 'R1005D' in df.columns:
        df['internet_4g'] = (df['R1005D'] == 1).astype(int)  # 5G/4G/LTE
    else:
        df['internet_4g'] = 0
    
    # Layanan online kantor desa (R1006B: 1=Berfungsi, 2=Jarang berfungsi, 3=Tidak berfungsi, 4=Tidak ada)
    if 'R1006B' in df.columns:
        df['kantor_online'] = (df['R1006B'] == 1).astype(int)  # Berfungsi
    else:
        df['kantor_online'] = 0
    
    return df

def calculate_health_indicators(df):
    """
    Menghitung indikator kesehatan dari Blok VII
    """
    df = df.copy()
    
    # Poskesdes (Pos Kesehatan Desa) - R704JK2 > 0 berarti ada poskesdes
    if 'R704JK2' in df.columns:
        df['ada_poskesdes'] = (df['R704JK2'] > 0).astype(int)
    else:
        df['ada_poskesdes'] = 0
    
    # Tempat praktik bidan - R704IK2 > 0 berarti ada praktik bidan
    if 'R704IK2' in df.columns:
        df['ada_bidan'] = (df['R704IK2'] > 0).astype(int)
    else:
        df['ada_bidan'] = 0
    
    # Puskesmas pembantu - R704EK2 > 0 berarti ada puskesmas pembantu
    if 'R704EK2' in df.columns:
        df['ada_pustu'] = (df['R704EK2'] > 0).astype(int)
    else:
        df['ada_pustu'] = 0
    
    # Apotek - R704LK2 > 0 berarti ada apotek
    if 'R704LK2' in df.columns:
        df['ada_apotek'] = (df['R704LK2'] > 0).astype(int)
    else:
        df['ada_apotek'] = 0
    
    # Taman Bacaan Masyarakat - R702C == 1 berarti ada TBM
    if 'R702C' in df.columns:
        df['ada_tbm'] = (df['R702C'] == 1).astype(int)
    else:
        df['ada_tbm'] = 0
    
    return df

def calculate_all_indicators(df):
    """
    Menghitung semua indikator untuk semua blok
    """
    df = df.copy()
    
    # Hitung indikator per blok
    df = create_blok_v_indicators(df)
    df = create_blok_vi_indicators(df)
    df = create_blok_vii_indicators(df)
    df = create_blok_x_indicators(df)
    df = calculate_health_indicators(df)  # Tambahkan indikator kesehatan
    
    return df

def get_block_summary(df):
    """
    Mengembalikan ringkasan per blok
    """
    summary = {}
    
    # Blok V
    blok_v_indicators = ['has_tps3r', 'has_bank_sampah', 'air_layak', 'jamban_layak']
    summary['Blok V'] = {
        'indicators': blok_v_indicators,
        'mean': df[blok_v_indicators].mean().mean() if all(col in df.columns for col in blok_v_indicators) else 0
    }
    
    # Blok VI  
    blok_vi_indicators = ['ada_bencana', 'sistem_peringatan']
    summary['Blok VI'] = {
        'indicators': blok_vi_indicators,
        'mean': df[blok_vi_indicators].mean().mean() if all(col in df.columns for col in blok_vi_indicators) else 0
    }
    
    # Blok VII
    blok_vii_indicators = ['jalan_aspal', 'ada_angkutan']
    summary['Blok VII'] = {
        'indicators': blok_vii_indicators,
        'mean': df[blok_vii_indicators].mean().mean() if all(col in df.columns for col in blok_vii_indicators) else 0
    }
    
    # Blok X
    blok_x_indicators = ['internet_4g', 'kantor_online']
    summary['Blok X'] = {
        'indicators': blok_x_indicators,
        'mean': df[blok_x_indicators].mean().mean() if all(col in df.columns for col in blok_x_indicators) else 0
    }
    
    return summary
