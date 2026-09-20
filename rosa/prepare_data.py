import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD
# ============================================================
df = pd.read_csv('airport_weather_monthly.csv', low_memory=False)

# Ensure numeric
for col in ['arr_flights','arr_del15','carrier_ct','weather_ct','nas_ct',
            'security_ct','late_aircraft_ct','airport_latitude','airport_longitude',
            'noaa_PRCP','noaa_TAVG']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ============================================================
# 2. AGGREGATE BY AIRPORT
# ============================================================
agg = df.groupby(['airport','airport_name','airport_latitude','airport_longitude']).agg({
    'arr_flights':'sum','arr_del15':'sum',
    'carrier_ct':'sum','weather_ct':'sum','nas_ct':'sum',
    'security_ct':'sum','late_aircraft_ct':'sum',
    'noaa_PRCP':'mean','noaa_TAVG':'mean'
}).reset_index()

agg['delay_rate'] = agg['arr_del15'] / agg['arr_flights']
agg['total_causes'] = agg[['carrier_ct','weather_ct','nas_ct','security_ct','late_aircraft_ct']].sum(axis=1)
agg['weather_pct'] = agg['weather_ct'] / agg['total_causes'] * 100

for c in ['carrier_ct','weather_ct','nas_ct','security_ct','late_aircraft_ct']:
    agg[f'{c}_pct'] = agg[c] / agg['total_causes'] * 100

# Export for D3
out = agg[['airport','airport_name','airport_latitude','airport_longitude',
           'arr_flights','delay_rate','weather_pct','noaa_PRCP','noaa_TAVG',
           'carrier_ct_pct','weather_ct_pct','nas_ct_pct','security_ct_pct','late_aircraft_ct_pct']].copy()
out['delay_rate'] = (out['delay_rate']*100).round(2)
out['weather_pct'] = out['weather_pct'].round(2)
out['noaa_PRCP'] = out['noaa_PRCP'].round(1)
out['noaa_TAVG'] = out['noaa_TAVG'].round(1)
for c in ['carrier_ct_pct','weather_ct_pct','nas_ct_pct','security_ct_pct','late_aircraft_ct_pct']:
    out[c] = out[c].round(1)
out.to_csv('airport_summary.csv', index=False)

# Export top 10 causes
top10 = agg.nlargest(10, 'arr_flights')[['airport','arr_flights',
    'carrier_ct_pct','weather_ct_pct','nas_ct_pct','security_ct_pct','late_aircraft_ct_pct']].copy()
for c in ['carrier_ct_pct','weather_ct_pct','nas_ct_pct','security_ct_pct','late_aircraft_ct_pct']:
    top10[c] = top10[c].round(1)
top10.to_csv('top10_causes.csv', index=False)

print("Generated: airport_summary.csv, top10_causes.csv")

# ============================================================
# 3. OPTIONAL: Generate 3 static PNGs for interim submission
# ============================================================
# --- Viz 1: Map ---
fig, ax = plt.subplots(figsize=(14,8))
continental = agg[(agg.airport_longitude>-125)&(agg.airport_longitude<-66)&(agg.airport_latitude>24)&(agg.airport_latitude<50)]
sizes = (continental.arr_flights/continental.arr_flights.max())*600+30
sc = ax.scatter(continental.airport_longitude, continental.airport_latitude,
                s=sizes, c=continental.delay_rate, cmap='RdYlBu_r',
                alpha=0.78, edgecolors='white', linewidth=1.2, vmin=0.08, vmax=0.30)
for _,r in continental.nlargest(8,'arr_flights').iterrows():
    ax.annotate(r.airport, (r.airport_longitude, r.airport_latitude),
                textcoords="offset points", xytext=(0,14), ha='center', fontsize=9, fontweight='bold')
plt.colorbar(sc, ax=ax, shrink=0.6).set_label('Delay Rate')
ax.set_xlim(-125,-66); ax.set_ylim(24,50)
ax.set_title('U.S. Airport Delay Rates & Flight Volumes (2020–2026)', fontsize=15, fontweight='bold')
plt.tight_layout(); plt.savefig('viz1_map.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close()

# --- Viz 2: Stacked Bars ---
fig, ax = plt.subplots(figsize=(12,7))
t10 = agg.nlargest(10,'arr_flights').copy()
causes = ['carrier_ct_pct','weather_ct_pct','nas_ct_pct','security_ct_pct','late_aircraft_ct_pct']
labels = ['Carrier','Weather','NAS','Security','Late Aircraft']
colors = ['#E74C3C','#3498DB','#2ECC71','#F39C12','#9B59B6']
y_pos = np.arange(len(t10)); left = np.zeros(len(t10))
for col,lab,color in zip(causes,labels,colors):
    vals = t10[col].values[::-1]
    ax.barh(y_pos, vals, left=left, color=color, edgecolor='white', linewidth=0.8, height=0.65, label=lab)
    for j,(v,l) in enumerate(zip(vals,left)):
        if v>10: ax.text(l+v/2, j, f'{v:.0f}%', ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    left += vals
ax.set_yticks(y_pos); ax.set_yticklabels(t10.airport.values[::-1], fontsize=11)
ax.set_xlabel('Delay Cause Composition (%)'); ax.set_title('Delay Cause Breakdown — Top 10 Busiest Airports', fontsize=14, fontweight='bold')
ax.set_xlim(0,100); ax.legend(loc='lower right', fontsize=9, title='Delay Causes')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout(); plt.savefig('viz2_stacked.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close()

# --- Viz 3: Scatter ---
fig, axes = plt.subplots(1,2, figsize=(16,6.5))
w = agg.dropna(subset=['noaa_PRCP','delay_rate'])
sc1 = axes[0].scatter(w.noaa_PRCP, w.delay_rate*100, s=w.arr_flights/3000,
                      c=w.weather_pct, cmap='YlOrRd', alpha=0.7, edgecolors='white', vmin=0, vmax=25)
axes[0].set_xlabel('Precipitation (mm)'); axes[0].set_ylabel('Delay Rate (%)'); axes[0].set_title('Precipitation vs Delay Rate')
plt.colorbar(sc1, ax=axes[0], shrink=0.8).set_label('Weather Delay %')
t = agg.dropna(subset=['noaa_TAVG','weather_pct'])
sc2 = axes[1].scatter(t.noaa_TAVG, t.weather_pct, s=t.arr_flights/3000,
                      c=t.delay_rate*100, cmap='RdYlBu_r', alpha=0.7, edgecolors='white', vmin=10, vmax=28)
axes[1].set_xlabel('Temperature (°C)'); axes[1].set_ylabel('Weather Delay Share (%)'); axes[1].set_title('Temperature vs Weather Delay %')
plt.colorbar(sc2, ax=axes[1], shrink=0.8).set_label('Delay Rate (%)')
plt.tight_layout(); plt.savefig('viz3_scatter.png', dpi=150, bbox_inches='tight', facecolor='white'); plt.close()

print("Generated: viz1_map.png, viz2_stacked.png, viz3_scatter.png")