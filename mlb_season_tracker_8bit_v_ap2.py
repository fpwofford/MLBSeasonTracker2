import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import math

# Page config
st.set_page_config(
    page_title="MLB Season Tracker - 8-Bit",
    page_icon="🎮",
    layout="wide"
)

# 8-BIT RETRO CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    * {
        font-family: 'Press Start 2P', monospace;
        image-rendering: pixelated;
        image-rendering: -moz-crisp-edges;
        image-rendering: crisp-edges;
    }
    
    /* Retro arcade background with scanlines */
    .main {
        background: #000000;
        position: relative;
    }
    
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 255, 0, 0.03) 0px,
            rgba(0, 255, 0, 0.03) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
        z-index: 1000;
    }
    
    /* Main content - arcade cabinet style */
    .block-container {
        background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
        border: 8px solid #444;
        border-radius: 0;
        padding: 2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 
            inset 0 0 20px rgba(0, 255, 0, 0.3),
            0 0 40px rgba(0, 255, 0, 0.2);
    }
    
    /* 8-bit title */
    h1 {
        color: #00FF00 !important;
        font-family: 'Press Start 2P', monospace !important;
        font-size: 2.2rem !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: 
            3px 3px 0px #006600,
            0 0 20px #00FF00;
        letter-spacing: 2px;
    }
    
    /* Retro subtitle */
    .subtitle {
        color: #FFD700;
        font-size: 0.7rem;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 0px #665500;
    }
    
    /* Pixel metrics */
    [data-testid="stMetric"] {
        background: #000000;
        border: 4px solid #00FF00;
        padding: 1rem;
        border-radius: 0;
        box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #00FF00 !important;
        font-size: 0.5rem !important;
        text-transform: uppercase;
        text-shadow: 2px 2px 0px #006600;
    }
    
    [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 1.5rem !important;
        text-shadow: 2px 2px 0px #665500;
    }
    
    /* 8-bit sidebar */
    [data-testid="stSidebar"] {
        background: #1a1a1a;
        border-right: 4px solid #444;
    }
    
    [data-testid="stSidebar"] * {
        color: #00FF00 !important;
        font-size: 0.6rem !important;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #FFD700 !important;
        font-size: 0.8rem !important;
        border-bottom: 4px solid #FFD700;
        padding-bottom: 0.5rem;
    }
    
    /* Retro checkbox */
    [data-testid="stCheckbox"] {
        background: #000000;
        border: 2px solid #00FF00;
        padding: 0.5rem;
    }
    
    /* Info/alerts - arcade style - BIGGER TEXT */
    .stAlert {
        background: #000000;
        border: 4px solid #FFFF00;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        border-radius: 0;
        font-weight: bold !important;
        padding: 1.5rem !important;
    }
    
    /* Ensure info boxes have white text - BIGGER */
    div[data-baseweb="notification"] {
        background: #000000 !important;
        border: 4px solid #FFFF00 !important;
    }
    
    div[data-baseweb="notification"] * {
        color: #FFFFFF !important;
        font-size: 1rem !important;
        font-weight: bold !important;
    }
    
    .stSuccess {
        background: #000000;
        border: 4px solid #00FF00;
        color: #00FF00;
        font-size: 0.6rem;
        border-radius: 0;
    }
    
    /* Retro HR */
    hr {
        border: none;
        height: 4px;
        background: repeating-linear-gradient(
            90deg,
            #00FF00 0px,
            #00FF00 10px,
            transparent 10px,
            transparent 20px
        );
        margin: 2rem 0;
    }
    
    /* Footer text */
    .stMarkdown p {
        color: #00FF00;
        font-size: 0.6rem;
        line-height: 1.8;
        text-shadow: 2px 2px 0px #006600;
    }
    </style>
