import streamlit as st
import requests
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Hisse Senedi Tahmin Paneli",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Hisse Fiyat Tahmini Paneli (GRU Modeli)")
st.markdown("Yahoo Finance verisi ve PyTorch derin öğrenme modeli ile anlık fiyat tahmini.")

# Kullanıcı Girdisi
col_input, col_btn = st.columns([3, 1])
with col_input:
    ticker = st.text_input(
        "Hisse Kodu Girin (BIST için THYAO, ASELS veya yabancı hisseler için AAPL, TSLA):",
        value="THYAO"
    )

with col_btn:
    st.write("") # Hizalama boşluğu
    st.write("")
    predict_btn = st.button("Tahmin Getir", use_container_width=True)

if predict_btn:
    clean_ticker = ticker.strip()
    if not clean_ticker:
        st.warning("Lütfen geçerli bir hisse kodu yazın.")
    else:
        with st.spinner(f"{clean_ticker} için veriler çekiliyor ve model çalıştırılıyor..."):
            try:
                # FastAPI backend servisine istek at
                response = requests.get(f"http://127.0.0.1:8000/predict?ticker={clean_ticker}")
                
                if response.status_code == 200:
                    data = response.json()
                    currency = data.get("currency", "$")

                    st.success(f"{data['ticker']} için tahmin başarıyla oluşturuldu!")

                    # Metrik Kartları
                    c1, c2, c3 = st.columns(3)
                    c1.metric(
                        label="Hisse Sembolü", 
                        value=data["ticker"]
                    )
                    c2.metric(
                        label="Son Kapanış Fiyatı", 
                        value=f"{data['last_price']} {currency}"
                    )
                    c3.metric(
                        label="Tahmini Gelecek Fiyat", 
                        value=f"{data['predicted_price']} {currency}",
                        delta=f"{data['change_percent']}%"
                    )

                    st.divider()

                    # Grafik Bölümü
                    st.subheader("📊 Son 15 Günün Fiyat Değişim Grafiği")
                    df_history = pd.DataFrame(data["history"])
                    df_history["date"] = pd.to_datetime(df_history["date"])
                    df_history.set_index("date", inplace=True)
                    df_history.rename(columns={"price": f"Kapanış Fiyatı ({currency})"}, inplace=True)

                    st.line_chart(df_history)

                else:
                    detail = response.json().get("detail", "Bilinmeyen bir hata oluştu.")
                    st.error(f"Tahmin alınamadı: {detail}")

            except requests.exceptions.ConnectionError:
                st.error("FastAPI backend sunucusuna bağlanılamadı! Lütfen terminalde `python -m uvicorn main:app --port 8000` komutunun çalıştığından emin olun.")
            except Exception as e:
                st.error(f"Beklenmeyen bir hata oluştu: {str(e)}")