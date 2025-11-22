import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import joblib
import pickle
import pandas as pd
from pydantic import BaseModel
import numpy as np
import os

# FastAPI uygulaması başlatıyoruz

app = FastAPI(title="Car Price Prediction API", version="1.0.0")
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Model_new.pkl")
#HTML dosyalarını alma

templates = Jinja2Templates(directory="templates")

# Model yükleme kısmı

try:
    with open(model_path, "rb") as f:
        saved_data = joblib.load(f)
        model = saved_data["model"]
        encoder = saved_data["encoders"]


    print("Model loaded")

# Dosya hatası model hatası varsa

except FileNotFoundError:
    print("Hata: Model dosyası bulunamadı!")
    model = None
    encoder = None
except Exception as e:
    print(f"Model yükleme hatası {str(e)}")
    model = None
    encoder = None

print("Model ve encoder başarıyla yüklendi")

class CarFeatures(BaseModel):
    title: str
    Mileage_miles: float
    Registration_Year:int
    Previous_Owners: float = 1.0  # Varsayılan değer
    Fuel_type:str
    Body_type:str
    Engine:float
    Gearbox:str
    Doors:float
    Seats:float
    Emission_Class:int
    Brand:str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(features: CarFeatures):
    try:
        print("Received features:", features)

        # Girdi özelliklerine uygun df oluşturulur

        input_data = pd.DataFrame([{
            "title": features.title,
            "Mileage(miles)": features.Mileage_miles,
            "Registration_Year": features.Registration_Year,
            "Previous Owners": features.Previous_Owners,
            "Fuel type": features.Fuel_type,
            "Body type": features.Body_type,
            "Engine": features.Engine,
            "Gearbox": features.Gearbox,
            "Doors": features.Doors,
            "Seats": features.Seats,
            "Emission Class": features.Emission_Class,
            "Brand": features.Brand
        }])

        # Kolon isimlerini düzelt

        column_mapping = {
            'Emission_Class': 'Emission Class',
            'Fuel_type': 'Fuel type',
            'Body_type': 'Body type',
            'Mileage_miles': 'Mileage(miles)'

        }
        #HTML den gelen isimleri model formatına çevir

        for old_name,new_name in column_mapping.items():
            if old_name in input_data.columns:
                input_data[new_name] = input_data[old_name]
                input_data = input_data.drop(old_name, axis=1)

        print("Input data:")
        print(input_data)
        print("Input data columns:", input_data.columns.tolist())
        print("Input data shape:", input_data.shape)
        print("Input data types:", input_data.dtypes)

        # Girdileri encode etme

        input_encoded = encoder.transform(input_data)

        print("Encoded data:")
        print(input_encoded)
        print(f"Encoded shape: {input_encoded.shape}")
        print("Encoded columns:", input_encoded.columns.tolist())

        # Tahmin etme

        prediction = model.predict(input_encoded)[0]

        print("Prediction:", prediction)


        return {
            "predicted_price": float(prediction),
            "predicted_price_formatted":f"{prediction:.2f}",
            "status":"success",
            "message":"Tahmin başarılı"
        }

    except Exception as e:
        import traceback
        print(f"Error during prediction: {str(e)}")
        print("Full error traceback:")
        print(traceback.format_exc())
        return {
            "error": f"Tahmin hatası: {str(e)}",
            "status": "error",
            "details": str(e)
        }

@app.get("/get_categories")
async def get_categories():
    """Mevcut kategori seçeneklerini döndür"""
    try:
        # Encoder'dan mevcut kategorileri al
        categories = {
            'fuel_types': ['Petrol', 'Diesel', 'Petrol Hybrid', 'Other'],
            'body_types': ['Hatchback', 'SUV', 'Saloon', 'MPV', 'Estate', 'Coupe', 'Convertible', 'Other'],
            'gearbox_types': ['Manual', 'Automatic'],
            'emission_classes': [1, 2, 3, 4, 5, 6]
        }
        return categories
    except Exception as e:
        return {"error": f"Kategori yükleme hatası: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
