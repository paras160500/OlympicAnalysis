import pandas as pd 
import streamlit as st 
import numpy as np 
import pickle
import matplotlib.pyplot as plt 
import preprocessor
import helper
import plotly.express as px 
import seaborn as sns
import plotly.figure_factory as ff

# Page config
st.set_page_config(
    page_title="Olympics Analytics",
    page_icon="🏅",
    layout="wide"
)

# Professional CSS with animations and colorful labels
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    .main {
        font-family: 'Roboto', sans-serif;
        background: #f5f7fa;
        color: #3498db;
    }
    
    .stApp {
        background: #f5f7fa;
        color: #3498db;
    }
    
    /* Make all Streamlit text blue */
    .stMarkdown, .stText, p, span, div, label {
        color: #3498db !important;
    }
    
    /* Streamlit specific elements */
    .stSelectbox label, .stButton label, .stDataFrame, .stTable {
        color: #3498db !important;
    }
    
    /* Navigation Bar */
    .nav-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 0;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
    }
    
    .logo {
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .nav-links {
        display: flex;
        gap: 30px;
    }
    
    .nav-link {
        color: white;
        text-decoration: none;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .nav-link:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    
    .nav-link.active {
        background: rgba(255,255,255,0.2);
        border-color: rgba(255,255,255,0.4);
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 20px;
        text-align: center;
        margin: -1rem -1rem 3rem -1rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.1;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0 0 20px 0;
        color: white !important;
        animation: fadeInUp 1s ease-out;
    }
    
    .hero p {
        font-size: 1.3rem;
        margin: 0;
        opacity: 0.9;
        color: white !important;
        animation: fadeInUp 1s ease-out 0.3s both;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Animated Counter */
    .counter {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3498db;
        display: block;
        animation: countUp 1.5s ease-out;
    }
    
    @keyframes countUp {
        from { 
            opacity: 0;
            transform: scale(0.5);
        }
        to { 
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .stat-box {
        background: white;
        padding: 30px 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 25px rgba(0,0,0,0.08);
        border: 1px solid #e1e8ed;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.1), transparent);
        transition: left 0.6s;
    }
    
    .stat-box:hover::before {
        left: 100%;
    }
    
    .stat-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        border-color: #667eea;
    }
    
    .stat-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        display: block;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 60%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        80% {
            transform: translateY(-5px);
        }
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #667eea;
        margin: 10px 0;
        position: relative;
    }
    
    .stat-label {
        color: #3498db;
        font-size: 1rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #3498db;
        margin: 50px 0 30px 0;
        text-align: center;
        position: relative;
        animation: slideIn 0.8s ease-out;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: #3498db;
        border-radius: 2px;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Chart Cards */
    .chart-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 25px 0;
        box-shadow: 0 4px 25px rgba(0,0,0,0.08);
        border: 1px solid #e1e8ed;
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chart-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #3498db;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Table Styling */
    .dataframe {
        animation: slideInTable 0.8s ease-out;
    }
    
    @keyframes slideInTable {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Filter Section */
    .filter-section {
        background: white;
        padding: 25px;
        border-radius: 12px;
        margin: 25px 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
    }
    
    .filter-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #3498db;
        margin-bottom: 15px;
    }
    
    /* Olympics rings decoration */
    .rings-decoration {
        text-align: center;
        margin: 40px 0;
        font-size: 3rem;
        animation: ringRotate 4s linear infinite;
    }
    
    @keyframes ringRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Medal badges */
    .medal-count {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 2px;
    }
    
    .gold { background: #ffd700; color: #8b4513; }
    .silver { background: #c0c0c0; color: #2f4f4f; }
    .bronze { background: #cd7f32; color: white; }
    
    /* Loading animation */
    .loading {
        text-align: center;
        padding: 40px;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* Remove dark mode color overrides */
    
    /* Remove default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    return preprocessor.preprocess(df, region_df)

df = load_data()

# Hero Section
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>🏅 Olympics Analytics Dashboard</h1>
        <p>Explore 120+ years of Olympic Games data with interactive visualizations</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Navigation
col1, col2, col3, col4 = st.columns(4)

with col1:
    medal_tally_btn = st.button("🏆 Medal Tally", use_container_width=True)
with col2:
    overall_btn = st.button("📊 Overall Stats", use_container_width=True)
with col3:
    country_btn = st.button("🌍 Country Analysis", use_container_width=True)
with col4:
    athlete_btn = st.button("👤 Athlete Analysis", use_container_width=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'overall'

# Update page based on button clicks
if medal_tally_btn:
    st.session_state.current_page = 'medal_tally'
elif overall_btn:
    st.session_state.current_page = 'overall'
elif country_btn:
    st.session_state.current_page = 'country'
elif athlete_btn:
    st.session_state.current_page = 'athlete'

# Medal Tally Page
if st.session_state.current_page == 'medal_tally':
    st.markdown('<h2 class="section-title">🏆 Olympic Medal Tally</h2>', unsafe_allow_html=True)
    
    # st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">📋 Filter Options</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        years, countries = helper.country_year_list(df)
        selected_year = st.selectbox('📅 Select Year', years, key="year")
    with col2:
        selected_country = st.selectbox('🌍 Select Country', countries, key="country")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    medal_tally = helper.fetch_metal_tally(df, selected_year, selected_country)
    
    # Dynamic title
    if selected_country == 'Overall' and selected_year == 'Overall':
        title = "🌟 All-Time Olympic Medal Standings"
    elif selected_country == 'Overall':
        title = f"🗓️ {selected_year} Olympic Medal Standings"
    elif selected_year == 'Overall':
        title = f"🏳️ {selected_country} - All-Time Medal Count"
    else:
        title = f"🏆 {selected_country} - {selected_year} Performance"
    
    st.markdown(f'<div class="chart-card"><h3 class="chart-title">{title}</h3>', unsafe_allow_html=True)
    st.dataframe(medal_tally, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Overall Analysis Page
elif st.session_state.current_page == 'overall':
    st.markdown('<h2 class="section-title">📊 Olympic Games Overview</h2>', unsafe_allow_html=True)
    
    # Calculate statistics
    editions = df['Year'].unique().shape[0] - 1 
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    # Stats grid
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-box">
            <span class="stat-icon">🏟️</span>
            <div class="stat-value counter">{editions}</div>
            <div class="stat-label">Olympic Editions</div>
        </div>
        <div class="stat-box">
            <span class="stat-icon">🏙️</span>
            <div class="stat-value counter">{cities}</div>
            <div class="stat-label">Host Cities</div>
        </div>
        <div class="stat-box">
            <span class="stat-icon">⚽</span>
            <div class="stat-value counter">{sports}</div>
            <div class="stat-label">Sports</div>
        </div>
        <div class="stat-box">
            <span class="stat-icon">🎪</span>
            <div class="stat-value counter">{events}</div>
            <div class="stat-label">Events</div>
        </div>
        <div class="stat-box">
            <span class="stat-icon">👥</span>
            <div class="stat-value counter">{athletes:,}</div>
            <div class="stat-label">Athletes</div>
        </div>
        <div class="stat-box">
            <span class="stat-icon">🌎</span>
            <div class="stat-value counter">{nations}</div>
            <div class="stat-label">Nations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # # Olympic rings decoration
    # st.markdown('<div class="rings-decoration">🔵⚫🔴🟡🟢</div>', unsafe_allow_html=True)

    # Charts
    st.markdown('<h3 class="section-title">📈 Growth Trends</h3>', unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown('<br>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<h4 class="chart-title">🌍 Nations Participation</h4>', unsafe_allow_html=True)
        nations_over_time = helper.participation_nation_over_time(df)
        fig = px.area(nations_over_time, x='Year', y='count', 
                     color_discrete_sequence=['#667eea'])
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<h4 class="chart-title">👥 Athletes Participation</h4>', unsafe_allow_html=True)
        athletes_over_time = helper.atheletes_over_time(df)
        fig = px.area(athletes_over_time, x='Year', y='count',
                     color_discrete_sequence=['#764ba2'])
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Events over time
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<h4 class="chart-title">🎪 Events Growth Timeline</h4>', unsafe_allow_html=True)
    events_over_time = helper.total_events_over_time(df)
    fig = px.bar(events_over_time, x='Year', y='count',
                color_discrete_sequence=['#ff6b6b'])
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Sports heatmap
    st.markdown('<h4 class="chart-title">🔥 Sports Evolution Heatmap</h4>', unsafe_allow_html=True)
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(16, 12))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    
    sns.heatmap(heatmap_data, annot=True, cmap='viridis', 
               linewidths=0.5, ax=ax, cbar_kws={'shrink': 0.8})
    ax.set_title('Olympic Sports Through the Years', fontsize=18, fontweight='bold', pad=20)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # Top athletes
    st.markdown('<h4 class="chart-title">⭐ Hall of Fame</h4>', unsafe_allow_html=True)
    # st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('🎯 Select Sport', sport_list, key="sport_overall")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    top_athletes = helper.most_successfull(df, selected_sport)
    st.dataframe(top_athletes, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Country Analysis Page
elif st.session_state.current_page == 'country':
    st.markdown('<h2 class="section-title">🌍 Country Performance Deep Dive</h2>', unsafe_allow_html=True)
    
    # st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">🎯 Select Country</div>', unsafe_allow_html=True)
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.selectbox('Choose Country', country_list, key="country_analysis")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Medal timeline
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(f'<h4 class="chart-title">📈 {selected_country} Medal Timeline</h4>', unsafe_allow_html=True)
    country_df = helper.year_wise_medal_tally(df, selected_country)
    
    fig = px.line(country_df, x='Year', y='Medal',
                 color_discrete_sequence=['#ff6b6b'])
    fig.update_traces(line=dict(width=3), marker=dict(size=6))
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sport performance heatmap
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(f'<h4 class="chart-title">🎯 {selected_country} Sport Performance Matrix</h4>', unsafe_allow_html=True)
    
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(pt, annot=True, cmap='RdYlBu_r', ax=ax,
               linewidths=0.5, cbar_kws={'shrink': 0.8})
    ax.set_title(f'{selected_country} - Medal Distribution by Sport and Year', 
                fontsize=16, fontweight='bold', pad=15)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # Top athletes
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(f'<h4 class="chart-title">🏆 {selected_country} Top Performers</h4>', unsafe_allow_html=True)
    top_athletes = helper.country_wise_top_athelete(df, selected_country)
    st.dataframe(top_athletes, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Athlete Analysis Page
elif st.session_state.current_page == 'athlete':
    st.markdown('<h2 class="section-title">👤 Athlete Demographics & Performance</h2>', unsafe_allow_html=True)
    
    # Age distribution
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<h4 class="chart-title">📊 Age Distribution Analysis</h4>', unsafe_allow_html=True)
    
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    all_ages = athlete_df.Age.dropna()
    gold_ages = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    silver_ages = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    bronze_ages = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    
    fig = ff.create_distplot(
        [all_ages, gold_ages, silver_ages, bronze_ages],
        ['All Athletes', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
        show_hist=False, show_rug=False,
        colors=['#95a5a6', '#f1c40f', '#bdc3c7', '#d35400']
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Height vs Weight
    # st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">🎯 Select Sport for Physical Analysis</div>', unsafe_allow_html=True)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    selected_sport = st.selectbox('Choose Sport', sport_list, key="sport_physical")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(f'<h4 class="chart-title">📏 {selected_sport} - Height vs Weight</h4>', unsafe_allow_html=True)
    
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    scatter = sns.scatterplot(data=temp_df, x='Weight', y='Height', 
                             hue='Medal', style='Sex', s=80, alpha=0.7, ax=ax)
    ax.set_title(f'Physical Attributes Distribution - {selected_sport}', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Weight (kg)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Height (cm)', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # Gender participation
    # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<h4 class="chart-title">⚖️ Gender Participation Evolution</h4>', unsafe_allow_html=True)
    
    gender_df = helper.men_women_participation(df)
    fig = px.area(gender_df, x='Year', y=['Male', 'Female'],
                 color_discrete_sequence=['#3498db', '#e74c3c'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #64748b;">
    <p><strong>Olympics Analytics Dashboard</strong> | Powered by Streamlit & Python</p>
    <p style="font-size: 0.9rem; margin-top: 10px;">🏅 Celebrating Olympic Excellence Through Data 🏅</p>
</div>
""", unsafe_allow_html=True)