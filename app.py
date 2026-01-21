import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import calendar
import random
import warnings
warnings.filterwarnings('ignore')

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="NutriLife Analytics Pro",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== DARK/LIGHT THEME SETTINGS ==========
def apply_theme(theme='light'):
    """Apply CSS theme based on selection"""
    if theme == 'dark':
        st.markdown("""
        <style>
            /* Dark Theme */
            .main {
                background-color: #0f172a;
                color: #f8fafc;
            }
            
            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            }
            
            /* Headers */
            .main-header {
                background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 25%, #ec4899 50%, #f97316 75%, #fbbf24 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .section-header {
                color: #e2e8f0;
                background: linear-gradient(90deg, rgba(96, 165, 250, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
                border-left: 5px solid #60a5fa;
            }
            
            /* Cards */
            .viz-card {
                background: #1e293b;
                border: 1px solid #334155;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
            }
            
            .metric-card {
                background: #1e293b;
                border: 1px solid #334155;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background: #334155;
            }
            
            .stTabs [data-baseweb="tab"] {
                background: #475569;
                color: #cbd5e1;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 100%);
                color: white;
            }
            
            /* Scrollbar */
            ::-webkit-scrollbar-track {
                background: #334155;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #60a5fa 0%, #8b5cf6 100%);
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            /* Light Theme (Default) */
            .main {
                background-color: #f8fafc;
            }
            
            .stApp {
                background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            }
            
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #ff7e5f 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .section-header {
                color: #1a202c;
                background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-left: 5px solid #667eea;
            }
            
            .viz-card {
                background: white;
                border: 1px solid #e2e8f0;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            }
            
            .metric-card {
                background: white;
                border: 1px solid #e2e8f0;
            }
        </style>
        """, unsafe_allow_html=True)

