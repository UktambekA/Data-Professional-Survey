import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import StringIO, BytesIO
import zipfile
import os

# Sahifa sarlavhasi
st.set_page_config(
    page_title="Data Professional Survey Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sarlavha
st.title("📊 Data Professional Survey Dashboard")
st.markdown("*Data sohasidagi mutaxassislar so'rovnomasi natijalari tahlili*")

# Kerakli kutubxonalar haqida xabar berish
required_packages = ['openpyxl', 'plotly', 'seaborn', 'matplotlib']
st.sidebar.header("Tavsiya etilgan kutubxonalar")
st.sidebar.info("""
Ushbu dasturni to'g'ri ishlashi uchun quyidagi kutubxonalar kerak:
```
pip install streamlit pandas numpy matplotlib seaborn plotly requests openpyxl
```
""")

# Stil qo'shish
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e8bf5;
        color: white;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .chart-container {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# GitHub'dan ma'lumotlarni yuklab olish funksiyasi
@st.cache_data
def download_and_process_data():
    """GitHub'dan ma'lumotlarni yuklab olish va qayta ishlash"""
    try:
        # 1. Avval GitHub API orqali fayllarni tekshiramiz
        repo_owner = "UktambekA"
        repo_name = "Data-Professional-Survey"
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
        
        response = requests.get(api_url)
        response.raise_for_status()
        
        # CSV yoki Excel fayllarni qidirish
        data_files = [item for item in response.json() if item['name'].endswith(('.csv', '.xlsx', '.xls'))]
        
        if data_files:
            # Birinchi topilgan faylni yuklab olish
            file_url = data_files[0]['download_url']
            file_name = data_files[0]['name']
            
            file_response = requests.get(file_url)
            file_response.raise_for_status()
            
            # Fayl kengaytmasiga qarab o'qish
            if file_name.endswith('.csv'):
                df = pd.read_csv(BytesIO(file_response.content))
            else:  # Excel fayl
                try:
                    df = pd.read_excel(BytesIO(file_response.content))
                except ImportError:
                    st.error("Excel fayllarni o'qish uchun 'openpyxl' kutubxonasi kerak. Iltimos, 'pip install openpyxl' buyrug'i orqali o'rnating.")
                    raise
            
            return df, file_name
        
        # Agar repozitoriyada to'g'ridan-to'g'ri fayl bo'lmasa, zaxira variantga o'tish
        st.warning("GitHub repozitoriyasida to'g'ridan-to'g'ri CSV yoki Excel fayl topilmadi. Boshqa manbadan yuklab olishga harakat qilinmoqda...")
        
        # Zaxira variant - agar umumiy ma'lumotlar topilmasa
        url = "https://raw.githubusercontent.com/AlexTheAnalyst/Power-BI/main/Power%20BI%20-%20Final%20Project.xlsx"
        response = requests.get(url)
        try:
            df = pd.read_excel(BytesIO(response.content))
            return df, "Power BI - Final Project.xlsx"
        except ImportError:
            st.error("Excel fayllarni o'qish uchun 'openpyxl' kutubxonasi kerak. Iltimos, 'pip install openpyxl' buyrug'i orqali o'rnating.")
            # Import Error kelganda namunali ma'lumotlarni yaratish
            raise
        return df, "Power BI - Final Project.xlsx"
        
    except Exception as e:
        st.error(f"Ma'lumotlarni yuklab olishda xatolik: {e}")
        
        # Namunali ma'lumot (GitHub'dan ma'lumot olishning iloji bo'lmasa)
        # Ushbu namuna ma'lumotlarni yaratish
        st.warning("Ma'lumotlar yuklab olishda muammo yuzaga keldi. Namunali ma'lumotlar yaratilmoqda...")
        
        # Data professional survey uchun namunali ma'lumotlar yaratish
        roles = ['Data Scientist', 'Data Analyst', 'Data Engineer', 'Machine Learning Engineer', 'BI Developer']
        countries = ['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'India', 'Japan', 'China', 'Brazil']
        education = ['Bachelor\'s', 'Master\'s', 'PhD', 'Self-taught', 'Bootcamp']
        salaries = np.random.randint(40000, 150000, 500)
        years_experience = np.random.randint(0, 20, 500)
        work_life_balance = np.random.randint(1, 11, 500)  # 1-10 scale
        job_satisfaction = np.random.randint(1, 11, 500)  # 1-10 scale
        career_switch = np.random.choice(['Yes', 'No'], 500)
        programming_languages = [', '.join(np.random.choice(['Python', 'R', 'SQL', 'Java', 'JavaScript', 'C++', 'Julia'], 
                                                        size=np.random.randint(1, 5))) for _ in range(500)]
        
        df = pd.DataFrame({
            'Role': np.random.choice(roles, 500),
            'Country': np.random.choice(countries, 500),
            'Education': np.random.choice(education, 500),
            'YearsExperience': years_experience,
            'Salary': salaries,
            'WorkLifeBalance': work_life_balance,
            'JobSatisfaction': job_satisfaction,
            'CareerSwitch': career_switch,
            'ProgrammingLanguages': programming_languages,
            'Age': np.random.randint(22, 65, 500),
            'Gender': np.random.choice(['Male', 'Female', 'Other', 'Prefer not to say'], 500),
            'RemoteWork': np.random.choice(['Fully Remote', 'Hybrid', 'In Office'], 500)
        })
        
        return df, "sample_data.csv"

# Ma'lumotlarni yuklab olish
with st.spinner("Ma'lumotlar yuklab olinmoqda..."):
    try:
        df, file_name = download_and_process_data()
    except Exception as e:
        st.error(f"Ma'lumotlarni yuklab olishda xatolik: {e}")
        st.info("Namunali ma'lumotlar yaratilmoqda...")
        
        # Namunali ma'lumot yaratish
        np.random.seed(42)  # Natijalar takrorlanishi uchun
        sample_size = 500
        
        # Data professional survey uchun namunali ma'lumotlar yaratish
        roles = ['Data Scientist', 'Data Analyst', 'Data Engineer', 'Machine Learning Engineer', 'BI Developer']
        countries = ['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'India', 'Japan', 'China', 'Brazil']
        education = ['Bachelor\'s', 'Master\'s', 'PhD', 'Self-taught', 'Bootcamp']
        salaries = np.random.randint(40000, 150000, sample_size)
        years_experience = np.random.randint(0, 20, sample_size)
        work_life_balance = np.random.randint(1, 11, sample_size)  # 1-10 scale
        job_satisfaction = np.random.randint(1, 11, sample_size)  # 1-10 scale
        career_switch = np.random.choice(['Yes', 'No'], sample_size)
        programming_languages = [', '.join(np.random.choice(['Python', 'R', 'SQL', 'Java', 'JavaScript', 'C++', 'Julia'], 
                                                        size=np.random.randint(1, 5))) for _ in range(sample_size)]
        
        df = pd.DataFrame({
            'Role': np.random.choice(roles, sample_size),
            'Country': np.random.choice(countries, sample_size),
            'Education': np.random.choice(education, sample_size),
            'YearsExperience': years_experience,
            'Salary': salaries,
            'WorkLifeBalance': work_life_balance,
            'JobSatisfaction': job_satisfaction,
            'CareerSwitch': career_switch,
            'ProgrammingLanguages': programming_languages,
            'Age': np.random.randint(22, 65, sample_size),
            'Gender': np.random.choice(['Male', 'Female', 'Other', 'Prefer not to say'], sample_size),
            'RemoteWork': np.random.choice(['Fully Remote', 'Hybrid', 'In Office'], sample_size)
        })
        
        file_name = "namuna_malumotlar.csv"
        st.success("Namunali ma'lumotlar muvaffaqiyatli yaratildi!")

# Ma'lumotlar haqida umumiy ma'lumot
st.subheader(f"📂 Yuklab olingan ma'lumotlar: {file_name}")
st.write(f"Ma'lumotlar o'lchami: {df.shape[0]} qator, {df.shape[1]} ustun")

# Tab-lar yaratish
tabs = st.tabs([
    "📋 Umumiy ma'lumot", 
    "👨‍💼 Demografik ma'lumotlar", 
    "💰 Maosh tahlili", 
    "📚 Ta'lim va tajriba", 
    "💻 Texnologiyalar", 
    "😊 Ish faoliyati"
])

# Ta'lim ustuni borligini tekshirish
has_education = any(col.lower() in ['education', 'highest education', 'degree'] for col in df.columns)
has_salary = any(col.lower() in ['salary', 'yearly salary', 'annual salary', 'income'] for col in df.columns)
has_experience = any(col.lower() in ['years experience', 'yearsexperience', 'years of experience', 'experience'] for col in df.columns)
has_role = any(col.lower() in ['role', 'job title', 'position', 'title'] for col in df.columns)
has_country = any(col.lower() in ['country', 'location', 'region'] for col in df.columns)
has_satisfaction = any(col.lower() in ['satisfaction', 'job satisfaction', 'jobsatisfaction'] for col in df.columns)
has_wlb = any(col.lower() in ['work life balance', 'worklifebalance', 'work-life balance'] for col in df.columns)
has_languages = any(col.lower() in ['programming languages', 'programminglanguages', 'languages', 'favorite programming language'] for col in df.columns)

# Ustunlarni standartlashtirish
column_mapping = {}
for col in df.columns:
    col_lower = col.lower()
    if 'education' in col_lower or 'degree' in col_lower:
        column_mapping[col] = 'Education'
    elif 'salary' in col_lower or 'income' in col_lower:
        column_mapping[col] = 'Salary'
    elif 'experience' in col_lower:
        column_mapping[col] = 'YearsExperience'
    elif 'role' in col_lower or 'title' in col_lower or 'position' in col_lower:
        column_mapping[col] = 'Role'
    elif 'country' in col_lower or 'location' in col_lower:
        column_mapping[col] = 'Country'
    elif 'satisfaction' in col_lower:
        column_mapping[col] = 'JobSatisfaction'
    elif 'work' in col_lower and 'balance' in col_lower:
        column_mapping[col] = 'WorkLifeBalance'
    elif 'language' in col_lower or 'programming' in col_lower:
        column_mapping[col] = 'ProgrammingLanguages'
    elif 'gender' in col_lower or 'sex' in col_lower:
        column_mapping[col] = 'Gender'
    elif 'age' in col_lower:
        column_mapping[col] = 'Age'

# Ustunlar mavjud bo'lsa, nomlarini o'zgartirish
if column_mapping:
    df = df.rename(columns=column_mapping)

# Umumiy ma'lumot tab
with tabs[0]:
    st.header("Umumiy ma'lumot")
    
    # Ma'lumotlar haqida qisqacha ma'lumot
    st.markdown("""
    Bu dashboard data sohasidagi mutaxassislar o'rtasida o'tkazilgan so'rovnoma natijalarini tahlil qiladi. 
    Dashboardda quyidagi ma'lumotlarni ko'rishingiz mumkin:
    - Demografik ma'lumotlar
    - Maosh statistikasi
    - Ta'lim va tajriba tahlili
    - Texnologiyalar va ko'nikmalar
    - Ish faoliyati va qoniqish darajasi
    """)
    
    # Ma'lumotlar jadvalini ko'rsatish
    st.subheader("Ma'lumotlar jadvali")
    st.dataframe(df.head(10))
    
    # Umumiy statistika
    st.subheader("Umumiy statistika")
    
    # Ustunlar tanlash
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if numeric_cols:
        # Statistik ma'lumotlarni ko'rsatish
        stat_df = df[numeric_cols].describe()
        # Qiymatlarni formatlash
        formatted_stats = stat_df.copy()
        # Maosh ustunini formatlash
        if 'Salary' in stat_df.columns:
            for idx in stat_df.index:
                formatted_stats.loc[idx, 'Salary'] = f"${int(stat_df.loc[idx, 'Salary']):,}"
        
        st.dataframe(formatted_stats)
    else:
        st.info("Raqamli ma'lumotlar mavjud emas. Ustunlarni tekshirib ko'ring:")
    
    # Yozma tahlil natijasi
    st.subheader("Asosiy xulosalar")
    
    analysis_text = """
    - So'rovnomada data sohasida ishlaydigan mutaxassislar qatnashgan
    - Natijalar data sohasidagi tendentsiyalar, maosh darajalari, va mutaxassislar ko'nikmalarini tahlil qilish imkonini beradi
    - Dashboard orqali siz data sohasidagi turli lavozimlar, maosh darajalari, va ko'nikmalar bo'yicha chuqur ma'lumot olishingiz mumkin
    """
    st.markdown(analysis_text)

# Demografik ma'lumotlar tab
with tabs[1]:
    st.header("Demografik ma'lumotlar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Lavozimlar bo'yicha taqsimot
        if has_role:
            st.subheader("Lavozimlar taqsimoti")
            role_counts = df['Role'].value_counts().reset_index()
            role_counts.columns = ['Role', 'Count']
            
            fig = px.pie(role_counts, values='Count', names='Role', 
                         title='Lavozimlar taqsimoti',
                         hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Lavozimlar haqida ma'lumot mavjud emas")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Mamlakat bo'yicha taqsimot
        if has_country:
            st.subheader("Mamlakat bo'yicha taqsimot")
            country_counts = df['Country'].value_counts().reset_index()
            country_counts.columns = ['Country', 'Count']
            
            # Top 10 mamlakatlar
            top_countries = country_counts.head(10)
            
            fig = px.bar(top_countries, x='Country', y='Count', 
                        title='Top 10 mamlakatlar',
                        color='Count', color_continuous_scale='Viridis')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Mamlakatlar haqida ma'lumot mavjud emas")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Qo'shimcha demografik ma'lumotlar
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    
    with col3:
        if 'Gender' in df.columns:
            st.subheader("Jinsi bo'yicha taqsimot")
            gender_counts = df['Gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']
            
            fig = px.bar(gender_counts, x='Gender', y='Count', 
                        color='Gender', title='Jinsi bo'yicha taqsimot')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Jins haqida ma'lumot mavjud emas")
    
    with col4:
        if 'Age' in df.columns:
            st.subheader("Yosh bo'yicha taqsimot")
            
            fig = px.histogram(df, x='Age', nbins=20, 
                            title='Yosh bo'yicha taqsimot',
                            color_discrete_sequence=['#3366CC'])
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Yosh haqida ma'lumot mavjud emas")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Maosh tahlili tab
with tabs[2]:
    st.header("Maosh tahlili")
    
    if has_salary:
        # Maosh statistikasi
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Maosh statistikasi")
        
        # Asosiy statistikani ko'rsatish
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("O'rtacha maosh", f"${int(df['Salary'].mean()):,}")
        
        with col2:
            st.metric("Mediana maosh", f"${int(df['Salary'].median()):,}")
        
        with col3:
            st.metric("Minimal maosh", f"${int(df['Salary'].min()):,}")
        
        with col4:
            st.metric("Maksimal maosh", f"${int(df['Salary'].max()):,}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            # Maosh taqsimoti
            st.subheader("Maosh taqsimoti")
            
            fig = px.histogram(df, x='Salary', nbins=30, 
                              title='Maosh taqsimoti',
                              color_discrete_sequence=['#22A7F0'])
            fig.update_layout(xaxis_title='Maosh ($)', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            # Lavozimlar bo'yicha o'rtacha maosh
            if has_role:
                st.subheader("Lavozimlar bo'yicha o'rtacha maosh")
                
                role_salary = df.groupby('Role')['Salary'].mean().sort_values(ascending=False).reset_index()
                
                fig = px.bar(role_salary, x='Role', y='Salary', 
                            title='Lavozimlar bo'yicha o'rtacha maosh',
                            color='Salary', color_continuous_scale='Viridis')
                fig.update_layout(yaxis_title='O'rtacha maosh ($)', height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Lavozimlar haqida ma'lumot mavjud emas")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Maosh va tajriba o'rtasidagi bog'liqlik
        if has_experience:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Maosh va tajriba o'rtasidagi bog'liqlik")
            
            fig = px.scatter(df, x='YearsExperience', y='Salary', 
                            title='Maosh va tajriba o'rtasidagi bog'liqlik',
                            color='Salary', size='Salary',
                            color_continuous_scale='Viridis')
            
            # Regression line qo'shish
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Korrelyatsiya koeffitsientini hisoblash
            correlation = df['YearsExperience'].corr(df['Salary'])
            st.write(f"Tajriba va maosh o'rtasidagi korrelyatsiya koeffitsienti: **{correlation:.2f}**")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Maosh haqida ma'lumot mavjud emas")

# Ta'lim va tajriba tab
with tabs[3]:
    st.header("Ta'lim va tajriba")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Ta'lim darajasi
        if has_education:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Ta'lim darajasi taqsimoti")
            
            edu_counts = df['Education'].value_counts().reset_index()
            edu_counts.columns = ['Education', 'Count']
            
            fig = px.pie(edu_counts, values='Count', names='Education', 
                        title='Ta\'lim darajasi taqsimoti',
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Ta'lim darajasi haqida ma'lumot mavjud emas")
    
    with col2:
        # Tajriba yillari
        if has_experience:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Tajriba yillari taqsimoti")
            
            fig = px.histogram(df, x='YearsExperience', nbins=20, 
                            title='Tajriba yillari taqsimoti',
                            color_discrete_sequence=['#72B01D'])
            fig.update_layout(xaxis_title='Tajriba (yil)', height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Tajriba yillari haqida ma'lumot mavjud emas")
    
    # Ta'lim darajasi va maosh o'rtasidagi bog'liqlik
    if has_education and has_salary:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Ta'lim darajasi va o'rtacha maosh")
        
        edu_salary = df.groupby('Education')['Salary'].mean().sort_values(ascending=False).reset_index()
        
        fig = px.bar(edu_salary, x='Education', y='Salary', 
                    title='Ta\'lim darajasi va o\'rtacha maosh',
                    color='Salary', color_continuous_scale='Viridis')
        fig.update_layout(yaxis_title='O\'rtacha maosh ($)', height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Lavozim va ta'lim o'rtasidagi bog'liqlik
    if has_role and has_education:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Lavozim va ta'lim darajasi o'rtasidagi bog'liqlik")
        
        # Crosstab yaratish
        role_edu = pd.crosstab(df['Role'], df['Education'])
        
        # Plotly Heatmap
        fig = px.imshow(role_edu, 
                        title='Lavozim va ta\'lim darajasi o\'rtasidagi bog\'liqlik',
                        color_continuous_scale='Viridis')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Texnologiyalar tab
with tabs[4]:
    st.header("Texnologiyalar va ko'nikmalar")
    
    if has_languages:
        # Programming languages (Split by comma)
        if df['ProgrammingLanguages'].dtype == 'object':  # String values
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Dasturlash tillari")
            
            # Split languages and count
            languages = []
            for lang_list in df['ProgrammingLanguages'].dropna():
                languages.extend([l.strip() for l in str(lang_list).split(',')])
            
            lang_count = pd.Series(languages).value_counts().reset_index()
            lang_count.columns = ['Language', 'Count']
            
            # Show top 10 languages
            top_langs = lang_count.head(10)
            
            fig = px.bar(top_langs, x='Language', y='Count', 
                        title='Eng mashhur dasturlash tillari (Top 10)',
                        color='Count', color_continuous_scale='Viridis')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Languages by role
            if has_role:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Lavozimlar bo'yicha mashhur dasturlash tillari")
                
                # Create a heatmap of roles vs languages
                # (This is complex and requires data processing which we'll simplify here)
                st.info("Bu seksiya uchun ma'lumotlar tahlil qilinmoqda...")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Dasturlash tillari to'g'risida ma'lumot mavjud emas yoki to'g'ri formatda emas")
    else:
        st.info("Dasturlash tillari haqida ma'lumot mavjud emas")
    
    # Remote work distribution if available
    if 'RemoteWork' in df.columns:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Masofaviy ish taqsimoti")
            
            remote_counts = df['RemoteWork'].value_counts().reset_index()
            remote_counts.columns = ['WorkType', 'Count']
            
            fig = px.pie(remote_counts, values='Count', names='WorkType', 
                        title='Masofaviy ish taqsimoti',
                        hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if has_salary:
                st.subheader("Ish turi bo'yicha o'rtacha maosh")
                
                remote_salary = df.groupby('RemoteWork')['Salary'].mean().reset_index()
                
                fig = px.bar(remote_salary, x='RemoteWork', y='Salary', 
                            title='Ish turi bo\'yicha o\'rtacha maosh',
                            color='RemoteWork')
                fig.update_layout(yaxis_title='O\'rtacha maosh ($)', height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Ish faoliyati tab
with tabs[5]:
    st.header("Ish faoliyati va qoniqish darajasi")
    
    # Ish qoniqish darajasi
    col1, col2 = st.columns(2)
    
    with col1:
        # Job satisfaction
        if has_satisfaction:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Ish faoliyatidan qoniqish darajasi")
            
            fig = px.histogram(df, x='JobSatisfaction', nbins=10, 
                            title='Ish faoliyatidan qoniqish darajasi taqsimoti',
                            color_discrete_sequence=['#FF6B6B'])
            fig.update_layout(xaxis_title='Qoniqish darajasi (1-10)', height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Ish faoliyatidan qoniqish darajasi haqida ma'lumot mavjud emas")
    
    with col2:
        # Work-life balance
        if has_wlb:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("Ish-hayot muvozanati")
            
            fig = px.histogram(df, x='WorkLifeBalance', nbins=10, 
                            title='Ish-hayot muvozanati taqsimoti',
                            color_discrete_sequence=['#4ECDC4'])
            fig.update_layout(xaxis_title='Ish-hayot muvozanati (1-10)', height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Ish-hayot muvozanati haqida ma'lumot mavjud emas")
    
    # Lavozim bo'yicha ish qoniqish darajasi
    if has_role and has_satisfaction:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Lavozim bo'yicha ish qoniqish darajasi")
        
        role_satisfaction = df.groupby('Role', observed=True)['JobSatisfaction'].mean().sort_values(ascending=False).reset_index()
        
        fig = px.bar(role_satisfaction, x='Role', y='JobSatisfaction', 
                    title='Lavozim bo\'yicha o\'rtacha ish qoniqish darajasi',
                    color='JobSatisfaction', color_continuous_scale='RdYlGn')
        fig.update_layout(yaxis_title='O\'rtacha qoniqish darajasi (1-10)', height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Maosh va ish qoniqish o'rtasidagi bog'liqlik
    if has_salary and has_satisfaction:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Maosh va ish qoniqish darajasi o'rtasidagi bog'liqlik")
        
        fig = px.scatter(df, x='Salary', y='JobSatisfaction', 
                        title='Maosh va ish qoniqish darajasi o\'rtasidagi bog\'liqlik',
                        color='JobSatisfaction', size='Salary',
                        color_continuous_scale='RdYlGn')
        fig.update_layout(height=500, 
                          xaxis_title='Maosh ($)',
                          yaxis_title='Ish qoniqish darajasi (1-10)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Korrelyatsiya koeffitsientini hisoblash
        correlation = df['Salary'].corr(df['JobSatisfaction'])
        st.write(f"Maosh va ish qoniqish darajasi o'rtasidagi korrelyatsiya koeffitsienti: **{correlation:.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Maosh va ish-hayot muvozanati o'rtasidagi bog'liqlik
    if has_salary and has_wlb:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Maosh va ish-hayot muvozanati o'rtasidagi bog'liqlik")
        
        # Maosh kategoriyalarga ajratish
        df['SalaryBin'] = pd.qcut(df['Salary'], q=5, labels=['Eng past', 'Past', "O'rta", 'Yuqori', 'Eng yuqori'])
        
        salary_wlb = df.groupby('SalaryBin', observed=True)['WorkLifeBalance'].mean().reset_index()
        
        fig = px.bar(salary_wlb, x='SalaryBin', y='WorkLifeBalance', 
                    title='Maosh kategoriyasi va o\'rtacha ish-hayot muvozanati',
                    color='WorkLifeBalance', color_continuous_scale='RdYlGn')
        fig.update_layout(height=400, 
                          xaxis_title='Maosh kategoriyasi',
                          yaxis_title='O\'rtacha ish-hayot muvozanati (1-10)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Qo'shimcha statistik analiz
if st.checkbox("Qo'shimcha statistik analiz ko'rsatish"):
    st.header("Qo'shimcha statistik analiz")
    
    # Korrelyatsiya matritsasi
    st.subheader("Korrelyatsiya matritsasi")
    
    # Raqamli ustunlarni olish
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        
        fig = px.imshow(corr_matrix, 
                       title='Raqamli ma\'lumotlar o\'rtasidagi korrelyatsiya',
                       color_continuous_scale='RdBu_r',
                       text_auto='.2f')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Korrelyatsiya matritsasi uchun yetarli raqamli ustunlar mavjud emas")
    
    # Lavozimlar bo'yicha statistika
    if has_role:
        st.subheader("Lavozimlar bo'yicha statistika")
        
        role_stats = df.groupby('Role', observed=True).agg({
            'YearsExperience': 'mean' if has_experience else 'count',
            'Salary': 'mean' if has_salary else 'count',
            'JobSatisfaction': 'mean' if has_satisfaction else 'count',
            'WorkLifeBalance': 'mean' if has_wlb else 'count'
        }).reset_index()
        
        st.dataframe(role_stats)

# Footer
st.markdown("---")
st.caption("Data Professional Survey Dashboardi | UktambekA/Data-Professional-Survey")
st.caption("Streamlit va Plotly yordamida yaratilgan | 2025")
