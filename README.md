# 🎓 Classification with Academic Success

Bu proje, [Kaggle Playground Series S4E6](https://www.kaggle.com/competitions/playground-series-s4e6) yarışması kapsamında yükseköğretimdeki öğrencilerin akademik riskini tahmin etmek amacıyla geliştirilmiştir. Çok sınıflı sınıflandırma (multi-class classification) yaklaşımıyla öğrencilerin **Dropout**, **Enrolled** veya **Graduate** olarak sınıflandırılması hedeflenmiştir.

---

## 📁 Proje Yapısı

```
├── train.csv                                        # Eğitim verisi
├── test.csv                                         # Test verisi
├── classification-with-an-academic-success.ipynb   # EDA, Feature Engineering, Modelleme
├── save_model.py                                    # Modeli eğitip kaydeder
├── app.py                                           # Streamlit uygulaması
├── model.pkl                                        # Eğitilmiş model
├── requirements.txt                                 # Gerekli kütüphaneler
└── README.md
```

---

## 🎯 Hedef Değişken

`Target` — 3 farklı akademik risk sınıfı:

| Sınıf | Açıklama |
|---|---|
| Dropout | Okulu bırakan öğrenci |
| Enrolled | Hâlâ kayıtlı olan öğrenci |
| Graduate | Mezun olan öğrenci |

---

## 🔧 Kullanılan Özellikler

### Orijinal Değişkenler
| Değişken | Açıklama |
|---|---|
| Marital status | Medeni durum |
| Application mode | Başvuru modu |
| Application order | Başvuru sırası |
| Course | Kurs kodu |
| Daytime/evening attendance | Ders saati türü |
| Previous qualification | Önceki yeterlilik |
| Mother's qualification | Anne eğitim seviyesi |
| Displaced | Yerinden edilme durumu |
| Debtor | Borç durumu |
| Tuition fees up to date | Öğrenim ücreti güncelliği |
| Gender | Cinsiyet |
| Scholarship holder | Burs durumu |
| Age at enrollment | Kayıt yaşı |
| Curricular units (enrolled/evaluations) | Dönem ders bilgileri |
| Inflation rate | Enflasyon oranı |

### Türetilen Değişkenler
| Değişken | Formül | Açıklama |
|---|---|---|
| `1st_sem_success_rate` | approved / enrolled | 1. dönem başarı oranı |
| `2nd_sem_success_rate` | approved / enrolled | 2. dönem başarı oranı |
| `total_approved` | 1st + 2nd approved | Toplam geçilen ders |
| `avg_grade` | (1st + 2nd grade) / 2 | Ortalama not |
| `grade_progress` | 2nd − 1st grade | Not gelişimi |
| `Age_Group` | pd.cut(age) | Yaş kategorisi |
| `Economic_Risk` | Unemployment − GDP | Ekonomik risk skoru |
| `avg_admission_grade` | (Admission + Prev. qual.) / 2 | Ortalama giriş notu |

---

## 📊 Proje Adımları

1. **EDA & Görselleştirme** — Hedef dağılımı, sayısal/kategorik değişken analizleri, korelasyon matrisi
2. **Feature Engineering** — Başarı oranları, not türetimleri, ekonomik risk skoru, yaş grubu
3. **Model Karşılaştırma** — 10 farklı algoritma test edildi
4. **Final Model** — LightGBM seçildi

---

## 🤖 Model Performansı

Karşılaştırılan modeller:

- BernoulliNB
- LogisticRegression
- DecisionTreeClassifier
- RandomForestClassifier
- GradientBoostingClassifier
- KNeighborsClassifier
- AdaBoostClassifier
- XGBClassifier
- **LGBMClassifier** ✅ En iyi
- CatBoostClassifier

---

## 🚀 Kurulum & Çalıştırma

```bash
# 1. Repoyu klonla
git clone https://github.com/tugcesi/Classification-with-Academic-Success.git
cd Classification-with-Academic-Success

# 2. Gereksinimleri yükle
pip install -r requirements.txt

# 3. Modeli eğit
python save_model.py

# 4. Uygulamayı başlat
streamlit run app.py
```

---

## 🖥️ Streamlit Uygulaması

Uygulama aracılığıyla:
- Öğrenciye ait kişisel ve akademik bilgileri girerek risk sınıfını öğrenebilirsiniz
- **Dropout**, **Enrolled** ve **Graduate** sınıfları için tahmin olasılıklarını grafik olarak görebilirsiniz

---

## 🛠️ Kullanılan Teknolojiler

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LightGBM](https://img.shields.io/badge/LightGBM-latest-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-latest-red)
![Pandas](https://img.shields.io/badge/Pandas-latest-150458?logo=pandas)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-latest-F7931E)

---

## 📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır.
