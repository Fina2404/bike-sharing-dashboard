import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("day_clean.csv")
day_df['date'] = pd.to_datetime(day_df['date'])
hour_df = pd.read_csv("hour_clean.csv")
hour_df['date'] = pd.to_datetime(hour_df['date'])

# Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# --- Sidebar: Filter Tanggal ---
st.sidebar.header("Filter Data Berdasarkan Tanggal")
min_date = day_df['date'].min()
max_date = day_df['date'].max()
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

st.sidebar.title("Proyek Analisis Data")
st.sidebar.markdown("""
**Nama:** Fina Dwi Aulia  
**Email:** mc671d5x0251@student.devacademy.id  
**ID Dicoding:** fina24  
""")

# Konversi ke datetime untuk filtering
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan tanggal yang dipilih
filtered_day_df = day_df[(day_df['date'] >= start_date) & (day_df['date'] <= end_date)]
filtered_hour_df = hour_df[(hour_df['date'] >= start_date) & (hour_df['date'] <= end_date)]

# --- Navigasi Menggunakan Tabs ---
tabs = st.tabs(["🏠 Home", "📊 Pertanyaan 1", "📊 Pertanyaan 2", "📌 Kesimpulan", "📑 Semua Data"])

# --- Halaman Home ---
with tabs[0]:  
    st.title("🚴‍♂️ Bike Sharing Dashboard")
    st.image("bike_image.jpg", use_container_width=True)
    st.markdown("Selamat datang di dashboard analisis data **Bike Sharing Dataset**. Pilih tab di atas untuk mulai eksplorasi data!")

# --- Halaman Pertanyaan 1 ---
with tabs[1]:  
    st.title("📊 Pertanyaan 1")
    st.subheader("Bagaimana pola penggunaan sepeda antara pengguna kasual dan terdaftar pada hari kerja vs. akhir pekan?")
    
    # Mengelompokkan data
    day_group = filtered_day_df.groupby(['workingday'])[['casual', 'registered']].mean()
    
    # Plot
    # --- Plot perbandingan pengguna kasual vs. terdaftar pada hari kerja dan akhir pekan ---
    fig, ax = plt.subplots(figsize=(8, 5))
    day_group.plot(kind="bar", stacked=False, colormap="RdBu", ax=ax)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Akhir Pekan", "Hari Kerja"], rotation=0)
    ax.set_xlabel("Kategori Hari")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.set_title("Pola Penggunaan Sepeda: Kasual vs. Terdaftar (Hari Kerja vs. Akhir Pekan)")
    ax.legend(["Pengguna Kasual", "Pengguna Terdaftar"])
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Menentukan batas atas sumbu y agar tidak terpotong
    max_value = day_group[['casual', 'registered']].max().max()
    ax.set_ylim(0, max_value * 1.2)

    # Menambahkan label di atas setiap batang
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.text(
                p.get_x() + p.get_width() / 2, 
                height + (max_value * 0.05), 
                f"{int(height)}", 
                ha="center", va="bottom", fontsize=10, color="black"
            )

    # Tampilkan plot di Streamlit
    st.pyplot(fig)


    st.markdown("### 🔍 Insight:")
    st.markdown("- **Pengguna kasual** lebih banyak menggunakan sepeda pada akhir pekan.")
    st.markdown("- **Pengguna terdaftar** lebih banyak menggunakan sepeda pada hari kerja, terutama saat jam sibuk.")

