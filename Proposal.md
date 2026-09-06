# Flight Delay Analysis: Understanding Causes, Patterns, and Propagation

**Group Members:** Yuxuan, Nora, Rosa

---

## 1. Topic, Goals, and Questions

Flight delays frustrate travelers and challenge airline operations. Understanding when, where, and why delays occur—and how they cascade through the network—can help both travelers and industry stakeholders make better decisions.

**Topic:** We explore U.S. domestic flight delays, including their distribution across airlines, airports, and seasons; underlying causes; and the "butterfly effect" of delay propagation between sequential flights.

**Goals:** For the general public, we provide a comprehensive understanding of delay reasons to inform flight selection. For airline administrators and policymakers, we reveal systemic patterns for improving the flight system.

**Audience:** Travelers, aviation analysts, airline operations managers, and transportation policymakers.

**Research Questions:**
- How do delays vary across airlines, airports, and seasons?
- What are the primary delay causes, and how do they differ across carriers and airports?
- Which airports are most vulnerable to weather-related delays?
- How do delays propagate through the airport network, and which airports are critical hubs?

---

## 2. Dataset(s)

### Primary: BTS Airline On-Time Statistics and Delay Causes
- **Source:** U.S. DOT Bureau of Transportation Statistics (BTS), tracking domestic flight performance since 2003.
- **Acquisition:** Download CSV files from the BTS TranStats portal.
- **Processing:** Filter to 2018–2026; remove missing values; standardize codes; compute delay rates and cause percentages.
- **Size:** ~500,000 records (carrier-airport-month) with 25 variables.
- **Key Attributes:** `year`, `month`, `carrier_name`, `airport`, `arr_flights`, `arr_del15`, and five cause counts (`carrier_ct`, `weather_ct`, `nas_ct`, `security_ct`, `late_aircraft_ct`) with delay minutes.
- **Link:** https://www.transtats.bts.gov/ot_delay/ot_delaycause1.asp

### Supplementary: Airport Locations
- **Source:** BTS/FAA reference tables.
- **Size:** ~400 U.S. airports with coordinates.
- **Link:** https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ

### Optional: NOAA Climate Data
- **Source:** NCEI Climate Data Online.
- **Purpose:** Meteorological context. We rely primarily on BTS weather delay fields due to difficulty matching hourly weather to airports.
- **Link:** https://www.ncei.noaa.gov/cdo-web/

---

## 3. Analysis and Visualization Methods

We use JavaScript, D3.js, HTML, and CSS for interactive visualization, with Python for initial data cleaning.

**Topic 1 — Airline On-Time Performance:** Group data by `carrier_name`, compute delay rate = `arr_del15` / `arr_flights`. *Technique:* Scatter plot (total flights vs. on-time rate). *Task:* Comparison. *Question:* Which airlines perform best and worst?

**Topic 2 — Airport Delay Geography:** Calculate airport-level delay rates; merge with lat/lon coordinates. *Technique:* Interactive U.S. map with proportional symbols (color = delay rate, size = volume). *Task:* Geographic exploration. *Question:* How do delay rates vary regionally, and which airports are outliers?

**Topic 3 — Seasonal Trends:** Aggregate monthly delay rates. *Technique:* Line chart (month/year vs. delay rate). *Task:* Trend identification. *Question:* Are there recurring seasonal patterns in delays?

**Topic 4 — Delay Cause Dashboard:** Decompose delays into five causes for the top 10 busiest airports. *Technique:* Interactive dashboard with linked views—KPI cards, 100% stacked horizontal bars (color saturation = absolute intensity), detail panel, and monthly trend chart. Clicking an airport updates all views; users can sort by total delay, weather %, or late-aircraft %. *Task:* Part-to-whole comparison and filtering. *Question:* What are the dominant causes, and how do profiles differ across busy airports?

**Topic 5 — Weather Factor:** Aggregate `weather_ct` by airport and month. *Technique:* Dual parallel coordinates. Plot (1) profiles airports across Total Flights, Delay Rate, Avg Delay, Weather Delay %, and Late Aircraft % (color = delay rate). Plot (2) compares Total, Weather, Carrier, NAS, and Late Aircraft delays (color = weather/total ratio). *Task:* Multi-dimensional comparison and outlier detection. *Question:* Which airports are disproportionately affected by weather?

**Topic 6 — Delay Propagation:** Model airports as nodes and routes as directed edges. *Technique:* Force-directed network graph (edge width/color = propagated delay severity). *Task:* Relationship discovery. *Question:* How do delays cascade, and which airports are propagation hubs?

---

## 4. Visualization Sketches or References

1. **Airline Scatter Plot** (Scatter plot). Reference: https://github.com/momo840505/flight-reliability-platform. Compares airline scale and reliability.

2. **Airport Map** (Interactive proportional-symbol map). Reference: https://0506zhengyi.github.io/Airline_on_time_performance/interactive-component.html. Explores geographic delay variation.

3. **Seasonal Line Chart** (Line chart). Reference: https://public.tableau.com/app/profile/mazen.karam/viz/seasonlflightdelays/SeasonalPatternsofDelays. Identifies seasonal peaks.

4. **Cause Dashboard** (Linked-view dashboard). Reference: https://github.com/cemputer/bts-airline-data-platform. Sketch: `viz4_delay_cause_dashboard.png`. Reveals delay-cause "DNA" across top 10 airports with interactive sorting and drill-down.

5. **Weather Parallel Coords** (Dual parallel coordinates). Reference: https://www.faa.gov/nextgen/programs/weather/faq. Sketch: `viz5_weather_parallel_coords.png`. Cross-references overall delay severity with weather-specific vulnerability.

6. **Propagation Network** (Force-directed graph). Reference: (To be added by Nora). Reveals delay cascade patterns and critical hubs.

---

## 5. Group Roles and Responsibilities

- **Yuxuan:** Data acquisition/cleaning; interface development; D3.js for scatter plot, map, and line chart; testing; documentation.
- **Nora:** Dataset sourcing; force-directed network design and D3.js implementation; topic definition.
- **Rosa:** Delay-cause and weather analysis; D3.js for dashboard and parallel coordinates; timeline planning; presentation preparation.

All members participate in weekly syncs, code reviews, and final integration.

---

## 6. Interim Presentation Deliverables

- Cleaned BTS subset (2018–2025) with derived fields in the repo.
- Summary statistics and preliminary static charts.
- Finalized research questions with design justifications.
- Mockups or low-fidelity D3.js prototypes for at least four visualizations.
- Working D3.js code for at least two interactive visualizations with tooltips.

---

## 7. Timeline and Milestones

| Week | Milestone | Tasks | Responsible | Output |
|------|-----------|-------|-------------|--------|
| **2** | Project Definition | Finalize questions; scope dataset; assign roles; set up repo | All | `proposal.md`; project board |
| **3** | Data Preparation | Download/clean BTS data; compute derived fields; merge coordinates | Yuxuan, Rosa, Nora | Cleaned CSVs; data dictionary |
| **4** | Visualization Design | Sketch all six visualizations; define colors/interactions; build HTML skeleton | Nora, Rosa, Yuxuan | Mockups; style guide; skeleton |
| **5** | Interim Prototype | D3.js prototypes for 4+ visualizations; tooltips/filters; presentation slides | Yuxuan, Rosa, Nora | Live prototype; interim slides |
| **6** | Implementation | Complete all six D3.js visualizations; brushing/linking; dashboard integration; testing | All | Interactive dashboard; test reports |
| **7** | Final Integration | Debug; document; record demo; final presentation; deploy to GitHub Pages | All | Final repo; deployed site; presentation |