# ========== ENHANCED DATA GENERATION ==========
@st.cache_data(ttl=3600, show_spinner="🔄 Loading comprehensive health data...")
def generate_enhanced_dataset(n_samples=5000):
    """Generate comprehensive synthetic health data with timeline"""
    np.random.seed(42)
    
    # Timeline periods with characteristics
    timeline_periods = ['Pre-Industrial (1700-1850)', 'Industrial (1850-1950)', 
                       'Post-War (1950-2000)', 'Modern (2000-Present)', 'Future (2024+)']
    timeline_weights = [0.05, 0.15, 0.25, 0.45, 0.10]
    
    # Enhanced country list
    countries_by_region = {
        'North America': ['USA', 'Canada', 'Mexico'],
        'Europe': ['UK', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands'],
        'Asia Pacific': ['China', 'Japan', 'India', 'Australia', 'South Korea', 'Singapore'],
        'Latin America': ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru'],
        'Middle East': ['UAE', 'Saudi Arabia', 'Israel', 'Turkey', 'Qatar'],
        'Africa': ['South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Morocco']
    }
    
    # Urbanization levels
    urbanization_levels = ['Rural', 'Suburban', 'Urban', 'Metropolitan']
    
    data = []
    
    for i in range(n_samples):
        # Determine timeline period
        timeline = np.random.choice(timeline_periods, p=timeline_weights)
        
        # Timeline-based adjustments
        if timeline == 'Pre-Industrial (1700-1850)':
            base_bmi = np.random.normal(22, 2)
            base_activity = 'Very Active'
            junk_factor = 0.1
            processed_food = 0.05
            avg_age = 45
            pollution_level = 0.2
            
        elif timeline == 'Industrial (1850-1950)':
            base_bmi = np.random.normal(23, 2.5)
            base_activity = 'Active'
            junk_factor = 0.3
            processed_food = 0.2
            avg_age = 55
            pollution_level = 0.6
            
        elif timeline == 'Post-War (1950-2000)':
            base_bmi = np.random.normal(24, 3)
            base_activity = 'Moderate'
            junk_factor = 0.5
            processed_food = 0.4
            avg_age = 65
            pollution_level = 0.4
            
        elif timeline == 'Modern (2000-Present)':
            base_bmi = np.random.normal(26, 3.5)
            base_activity = 'Light'
            junk_factor = 0.7
            processed_food = 0.6
            avg_age = 75
            pollution_level = 0.3
            
        else:  # Future
            base_bmi = np.random.normal(27, 4)
            base_activity = 'Sedentary'
            junk_factor = 0.9
            processed_food = 0.8
            avg_age = 80
            pollution_level = 0.5
        
        # Age with timeline adjustment
        age = np.random.normal(avg_age, 15)
        age = max(18, min(95, age))
        age_group = '18-29' if age < 30 else '30-44' if age < 45 else '45-59' if age < 60 else '60+'
        
        # Demographics
        gender = np.random.choice(['Male', 'Female', 'Other'], p=[0.48, 0.50, 0.02])
        
        # Select region and country
        region = np.random.choice(list(countries_by_region.keys()))
        country = np.random.choice(countries_by_region[region])
        
        # Urbanization
        urbanization = np.random.choice(urbanization_levels, 
                                      p=[0.3, 0.3, 0.25, 0.15])
        
        # Income levels by country (simplified)
        if country in ['USA', 'Germany', 'Japan', 'Australia', 'UAE', 'Singapore']:
            income = np.random.choice(['Low', 'Middle', 'High'], p=[0.2, 0.5, 0.3])
        else:
            income = np.random.choice(['Low', 'Middle', 'High'], p=[0.4, 0.5, 0.1])
        
        # Lifestyle factors
        activity_levels = ['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active']
        activity_probs = {
            'Sedentary': [0.4, 0.3, 0.2, 0.1, 0.0],
            'Light': [0.3, 0.4, 0.2, 0.1, 0.0],
            'Moderate': [0.1, 0.3, 0.4, 0.15, 0.05],
            'Active': [0.05, 0.15, 0.3, 0.4, 0.1],
            'Very Active': [0.0, 0.05, 0.15, 0.3, 0.5]
        }
        
        activity_level = np.random.choice(activity_levels, 
                                        p=activity_probs[base_activity])
        
        junk_frequency = np.random.choice([
            'Never', 'Rarely (1-2/month)', 'Occasional (1-2/week)', 
            'Frequent (3-4/week)', 'Daily'
        ], p=[0.15 - junk_factor*0.1, 
              0.25 - junk_factor*0.15, 
              0.35 + junk_factor*0.1, 
              0.15 + junk_factor*0.1, 
              0.1 + junk_factor*0.05])
        
        sleep_hours = np.random.normal(7.2 - junk_factor*0.5, 1.5)
        sleep_hours = max(4, min(10, sleep_hours))
        
        stress_level = np.random.normal(5.5 + junk_factor*1.5, 2.0)
        stress_level = max(1, min(10, stress_level))
        
        # Health metrics with timeline effects
        bmi = max(15, min(40, base_bmi + np.random.normal(0, 2)))
        
        # Blood pressure influenced by timeline and lifestyle
        bp_systolic = np.random.normal(120 + junk_factor*15 + (age/2), 15)
        bp_diastolic = bp_systolic * 0.65 + np.random.normal(0, 5)
        
        # Glucose levels
        glucose = np.random.normal(90 + junk_factor*20 + (age/3), 15)
        
        # Cholesterol with timeline effect
        hdl = np.random.normal(55 - junk_factor*15, 10)
        ldl = np.random.normal(115 + junk_factor*30, 25)
        
        # Calculate health scores
        health_score = max(0, min(100,
            75 - (junk_factor * 25) + 
            (activity_levels.index(activity_level) * 5) -
            (abs(sleep_hours - 7.5) * 4) -
            (stress_level * 2) -
            (pollution_level * 10) +
            np.random.normal(0, 8)
        ))
        
        # Risk calculations
        cvd_risk = min(100, max(5,
            5 + (age/2) + 
            (junk_factor * 40) +
            (bp_systolic - 120)/2 +
            (ldl - 100)/5 +
            (1 if activity_level in ['Sedentary', 'Light'] else 0) * 15 +
            np.random.normal(0, 5)
        ))
        
        diabetes_risk = min(100, max(5,
            5 + (age/3) +
            (junk_factor * 35) +
            (glucose - 90)/2 +
            (bmi - 22) * 2 +
            (1 if activity_level in ['Sedentary', 'Light'] else 0) * 12 +
            np.random.normal(0, 4)
        ))
        
        # Cancer risk
        cancer_risk = min(100, max(5,
            5 + (age/4) +
            (junk_factor * 25) +
            (pollution_level * 20) +
            np.random.normal(0, 5)
        ))
        
        # Economic impact
        annual_cost = max(500, min(50000,
            500 +
            (junk_factor * 3000) +
            (cvd_risk * 50) +
            (diabetes_risk * 40) +
            (age/2) * 100 +
            np.random.normal(0, 500)
        ))
        
        data.append({
            # Identifiers
            'id': f"P{10000 + i:05d}",
            
            # Timeline & Location
            'timeline_period': timeline,
            'region': region,
            'country': country,
            'urbanization': urbanization,
            
            # Demographics
            'age': int(age),
            'age_group': age_group,
            'gender': gender,
            'income_level': income,
            
            # Lifestyle
            'junk_frequency': junk_frequency,
            'activity_level': activity_level,
            'sleep_hours': round(sleep_hours, 1),
            'stress_level': round(stress_level, 1),
            'processed_food_index': round(processed_food + np.random.normal(0, 0.1), 2),
            'pollution_exposure': round(pollution_level + np.random.normal(0, 0.1), 2),
            
            # Health Metrics
            'bmi': round(bmi, 1),
            'blood_pressure': f"{int(bp_systolic)}/{int(bp_diastolic)}",
            'blood_glucose': round(glucose),
            'cholesterol_total': round(hdl + ldl + np.random.normal(35, 10)),
            'hdl_cholesterol': round(max(20, hdl)),
            'ldl_cholesterol': round(max(30, ldl)),
            
            # Scores
            'health_score': round(health_score),
            'cvd_risk_score': round(cvd_risk),
            'diabetes_risk_score': round(diabetes_risk),
            'cancer_risk_score': round(cancer_risk),
            'mental_health_score': round(100 - (stress_level * 7.5)),
            'longevity_index': round(100 - (cvd_risk * 0.3) - (diabetes_risk * 0.2) - (age/4), 1),
            
            # Economic Impact
            'annual_healthcare_cost': round(annual_cost),
            'productivity_loss_days': int(np.random.normal(5, 3) + junk_factor * 10),
            'lifetime_cost_estimate': round(annual_cost * (85 - age)),
            
            # Behavioral Metrics
            'health_literacy': np.random.choice(['Low', 'Medium', 'High'], p=[0.3, 0.5, 0.2]),
            'preventive_care': np.random.choice(['None', 'Basic', 'Regular', 'Comprehensive'], 
                                               p=[0.2, 0.4, 0.3, 0.1]),
            'technology_adoption': np.random.choice(['Low', 'Medium', 'High'], 
                                                   p=[0.3, 0.4, 0.3]),
            
            # Flags
            'high_risk_flag': int(cvd_risk > 60 or diabetes_risk > 60 or cancer_risk > 60),
            'intervention_needed': int(health_score < 60 or cvd_risk > 50 or diabetes_risk > 50),
            'positive_trend': np.random.choice([0, 1], p=[0.7, 0.3]),
        })
    
    df = pd.DataFrame(data)
    
    # Add derived columns with FIXED bin edges
    df['risk_category'] = pd.cut(df['cvd_risk_score'], 
        bins=[0, 20, 40, 60, 80, 100],
        labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High']
    )
    
    # FIXED: Corrected bin edges for health_category (6 edges for 5 intervals)
    df['health_category'] = pd.cut(df['health_score'],
        bins=[0, 40, 60, 80, 90, 100],  # 6 edges = 5 intervals
        labels=['Critical', 'Poor', 'Fair', 'Good', 'Excellent']  # 5 labels
    )
    
    # Fix the sunburst chart issue by ensuring all leaves
    # We'll aggregate the data for the sunburst chart separately
    df_sunburst = df.groupby(['region', 'age_group', 'health_category']).agg({
        'id': 'count',
        'health_score': 'mean',
        'cvd_risk_score': 'mean'
    }).reset_index()
    df_sunburst = df_sunburst.rename(columns={'id': 'count'})
    
    return df, df_sunburst

# ========== FIXED VISUALIZATION FUNCTIONS ==========
def create_fixed_sunburst_chart(df_sunburst):
    """Create sunburst chart with fixed dataframe"""
    try:
        fig = px.sunburst(
            df_sunburst,
            path=['region', 'age_group', 'health_category'],
            values='count',
            color='health_score',
            color_continuous_scale='RdYlGn',
            title="🌳 Health Distribution by Region & Age (Aggregated)",
            hover_data=['cvd_risk_score']
        )
        fig.update_layout(height=600)
        return fig
    except Exception as e:
        # Create a simple bar chart as fallback
        st.error(f"Sunburst chart error: {str(e)}")
        return create_fallback_chart(df_sunburst)

def create_fallback_chart(df):
    """Create fallback bar chart"""
    fig = px.bar(df.head(20), x='region', y='count', color='health_category',
                title="Health Distribution by Region")
    fig.update_layout(height=500)
    return fig

def create_3d_scatter_health(df):
    """Create 3D scatter plot of health metrics"""
    # Sample for better performance
    sample_df = df.sample(min(1000, len(df)))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=sample_df['age'],
        y=sample_df['bmi'],
        z=sample_df['health_score'],
        mode='markers',
        marker=dict(
            size=6,
            color=sample_df['cvd_risk_score'],
            colorscale='Viridis',
            opacity=0.8,
            colorbar=dict(title="CVD Risk", x=1.02)
        ),
        text=sample_df.apply(lambda row: f"Country: {row['country']}<br>Activity: {row['activity_level']}", axis=1),
        hovertemplate="<b>Age:</b> %{x}<br>" +
                     "<b>BMI:</b> %{y}<br>" +
                     "<b>Health Score:</b> %{z}<br>" +
                     "%{text}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title="🎯 3D Health Metrics: Age vs BMI vs Health Score",
        scene=dict(
            xaxis_title="Age (years)",
            yaxis_title="BMI",
            zaxis_title="Health Score",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=600,
        margin=dict(l=0, r=100, t=50, b=0)
    )
    
    return fig

def create_3d_timeline_evolution(df):
    """Create 3D timeline evolution plot"""
    # Aggregate by timeline period
    timeline_data = df.groupby('timeline_period').agg({
        'health_score': 'mean',
        'bmi': 'mean',
        'cvd_risk_score': 'mean',
        'age': 'mean',
        'id': 'count'
    }).reset_index().rename(columns={'id': 'count'})
    
    # Sort by timeline order
    timeline_order = ['Pre-Industrial (1700-1850)', 'Industrial (1850-1950)', 
                     'Post-War (1950-2000)', 'Modern (2000-Present)', 'Future (2024+)']
    timeline_data['timeline_order'] = timeline_data['timeline_period'].apply(
        lambda x: timeline_order.index(x) if x in timeline_order else len(timeline_order)
    )
    timeline_data = timeline_data.sort_values('timeline_order')
    
    fig = go.Figure()
    
    # Add 3D line
    fig.add_trace(go.Scatter3d(
        x=timeline_data['timeline_order'],
        y=timeline_data['bmi'],
        z=timeline_data['health_score'],
        mode='lines+markers+text',
        line=dict(color='#667eea', width=4),
        marker=dict(
            size=12,
            color=timeline_data['cvd_risk_score'],
            colorscale='Hot',
            showscale=True,
            colorbar=dict(title="CVD Risk", x=1.02)
        ),
        text=timeline_data['timeline_period'],
        textposition="top center",
        hovertemplate="<b>%{text}</b><br>" +
                     "<b>Avg BMI:</b> %{y:.1f}<br>" +
                     "<b>Avg Health Score:</b> %{z:.1f}<br>" +
                     "<b>Avg CVD Risk:</b> %{marker.color:.1f}<br>" +
                     "<extra></extra>"
    ))
    
    fig.update_layout(
        title="📜 3D Timeline Evolution: Health Trends Through History",
        scene=dict(
            xaxis_title="Timeline Period",
            yaxis_title="Average BMI",
            zaxis_title="Average Health Score",
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.2)
            )
        ),
        height=600,
        margin=dict(l=0, r=100, t=50, b=0)
    )
    
    return fig

