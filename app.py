import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ── Model Yükleme ─────────────────────────────────────────────────────────────
with open('model.pkl', 'rb') as f:
    payload  = pickle.load(f)
    model    = payload['model']
    FEATURES = payload['features']

target_map_inverse = {0: 'Dropout', 1: 'Enrolled', 2: 'Graduate'}
label_colors       = {
    'Dropout' : '#e74c3c',
    'Enrolled': '#f1c40f',
    'Graduate': '#2ecc71'
}

# ── Sayfa ─────────────────────────────────────────────────────────────────────
st.set_page_config(page_title='Akademik Risk Tahmini', page_icon='🎓', layout='centered')
st.title('🎓 Akademik Risk Tahmini')
st.markdown('Öğrenciye ait bilgileri girerek akademik risk sınıfını öğrenin.')
st.divider()

# ── Girdiler ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader('👤 Kişisel Bilgiler')
    marital_status      = st.selectbox('Medeni Durum', [1, 2, 3, 4, 5, 6],
                                        format_func=lambda x: {1:'Bekar',2:'Evli',3:'Dul',4:'Boşanmış',5:'Birlikte',6:'Ayrı'}[x])
    gender              = st.selectbox('Cinsiyet', [0, 1], format_func=lambda x: 'Kadın' if x == 0 else 'Erkek')
    age                 = st.slider('Kayıt Yaşı', 17, 70, 20)
    displaced           = st.selectbox('Yerinden edilmiş mi?', [0, 1], format_func=lambda x: 'Hayır' if x == 0 else 'Evet')
    debtor              = st.selectbox('Borçlu mu?', [0, 1], format_func=lambda x: 'Hayır' if x == 0 else 'Evet')
    tuition_up_to_date  = st.selectbox('Öğrenim ücreti güncel mi?', [0, 1], format_func=lambda x: 'Hayır' if x == 0 else 'Evet')
    scholarship         = st.selectbox('Burs alıyor mu?', [0, 1], format_func=lambda x: 'Hayır' if x == 0 else 'Evet')

with col2:
    st.subheader('📚 Akademik Bilgiler')
    application_mode    = st.number_input('Başvuru Modu', 1, 53, 1)
    application_order   = st.slider('Başvuru Sırası', 0, 9, 1)
    course              = st.number_input('Kurs Kodu', 33, 9991, 9238)
    attendance          = st.selectbox('Ders Saati', [0, 1], format_func=lambda x: 'Akşam' if x == 0 else 'Gündüz')
    prev_qualification  = st.number_input('Önceki Yeterlilik', 1, 43, 1)
    mothers_qual        = st.number_input("Anne Eğitim Seviyesi", 1, 44, 19)
    inflation_rate      = st.number_input('Enflasyon Oranı', -1.0, 4.0, 1.4, step=0.1)

st.divider()
st.subheader('📊 Dönem Bilgileri')
col3, col4 = st.columns(2)

with col3:
    sem1_enrolled    = st.slider('1. Dönem Kayıtlı Ders', 0, 26, 6)
    sem1_approved    = st.slider('1. Dönem Geçilen Ders', 0, 26, 5)
    sem1_grade       = st.slider('1. Dönem Not Ort.', 0.0, 20.0, 12.0, step=0.1)
    sem1_evaluations = st.slider('1. Dönem Sınav Sayısı', 0, 45, 7)

with col4:
    sem2_enrolled    = st.slider('2. Dönem Kayıtlı Ders', 0, 23, 6)
    sem2_approved    = st.slider('2. Dönem Geçilen Ders', 0, 20, 5)
    sem2_grade       = st.slider('2. Dönem Not Ort.', 0.0, 20.0, 12.0, step=0.1)
    sem2_evaluations = st.slider('2. Dönem Sınav Sayısı', 0, 33, 7)

st.divider()

# ── Tahmin ────────────────────────────────────────────────────────────────────
if st.button('🔍 Tahmin Et', use_container_width=True):

    # Türetilen değişkenler
    success_1   = sem1_approved / sem1_enrolled if sem1_enrolled > 0 else 0
    success_2   = sem2_approved / sem2_enrolled if sem2_enrolled > 0 else 0
    total_appr  = sem1_approved + sem2_approved
    avg_grade   = (sem1_grade + sem2_grade) / 2
    grade_prog  = sem2_grade - sem1_grade
    age_group   = pd.cut([age], bins=[0,20,25,35,200], labels=[0,1,2,3]).astype(int)[0]
    avg_adm_gr  = 125.0  # sabit ortalama (kullanıcıdan alınmıyor)
    econ_risk   = 11.1 - 0.32  # sabit ortalama değerler

    raw = {
        'Marital status'                        : marital_status,
        'Application mode'                      : application_mode,
        'Application order'                     : application_order,
        'Course'                                : course,
        'Daytime/evening attendance'            : attendance,
        'Previous qualification'                : prev_qualification,
        'Mother\'s qualification'               : mothers_qual,
        'Displaced'                             : displaced,
        'Debtor'                                : debtor,
        'Tuition fees up to date'               : tuition_up_to_date,
        'Gender'                                : gender,
        'Scholarship holder'                    : scholarship,
        'Age at enrollment'                     : age,
        'Curricular units 1st sem (enrolled)'   : sem1_enrolled,
        'Curricular units 1st sem (evaluations)': sem1_evaluations,
        'Curricular units 2nd sem (enrolled)'   : sem2_enrolled,
        'Curricular units 2nd sem (evaluations)': sem2_evaluations,
        'Inflation rate'                        : inflation_rate,
        '1st_sem_success_rate'                  : success_1,
        '2nd_sem_success_rate'                  : success_2,
        'total_approved'                        : total_appr,
        'avg_grade'                             : avg_grade,
        'grade_progress'                        : grade_prog,
        'Age_Group'                             : age_group,
        'Economic_Risk'                         : econ_risk,
        'avg_admission_grade'                   : avg_adm_gr,
    }

    input_df = pd.DataFrame([raw])[FEATURES]

    pred       = model.predict(input_df)[0]
    pred_proba = model.predict_proba(input_df)[0]
    label      = target_map_inverse[pred]
    color      = label_colors[label]

    st.markdown(f"""
    <div style='background-color:{color}22; border-left:6px solid {color};
                padding:20px; border-radius:8px; margin-top:10px'>
        <h2 style='color:{color}; margin:0'>🎯 {label}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('#### 📊 Sınıf Olasılıkları')
    proba_df = pd.DataFrame({
        'Sınıf'    : list(target_map_inverse.values()),
        'Olasılık' : pred_proba
    }).sort_values('Olasılık', ascending=False)
    st.bar_chart(proba_df.set_index('Sınıf')['Olasılık'])