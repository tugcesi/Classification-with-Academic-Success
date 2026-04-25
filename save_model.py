import pandas as pd
import numpy as np
import pickle
from lightgbm import LGBMClassifier

# ── Veri ─────────────────────────────────────────────────────────────────────
train = pd.read_csv('train.csv')

# ── Feature Engineering ───────────────────────────────────────────────────────
def feature_engineering(df):
    df = df.copy()

    df['1st_sem_success_rate'] = (df['Curricular units 1st sem (approved)'] /
                                   df['Curricular units 1st sem (enrolled)'].replace(0, np.nan)).fillna(0)

    df['2nd_sem_success_rate'] = (df['Curricular units 2nd sem (approved)'] /
                                   df['Curricular units 2nd sem (enrolled)'].replace(0, np.nan)).fillna(0)

    df['total_approved'] = df['Curricular units 1st sem (approved)'] + \
                            df['Curricular units 2nd sem (approved)']

    df['avg_grade'] = (df['Curricular units 1st sem (grade)'] +
                        df['Curricular units 2nd sem (grade)']) / 2

    df['grade_progress'] = df['Curricular units 2nd sem (grade)'] - \
                            df['Curricular units 1st sem (grade)']

    df['Age_Group'] = pd.cut(df['Age at enrollment'],
                              bins=[0, 20, 25, 35, 200],
                              labels=[0, 1, 2, 3]).astype(int)

    df['Economic_Risk']       = df['Unemployment rate'] - df['GDP']
    df['avg_admission_grade'] = (df['Admission grade'] +
                                  df['Previous qualification (grade)']) / 2

    drop_cols = [
        'id', 'Nacionality', 'International', 'Educational special needs',
        'Curricular units 1st sem (credited)', 'Curricular units 2nd sem (credited)',
        'Curricular units 1st sem (without evaluations)', 'Curricular units 2nd sem (without evaluations)',
        'Curricular units 1st sem (approved)', 'Curricular units 2nd sem (approved)',
        'Curricular units 1st sem (grade)', 'Curricular units 2nd sem (grade)',
        'Admission grade', 'Previous qualification (grade)',
        'Unemployment rate', 'GDP',
        "Father's qualification", "Father's occupation", "Mother's occupation"
    ]
    df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)

    return df

target_map = {'Dropout': 0, 'Enrolled': 1, 'Graduate': 2}

df = feature_engineering(train)
X = df.drop(columns=['Target'])
y = df['Target'].map(target_map)

FEATURES = X.columns.tolist()

# ── Model Eğitimi ─────────────────────────────────────────────────────────────
model = LGBMClassifier(verbose=-1, random_state=42)
model.fit(X, y)

# ── Kaydet ────────────────────────────────────────────────────────────────────
with open('model.pkl', 'wb') as f:
    pickle.dump({'model': model, 'features': FEATURES}, f)

print("Model kaydedildi → model.pkl")
print(f"Feature sayısı : {len(FEATURES)}")
print(f"Features       : {FEATURES}")