""", unsafe_allow_html=True)

# Title - 8-bit style
st.title("⚾ MLB SEASON TRACKER ⚾")
st.markdown("<p class='subtitle'>** ADIOOOOS PELOTAAA **</p>", unsafe_allow_html=True)

# Season dates (2026 season)
OPENING_DAY = datetime(2026, 3, 26)
SEASON_END = datetime(2026, 9, 27)
TOTAL_GAMES = 162

# Calculate current progress
today = datetime.now()

if today < OPENING_DAY:
    days_into_season = 0
    games_played = 0
    days_until_opening = (OPENING_DAY - today).days
    pre_season = True
elif today > SEASON_END:
    days_into_season = (SEASON_END - OPENING_DAY).days
    games_played = TOTAL_GAMES
    pre_season = False
else:
    days_into_season = (today - OPENING_DAY).days
    total_season_days = (SEASON_END - OPENING_DAY).days
    games_played = int((days_into_season / total_season_days) * TOTAL_GAMES)
    pre_season = False

# Add demo mode in sidebar
st.sidebar.header("DEMO MODE")
demo_mode = st.sidebar.checkbox("PREVIEW SEASON", value=False)

if demo_mode:
    demo_percent = st.sidebar.slider("SEASON %", 0, 100, 56, 1)
    games_played = int((demo_percent / 100) * TOTAL_GAMES)
    progress_pct = demo_percent
    st.sidebar.success(f">>> GAME {games_played} ({demo_percent}%) <<<")
else:
    # Use actual calculated values
    pass

# Ensure games_played is within bounds
games_played = max(0, min(games_played, TOTAL_GAMES))

# Calculate progress percentage
progress_pct = (games_played / TOTAL_GAMES) * 100

# Create 8-BIT baseball diamond
def create_8bit_baseball_diamond(games_played, progress_pct, today):
    """Create a retro 8-bit pixel art baseball diamond"""
    
    # Diamond coordinates (rotated 45 degrees)
    home_x, home_y = 0, 0
    first_x, first_y = 1.2, 1.2
    second_x, second_y = 0, 2.4
    third_x, third_y = -1.2, 1.2
    
    fig = go.Figure()
    
    # RETRO GRASS - solid bright green
    outfield_size = 2.0
    fig.add_trace(go.Scatter(
        x=[-outfield_size, outfield_size, outfield_size, -outfield_size, -outfield_size],
        y=[-0.5, -0.5, 2.9, 2.9, -0.5],
        fill='toself',
        fillcolor='#00AA00',  # Bright 8-bit green
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # INFIELD DIRT - 8-bit brown
    infield_dirt_x = [home_x, first_x, second_x, third_x, home_x]
    infield_dirt_y = [home_y, first_y, second_y, third_y, home_y]
    
    fig.add_trace(go.Scatter(
        x=infield_dirt_x,
        y=infield_dirt_y,
        fill='toself',
        fillcolor='#AA6600',  # Bright 8-bit brown
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # PITCHER'S MOUND - pixel circle
    mound_x = (home_x + second_x) / 2
    mound_y = (home_y + second_y) / 2
    
    # Pixelated mound circle
    mound_theta = [i * 3.14159 / 180 for i in range(361)]
    mound_radius = 0.35
    mound_circle_x = [mound_x + mound_radius * math.cos(t) for t in mound_theta]
    mound_circle_y = [mound_y + mound_radius * math.sin(t) for t in mound_theta]
    
    fig.add_trace(go.Scatter(
        x=mound_circle_x,
        y=mound_circle_y,
        fill='toself',
        fillcolor='#884400',
        line=dict(color='#000000', width=4),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # DATE AND PROGRESS on mound - 8-bit style (BIGGER FONTS!)
    date_text = today.strftime('%m/%d/%y')
    progress_text = f"{int(progress_pct)}%"
    
    fig.add_trace(go.Scatter(
        x=[mound_x],
        y=[mound_y + 0.1],
        mode='text',
        text=date_text,
        textfont=dict(size=11, color='#FFFF00', family='Press Start 2P'),  # Pixel font!
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=[mound_x],
        y=[mound_y - 0.1],
        mode='text',
        text=progress_text,
        textfont=dict(size=14, color='#00FF00', family='Press Start 2P'),  # Pixel font!
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # BASE PATHS - thick pixel lines
    diamond_x = [home_x, first_x, second_x, third_x, home_x]
    diamond_y = [home_y, first_y, second_y, third_y, home_y]
    
    fig.add_trace(go.Scatter(
        x=diamond_x,
        y=diamond_y,
        mode='lines',
        line=dict(color='#FFFF00', width=6),  # Bright yellow pixel path
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # BASES - pixel squares (not rotated, pure squares)
    bases = [
        {'x': home_x, 'y': home_y, 'name': 'HOME', 'games': 0},
        {'x': first_x, 'y': first_y, 'name': '1ST', 'games': 41},
        {'x': second_x, 'y': second_y, 'name': '2ND', 'games': 81},
        {'x': third_x, 'y': third_y, 'name': '3RD', 'games': 122},
    ]
    
    for base in bases:
        reached = games_played >= base['games']
        
        # Pure square base (8-bit style)
        base_size = 0.12
        base_square_x = [
            base['x'] - base_size, base['x'] + base_size, 
            base['x'] + base_size, base['x'] - base_size, 
            base['x'] - base_size
        ]
        base_square_y = [
            base['y'] - base_size, base['y'] - base_size, 
            base['y'] + base_size, base['y'] + base_size, 
            base['y'] - base_size
        ]
        
        fig.add_trace(go.Scatter(
            x=base_square_x,
            y=base_square_y,
            fill='toself',
            fillcolor='#FFFFFF' if reached else '#666666',
            line=dict(color='#000000', width=4),
            showlegend=False,
            hoverinfo='text',
            hovertext=f"{base['name']}<br>GAME {base['games']}"
        ))
    
    # Calculate runner position
    if games_played <= 41:
        t = games_played / 41
        runner_x = home_x + t * (first_x - home_x)
        runner_y = home_y + t * (first_y - home_y)
    elif games_played <= 81:
        t = (games_played - 41) / 40
        runner_x = first_x + t * (second_x - first_x)
        runner_y = first_y + t * (second_y - first_y)
    elif games_played <= 122:
        t = (games_played - 81) / 41
        runner_x = second_x + t * (third_x - second_x)
        runner_y = second_y + t * (third_y - second_y)
    else:
        t = (games_played - 122) / 40
        runner_x = third_x + t * (home_x - third_x)
        runner_y = third_y + t * (home_y - third_y)
    
    # RUNNER - 8-bit BASEBALL SPRITE (bigger!)
    # Main baseball body (white circle with red outline for stitching)
    fig.add_trace(go.Scatter(
        x=[runner_x],
        y=[runner_y],
        mode='markers',
        marker=dict(
            size=35,  # MUCH BIGGER!
            color='#FFFFFF',
            symbol='circle',  # Circle for baseball
            line=dict(color='#FF0000', width=4)  # Red outline (stitching)
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Black inner ring for depth
    fig.add_trace(go.Scatter(
        x=[runner_x],
        y=[runner_y],
        mode='markers',
        marker=dict(
            size=25,
            color='#FFFFFF',
            symbol='circle',
            line=dict(color='#000000', width=2)  # Black inner detail
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Game number on the baseball
    fig.add_trace(go.Scatter(
        x=[runner_x],
        y=[runner_y],
        mode='text',
        text=str(games_played),
        textfont=dict(size=12, color='#000000', family='Courier New'),
        textposition='middle center',
        showlegend=False,
        hoverinfo='text',
        hovertext=f'CURRENT<br>GAME {games_played}<br>{progress_pct:.0f}% COMPLETE'
    ))
    
    # Update layout - 8-bit style
    fig.update_layout(
        plot_bgcolor='#00AA00',  # Match grass
        paper_bgcolor='#000000',
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-2.2, 2.2],
            fixedrange=True  # Disable zoom
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-0.7, 3.1],
            scaleanchor='x',
            scaleratio=1,
            fixedrange=True  # Disable zoom
        ),
        height=700,
        width=800,  # Fixed width to prevent resizing
        margin=dict(l=20, r=20, t=60, b=20),
        title=dict(
            text=f'>>> GAME {games_played} / {TOTAL_GAMES} <<<',
            font=dict(size=14, color='#00FF00', family='Press Start 2P'),  # Pixel font!
            x=0.5,
            xanchor='center'
        )
    )
    
    return fig

# Two column layout - Diamond left, Stats right
col_diamond, col_stats = st.columns([2, 1])

with col_diamond:
    # Display the 8-bit diamond
    st.plotly_chart(create_8bit_baseball_diamond(games_played, progress_pct, today), config={'displayModeBar': False, 'staticPlot': False})

with col_stats:
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)  # Add spacing
    
    # Stats in right column
    st.metric(
        label="GAMES PLAYED",
        value=f"{games_played}",
        delta=f"{games_played}/{TOTAL_GAMES}"
    )
    
    st.metric(
        label="GAMES LEFT",
        value=f"{TOTAL_GAMES - games_played}",
        delta=f"{100 - progress_pct:.0f}%"
    )
    
    st.metric(
        label="PROGRESS",
        value=f"{progress_pct:.0f}%"
    )
    
    if pre_season:
        st.metric(
            label="DAYS TO START",
            value=f"{days_until_opening}"
        )
    else:
        days_remaining = (SEASON_END - today).days if today < SEASON_END else 0
        st.metric(
            label="DAYS LEFT",
            value=f"{max(0, days_remaining)}"
        )

# Key dates section - centered at bottom in green-themed box
st.markdown("""
<div style='background: linear-gradient(135deg, #00AA00 0%, #008800 100%); 
            padding: 2rem; 
            border-radius: 0;
            margin-top: 2rem;
            border: 4px solid #000000;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);'>
    <p style='text-align: center; color: #FFFF00; font-size: 0.8rem; margin-bottom: 1rem;'>
        *** KEY DATES ***
    </p>
    <div style='text-align: center; color: #FFFFFF; font-size: 0.6rem; line-height: 2; font-family: "Press Start 2P", monospace;'>
        MAY 1ST<br>
        MOTHERS DAY - MAY 10<br>
        MEMORIAL DAY - MAY 25<br>
        FATHERS DAY - JUNE 21<br>
        4TH OF JULY - JULY 4<br>
        ALL-STAR BREAK - JULY 15<br>
        TRADE DEADLINE - JULY 31<br>
        SEPT 1ST - ROSTER EXPANSION
    </div>
</div>
""", unsafe_allow_html=True)

# 8-bit footer
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <p>*** 2026 MLB SEASON ***</p>
    <p>OPENING: 03/26/26 | END: 09/27/26</p>
    <p>162 GAMES | 4 BASES = 100%</p>
    <br>
    <p style='color: #FFD700;'>*** INSERT COIN TO CONTINUE ***</p>
</div>
""", unsafe_allow_html=True)
