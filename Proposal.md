# Visualizing Flight Delays and Their Causes

## 1 Topic Goals and Research Questions

- **Topic:** Explore U.S. domestic flight delays across airlines, airports, and seasons, including reported causes and delay propagation across consecutive flights operated by the same aircraft.
- **Public audience:** Help travelers understand disruptions, compare historical reliability, and identify patterns relevant to flight selection.
- **Administrative audience:** Help airline, airport, and government teams identify operational patterns and opportunities for further investigation.
- **Visualization goals:** Connect geographic, temporal, and causal perspectives through interactive views that support comparison and exploration.
- **Research questions:** Which airlines and airports have higher delay rates? What seasonal patterns recur? Which causes dominate delay frequency and duration? How do weather-related delays relate to other categories? Where do aircraft journeys accumulate or recover delays?

## 2 Datasets and Preparation

We will download [BTS Airline On-Time Statistics and Delay Causes](https://www.transtats.bts.gov/ot_delay/ot_delaycause1.asp) CSV files, initially targeting 2020–2025 and more than 10,000 carrier–airport–month records. Key fields include carrier, airport, year, month, arrival totals, delayed arrivals, and counts and minutes for five reported causes. An airport coordinate table will support mapping.

Propagation analysis requires separate flight-level data with tail numbers, airports, timestamps, and delays, initially scoped to 2020–2022. [NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) is an optional supplement, subject to suitable hourly coverage and airport proximity. Final periods and record counts will depend on availability and completeness.

## 3 Analysis and Visualization Methods

**Tools and implementation.** Python and pandas will handle preparation and aggregation. JavaScript and D3.js will implement interactive visualizations, with HTML/CSS providing the interface. Prepared CSV files will load through `d3.csv()`. Shared date, airline, and airport filters will connect the views; tooltips will explain metrics and denominators.

**Cleaning and derived metrics.** We will check duplicates, standardize airport and carrier identifiers, inspect missing values, and validate denominators. Delay rate equals `sum(arr_del15) / sum(arr_flights)`. Aggregating counts before division avoids equally weighting groups with different flight volumes. We will verify the arrival-total definition before labeling the complement as an on-time rate, and distinguish cancellations and diversions where available.

**Comparative and temporal analysis.** Airline and airport comparisons will combine rates with traffic volume. Monthly aggregation will preserve year–month order to distinguish recurring seasonal peaks from isolated disruptions. Cause shares will compare summed attributed counts against delayed arrivals, accounting for fractional attribution; a separate minutes-based comparison will show whether frequent causes also produce longer delays.

**Weather and propagation analysis.** Airport-level weather profiles will compare normalized dimensions and associations among delay categories. Weather-station integration, if feasible, will use documented distance and time windows. Flight sequences will match tail numbers, connecting airports, and plausible turnaround times after timestamp normalization. We will calculate changes between consecutive flights and summarize journey counts and median delay changes. Missing identifiers will limit scope; observed associations will not establish causation.

**Techniques and user tasks.** Six coordinated views will use scatter plots, proportional-symbol maps, line charts, stacked bars, parallel coordinates, and directional flow maps. Together they support comparison, trend identification, filtering, geographic exploration, relationship discovery, and outlier detection. Selecting airports or routes will reveal details while preserving the broader context.

## 4 Visualization Sketches and References

### 1 Airline Performance Scatter Plot

Each airline is a point: horizontal position shows arrival volume and vertical position shows on-time rate. Tooltips expose totals. Users compare airline reliability and explore its relationship with operational scale.

![v1](pic/v1)

Reference: [Flight Reliability Analytics Platform — Airline Scale vs Reliability](https://github.com/momo840505/flight-reliability-platform).

### 2 Airport Delay Map

Airport marker size represents flight volume; color represents delay rate. Hovering reveals details, and selection filters related views. Users explore geographic variation and identify unusually high or low rates.

![v2](pic/v2)

Reference: [USA Airlines On-Time Performance](https://0506zhengyi.github.io/Airline_on_time_performance/interactive-component.html).

### 3 Monthly Delay Line Chart

A chronological line shows monthly delay rates by year, with airline and airport filters. Users identify peaks, declines, and repeated seasonal patterns rather than relying on four-season averages.

![v3](pic/v3)

Reference: [Seasonal Patterns of Delays](https://public.tableau.com/app/profile/mazen.karam/viz/seasonlflightdelays/SeasonalPatternsofDelays?publish=yes).

### 4 Delay Cause Stacked Bars

A 100% stacked horizontal bar chart compares carrier, weather, NAS, security, and late-aircraft causes across the ten busiest airports. Users switch between counts and minutes, re-sort airports, and select bars to update details and monthly trends.

![v4](pic/v4)

Design reference: [BTS Airline Data Platform](https://github.com/cemputer/bts-airline-data-platform).

### 5 Weather and Delay Profiles

Two linked parallel-coordinates plots show airport severity profiles and normalized cause counts. Axes include flight volume, delay rate, average delay, weather share, and late-aircraft share. Brushing highlights similar airports and explores weather associations without treating reported weather delays as all weather impacts.

![v5](pic/v5)

Subject reference: [FAA Weather Delay FAQ](https://www.faa.gov/nextgen/programs/weather/faq); the paired plots illustrate our proposed comparison design.

### 6 Delay Propagation Flow Map

A directional map centered on Chicago O’Hare traces connected aircraft journeys. Width shows journey counts; color shows growing, recovering, or stable delays. Date and airline filters support route comparisons; selecting routes reveals subsequent flights and unusually large delay changes.

![v6](pic/v6)

Image reference: AI-generated conceptual sketch of the proposed flow map.

## 5 Group Roles and Responsibilities

Yuxuan leads airline, airport, and seasonal views. Rosa leads cause decomposition and weather profiles. Nora leads flight-sequence preparation and propagation visualization. All members contribute to validation, interface integration, testing, documentation, and presentations, and review the complete workflow.

## 6 Interim Presentation Deliverables

We will present cleaned CSV subsets, a data dictionary, preliminary summaries, finalized questions, and mockups or prototypes for at least four views. At least two views will demonstrate working tooltips and filters, alongside an assessment of flight-sequence feasibility.

## 7 Timeline and Milestones

- **Week 2:** Finalize scope, questions, responsibilities, and repository.
- **Week 3:** Acquire and clean data, derive metrics, and match coordinates.
- **Week 4:** Complete six sketches, interaction plans, and interface structure.
- **Week 5:** Deliver interim prototypes and presentation materials.
- **Week 6:** Complete linked views and test calculations, filters, and browser behavior.
- **Week 7:** Debug, document, deploy to GitHub Pages, and present findings and limitations.
