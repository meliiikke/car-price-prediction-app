# 🚗 Araç Fiyat Tahmin Projesi - FastAPI

Bu proje, kullanılmış araçların fiyatlarını tahmin etmek için makine öğrenmesi kullanan modern bir FastAPI web uygulamasıdır.

## 🎯 Proje Özellikleri

- **Makine Öğrenmesi Modeli**: Random Forest algoritması (R² Score: 0.86)
- **Backend**: FastAPI ile yüksek performanslı API
- **Frontend**: Modern ve responsive Bootstrap arayüzü
- **Encoding**: Otomatik kategorik değişken encoding sistemi
- **Real-time**: Anlık fiyat tahminleri

## 📁 Proje Yapısı

```
CarPricePredictionProject/
├── app.py                        # FastAPI ana uygulaması
├── templates/
│   └── index.html                # Web arayüzü
├── requirements.txt               # Python bağımlılıkları
├── Model_new.pkl                     # Eğitilmiş makine öğrenmesi modeli
├── Model-Notebook.ipynb          # Model eğitim notebook'u
└── used_cars_UK.csv              # Veri seti
```

## 🛠️ Kurulum

### **1. Gereksinimler**

- Python 3.8+
- pip (Python paket yöneticisi)
- Git (opsiyonel)

### **2. Projeyi İndirin**

```bash
# Eğer Git kullanıyorsanız:
git clone <repository-url>
cd CarPricePredictionProject

# Veya manuel olarak dosyaları indirin
```

### **3. Sanal Ortam Oluşturun (Önerilen)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **4. Bağımlılıkları Yükleyin**

```bash
pip install -r requirements.txt
```

## 🚀 Çalıştırma

### **1. Uygulamayı Başlatın**

```bash
python app.py
```

### **2. Tarayıcıda Açın**

- **Ana sayfa**: http://localhost:8000

## 🌐 Kullanım

### **Web Arayüzü ile:**

1. Tarayıcıda http://localhost:8000 adresini açın
2. Formu doldurun:
   - **Marka & Model**: Araç markası ve modeli
   - **Temel Özellikler**: Yakıt tipi, kasa tipi, vites
   - **Motor & Performans**: Motor hacmi, kilometre, kayıt yılı
   - **Diğer**: Kapı sayısı, koltuk sayısı, önceki sahip
3. "Fiyat Tahmini Yap" butonuna tıklayın
4. Tahmin sonucunu görün

### **API ile:**

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Ford Fiesta",
       "Mileage_miles": 50000,
       "Registration_Year": 2018,
       "Previous_Owners": 1,
       "Fuel_type": "Petrol",
       "Body_type": "Hatchback",
       "Engine": 1.2,
       "Gearbox": "Manual",
       "Doors": 5,
       "Seats": 5,
       "Emission_Class": 6,
       "Brand": "Ford"
     }'
```

## 🔧 API Endpoints

| Endpoint          | Method | Açıklama                        |
| ----------------- | ------ | ------------------------------- |
| `/`               | GET    | Ana sayfa (HTML form)           |
| `/predict`        | POST   | Fiyat tahmini yapar             |
| `/get_categories` | GET    | Kategori seçeneklerini döndürür |

## 📊 Model Bilgileri

- **Algoritma**: Random Forest Regressor
- **Performans**: R² Score = 0.86 (çok iyi!)
- **Encoding**:
  - Title: Target Encoding
  - Fuel Type, Body Type, Brand: One-Hot Encoding
  - Gearbox: Label Encoding
- **Veri Seti**: 2,757 araç kaydı
- **Özellikler**: 12 farklı araç özelliği

## 🎨 Form Alanları

### **Zorunlu Alanlar:**

- **title**: Araç modeli (örn: "Ford Fiesta")
- **Brand**: Marka (örn: "Ford")
- **Fuel_type**: Yakıt tipi (Petrol, Diesel, Hybrid, Other)
- **Body_type**: Kasa tipi (Hatchback, SUV, Saloon, MPV, Estate, Coupe, Convertible, Other)
- **Gearbox**: Vites (Manual, Automatic)
- **Engine**: Motor hacmi (0.8 - 6.0 L)
- **Mileage_miles**: Kilometre (0 - 200,000)
- **Registration_Year**: Kayıt yılı (1995 - 2024)
- **Emission_Class**: Emisyon sınıfı (1-6)
- **Doors**: Kapı sayısı (2-5)
- **Seats**: Koltuk sayısı (2-9)
- **Previous_Owners**: Önceki sahip sayısı (0-10)

### **2. Kategoriler:**

```bash
curl http://localhost:8000/get_categories
```

### **3. Örnek Tahmin:**

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "BMW 3 Series",
       "Mileage_miles": 30000,
       "Registration_Year": 2020,
       "Previous_Owners": 1,
       "Fuel_type": "Diesel",
       "Body_type": "Saloon",
       "Engine": 2.0,
       "Gearbox": "Automatic",
       "Doors": 4,
       "Seats": 5,
       "Emission_Class": 6,
       "Brand": "BMW"
     }'
```

## 🚨 Hata Giderme

### **Yaygın Hatalar:**

#### **1. Port Zaten Kullanımda:**

```bash
# Farklı port kullanın
python app.py --port 8001
```

#### **2. Model Dosyası Bulunamadı:**

```
FileNotFoundError: [Errno 2] No such file or directory: 'Model_new.pkl'
```

**Çözüm**: `Model_new.pkl` dosyasının proje klasöründe olduğundan emin olun.

#### **3. Bağımlılık Hatası:**

```bash
# Sanal ortamı aktive edin
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Bağımlılıkları yeniden yükleyin
pip install -r requirements.txt
```

### **Debug Modu:**

```bash
# Debug modunda çalıştırın
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 Production Deployment

### **Gunicorn ile (Linux/Mac):**

```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### **Waitress ile (Windows):**

```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=8000 app:app
```

### **Docker ile:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app1:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Performans İyileştirmeleri

### **1. Model Optimizasyonu:**

- Hyperparameter tuning
- Feature selection
- Ensemble methods

### **2. API Optimizasyonu:**

- Caching (Redis)
- Rate limiting
- Load balancing

### **3. Frontend Optimizasyonu:**

- Lazy loading
- Progressive Web App (PWA)
- Offline support

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

Projenizi başarıyla çalıştırdığınızda:

- ✅ FastAPI backend çalışıyor
- ✅ Web arayüzü erişilebilir
- ✅ Model tahminleri yapılıyor
- ✅ API dokümantasyonu mevcut

**İyi çalışmalar! 🚀**
