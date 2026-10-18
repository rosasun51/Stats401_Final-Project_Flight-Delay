from pathlib import Path
import shutil, zipfile, re
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator

root=Path(__file__).resolve().parents[1]
out=root
(out/'vis').mkdir(parents=True,exist_ok=True)
(out/'data').mkdir(exist_ok=True)
src=root/'data'
d=pd.read_csv(src/'airline_performance.csv').sort_values('arr_flights',ascending=False)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titleweight':'bold'})
fig=plt.figure(figsize=(15,9),facecolor='#ffffff')
ax=fig.add_axes([.07,.22,.60,.60],facecolor='white')
ax.scatter(d.arr_flights,d.on_time_rate*100,s=85,color='#2d87b6',edgecolor='white',linewidth=1.1,zorder=3)
median=float(d.arr_flights.median())
assert len(d)==25 and d.carrier.nunique()==25
print('Median reported flights:',median)
print('Below / at / above:',int((d.arr_flights<median).sum()),int((d.arr_flights==median).sum()),int((d.arr_flights>median).sum()))
ax.axvline(median,color='#ee985e',ls=(0,(5,4)),lw=1.4,zorder=2)
ax.annotate(f'Median: {median:,.0f} flights',xy=(median,88.4),xytext=(9,0),textcoords='offset points',fontsize=10,color='#b86b36',ha='left',va='center',bbox=dict(facecolor='white',edgecolor='none',pad=3))
overall=d.on_time_flights.sum()/d.arr_flights.sum()*100
ax.axhline(overall,color='#7893a3',ls=(0,(4,4)),lw=1.2,zorder=1)
ax.text(8.75e6,overall+.25,f'Overall {overall:.1f}%',ha='right',fontsize=9,color='#587188')
offsets={'WN':(8,10),'DL':(8,8),'AA':(8,-13),'OO':(8,8),'UA':(8,8),'YX':(8,8),'MQ':(8,-12),'B6':(8,-12)}
for r in d.head(8).itertuples():
 ax.annotate(r.carrier,(r.arr_flights,r.on_time_rate*100),xytext=offsets[r.carrier],textcoords='offset points',fontsize=10,fontweight='bold',color='#173b59',arrowprops=dict(arrowstyle='-',color='#9baead',lw=.6))
ax.set_xlim(-.15e6,9e6);ax.set_ylim(65,90)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v/1e6:g}M'))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:.0f}%'))
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.set_xlabel('Total reported flights',labelpad=14,color='#173b59')
ax.set_ylabel('On-time rate',labelpad=12,color='#173b59')
ax.grid(axis='y',color='#e1edf2');ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False)
ax.spines[['left','bottom']].set_color('#d4e4ec')
ax.tick_params(colors='#587188')
fig.text(.07,.925,'4',fontsize=13,weight='bold',color='white',bbox=dict(boxstyle='round,pad=.4',facecolor='#0d9daa',edgecolor='none'))
fig.text(.105,.925,'Airline scale & reliability',fontsize=22,color='#14324e',weight='bold')
fig.text(.07,.87,'January 2020–June 2026 · 25 carriers · 146,438 cleaned monthly records',fontsize=11,color='#587188')
fig.text(.715,.80,'CARRIER',fontsize=10,color='#587188',weight='bold')
fig.text(.955,.80,'ON TIME',ha='right',fontsize=10,color='#587188',weight='bold')
for i,r in enumerate(d.itertuples()):
 y=.771-i*.022
 name=r.carrier_name.replace(' Airlines Network','').replace(' Air Lines Network','').replace(' Airlines Inc.','').replace(' Airlines Corp','').replace(' LLC d/b/a United Express','').replace(' LLC dba CommuteAir','').replace(' Inc.','')
 if len(name)>29:name=name[:28]+'…'
 fig.text(.715,y,r.carrier,fontsize=8.5,color='#2d87b6',weight='bold')
 fig.text(.746,y,name,fontsize=8.5,color='#173b59')
 fig.text(.955,y,f'{r.on_time_rate:.1%}',ha='right',fontsize=8.5,color='#173b59')
fig.text(.07,.145,'Each point is one carrier. Labels identify the eight busiest carriers; the table lists all 25.',fontsize=10,color='#587188')
fig.text(.07,.112,'Vertical line: median of the 25 carrier flight totals; a dataset comparison, not an official airline-size category.',fontsize=10,color='#b86b36')
fig.text(.07,.08,'On-time rate = (reported flights − delayed arrivals − cancellations − diversions) / reported flights.',fontsize=10,color='#587188')
fig.text(.07,.05,'Rates use summed counts. The vertical axis starts at 65%. Carriers differ in reporting months and service mix.',fontsize=10,color='#587188')
fig.text(.07,.02,'Source: U.S. Bureau of Transportation Statistics, Airline On-Time Statistics and Delay Causes.',fontsize=9,color='#587188')
fig.savefig(out/'vis'/'viz4_airlines.png',dpi=180,facecolor=fig.get_facecolor())
plt.close(fig)
