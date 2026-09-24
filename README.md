# Hisse Senedi Fiyatı Tahmini (LSTM & GRU) — PyTorch

Bu proje, PyTorch kullanarak LSTM ve GRU modelleriyle hisse senedi fiyatı tahmini yapan bir zaman serisi regresyon projesidir. Makine öğrenmesi temellerinden başlayarak adım adım geliştirilmiştir.

## Kurulum

\`\`\`
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
\`\`\`

## Klasör Yapısı

- `notebooks/week1/` — ML temelleri ve mini regresyon alıştırması
- `notebooks/week2/` — PyTorch temelleri
- `notebooks/week4/` — Veri hazırlığı
- `notebooks/week5/` — LSTM & GRU model eğitimi ve karşılaştırması
- `models/` — Eğitilmiş model ve scaler dosyaları
- `backend/` — FastAPI ile tahmin servisi (geliştirme aşamasında)
## İlerleme

- [x] **Hafta 1:** Ortam kurulumu (Python, VS Code, Git/GitHub, venv)
- [x] **Hafta 2-3:** ML temelleri, PyTorch temelleri (tensor, autograd, nn.Module), RNN/LSTM/GRU kavramları
- [x] **Hafta 4:** Veri hazırlığı (AMZN hisse verisi, MinMaxScaler, sliding window, train/test split)
- [x] **Hafta 5:** LSTM ve GRU modellerinin eğitimi ve karşılaştırılması, hiperparametre ayarlaması
- [ ] **Hafta 6:** Dokümantasyon ve kapanış

## Sonuçlar

Amazon (AMZN) hisse senedi kapanış fiyatları (2006-2018) kullanılarak, geçmiş 30 günlük 
fiyat penceresinden bir sonraki günün fiyatını tahmin eden LSTM ve GRU modelleri eğitildi.

| Model | Lookback | Epoch | Test RMSE (ölçekli) |
|-------|----------|-------|----------------------|
| LSTM  | 30       | 200   | 0.454                |
| GRU   | 30       | 200   | **0.089**            |

**Bulgular:**
- GRU, tüm denemelerde LSTM'den daha düşük test hatası elde etti.
- Lookback penceresini 20'den 30 güne çıkarmak her iki modeli de iyileştirdi, GRU bundan 
  (%52 iyileşme) LSTM'e (%11 iyileşme) göre çok daha fazla fayda gördü.
- Modeller genel fiyat trendini takip edebiliyor, ancak hızlı yükseliş dönemlerinde 
  gerçek fiyatın altında kalma eğiliminde (zaman serisi tahmininde yaygın bir "gecikme" davranışı).