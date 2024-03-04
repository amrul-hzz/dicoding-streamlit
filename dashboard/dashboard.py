import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

df_day = pd.read_csv('data/day.csv')
df_hour = pd.read_csv('data/hour.csv')
df_day_no_out = pd.read_csv('dashboard/day_no_out.csv')
df_hour_no_out = pd.read_csv('dashboard/hour_no_out.csv')


st.title("Proyek Analisis Data: Bike-sharing Dataset")


def question_1():
    seasons_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}

    seasonal_users = df_day_no_out.groupby('season')[['casual', 'registered']].sum().reset_index()
    seasonal_users['season_name'] = seasonal_users['season'].map(seasons_mapping)

    plt.figure(figsize=(10, 6))
    plt.bar(seasonal_users['season_name'], seasonal_users['registered'], label='Registered', color='darkblue')
    plt.bar(seasonal_users['season_name'], seasonal_users['casual'], bottom=seasonal_users['registered'], label='casual', color='lightblue')
    plt.title('Rata-rata Jumlah Penyewaan Sepeda berdasarkan Musim')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')
    plt.legend()

    st.pyplot(plt)

    st.write("""
             Dari musim semi ke musim panas, terdapat kenaikan yang signifikan dalam jumlah rata-rata penyewa. 
             Pada musim semi, jumlah rata-rata penyewa sekitar 400.000 sedangkan pada musim panas naik hampir dua kali lipat menjadi sekitar 700.000. 
             Hal ini juga masuk akal jika dikaitkan dengan hasil uji korelasi pada EDA sebelumnya, dimana suhu mempunyai korelasi positif moderat dengan jumlah penyewa. 
             Akan tetapi, jumlah penyewa paling memuncak di musim gugur. Cuaca musim gugur lebih teduh dari musim panas, tetapi belum sedingin musim dingin jadi cocok sekali untuk bersepeda.
             """)
    
    st.write("### Strategi apa yang dapat kita terapkan untuk menjaga/meningkatkan keterlibatan pengguna sepanjang tahun?")
    st.write("""
                #### 1. Adaptasi terhadap cuaca
                - **Menyertakan aksesoris tambahan**: Selain sewa sepeda, tawarkan pula aksesoris yang dapat membantu penyewa melawan kondisi cuaca yang di luar kendali mereka. Contohnya, menyewakan jas hujan pada pos tempat pengembalian sepeda.
                - **Tambahkan fitur cuaca langsung di aplikasi**: Tingkatkan pengalaman penyewa dengan menambahkan fitur berita cuaca dan sistem _routing_ yang merekomendasikan rute terbaik yang sesuai.

                #### 2. Perbaikan infrastruktur
                - **Bekerjasama dengan pemerintah**: Perbaikan infrastruktur adalah investasi yang baik agar penyewa merasa aman untuk mengendarai sepeda sepanjang tahun. 

                #### 3. Menjalin _partnership_
                - **Diskon pegawai**: Tawarkan diskon untuk kantor/bisnis sekitar agar pegawai terdorong untuk menggunakan sepeda untuk, misalnya, mencari makan siang atau bahkan pulang-pergi.
                - **Paket turis**: Berkolaborasi dengan _tourism boards_ lokal untuk membuat tawaran spesial bagi turis yang berkunjung.
            """)

def question_2():
    df_hour_no_out['day_type'] = df_hour_no_out['weekday'].apply(lambda x: 0 if x in [1, 2, 3, 4, 5] else 1)

    hourly_agg = df_hour_no_out.groupby(['day_type', 'hr'])['cnt'].mean().unstack(0)

    plt.figure(figsize=(14, 7))
    plt.plot(hourly_agg.index, hourly_agg[0], label='Hari Kerja', color='blue', marker='o')
    plt.plot(hourly_agg.index, hourly_agg[1], label='Akhir Pekan', color='red', marker='o')
    plt.title('Rata-rata Jumlah Penyewaan Sepeda berdasarkan Jam: Hari Kerja vs. Akhir Pekan')
    plt.xlabel('Jam')
    plt.xticks(hourly_agg.index)
    plt.grid(axis='y', linestyle='--')
    plt.legend()

    st.pyplot(plt)

    st.write("""
            Didapati bahwa pada hari kerja, jam dengan paling banyak penyewaan adalah sekitar pukul 08.00 dan pukul 17.00-18.00 sedangkan pada akhir pekan adalah sekitar pukul 12.00.
            ### Kita dapat lanjut dengan melakukan analisis kluster terhadap grafik di atas. 
             
            Dari jam-jam yang banyak penyewa, kita dapat memprediksi tipe-tipe penyewa sepeda seperti berikut:
            1. ***Penyewa _Commuting_*** : Puncak jumlah penyewa pada hari kerja pukul 08.00 dan 17.00-18.00 ada di angka yang mirip. Kita dapat berasumsi bahwa ini adalah kelompok penyewa yang menggunakan sepeda untuk pulang-pergi dari tempat kerja
            2. ***Penyewa Jam Makan Siang***: Selain para _commuters_, ada sedikit kenaikan penyewa di hari kerja di dekat pukul 12.00. Ini biasanya adalah jam makan siang, kemungkinan besar ini adalah penyewa yang menggunakan sepeda untuk mencari makan siang di tempat yang sedikit jauh atau hanya ingin jalan-jalan pada jam istirahat mereka.
            3. ***Penyewa Santai***: Pada akhir pekan, hanya terdapat satu puncak yaitu di sekitar pukul 12.00. Biasanya, orang-orang mulai keluar dari rumah untuk bersantai atau jalan-jalan di sekitar jam ini.
            """)
    
    st.write("### Bagaimana kita dapat menyesuaikan ketersediaan sepeda untuk memenuhi permintaan selama waktu-waktu tersebut?")
    st.write("""
            - **Alokasi dinamis**: sesuaikan jumlah sepeda di pos peminjaman dengan jumlah permintaan pada jam tertentu. Misal, menambah jumlah sepeda dekat perkantoran selama jam sibuk.
            - **Kerjasama antar pengguna**: tawarkan insentif (cth: poin bonus) kepada pengguna untuk mengembalikan sepeda ke stasiun sekitar yang membutuhkan lebih banyak sepeda.
            - **Sesuaikan harga**: ratakan permintaan sepanjang hari dengan menurunkan harga pada jam-jam senggang.
            """)

