import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pickle
import joblib

class CarPriceEncoder:
    def __init__(self):
        self.label_encoders = {}
        self.onehot_encoders = {}
        self.target_encoding_dict = {}
        self.feature_names = []

    def fit_transform(self, X,y):
        """
        Eğitim verisi için encode işlemleri
        """

        df_encoded = X.copy()

        # Target Encoding

        self.target_encoding_dict = pd.concat([X, y], axis=1).groupby("title")["Price"].mean().to_dict()
        df_encoded["title_encoded"] = df_encoded["title"].map(self.target_encoding_dict)

        # Label Encoding

        self.label_encoders["Gearbox"] = LabelEncoder()
        df_encoded["Gearbox"] = self.label_encoders["Gearbox"].fit_transform(df_encoded["Gearbox"])

        # One Hot Encoding

        categorical_cols = ["Fuel type", "Body type","Brand"]

        for col in categorical_cols:
            self.onehot_encoders[col] = OneHotEncoder(drop="first",sparse_output=False)
            encoded_data = self.onehot_encoders[col].fit_transform(df_encoded[[col]])

            #feature isimleri:

            feature_names = [f"{col}_{val}" for val in self.onehot_encoders[col].categories_[0][1:]]
            self.feature_names.extend(feature_names)

            # Df e ekle

            encoded_df = pd.DataFrame(encoded_data,columns=feature_names,index=df_encoded.index)
            df_encoded = pd.concat([df_encoded,encoded_df],axis=1)
        # orijinal kolonları kaldır

        df_encoded = df_encoded.drop(["title","Fuel type","Body type","Brand"],axis=1)

        return df_encoded

    def transform(self, df):

        """
        X_test için
        """

        df_encoded = df.copy()

        # 1. Title için Target Encoding (bilinmeyen değerler için ortalama fiyat)

        if "title" in df_encoded.columns:
            df_encoded["title_encoded"] = df_encoded["title"].map(self.target_encoding_dict)
            # Bilinmeyen title'lar için ortalama fiyat kullan

            mean_price = np.mean(list(self.target_encoding_dict.values()))
            df_encoded["title_encoded"].fillna(mean_price,inplace=True)

        # 2. Gearbox için Label Encoding

        if "Gearbox" in df_encoded.columns:
            df_encoded["Gearbox"] = self.label_encoders["Gearbox"].transform(df_encoded["Gearbox"])

        # 3. Fuel type, Body type, Brand için One-Hot Encoding

        categorical_cols = ['Fuel type', 'Body type', 'Brand']

        for col in categorical_cols:
            if col in df_encoded.columns:
                #Bilinmeyen kategoriler için 0 değeri ata
                encoded_data = self.onehot_encoders[col].transform(df_encoded[[col]])
                feature_names = [f"{col}_{val}"for val in self.onehot_encoders[col].categories_[0][1:]]

                encoded_df = pd.DataFrame(encoded_data,columns=feature_names,index=df_encoded.index)
                df_encoded = pd.concat([df_encoded,encoded_df],axis=1)

        # Orijinal kategorik sütunları kaldır
        df_encoded = df_encoded.drop(['title', 'Fuel type', 'Body type', 'Brand'], axis=1)

        return df_encoded