def create_choropleth_world_map(df):
    """Create choropleth world map"""
    # Aggregate by country
    country_data = df.groupby('country').agg({
        'health_score': 'mean',
        'cvd_risk_score': 'mean',
        'id': 'count'
    }).reset_index().rename(columns={'id': 'participants'})
    
    # Country ISO codes mapping (simplified)
    country_iso = {
        'USA': 'USA', 'Canada': 'CAN', 'Mexico': 'MEX',
        'UK': 'GBR', 'Germany': 'DEU', 'France': 'FRA', 'Italy': 'ITA', 
        'Spain': 'ESP', 'Netherlands': 'NLD',
        'China': 'CHN', 'Japan': 'JPN', 'India': 'IND', 
        'Australia': 'AUS', 'South Korea': 'KOR', 'Singapore': 'SGP',
        'Brazil': 'BRA', 'Argentina': 'ARG', 'Chile': 'CHL', 
        'Colombia': 'COL', 'Peru': 'PER',
        'UAE': 'ARE', 'Saudi Arabia': 'SAU', 'Israel': 'ISR', 
        'Turkey': 'TUR', 'Qatar': 'QAT',
        'South Africa': 'ZAF', 'Nigeria': 'NGA', 'Kenya': 'KEN', 
        'Egypt': 'EGY', 'Morocco': 'MAR'
    }
    
    country_data['iso_alpha'] = country_data['country'].map(country_iso)
    
    fig = px.choropleth(
        country_data,
        locations='iso_alpha',
        color='health_score',
        hover_name='country',
        hover_data=['cvd_risk_score', 'participants'],
        color_continuous_scale='RdYlGn',
        title="🗺️ Global Health Score Distribution",
        projection='natural earth'
    )
    
    fig.update_layout(height=500, margin=dict(l=0, r=0, t=50, b=0))
    fig.update_geos(showcoastlines=True, coastlinecolor="Black",
                   showland=True, landcolor="lightgray")
    
    return fig