def explore_center_symmetry(df):
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    # select column 
    selected_column = st.selectbox('Select Column to View Histogram', numeric_columns)

    # chart 
    chart = alt.Chart(df).transform_fold(
        numeric_columns
    ).transform_bin(
        'bin',
        field=selected_column,
        bin=alt.Bin(maxbins=20)
    ).mark_bar().encode(
        alt.X('bin:O', title='', axis=alt.Axis(format='.2f')),  # Format x-axis labels to two decimal places
        alt.Y('count()', title='Frequency'),
        alt.Color('key:N', legend=None),
        tooltip=[alt.Tooltip('bin:N', title='Value'), alt.Tooltip('count()', title='Frequency')]
    ).transform_filter(
        alt.datum.key == selected_column
    ).properties(
        width=200,
        height=200
    )

    st.altair_chart(chart, use_container_width=True)

def explore_outliers(df):
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    # select column 
    selected_column = st.selectbox('Select Column', numeric_columns)

    # create a constant field for x-axis
    df['constant'] = selected_column

    # compute quartiles
    q1 = df[selected_column].quantile(0.25)
    q3 = df[selected_column].quantile(0.75)
    iqr = q3 - q1

    # identify outliers
    outliers = df[(df[selected_column] < q1 - 1.5 * iqr) | (df[selected_column] > q3 + 1.5 * iqr)]

    # create box plot
    box_plot = alt.Chart(df).mark_boxplot().encode(
        x=alt.X('constant:N', title=''),  # Use nominal data type with a single category
        y=alt.Y(selected_column, title='Value')
    )

    # create scatter plot for outliers
    scatter_plot = alt.Chart(outliers).mark_circle(color='red', opacity=1, size=100).encode(
        x=alt.X('constant:N'),
        y=alt.Y(selected_column),
        tooltip=[selected_column]
    )

    # combine box plot and outliers
    combined_plot = (box_plot + scatter_plot).properties(
        width=400,
        height=300
    ).configure_axis(
        labelAngle=0 
    )

    st.altair_chart(combined_plot, use_container_width=True)

def explore_relationship(df, title=''):
    numeric_df = df.select_dtypes(include=['number'])

    corr = numeric_df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
    plt.title('Korelasi Pearson - {}'.format(title))
    st.pyplot(plt)

    corr = numeric_df.corr(method='spearman')

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 10})
    plt.title('Korelasi Spearman - {}'.format(title)) 
    st.pyplot(plt)

with st.sidebar:
    st.write(" # Made by **Amanda Nurul Izzah**")
    st.write("Final Project Belajar Analisis Data dengan Python")
    st.write("**Email Dicoding**: amanda.nurul11@ui.ac.id")
    st.write("**Email Bangkit**: m010d4kx1985@bangkit.academy")


tab1, tab2, tab3 = st.tabs(["Hasil dan Kesimpulan", "EDA", "About"])
 
with tab1:
    st.write("## Pertanyaan #1: Bagaimana perubahan musim memengaruhi volume penyewaan sepeda?")
    question_1()

    st.write("## Pertanyaan #2: Bagaimana perubahan musim memengaruhi volume penyewaan sepeda?")
    question_2()

    st.write("""
            ## Kesimpulan
            - Penyewa paling banyak di musim gugur karena cuaca dan suhu paling mendukung untuk bersepeda. 
             Agar jumlah pengguna lebih stabil sepanjang tahun, kita bisa menambahkan jasa dan produk tambahan demi keamanan dan kenyamanan pengguna di berbagai musim.
            - Terdapat 3 tipe alasan utama untuk menyewa sepeda: _commuting_, mencari makan siang, dan bersantai. 
             Sesuaikan alokasi sepeda dan harga sewa dengan jam masing-masing kluster untuk meratakan _demand_.
             """)