# --- Halaman Pertanyaan 2 ---
with tabs[2]:  
    st.title("📊 Pertanyaan 2")
    st.subheader("Pada jam berapa dan di hari apa stok sepeda perlu ditambah untuk memenuhi permintaan tinggi?")
    
    # Heatmap permintaan
    hour_group = filtered_hour_df.pivot_table(values='count', index='hour', columns='weekday', aggfunc='mean')
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.heatmap(hour_group, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=0.5, ax=ax2)
    ax2.set_xlabel("Hari dalam Seminggu")
    ax2.set_ylabel("Jam")
    ax2.set_title("Heatmap Permintaan Sepeda per Jam dan Hari")
    ax2.set_xticks(range(7))
    ax2.set_xticklabels(["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
    
    # Tampilkan heatmap
    st.pyplot(fig2)

    st.markdown("### 🔍 Insight:")
    st.markdown("- **Puncak peminjaman** terjadi pada sore hari (16:00 - 19:00), terutama hari kerja.")
    st.markdown("- **Hari dengan permintaan tertinggi** adalah Selasa sore dan Jumat sore.")
    st.markdown("- **Akhir pekan** menunjukkan pola peminjaman lebih merata sepanjang hari.")

# --- Halaman Kesimpulan ---
with tabs[3]:  
    st.title("📌 Kesimpulan")

    st.markdown("### 1️⃣ Pola Penggunaan Sepeda antara Pengguna Kasual dan Terdaftar")
    st.markdown("- Pengguna terdaftar dominan pada hari kerja, terutama saat jam sibuk pagi (07:00 - 09:00) dan sore (17:00 - 19:00).")
    st.markdown("- Pengguna kasual lebih sering menggunakan sepeda pada akhir pekan untuk rekreasi, dengan puncak di siang hingga sore hari (10:00 - 17:00).")
    st.markdown("- Pada akhir pekan, jumlah pengguna kasual bisa melebihi pengguna terdaftar.")

    st.markdown("### 2️⃣ Waktu dan Hari untuk Menambah Stok Sepeda")
    st.markdown("- **Hari kerja:** Stok sepeda perlu ditambah pada jam 07:00 - 09:00 dan 17:00 - 19:00.")
    st.markdown("- **Akhir pekan:** Stok sepeda perlu lebih banyak tersedia pada siang hari (10:00 - 17:00).")
    st.markdown("- **Hari dengan permintaan tertinggi:** Jumat sore dan Sabtu siang hingga sore.")

# --- Halaman Semua Data ---
with tabs[4]:  
    st.title("📑 Semua Data - Bike Sharing Dataset")

    # --- Tampilkan Data ---
    st.subheader("📌 Dataset Harian")
    st.dataframe(filtered_day_df)

    st.subheader("📌 Dataset Per Jam")
    st.dataframe(filtered_hour_df)

    # --- Visualisasi 1: Pola Penggunaan Kasual vs Terdaftar ---
    st.subheader("📊 Pola Penggunaan Sepeda: Kasual vs Terdaftar")
    # --- Plot perbandingan pengguna kasual vs. terdaftar pada hari kerja dan akhir pekan ---
    fig1, ax = plt.subplots(figsize=(8, 5))
    day_group.plot(kind="bar", stacked=False, colormap="RdBu", ax=ax)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Akhir Pekan", "Hari Kerja"], rotation=0)
    ax.set_xlabel("Kategori Hari")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.set_title("Pola Penggunaan Sepeda: Kasual vs. Terdaftar (Hari Kerja vs. Akhir Pekan)")
    ax.legend(["Pengguna Kasual", "Pengguna Terdaftar"])
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Menentukan batas atas sumbu y agar tidak terpotong
    max_value = day_group[['casual', 'registered']].max().max()
    ax.set_ylim(0, max_value * 1.2)

    # Menambahkan label di atas setiap batang
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.text(
                p.get_x() + p.get_width() / 2, 
                height + (max_value * 0.05), 
                f"{int(height)}", 
                ha="center", va="bottom", fontsize=10, color="black"
            )

    # Tampilkan plot di Streamlit
    st.pyplot(fig1)


    # --- Visualisasi 2: Heatmap Permintaan Sepeda ---
    st.subheader("📊 Heatmap Permintaan Sepeda per Jam dan Hari")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.heatmap(hour_group, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=0.5, ax=ax2)
    ax2.set_xlabel("Hari dalam Seminggu")
    ax2.set_ylabel("Jam")
    ax2.set_title("Heatmap Permintaan Sepeda per Jam dan Hari")
    ax2.set_xticks(range(7))
    ax2.set_xticklabels(["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"])
    st.pyplot(fig2)

    # --- Statistik Ringkasan ---
    st.subheader("📊 Statistik Ringkasan Dataset Harian")
    st.write(filtered_day_df.describe())

    st.subheader("📊 Statistik Ringkasan Dataset Per Jam")
    st.write(filtered_hour_df.describe())