📈 Hisse Senedi Fiyatı Tahmini — LSTM & GRU (PyTorch)

Amazon (AMZN) hissesinin geçmiş fiyat verilerini kullanarak gelecekteki fiyatı tahmin eden, PyTorch ile sıfırdan geliştirilmiş bir zaman serisi regresyon projesi. Proje; veri hazırlığından model eğitimine, model karşılaştırmasından bir REST API ve web arayüzüne kadar uçtan uca bir makine öğrenmesi iş akışını kapsar.

🎯 Projenin Amacı

Bu proje, makine öğrenmesi ve derin öğrenmenin temellerinden başlanarak, gerçek dünya verisiyle çalışan, karşılaştırmalı bir zaman serisi tahmin sistemi geliştirmek amacıyla oluşturuldu. Sadece bir model eğitmekle kalınmadı; sonuçlar sistematik olarak değerlendirildi, hiperparametre ayarlaması yapıldı ve model bir web servisine (API + arayüz) dönüştürüldü.

✨ Özellikler
📊 Gerçek Amazon (AMZN) hisse senedi verisi (2006–2018) ile eğitim
🧠 PyTorch ile sıfırdan yazılmış LSTM ve GRU modelleri
⚖️ İki mimarinin sistematik karşılaştırması (RMSE bazlı)
🔧 Hiperparametre ayarlaması (lookback penceresi optimizasyonu)
🚀 Eğitilmiş modeli sunan FastAPI backend'i
🖥️ Streamlit ile interaktif web arayüzü
📓 Haftalık olarak organize edilmiş, öğrenme sürecini belgeleyen Jupyter Notebook'lar
🛠️ Kullanılan Teknolojiler
Katman	Teknoloji
Dil	Python 3.13
Derin Öğrenme	PyTorch
Veri İşleme	Pandalar, NumPy
Ölçekleme	Scikit-learn (MinMaxScaler)
Görselleştirme	Matplotlib
Backend / API	FastAPI, Uvicorn
Ön uç	Akıcı Aydınlatma
Ortam Yönetimi	venv
Versiyon Kontrolü	Git & GitHub
📁 Proje Yapısı
stock-price-prediction/
├── README.md
├── requirements.txt
├── .gitignore
├── app.py                      # Streamlit web arayüzü (tahmin ekranı)
├── data/
│   └── amzn_stock.csv          # Ham veri (AMZN, 2006-2018)
├── models/
│   ├── gru_model.pth           # Eğitilmiş GRU model ağırlıkları
│   └── scaler.pkl              # Kayıtlı MinMaxScaler nesnesi
├── backend/
│   └── main.py                 # FastAPI tahmin servisi (REST API)
└── notebooks/
    ├── week1/                  # ML temelleri, mini regresyon alıştırması
    ├── week2/                  # PyTorch temelleri (tensor, autograd, nn.Module)
    ├── week4/                  # Veri hazırlığı, ölçekleme, sliding window
    └── week5/                  # LSTM & GRU eğitimi, karşılaştırma, hiperparametre ayarlaması
