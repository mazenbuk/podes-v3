# 🏘️ Data Desa Dalam Genggaman - PODES 2024

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📊 Overview

**Data Desa Dalam Genggaman** adalah aplikasi dashboard interaktif untuk menganalisis data **Potensi Desa (PODES) 2024** wilayah Kota Batu (kode 3579). Aplikasi ini membantu visualisasi dan analisis kondisi infrastruktur dan fasilitas di tingkat desa.

## ✨ Features

### 🎯 **Dashboard Overview**
- **Prioritas Urgent**: Analisis fasilitas yang memerlukan perhatian segera
- **Indikator KPI**: Metrics lengkap dengan angka konkrit
- **Filter Kecamatan**: Analisis per kecamatan atau seluruh kota
- **Status Capaian**: Ringkasan kondisi setiap indikator

### 🏷️ **Analisis Per Desa**
- **Status Fasilitas**: Visual cards untuk data binary (ada/tidak ada)
- **Prioritas Pembangunan**: Donut chart untuk rekomendasi prioritas
- **Perbandingan Radar**: Comparison dengan desa lain
- **Ranking Kecamatan**: Posisi desa di tingkat kecamatan
- **Smart Insights**: Analisis otomatis dengan rekomendasi

### 🎨 **UI/UX**
- **Dark Mode**: Interface gelap dengan kontras tinggi
- **Responsive Design**: Optimal di berbagai ukuran layar
- **Clean Layout**: Tanpa toolbar download yang mengganggu
- **Consistent Styling**: Header dan card yang seragam

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone repository**
```bash
git clone https://github.com/haikalthrq/podes-v3.git
cd podes-v3
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run aplikasi**
```bash
streamlit run app.py
```

4. **Buka browser**
```
http://localhost:8501
```

## 📁 Project Structure

```
podes-v3/
├── app.py                 # Landing page aplikasi
├── requirements.txt       # Dependencies
├── README.md             # Dokumentasi
├── .gitignore           # Git ignore rules
├── data/
│   └── raw/
│       ├── master_podes_desa.csv      # Data PODES 2024
│       ├── podes_dictionary.md        # Data dictionary
│       └── Kuesioner Podes 2024 - Desa.pdf
├── src/                              # Source code modules
│   ├── __init__.py
│   ├── loader.py                     # Data loading functions
│   ├── indicators.py                 # Indikator calculations
│   └── ui_helpers.py                 # UI helper functions
├── pages/                            # Streamlit pages
│   ├── 1_📊_Overview.py             # Dashboard overview
│   └── 2_🏷️_Per_Desa.py           # Analisis per desa
└── notebooks/                        # Jupyter notebooks
    └── EDA_PODES.ipynb              # Exploratory Data Analysis
```

## 📊 Data Overview

### Dataset
- **Source**: PODES (Potensi Desa) 2024
- **Scope**: Kota Batu (kode wilayah 3579)
- **Coverage**: 24 desa, 3 kecamatan
- **Records**: 638 RT/RW teragregasi ke level desa

### Key Indicators
#### 🚨 **Prioritas Urgent**
- **TPS3R**: Tempat Pengolahan Sampah 3R
- **Poskesdes**: Pos Kesehatan Desa  
- **Air Layak**: Akses air bersih layak minum
- **Sistem Peringatan**: Sistem peringatan dini bencana

#### 📈 **Indikator Lengkap**
- Fasilitas kesehatan (Bidan, Pustu, Apotek)
- Infrastruktur (Jalan aspal, Angkutan umum)
- Digital (Internet 4G, Kantor online)
- Lingkungan (Bank sampah, Jamban layak)

## 🛠️ Technical Stack

- **Framework**: Streamlit 1.28+
- **Visualization**: Plotly 5.15+
- **Data Processing**: Pandas 2.0+
- **Styling**: CSS dengan dark mode theme
- **Deployment**: Ready for Streamlit Cloud

## 📈 Usage Examples

### 1. **Analisis Prioritas Urgent**
```python
# Lihat desa yang belum memiliki TPS3R
urgent_tps3r = df[df['has_tps3r'] == 0]
print(f"Desa tanpa TPS3R: {len(urgent_tps3r)} dari 24 desa")
```

### 2. **Filter per Kecamatan** 
```python
# Analisis khusus Kecamatan Batu
kec_batu = df[df['NAMA_KEC'] == 'BATU']
coverage = kec_batu['has_poskesdes'].mean() * 100
print(f"Coverage Poskesdes di Kec. Batu: {coverage:.1f}%")
```

## 🎯 Key Insights

### 🔴 **Critical Issues**
- **83.3%** desa belum memiliki TPS3R (20/24 desa)
- **75%** desa belum memiliki Poskesdes (18/24 desa)
- **66.7%** desa belum memiliki akses air layak (16/24 desa)

### ✅ **Strong Areas**
- **100%** desa memiliki Internet 4G
- **100%** desa memiliki Kantor Online
- **95.8%** desa memiliki Praktik Bidan

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

Project ini menggunakan data publik PODES 2024 dari BPS.

## 👥 Contact

- **Developer**: Haikal Thoriq
- **GitHub**: [@haikalthrq](https://github.com/haikalthrq)
- **Repository**: [podes-v3](https://github.com/haikalthrq/podes-v3)

---

**🚀 Built with ❤️ using Streamlit | 📊 Powered by PODES 2024 Data**