def create_timeline_comparison(df):
    """Create timeline comparison visualization"""
    timeline_comparison = df.groupby('timeline_period').agg({
        'health_score': ['mean', 'std'],
        'bmi': 'mean',
        'cvd_risk_score': 'mean',
        'diabetes_risk_score': 'mean',
        'annual_healthcare_cost': 'mean',
        'id': 'count'
    }).reset_index()
    
    timeline_comparison.columns = ['timeline_period', 'health_mean', 'health_std', 
                                  'bmi_mean', 'cvd_mean', 'diabetes_mean', 
                                  'cost_mean', 'count']
    
    # Sort by timeline order
    timeline_order = ['Pre-Industrial (1700-1850)', 'Industrial (1850-1950)', 
                     'Post-War (1950-2000)', 'Modern (2000-Present)', 'Future (2024+)']
    timeline_comparison['order'] = timeline_comparison['timeline_period'].apply(
        lambda x: timeline_order.index(x) if x in timeline_order else len(timeline_order)
    )
    timeline_comparison = timeline_comparison.sort_values('order')
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Health Score Trend', 'BMI Trend', 
                       'Risk Score Trends', 'Healthcare Costs'),
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )
    
    # Health Score
    fig.add_trace(
        go.Scatter(
            x=timeline_comparison['timeline_period'],
            y=timeline_comparison['health_mean'],
            error_y=dict(
                type='data',
                array=timeline_comparison['health_std'],
                visible=True
            ),
            mode='lines+markers',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=10),
            name='Health Score'
        ),
        row=1, col=1
    )
    
    # BMI
    fig.add_trace(
        go.Bar(
            x=timeline_comparison['timeline_period'],
            y=timeline_comparison['bmi_mean'],
            marker_color=['#3498db', '#9b59b6', '#e74c3c', '#f39c12', '#1abc9c'],
            name='BMI'
        ),
        row=1, col=2
    )
    
    # Risk Scores
    fig.add_trace(
        go.Scatter(
            x=timeline_comparison['timeline_period'],
            y=timeline_comparison['cvd_mean'],
            mode='lines+markers',
            line=dict(color='#e74c3c', width=3),
            name='CVD Risk'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=timeline_comparison['timeline_period'],
            y=timeline_comparison['diabetes_mean'],
            mode='lines+markers',
            line=dict(color='#f39c12', width=3),
            name='Diabetes Risk'
        ),
        row=2, col=1
    )
    
    # Healthcare Costs
    fig.add_trace(
        go.Bar(
            x=timeline_comparison['timeline_period'],
            y=timeline_comparison['cost_mean'],
            marker_color=['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12'],
            name='Healthcare Cost'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=700, showlegend=True)
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_country_comparison(df):
    """Create country comparison visualization"""
    top_countries = df['country'].value_counts().head(10).index.tolist()
    country_data = df[df['country'].isin(top_countries)]
    
    country_stats = country_data.groupby('country').agg({
        'health_score': 'mean',
        'cvd_risk_score': 'mean',
        'bmi': 'mean',
        'annual_healthcare_cost': 'mean',
        'id': 'count'
    }).reset_index().rename(columns={'id': 'participants'})
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Health Score by Country', 'CVD Risk by Country',
                       'Average BMI by Country', 'Healthcare Costs by Country'),
        vertical_spacing=0.15,
        horizontal_spacing=0.15
    )
    
    # Health Score
    fig.add_trace(
        go.Bar(
            x=country_stats['country'],
            y=country_stats['health_score'],
            marker_color=px.colors.sequential.Viridis,
            name='Health Score'
        ),
        row=1, col=1
    )
    
    # CVD Risk
    fig.add_trace(
        go.Bar(
            x=country_stats['country'],
            y=country_stats['cvd_risk_score'],
            marker_color=px.colors.sequential.Reds,
            name='CVD Risk'
        ),
        row=1, col=2
    )
    
    # BMI
    fig.add_trace(
        go.Bar(
            x=country_stats['country'],
            y=country_stats['bmi'],
            marker_color=px.colors.sequential.Blues,
            name='BMI'
        ),
        row=2, col=1
    )
    
    # Healthcare Costs
    fig.add_trace(
        go.Bar(
            x=country_stats['country'],
            y=country_stats['annual_healthcare_cost'],
            marker_color=px.colors.sequential.Greens,
            name='Healthcare Cost'
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=700, showlegend=False)
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_custom_heatmap(df):
    """Create custom heatmap visualization"""
    # Prepare data for heatmap
    heatmap_data = df.groupby(['urbanization', 'income_level']).agg({
        'health_score': 'mean',
        'cvd_risk_score': 'mean',
        'id': 'count'
    }).reset_index()
    
    # Pivot for heatmap
    health_pivot = heatmap_data.pivot(index='urbanization', 
                                     columns='income_level', 
                                     values='health_score')
    
    risk_pivot = heatmap_data.pivot(index='urbanization', 
                                   columns='income_level', 
                                   values='cvd_risk_score')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Average Health Score', 'Average CVD Risk'),
        shared_yaxes=True
    )
    
    # Health Score Heatmap
    fig.add_trace(
        go.Heatmap(
            z=health_pivot.values,
            x=health_pivot.columns,
            y=health_pivot.index,
            colorscale='RdYlGn',
            text=np.round(health_pivot.values, 1),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(x=0.45, title="Health Score"),
            hovertemplate="Urbanization: %{y}<br>Income: %{x}<br>Health Score: %{z:.1f}<extra></extra>"
        ),
        row=1, col=1
    )
    
    # Risk Score Heatmap
    fig.add_trace(
        go.Heatmap(
            z=risk_pivot.values,
            x=risk_pivot.columns,
            y=risk_pivot.index,
            colorscale='Reds',
            text=np.round(risk_pivot.values, 1),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="CVD Risk"),
            hovertemplate="Urbanization: %{y}<br>Income: %{x}<br>CVD Risk: %{z:.1f}<extra></extra>"
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title="🔥 Heatmap: Urbanization vs Income Level",
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

# ========== ENHANCED FILTERS SIDEBAR ==========
def create_enhanced_sidebar():
    """Create enhanced sidebar with all filters"""
    with st.sidebar:
        # Theme selector at the top
        st.markdown("### 🎨 Theme Settings")
        theme = st.selectbox("Select Theme", ["Light", "Dark"], index=0)
        apply_theme(theme.lower())
        
        st.markdown("---")
        st.markdown("### 🔍 Advanced Filters")
        
        # Timeline Filter
        st.markdown("#### 📅 Timeline Period")
        timeline_options = ['All Periods', 'Pre-Industrial (1700-1850)', 
                          'Industrial (1850-1950)', 'Post-War (1950-2000)', 
                          'Modern (2000-Present)', 'Future (2024+)']
        selected_timeline = st.multiselect(
            "Select Timeline Periods",
            options=timeline_options[1:],
            default=timeline_options[1:]
        )
        
        # Region Filter
        st.markdown("#### 🌍 Regions")
        all_regions = ['North America', 'Europe', 'Asia Pacific', 
                      'Latin America', 'Middle East', 'Africa']
        selected_regions = st.multiselect(
            "Select Regions",
            options=all_regions,
            default=all_regions
        )
        
        # Country Filter (dependent on region)
        st.markdown("#### 🏙️ Countries")
        country_options = {
            'North America': ['USA', 'Canada', 'Mexico'],
            'Europe': ['UK', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands'],
            'Asia Pacific': ['China', 'Japan', 'India', 'Australia', 'South Korea', 'Singapore'],
            'Latin America': ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru'],
            'Middle East': ['UAE', 'Saudi Arabia', 'Israel', 'Turkey', 'Qatar'],
            'Africa': ['South Africa', 'Nigeria', 'Kenya', 'Egypt', 'Morocco']
        }
        
        # Get countries from selected regions
        available_countries = []
        for region in selected_regions:
            available_countries.extend(country_options.get(region, []))
        
        selected_countries = st.multiselect(
            "Select Countries",
            options=sorted(set(available_countries)),
            default=available_countries[:min(5, len(available_countries))]
        )
        
        # Demographics Filters
        st.markdown("#### 👥 Demographics")
        
        col1, col2 = st.columns(2)
        with col1:
            age_groups = ['18-29', '30-44', '45-59', '60+']
            selected_ages = st.multiselect(
                "Age Groups",
                options=age_groups,
                default=age_groups
            )
        
        with col2:
            gender_options = ['Male', 'Female', 'Other']
            selected_genders = st.multiselect(
                "Gender",
                options=gender_options,
                default=gender_options
            )
        
        # Lifestyle Filters
        st.markdown("#### 🏃 Lifestyle")
        
        activity_levels = ['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active']
        selected_activity = st.multiselect(
            "Activity Level",
            options=activity_levels,
            default=activity_levels
        )
        
        junk_frequencies = ['Never', 'Rarely (1-2/month)', 'Occasional (1-2/week)', 
                           'Frequent (3-4/week)', 'Daily']
        selected_junk = st.multiselect(
            "Junk Food Frequency",
            options=junk_frequencies,
            default=junk_frequencies
        )
        
        # Urbanization Filter
        st.markdown("#### 🏙️ Urbanization")
        urbanization_levels = ['Rural', 'Suburban', 'Urban', 'Metropolitan']
        selected_urbanization = st.multiselect(
            "Urbanization Level",
            options=urbanization_levels,
            default=urbanization_levels
        )
        
        # Income Filter
        st.markdown("#### 💰 Income Level")
        income_levels = ['Low', 'Middle', 'High']
        selected_income = st.multiselect(
            "Income Level",
            options=income_levels,
            default=income_levels
        )
        
        # Health Filters
        st.markdown("#### 🏥 Health Status")
        
        col1, col2 = st.columns(2)
        with col1:
            min_health = st.slider("Min Health Score", 0, 100, 0)
            max_health = st.slider("Max Health Score", 0, 100, 100)
        
        with col2:
            min_risk = st.slider("Min CVD Risk", 0, 100, 0)
            max_risk = st.slider("Max CVD Risk", 0, 100, 100)
        
        # Risk Category Filter
        risk_categories = ['Very Low', 'Low', 'Moderate', 'High', 'Very High']
        selected_risks = st.multiselect(
            "Risk Categories",
            options=risk_categories,
            default=risk_categories
        )
        
        # Data sampling for performance
        st.markdown("---")
        st.markdown("### ⚡ Performance Settings")
        sample_percentage = st.slider("Data Sample %", 10, 100, 50)
        
        return {
            'theme': theme,
            'selected_timeline': selected_timeline,
            'selected_regions': selected_regions,
            'selected_countries': selected_countries,
            'selected_ages': selected_ages,
            'selected_genders': selected_genders,
            'selected_activity': selected_activity,
            'selected_junk': selected_junk,
            'selected_urbanization': selected_urbanization,
            'selected_income': selected_income,
            'min_health': min_health,
            'max_health': max_health,
            'min_risk': min_risk,
            'max_risk': max_risk,
            'selected_risks': selected_risks,
            'sample_percentage': sample_percentage
        }

# ========== MAIN DASHBOARD ==========
def main():
    # Load data
    df, df_sunburst = generate_enhanced_dataset()
    
    # Create enhanced sidebar and get filters
    filters = create_enhanced_sidebar()
    
    # Apply filters
    mask = pd.Series(True, index=df.index)
    
    # Timeline filter
    if 'All Periods' not in filters['selected_timeline'] and filters['selected_timeline']:
        mask = mask & df['timeline_period'].isin(filters['selected_timeline'])
    
    # Region filter
    if filters['selected_regions']:
        mask = mask & df['region'].isin(filters['selected_regions'])
    
    # Country filter
    if filters['selected_countries']:
        mask = mask & df['country'].isin(filters['selected_countries'])
    
    # Age filter
    if filters['selected_ages']:
        mask = mask & df['age_group'].isin(filters['selected_ages'])
    
    # Gender filter
    if filters['selected_genders']:
        mask = mask & df['gender'].isin(filters['selected_genders'])
    
    # Activity filter
    if filters['selected_activity']:
        mask = mask & df['activity_level'].isin(filters['selected_activity'])
    
    # Junk food filter
    if filters['selected_junk']:
        mask = mask & df['junk_frequency'].isin(filters['selected_junk'])
    
    # Urbanization filter
    if filters['selected_urbanization']:
        mask = mask & df['urbanization'].isin(filters['selected_urbanization'])
    
    # Income filter
    if filters['selected_income']:
        mask = mask & df['income_level'].isin(filters['selected_income'])
    
    # Health score range
    mask = mask & (df['health_score'] >= filters['min_health']) & (df['health_score'] <= filters['max_health'])
    
    # Risk score range
    mask = mask & (df['cvd_risk_score'] >= filters['min_risk']) & (df['cvd_risk_score'] <= filters['max_risk'])
    
    # Risk category filter
    if filters['selected_risks']:
        mask = mask & df['risk_category'].isin(filters['selected_risks'])
    
    filtered_df = df[mask].copy()
    
    # Apply sampling for performance
    if filters['sample_percentage'] < 100:
        sample_size = int(len(filtered_df) * filters['sample_percentage'] / 100)
        filtered_df = filtered_df.sample(min(sample_size, len(filtered_df)), random_state=42)
    
    # Main header with stats
    st.markdown(f"<h1 class='main-header'>NutriLife Analytics Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: center; color: #64748b; margin-bottom: 2rem; font-size: 1.1rem;'>
    Complete Health Analytics Platform | {len(filtered_df):,} Participants | {len(filters['selected_countries'])} Countries
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Participants", f"{len(filtered_df):,}", 
                 f"{len(filters['selected_countries'])} countries")
    with col2:
        st.metric("Avg Health Score", f"{filtered_df['health_score'].mean():.1f}/100", 
                 f"±{filtered_df['health_score'].std():.1f}")
    with col3:
        high_risk_pct = (filtered_df['high_risk_flag'] == 1).mean() * 100
        st.metric("High Risk", f"{high_risk_pct:.1f}%", 
                 f"{filtered_df['high_risk_flag'].sum():,} individuals")
    with col4:
        avg_cost = filtered_df['annual_healthcare_cost'].mean()
        st.metric("Avg Healthcare Cost", f"${avg_cost:,.0f}", 
                 f"${filtered_df['annual_healthcare_cost'].sum()/1_000_000:.1f}M total")
    
    # ========== TIMELINE SECTION ==========
    st.markdown("<h2 class='section-header'>📜 Timeline Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='viz-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-header'>3D Timeline Evolution</h3>", unsafe_allow_html=True)
        fig_timeline_3d = create_3d_timeline_evolution(filtered_df)
        st.plotly_chart(fig_timeline_3d, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='viz-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-header'>Timeline Comparison</h3>", unsafe_allow_html=True)
        fig_timeline = create_timeline_comparison(filtered_df)
        st.plotly_chart(fig_timeline, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== GEOGRAPHICAL SECTION ==========
    st.markdown("<h2 class='section-header'>🌍 Geographical Analysis</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='viz-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='subsection-header'>Global Health Map</h3>", unsafe_allow_html=True)
    fig_world = create_choropleth_world_map(filtered_df)
    st.plotly_chart(fig_world, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='viz-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-header'>Country Comparison</h3>", unsafe_allow_html=True)
        fig_country = create_country_comparison(filtered_df)
        st.plotly_chart(fig_country, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='viz-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-header'>Health Distribution</h3>", unsafe_allow_html=True)
        fig_sunburst = create_fixed_sunburst_chart(df_sunburst)
        st.plotly_chart(fig_sunburst, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== 3D VISUALIZATIONS SECTION ==========
    st.markdown("<h2 class='section-header'>🎯 3D Visualizations</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='viz-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-header'>3D Health Metrics</h3>", unsafe_allow_html=True)
        fig_3d = create_3d_scatter_health(filtered_df)
        st.plotly_chart(fig_3d, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='viz-card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-header'>Urbanization & Income Heatmap</h3>", unsafe_allow_html=True)
        fig_heatmap = create_custom_heatmap(filtered_df)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== DETAILED ANALYSIS SECTION ==========
    st.markdown("<h2 class='section-header'>📊 Detailed Analysis</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Demographic Insights", "🏥 Health Metrics", "💰 Economic Impact"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution by timeline
            age_timeline = pd.crosstab(filtered_df['age_group'], filtered_df['timeline_period'])
            fig = px.bar(age_timeline, 
                        title="Age Distribution by Timeline Period",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gender distribution by region
            gender_region = pd.crosstab(filtered_df['region'], filtered_df['gender'])
            fig = px.bar(gender_region, 
                        title="Gender Distribution by Region",
                        barmode='group')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk score distribution
            fig = px.histogram(filtered_df, x='cvd_risk_score', nbins=30,
                              title="CVD Risk Score Distribution",
                              color_discrete_sequence=['#e74c3c'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Health score vs activity level
            fig = px.box(filtered_df, x='activity_level', y='health_score',
                        title="Health Score by Activity Level",
                        color='activity_level')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Healthcare costs by country
            cost_by_country = filtered_df.groupby('country')['annual_healthcare_cost'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(x=cost_by_country.index, y=cost_by_country.values,
                        title="Top 10 Countries by Healthcare Costs",
                        labels={'x': 'Country', 'y': 'Average Annual Cost ($)'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Productivity loss by junk food frequency
            prod_loss = filtered_df.groupby('junk_frequency')['productivity_loss_days'].mean()
            fig = px.bar(x=prod_loss.index, y=prod_loss.values,
                        title="Productivity Loss by Junk Food Frequency",
                        labels={'x': 'Junk Food Frequency', 'y': 'Average Lost Days/Year'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # ========== DATA EXPLORER ==========
    st.markdown("<h2 class='section-header'>🔍 Data Explorer</h2>", unsafe_allow_html=True)
    
    explorer_tab1, explorer_tab2, explorer_tab3 = st.tabs(["📋 Raw Data", "📊 Statistics", "📤 Export"])
    
    with explorer_tab1:
        # Column selector
        available_columns = filtered_df.columns.tolist()
        selected_columns = st.multiselect(
            "Select columns to display",
            options=available_columns,
            default=['country', 'timeline_period', 'age_group', 'gender', 
                    'health_score', 'cvd_risk_score', 'annual_healthcare_cost']
        )
        
        if selected_columns:
            st.dataframe(
                filtered_df[selected_columns].sort_values('health_score', ascending=False).head(100),
                height=400,
                use_container_width=True
            )
    
    with explorer_tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Numerical Statistics")
            st.dataframe(
                filtered_df.select_dtypes(include=[np.number]).describe().round(2),
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### 📊 Categorical Distribution")
            for col in ['timeline_period', 'region', 'country', 'risk_category']:
                if col in filtered_df.columns:
                    st.write(f"**{col.replace('_', ' ').title()}:**")
                    dist = filtered_df[col].value_counts()
                    st.dataframe(dist, use_container_width=True)
    
    with explorer_tab3:
        st.markdown("#### 📥 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv_data,
                file_name="nutrilife_complete_data.csv",
                mime="text/csv"
            )
        
        with col2:
            # Generate summary report
            summary_stats = pd.DataFrame({
                'Metric': ['Total Participants', 'Average Health Score', 'Average CVD Risk',
                          'Total Healthcare Cost', 'High Risk Participants'],
                'Value': [len(filtered_df), 
                         round(filtered_df['health_score'].mean(), 2),
                         round(filtered_df['cvd_risk_score'].mean(), 2),
                         f"${filtered_df['annual_healthcare_cost'].sum():,.0f}",
                         filtered_df['high_risk_flag'].sum()]
            })
            
            summary_csv = summary_stats.to_csv(index=False)
            st.download_button(
                label="📋 Download Summary",
                data=summary_csv,
                file_name="nutrilife_summary.csv",
                mime="text/csv"
            )
        
        with col3:
            if st.button("📄 Generate PDF Report"):
                st.success("📄 PDF report generation initiated!")
                st.info("This feature requires PDF generation libraries. The data is ready for export.")
    
    # ========== FOOTER ==========
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #64748b; font-size: 0.9rem; padding: 2rem;'>
        <div style='margin-bottom: 1rem;'>
            <span style='color: #667eea; font-weight: bold;'>NutriLife Analytics Pro</span> • 
            <span>Complete Edition v5.0</span>
        </div>
        <div>
            <span style='font-size: 0.85rem; color: #94a3b8;'>
            Includes: Timeline Analysis (1700-Present) • 26 Countries • Enhanced Filters • Dark/Light Theme<br>
            All data is synthetic for demonstration purposes. © 2024 NutriLife Analytics
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== RUN APP ==========
if __name__ == "__main__":
    main()
