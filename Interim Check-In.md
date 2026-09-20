# Final Project Milestone: Interim Check-In

## 1. Dataset

### Raw Dataset

- **Data Source:** U.S. Bureau of Transportation Statistics (BTS) Airline On-Time Statistics, merged with NOAA Climate Data Online (NCEI) via nearest weather station matching.
- **Description:** Monthly aggregated flight delay records by airport, combined with corresponding monthly weather observations (precipitation, temperature, wind) from the nearest NOAA station within 25km.
- **Number of Observations:** 16,508 rows (airport-month combinations, 2020–2026)
- **Key Variables:** `airport`, `year`, `month`, `arr_flights`, `arr_del15`, `carrier_ct`, `weather_ct`, `nas_ct`, `security_ct`, `late_aircraft_ct`, `airport_latitude`, `airport_longitude`, `noaa_PRCP`, `noaa_TAVG`, `noaa_AWND`
- **Time Period / Coverage:** January 2020 – June 2026, 235 U.S. airports with valid weather station mappings

### Processed Dataset

- **Description:** Two aggregated CSV files derived from the raw merged data: (1) `airport_summary.csv` — airport-level aggregation summing all delay causes and averaging weather metrics across the full time period; (2) `top10_causes.csv` — subset of the 10 busiest airports with computed delay-cause percentages.
- **Number of Observations:** `airport_summary.csv`: 224 rows (one per airport); `top10_causes.csv`: 10 rows
- **Variables Used:** `airport`, `arr_flights`, `delay_rate`, `weather_pct`, `noaa_PRCP`, `noaa_TAVG`, plus five cause percentages (`carrier_ct_pct`, `weather_ct_pct`, `nas_ct_pct`, `security_ct_pct`, `late_aircraft_ct_pct`)

### Data Cleaning and Processing

1. **Type conversion:** Parsed all numeric columns (delay counts, weather metrics, coordinates) from string to float; coerced invalid entries to NaN.
2. **Aggregation:** Grouped raw airport-month data by airport code, summing `arr_flights`, `arr_del15`, and all five delay-cause counts; computed mean `noaa_PRCP` and `noaa_TAVG` per airport.
3. **Derived fields:** Calculated `delay_rate` = `arr_del15 / arr_flights`; `weather_pct` = `weather_ct / total_causes × 100`; and proportional percentages for all five delay causes.
4. **Geographic filtering:** Retained only continental U.S. airports (longitude −125 to −66, latitude 24 to 50) to ensure valid projection on the Albers USA map.

---

## 2. Visualizations

### Visualization 1: U.S. Airport Delay Map

**Purpose:** To reveal the geographic distribution of flight delays across the United States and identify regional patterns. Bubble size encodes total flight volume (larger = busier airport), while color encodes delay rate (red = higher delay, blue = lower delay). This allows users to simultaneously compare "how busy" and "how delayed" each airport is.

![Airport Delay Map](viz1_airport_map_real.png)

### Visualization 2: Delay Cause Breakdown — Top 10 Busiest Airports

**Purpose:** To decompose overall delays into their five reported causes (Carrier, Weather, NAS, Security, Late Aircraft) for the busiest airports. Using 100% stacked horizontal bars, users can compare the "delay DNA" of each airport—e.g., whether one airport suffers disproportionately from weather while another is dominated by late aircraft.

![Delay Cause Stacked Bars](viz2_cause_stacked_real.png)

### Visualization 3: Weather vs. Delay Rate Scatter Plot

**Purpose:** To investigate the relationship between meteorological conditions and flight delays. The left panel plots average monthly precipitation against overall delay rate; the right panel plots average temperature against weather-delay share. Bubble size represents flight volume, and color encodes weather-delay percentage, enabling multi-dimensional outlier detection.

![Weather Delay Correlation](viz3_weather_corr_real.png)

---

## 3. Interaction / Animation Plan

### Visualization 1 — Airport Delay Map

**Planned Interaction / Animation:**
- **Year filter dropdown:** A `&lt;select&gt;` dropdown (2020–2026) will re-aggregate data to a single selected year and transition bubble sizes/colors with D3 `.transition().duration(600)`.
- **Zoom and pan:** Integrate `d3.zoom()` so users can zoom into dense regions (e.g., Northeast corridor) without losing context.
- **Enhanced tooltip:** On hover, display a sparkline mini-chart showing the selected airport's monthly delay rate trend.

**Purpose:** To support temporal exploration—users can observe whether an airport's delay performance improved or worsened over the pandemic/recovery years. Zoom prevents occlusion in high-density regions.

### Visualization 2 — Delay Cause Stacked Bars

**Planned Interaction / Animation:**
- **Sort buttons (already implemented):** Clicking "By Weather %" or "By Late Aircraft %" re-sorts bars with a 500ms D3 transition.
- **Drill-down on click:** Clicking an airport's bar will expand a detail panel below showing a monthly stacked-area trend chart for that specific airport.
- **Hover highlight:** Hovering a segment dims other segments to emphasize the selected cause.

**Purpose:** Sorting enables different analytical perspectives (e.g., finding the most weather-vulnerable airport regardless of size). Drill-down supports from-overview-to-detail navigation, a key dashboard pattern.

### Visualization 3 — Weather Scatter Plot

**Planned Interaction / Animation:**
- **Brush filtering (already implemented):** `d3.brush()` lets users drag a rectangle to filter points; double-click resets.
- **Linked highlighting:** Brushed points in the scatter plot will highlight corresponding bubbles on the Map (cross-view linking).
- **Play slider (temporal animation):** A range slider stepping through years will animate dot positions, showing how the precipitation-delay relationship shifts seasonally.

**Purpose:** Brush filtering supports exploratory subset analysis (e.g., "show me only airports with &gt;100mm rain and &gt;20% delay"). Temporal animation reveals whether weather-delay correlations strengthen in winter months.

---

## 4. Evaluation Plan

### What Will Be Evaluated?

- **Encoding effectiveness:** Whether the map's dual encoding (size + color) allows users to quickly identify high-delay, high-volume airports without confusion.
- **Interaction intuitiveness:** Whether users understand how to use sort buttons, brush filters, and the reset mechanism (double-click) without explicit instruction.
- **Insight generation:** Whether users can derive non-obvious findings—e.g., identifying ORD as a weather-delay outlier or noticing the weak precipitation-delay correlation.

### How Will It Be Evaluated?

- **Cognitive walkthrough:** Each group member will complete three timed tasks: (a) locate the airport with the highest weather-delay percentage, (b) use brush to count airports with &gt;150mm precipitation and &gt;18% delay, (c) identify which delay cause dominates ATL. We record completion time and error counts.
- **Heuristic evaluation:** We will inspect the visualization against Nielsen's 10 heuristics, with special attention to **system status visibility** (does the user know what filter is active?), **error prevention** (is the brush reset obvious?), and **flexibility** (do sort buttons offer meaningful alternatives?).
- **Peer review:** We will ask another project group to interact with the D3 prototype for 5 minutes and verbalize their thought process; we will note where they hesitate or misinterpret encodings.

### Data / Feedback to Be Collected

- **Task metrics:** Completion time per task (target &lt; 20 seconds), number of misclicks, and whether the user needed to ask for help.
- **Questionnaire:** Three Likert-scale items ("The color scale was intuitive," "I understood how to reset the brush," "The sort buttons helped me see new patterns") plus one open-ended question: "What additional interaction would you want?"
- **Interaction logs:** Screen recordings of peer-review sessions to analyze common navigation paths and stumbling blocks.