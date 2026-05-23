import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Sayfa başlığı
st.set_page_config(page_title="2026 Proje Anket & Grafik", layout="centered")

# --- ŞİFRELEME MEKANİZMASI ---
DOGRU_SIFRE = "ForJustice0214"

if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False

if not st.session_state.giris_yapildi:
    st.title("🔒 Giriş Yapın")
    st.write(
        "Bu arayüze erişmek için lütfen size verilen erişim şifresini giriniz."
    )
    girilen_sifre = st.text_input("Şifre:", type="password")

    if st.button("Giriş Yap"):
        if girilen_sifre == DOGRU_SIFRE:
            st.session_state.giris_yapildi = True
            st.success("Şifre doğru! Sayfa yükleniyor...")
            st.rerun()
        else:
            st.error("Hatalı şifre girdiniz! Lütfen tekrar deneyin.")
    st.stop()


# --- ANKET VE GRAFİK ARAYÜZÜ ---
st.markdown("## 👋 Hoş Geldiniz")
st.title("📊 Anket Sonuçları ve Canlı Grafik")

if st.sidebar.button("Güvenli Çıkış"):
    st.session_state.giris_yapildi = False
    st.rerun()

# Hafızada anket verilerini tutmak için alan (Memnuniyet sütununu da ekledik)
if "anket_verileri" not in st.session_state:
    st.session_state.anket_verileri = pd.DataFrame(
        columns=["Cinsiyet", "Yapay_Zeka_Kullanimi", "Memnuniyet"]
    )

st.subheader("Ankete Katılın")

# Arayüzü 3 sütuna bölüyoruz
col1, col2, col3 = st.columns(3)

with col1:
    cinsiyet = st.radio("Cinsiyetiniz:", ("Kadın", "Erkek"))

with col2:
    yz_kullanimi = st.radio(
        "Yapay zeka araçları kullanıyor musunuz?:", ("Evet", "Hayır")
    )

with col3:
    # 1'den 5'e kadar memnuniyet puanı seçimi (Slider - kaydırma çubuğu ile)
    memnuniyet = st.slider(
        "Sistemden memnun musunuz? (1-5):",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
    )

# Oyla Butonu
if st.button("Cevabı Kaydet ve Grafiğe Ekle"):
    yeni_cevap = pd.DataFrame(
        [
            {
                "Cinsiyet": cinsiyet,
                "Yapay_Zeka_Kullanimi": yz_kullanimi,
                "Memnuniyet": memnuniyet,
            }
        ]
    )
    st.session_state.anket_verileri = pd.concat(
        [st.session_state.anket_verileri, yeni_cevap], ignore_index=True
    )
    st.success("Cevabınız kaydedildi!")

# --- GRAFİKLER BÖLÜMÜ ---

st.subheader("📊 Güncel Grafik Sonuçları")
df = st.session_state.anket_verileri

if df.empty:
    st.info(
        "Henüz hiç veri girişi yapılmadı. Yukarıdan seçim yapıp butona basın."
    )
else:
    st.metric(label="Toplam Katılımcı Sayısı", value=len(df))

    # YAN YANA İKİ GRAFİK GÖSTERMEK İÇİN MATPLOTLIB MATRİSİ AYARLIYORUZ
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    sns.set_theme(style="whitegrid")

    # 1. Grafik: Eski Grafik (Cinsiyet ve Kullanım)
    sns.countplot(
        x="Cinsiyet",
        hue="Yapay_Zeka_Kullanimi",
        data=df,
        palette="muted",
        ax=ax1,
        order=["Kadın", "Erkek"],
        hue_order=["Evet", "Hayır"],
    )
    ax1.set_title("Cinsiyete Göre Kullanım", fontsize=12, pad=10)
    ax1.set_xlabel("Cinsiyet")
    ax1.set_ylabel("Kişi Sayısı")
    ax1.legend(title="YZ Kullanımı")

    # 2. Grafik: Yeni Grafik (Memnuniyet Puan Dağılımı)
    # Burada 1'den 5'e kadar olan puanların kaçar tane seçildiğini sayıyoruz
    sns.countplot(
        x="Memnuniyet",
        data=df,
        palette="crest",
        ax=ax2,
        order=[1, 2, 3, 4, 5],
    )
    ax2.set_title("Sistem Memnuniyet Puanları (1-5)", fontsize=12, pad=10)
    ax2.set_xlabel("Verilen Puan")
    ax2.set_ylabel("Kişi Sayısı")

    # Sütunların üzerine sayıları yazdırma
    for ax in [ax1, ax2]:
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(
                    f"{int(height)}",
                    (p.get_x() + p.get_width() / 2.0, height),
                    ha="center",
                    va="center",
                    xytext=(0, 5),
                    textcoords="offset points",
                )

    # Grafikleri ekrana bas
    st.pyplot(fig)