📊 Veri Seti
Kaynak: Kaggle — DJIA 30 Stok Zaman Serisi
Kapsam: Amazon (AMZN) hissesi, 2006-01-03 – 2017-12-29 arası günlük veriler
Kullanılan sütun: (kapanış fiyatı)Close
Örnek sayısı: ~3.019 işlem günü
🧪 Metodoloji
Veri Hazırlığı
Kapanış fiyatları ile [-1, 1] aralığına ölçeklendiMinMaxScaler
"Sliding window" (kayan pencere) yöntemiyle, geçmiş N günlük fiyat dizisinden bir sonraki günü tahmin eden örnekler oluşturuldu (N=30)
Veri, zaman sırası korunarak (karıştırılmadan) %80 eğitim / %20 test olarak ayrıldı — zaman serisinde rastgele karıştırma veri sızıntısına yol açacağından kullanılmadı
Model Mimarisi
Her iki model de aynı yapı kullanır: , , , input_size=1hidden_size=32num_layers=2output_size=1
LSTM: 3 kapılı (unutma, giriş, çıkış) hafıza mekanizması + ayrı hücre durumu
GRU: 2 kapılı (reset, update), daha az parametreli, daha basit yapı
Eğitim
Kayıp fonksiyonu: MSELoss
Optimize edici: (lr=0.001)Adam
Epoch sayısı: 200
Hiperparametre ayarlaması: lookback penceresi 20 → 30 güne çıkarılarak test edildi
📈 Sonuçlar
Model	Geçmişe Bakış	Dönem	Test RMSE (ölçekli)
LSTM	20	200	0.508
GRU	20	200	0.186
LSTM	30	200	0.454
GRU	30	200	0.089
🔑 Temel Bulgular
GRU, tüm denemelerde LSTM'den daha düşük test hatası elde etti.
Lookback penceresini 20'den 30 güne çıkarmak her iki modeli de iyileştirdi; ancak GRU bundan (%52 iyileşme) LSTM'e (%11 iyileşme) çok daha fazla fayda gördü. Bu, GRU'nun bu veri setinde daha uzun geçmiş bağlamı daha verimli kullandığını, LSTM'in daha karmaşık iç yapısının aynı eğitim süresinde bu ekstra bilgiyi tam değerlendiremediğini düşündürüyor.
Modeller genel fiyat trendini başarıyla takip edebiliyor, ancak özellikle hızlı yükseliş dönemlerinde gerçek fiyatın bir miktar altında kalma eğiliminde — zaman serisi tahmininde sıkça karşılaşılan bir "gecikme" (lag) davranışı.
Bu sonuçlar, hisse senedi fiyat tahmininin doğası gereği zor bir problem olduğunu ve modellerin sınırlamalarının şeffaf biçimde ele alınması gerektiğini bir kez daha doğruluyor.
🚀 Kurulum ve Çalıştırma
1. Ortamı hazırlayın
Bash
git clone https://github.com/gokdenizasik/stock-price-prediction.git
cd stock-price-prediction

python -m venv venv
.\venv\Scripts\Activate.ps1      # Windows
# source venv/bin/activate       # macOS/Linux

pip install -r requirements.txt
2. Notebook'ları inceleyin
Bash
jupyter lab

notebooks/week5/lstm_gru_models.ipynb dosyasını açarak veri hazırlığından model karşılaştırmasına kadar tüm süreci adım adım görebilirsiniz.

3. Backend'i (API) çalıştırın
Bash
cd backend
uvicorn main:app --reload

API varsayılan olarak adresinde çalışır. İnteraktif dokümantasyon için adresini ziyaret edebilirsiniz.http://127.0.0.1:8000http://127.0.0.1:8000/docs

Örnek istek (POST /tahmin):

JSON
{
  "prices": [123.4, 125.1, 124.8, "... (toplam 30 değer)"]
}

Örnek yanıt:

JSON
{
  "predicted_price": 128.75
}
4. Frontend'i (Streamlit) çalıştırın

Proje kök dizininde:

Bash
streamlit run app.py

Tarayıcınızda otomatik olarak açılan arayüzden hisse fiyatlarını girip tahmin alabilirsiniz.

🔮 Gelecek Geliştirmeler
 LSTM için daha uzun eğitim (400+ epoch) ile GRU farkının kapanıp kapanmadığını test etmek
 Ek özellikler eklemek (Volume, Open/High/Low)
 Farklı hisse senetleri ile genelleme testi
 Attention mekanizmaları veya Transformer tabanlı modellerle karşılaştırma
 Backend'i bulut ortamına (Render/Railway) deploy etmek
📚 Öğrenme Süreci

Bu proje, sıfırdan (Python/PyTorch deneyimi olmadan) başlanarak 6 haftalık yapılandırılmış bir öğrenme programıyla geliştirilmiştir. Süreç; ML temelleri, PyTorch temelleri (tensor, autograd, gradient descent), RNN/LSTM/GRU teorisi ve uçtan uca proje uygulamasını kapsamaktadır. Detaylı haftalık ilerleme klasöründeki notebook'larda belgelenmiştir.notebooks/

⚠️ Sorumluluk Reddi

Bu proje eğitim amaçlıdır. Üretilen tahminler gerçek yatırım kararları için kullanılmamalıdır. Hisse senedi piyasaları çok sayıda öngörülemeyen faktörden etkilenir ve geçmiş veriye dayalı modeller gelecekteki performansı garanti etmez.

👤 İletişim

Gökdeniz Aşık GitHub: @gokdenizasik