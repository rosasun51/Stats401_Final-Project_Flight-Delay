"""
Rosa's Visualizations for Flight Delay Analysis
Dataset: airport_weather_monthly.csv (BTS + NOAA merged, airport-monthly granularity)
Requirements: pandas, matplotlib, numpy, geopandas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

# ============================================================
# 1. LOAD & PREPARE DATA
# ============================================================
df = pd.read_csv('airport_weather_monthly.csv', sep='\t')

# Ensure numeric types
numeric_cols = ['arr_flights', 'arr_del15', 'carrier_ct', 'weather_ct', 
                'nas_ct', 'security_ct', 'late_aircraft_ct', 
                'delay_rate', 'airport_latitude', 'airport_longitude',
                'noaa_PRCP', 'noaa_TAVG']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Aggregate by airport (sum across all months/years)
airport_agg = df.groupby(['airport', 'airport_name', 'airport_latitude', 'airport_longitude']).agg({
    'arr_flights': 'sum',
    'arr_del15': 'sum',
    'carrier_ct': 'sum',
    'weather_ct': 'sum',
    'nas_ct': 'sum',
    'security_ct': 'sum',
    'late_aircraft_ct': 'sum',
}).reset_index()

airport_agg['delay_rate'] = airport_agg['arr_del15'] / airport_agg['arr_flights']
airport_agg['total_causes'] = (airport_agg['carrier_ct'] + airport_agg['weather_ct'] + 
                                airport_agg['nas_ct'] + airport_agg['security_ct'] + 
                                airport_agg['late_aircraft_ct'])

# Also aggregate for weather correlation (keep monthly averages)
weather_agg = df.groupby(['airport', 'airport_name', 'airport_latitude', 'airport_longitude']).agg({
    'arr_flights': 'sum',
    'arr_del15': 'sum',
    'weather_ct': 'sum',
    'carrier_ct': 'sum',
    'nas_ct': 'sum',
    'late_aircraft_ct': 'sum',
    'noaa_PRCP': 'mean',
    'noaa_TAVG': 'mean',
}).reset_index()
weather_agg['delay_rate'] = weather_agg['arr_del15'] / weather_agg['arr_flights']
weather_agg['weather_pct'] = (weather_agg['weather_ct'] / 
    (weather_agg['weather_ct'] + weather_agg['carrier_ct'] + 
     weather_agg['nas_ct'] + weather_agg['late_aircraft_ct']) * 100)

# Download US states shapefile (run once, cached)
states = gpd.read_file("https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_1_states_provinces.zip")
us_states = states[states['admin'] == 'United States of America']
us_states_mainland = us_states[~us_states['name'].isin(['Alaska', 'Hawaii'])]

# Color scheme
CAUSE_COLORS = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
CAUSE_LABELS = ['Carrier', 'Weather', 'NAS', 'Security', 'Late Aircraft']
CAUSE_COLS = ['carrier_ct', 'weather_ct', 'nas_ct', 'security_ct', 'late_aircraft_ct']

# ============================================================
# VIZ 1: AIRPORT DELAY MAP
# ============================================================
fig, ax = plt.subplots(figsize=(14, 9))

us_states_mainland.plot(ax=ax, color='#E8E8E8', edgecolor='white', linewidth=0.8)

sizes = (airport_agg['arr_flights'] / airport_agg['arr_flights'].max()) * 800 + 100
scatter = ax.scatter(
    airport_agg['airport_longitude'], 
    airport_agg['airport_latitude'],
    s=sizes,
    c=airport_agg['delay_rate'],
    cmap='RdYlBu_r',
    alpha=0.75,
    edgecolors='white',
    linewidth=1.5,
    vmin=0.10, vmax=0.35,
    zorder=5
)

# Label top 10 by volume
top10 = airport_agg.nlargest(10, 'arr_flights')
for _, row in top10.iterrows():
    ax.annotate(row['airport'], (row['airport_longitude'], row['airport_latitude']),
                textcoords="offset points", xytext=(0, 18), ha='center',
                fontsize=10, fontweight='bold', color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='gray', alpha=0.9))

cbar = plt.colorbar(scatter, ax=ax, shrink=0.6, pad=0.02, aspect=25)
cbar.set_label('Delay Rate', fontsize=11)

# Bubble size legend
legend_sizes = [5000, 15000, 30000]
legend_bubbles = [plt.scatter([], [], s=(ls/airport_agg['arr_flights'].max())*800+100, 
                               c='gray', alpha=0.5, edgecolors='white') for ls in legend_sizes]
ax.legend(legend_bubbles, [f'{ls:,} flights' for ls in legend_sizes], 
          title='Total Flights', loc='lower left', bbox_to_anchor=(0.01, 0.01), fontsize=9)

ax.set_xlim(-125, -66)
ax.set_ylim(24, 50)
ax.set_title('U.S. Airport Delay Rates & Flight Volumes', fontsize=16, fontweight='bold', pad=15)
ax.axis('off')
plt.tight_layout()
plt.savefig('viz1_airport_delay_map.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Viz 1 saved: viz1_airport_delay_map.png")

# ============================================================
# VIZ 2: DELAY CAUSE STACKED BARS (TOP 10)
# ============================================================
for col in CAUSE_COLS:
    airport_agg[f'{col}_pct'] = airport_agg[col] / airport_agg['total_causes'] * 100

pct_cols = [f'{c}_pct' for c in CAUSE_COLS]
top10_airports = airport_agg.nlargest(10, 'arr_flights').copy()

fig, ax = plt.subplots(figsize=(12, 7))
airport_names = top10_airports['airport'].values[::-1]
y_pos = np.arange(len(airport_names))
left = np.zeros(len(airport_names))

for col, label, color in zip(pct_cols, CAUSE_LABELS, CAUSE_COLORS):
    values = top10_airports[col].values[::-1]
    ax.barh(y_pos, values, left=left, color=color, edgecolor='white', 
            linewidth=0.8, alpha=0.9, label=label, height=0.65)
    for j, (v, l) in enumerate(zip(values, left)):
        if v > 12:
            ax.text(l + v/2, j, f'{v:.0f}%', ha='center', va='center',
                   fontsize=8, fontweight='bold', color='white')
    left += values

ax.set_yticks(y_pos)
ax.set_yticklabels(airport_names, fontsize=11)
ax.set_xlabel('Delay Cause Composition (%)', fontsize=12)
ax.set_title('Delay Cause Breakdown — Top 10 Busiest Airports', fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, 100)

for i, (_, row) in enumerate(top10_airports.iloc[::-1].iterrows()):
    ax.text(102, i, f"{row['arr_flights']:,} flights", va='center', ha='left', fontsize=9, color='gray')

ax.legend(loc='lower right', fontsize=9, title='Delay Causes', frameon=True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.grid(True, linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('viz2_delay_cause_stacked.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Viz 2 saved: viz2_delay_cause_stacked.png")

# ============================================================
# VIZ 3: WEATHER-DELAY CORRELATION
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))

# Left: Precipitation vs Delay Rate
ax1 = axes[0]
scatter1 = ax1.scatter(weather_agg['noaa_PRCP'], weather_agg['delay_rate']*100,
    s=weather_agg['arr_flights']/100, c=weather_agg['weather_pct'],
    cmap='YlOrRd', alpha=0.7, edgecolors='white', linewidth=1, vmin=0, vmax=40)

for _, row in weather_agg.iterrows():
    ax1.annotate(row['airport'], (row['noaa_PRCP'], row['delay_rate']*100),
                textcoords="offset points", xytext=(8, 5), fontsize=9, color='#2C3E50')

z = np.polyfit(weather_agg['noaa_PRCP'], weather_agg['delay_rate']*100, 1)
p = np.poly1d(z)
x_line = np.linspace(weather_agg['noaa_PRCP'].min(), weather_agg['noaa_PRCP'].max(), 100)
ax1.plot(x_line, p(x_line), '--', color='gray', alpha=0.7, linewidth=1.5, label='Trend')

ax1.set_xlabel('Average Monthly Precipitation (mm)', fontsize=12)
ax1.set_ylabel('Overall Delay Rate (%)', fontsize=12)
ax1.set_title('Precipitation vs. Delay Rate by Airport', fontsize=13, fontweight='bold')
ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)
ax1.legend(loc='upper left')
plt.colorbar(scatter1, ax=ax1, shrink=0.8, aspect=20).set_label('Weather Delay %', fontsize=10)

# Right: Temperature vs Weather Delay %
ax2 = axes[1]
scatter2 = ax2.scatter(weather_agg['noaa_TAVG'], weather_agg['weather_pct'],
    s=weather_agg['arr_flights']/100, c=weather_agg['delay_rate']*100,
    cmap='RdYlBu_r', alpha=0.7, edgecolors='white', linewidth=1, vmin=10, vmax=35)

for _, row in weather_agg.iterrows():
    ax2.annotate(row['airport'], (row['noaa_TAVG'], row['weather_pct']),
                textcoords="offset points", xytext=(8, 5), fontsize=9, color='#2C3E50')

ax2.set_xlabel('Average Monthly Temperature (°C)', fontsize=12)
ax2.set_ylabel('Weather Delay Share (%)', fontsize=12)
ax2.set_title('Temperature vs. Weather Delay Proportion', fontsize=13, fontweight='bold')
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
plt.colorbar(scatter2, ax=ax2, shrink=0.8, aspect=20).set_label('Delay Rate (%)', fontsize=10)

# Shared size legend
legend_sizes = [10000, 30000, 50000]
legend_bubbles = [plt.scatter([], [], s=ls/100, c='gray', alpha=0.5, edgecolors='white') 
                  for ls in legend_sizes]
fig.legend(legend_bubbles, [f'{ls:,} flights' for ls in legend_sizes],
           title='Flight Volume', loc='upper center', ncol=3, 
           bbox_to_anchor=(0.5, 1.02), frameon=False, fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.savefig('viz3_weather_delay_correlation.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ Viz 3 saved: viz3_weather_delay_correlation.png")
print("\n🎉 All 3 visualizations generated successfully!")