import os
import pickle
import numpy as np
import torch
import torch.nn as nn
import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Model Mimarisi (Eğittiğin notebook ile birebir aynı)
class GRUModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=32, num_layers=2, output_size=1):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        out, _ = self.gru(x, h0)
        out = self.fc(out[:, -1, :])
        return out

# 2. FastAPI Uygulaması ve CORS
app = FastAPI(title="Stock Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Model ve Scaler Yükleme (Dosya yollarını güvenli bulma)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "gru_model.pth")
SCALER_PATH = os.path.join(BASE_DIR, "..", "models", "scaler.pkl")

# Modeli ayağa kaldır
model = GRUModel()
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

# Scaler'ı yükle
with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

# 4. Tahmin Endpoint'i
@app.get("/predict")
def predict(ticker: str = "THYAO.IS"):
    try:
        clean_ticker = ticker.strip().upper()

        # Nokta içermeyen ve popüler Türk hissesi olan girdilere otomatik .IS ekle
        # Veya doğrudan ilk denemeyi yap, veri boşsa .IS ekleyip tekrar dene
        stock = yf.Ticker(clean_ticker)
        df = stock.history(period="6mo")

        if df.empty and not clean_ticker.endswith(".IS"):
            clean_ticker = f"{clean_ticker}.IS"
            stock = yf.Ticker(clean_ticker)
            df = stock.history(period="6mo")

        if len(df) < 30:
            raise HTTPException(
                status_code=400, 
                detail=f"'{clean_ticker}' için yeterli geçmiş veri bulunamadı. Lütfen BIST hisseleri için sonuna .IS eklemeyi deneyin (Örn: ASELS.IS)."
            )

        # Tarih ve saat dilimi temizliği
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)

        close_prices = df["Close"].values
        last_price = float(close_prices[-1])

        # Ölçeklendirme ve tahmin
        scaled_data = scaler.transform(close_prices.reshape(-1, 1))
        seq = scaled_data[-30:].reshape(1, 30, 1)
        seq_tensor = torch.tensor(seq, dtype=torch.float32)

        with torch.no_grad():
            pred_scaled = model(seq_tensor).numpy()

        predicted_price = float(scaler.inverse_transform(pred_scaled)[0][0])
        currency = "TL" if clean_ticker.endswith(".IS") else "$"

        history = [
            {"date": date.strftime("%Y-%m-%d"), "price": round(float(price), 2)}
            for date, price in zip(df.index[-15:], close_prices[-15:])
        ]

        return {
            "ticker": clean_ticker,
            "currency": currency,
            "last_price": round(last_price, 2),
            "predicted_price": round(predicted_price, 2),
            "change_percent": round(((predicted_price - last_price) / last_price) * 100, 2),
            "history": history
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(e)}")

        return {
            "ticker": symbol_to_fetch,
            "currency": currency,
            "last_price": round(last_price, 2),
            "predicted_price": round(predicted_price, 2),
            "change_percent": round(((predicted_price - last_price) / last_price) * 100, 2),
            "history": history
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")

        return {
            "ticker": ticker.upper(),
            "last_price": round(last_price, 2),
            "predicted_price": round(predicted_price, 2),
            "change_percent": round(((predicted_price - last_price) / last_price) * 100, 2),
            "history": history
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))