with tab2:
    st.write("""
            ## Explore Central Tendency and Symmetry
            Menggunakan histogram, kita dapat melihat distribusi data sekaligus mendapat gambaran tentang simetri data. 
            Kemudian, untuk melihat central tendency dan statistik deskriptif lainnya kita bisa menggunakan `.describe()`.
            Untuk bagian histogram juga memuat outlier sebagai visualisasi sebelum maupun sesudah pembuangan outlier (versi yang sesudah tinggal abaikan saja _extreme tail_ dari masing-masing histogram)
             """)
    st.write("### Data per Hari")
    explore_center_symmetry(df_day)
    st.write("### Data per Jam")
    explore_center_symmetry(df_hour)

    st.write("""
            ## Explore Outliers
            Walaupun sebelumnya kita sudah menciptakan dataframe versi tanpa outlier demi kebersihan data, sebenarnya outlier masih berguna untuk tujuan _exploratory_. 
            Outlier bersifat ekstrim dan "unik" sehingga disini kita akan mencoba melihat apakah ada fenomena yang menarik yang ditandai dengan adanya outlier 
            ataukah outlier disini hanya gejala dari error pada dataset.
            """)
    st.write("### Data per Hari")
    explore_outliers(df_day)
    st.write("""
            Didapati bahwa ada beberapa kolom numerik dengan outlier pada `df_day` sebagai berikut
            - holiday: outlier pada kolom ini sebenarnya tidak aneh karena memang lebih banyak hari keja (0) daripada hari libur (1) jadi bisa diabaikan
            - hum: ada beberapa hari dimana kelembapan lebih jauh lebih rendah dari biasanya
            - windspeed: ada beberapa hari dimana kecepatan angin jauh lebih tinggi dari biasanya
            - casual: ada beberapa hari dimana jumlah pengguna kasual lebih tinggi dari biasanya
             """)
    st.write("### Data per Jam")
    explore_outliers(df_hour)
    st.write("""
            Terdapat lebih banyak kolom dengan outlier pada `df_hour` daripada `df_day`, kemungkinan besar karena `df_hour` berisikan info per jam yang lebih detail dan dapat hilang tergeneralisasi saat diagregasi per harinya. Berikut adalah kolom-kolom pada `df_hour` yang memiliki outlier:
            - holiday: outlier pada kolom ini sebenarnya tidak aneh karena memang lebih banyak hari keja (0) daripada hari libur (1) jadi bisa diabaikan
            - weathersit: ada beberapa jam dimana kondisi cuaca lebih ekstrem dari biasanya
            - hum: ada beberapa jam dimana kelembapan lebih jauh lebih rendah dari biasanya
            - windspeed: ada beberapa jam dimana kecepatan angin jauh lebih tinggi dari biasanya
            - casual: ada beberapa jam dimana jumlah pengguna kasual lebih tinggi dari biasanya
            - registered:  ada beberapa jam dimana jumlah pengguna terdaftar lebih tinggi dari biasanya
            - cnt:  ada beberapa jam dimana jumlah pengguna total lebih tinggi dari biasanya
             """)
    st.write("Ada beberapa fenomena terkait metrik cuaca (kondisi, kelembapan, kecepatan angin) dan jumlah pengguna (kasual atau terdaftar) yang cukup _note-worthy_")

    st.write("""
            ### Explore Relationship
             
             """)
    st.write("""
            ## Explore Relationship
            Untuk mengecek hubungan antar variabel, kita gunakan korelasi. Pada uji korelasi, kita akan menggunakan data tanpa outlier sehingga mendapatkan pola yang lebih umum dan tidak _overfit_ terhadap outlier
            """)
    st.write("### Data per Hari")
    explore_relationship(df_day_no_out, 'Data per Hari')
    st.write("Dari matriks korelasi di atas, terdapat korelasi positif moderat antara suhu dan jumlah penyewa (baik casual maupun registered)")
    st.write("### Data per Jam")
    explore_relationship(df_hour_no_out, 'Data per Jam')
    st.write("Korelasi antara suhu dan jumlah penyewa yang terdaftar (registered) menurun, tetapi untuk penyewa kasual tidak terlalu menurun.")


    st.write("""
            ## Kesimpulan EDA
            Dari beberapa EDA di atas, didapati dua hal yang dirasa cukup menarik dan ingin dikulik lebih lanjut, yaitu cuaca dan jam per hari. Oleh karena itu, diformulasikan pertanyaan bisnis sebagai berikut:
            - Bagaimana perubahan musim memengaruhi volume penyewaan sepeda? (anggapannya cuaca akan berubah sesuai musim)
            - Kapan waktu puncak untuk penyewaan sepeda pada hari kerja dibandingkan dengan akhir pekan?
            """)

with tab3:
    st.markdown("Original Dataset: [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)")
