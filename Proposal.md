# Visualizing Flight Delays and Their Causes

## Topic Goals and Research Questions

We propose an interactive visualization dashboard exploring U.S. domestic flight delays across airlines, airports, and seasons. The project will examine reported delay causes and investigate how delays persist, worsen, or recover across consecutive flights operated by the same aircraft.

Our primary audience is travelers seeking to understand disruptions and compare historical flight reliability. A second audience includes airline, airport, and government administrators interested in operational patterns. The dashboard will support informed exploration without presenting historical averages as predictions for individual journeys.

Our questions are: Which airlines and airports experience higher delay rates? How do delays vary seasonally? Which reported causes contribute most to delay frequency and duration? How are weather-related delays associated with other categories? Where do delays accumulate or recover along aircraft journeys?

## Datasets and Preparation

Our main source is the [Bureau of Transportation Statistics Airline On-Time Statistics and Delay Causes](https://www.transtats.bts.gov/ot_delay/ot_delaycause1.asp). We will download CSV data and initially target 2020–2025, adjusting the scope after checking completeness. The working dataset should contain more than 10,000 carrier–airport–month records; these are aggregated observations, not individual flights.

Key attributes include year, month, carrier, airport, arrival-flight totals, delayed-arrival totals, and counts and minutes attributed to carrier, weather, National Aviation System (NAS), security, and late-aircraft causes. An airport coordinate reference table will support mapping. We will obtain separate flight-level records containing aircraft tail numbers, origin and destination airports, timestamps, and delays for the propagation analysis, initially exploring 2020–2022.

Preparation will include checking duplicates, standardizing identifiers, documenting missing values, and validating denominators. We will sum delayed arrivals and arrival totals before calculating rates, avoiding unweighted averages across differently sized groups. Cancellations and diversions will be reported separately where available, with metric definitions made explicit. Flight-level timestamps will be standardized across time zones before connecting aircraft journeys.

[NOAA Climate Data Online](https://www.ncei.noaa.gov/cdo-web/) is a possible supplementary source. Weather integration remains optional until suitable station coverage and temporal resolution are confirmed. Any matching procedure will document station distance, time windows, and missing observations.

## Analysis and Implementation

We will use Python and pandas for preparation, and JavaScript, D3.js, HTML, and CSS for the dashboard. Prepared CSV files will be loaded with `d3.csv()`. Shared airline, airport, and date filters will connect comparisons across views, while tooltips explain values and denominators.

Delay rate will be calculated as `sum(arr_del15) / sum(arr_flights)`. We will verify the arrival-total definition before labeling its complement as an on-time rate. Cause comparisons will distinguish attributed counts from delay minutes and account for fractional attribution. Associations between categories will be treated as exploratory evidence rather than proof of causation.

## Visualization Designs

### 1 Airline Performance Scatter Plot

Each point represents an airline, with arrival volume on the horizontal axis and on-time rate on the vertical axis. Tooltips show totals and rates. This view supports reliability comparisons while making differences in operational scale visible.

![v1](pic/v1)

### 2 Airport Delay Map

A U.S. proportional-symbol map will encode airport flight volume through marker size and delay rate through color. Hovering reveals airport details; selecting an airport filters related views. This design helps users locate geographic patterns and unusually high or low delay rates.

![v2](pic/v2)

### 3 Monthly Delay Line Chart

A chronological line chart will show monthly delay rates, preserving year and month rather than collapsing observations into four seasons. Airline and airport filters will support comparisons. Repeated peaks across years will help users investigate seasonal patterns and distinguish them from isolated disruptions.

![v3](pic/v3)

### 4 Delay Cause Stacked Bars

A 100% stacked horizontal bar chart will compare five reported causes across the ten busiest airports in the selected period. Users can switch between attributed counts and delay minutes, sort airports, and inspect linked details and monthly trends. This view reveals whether frequent causes also account for substantial delay duration.

![v4](pic/v4)

### 5 Weather and Delay Profiles

Two linked parallel-coordinates plots will compare airport profiles. The first combines flight volume, delay rate, average delay duration, weather share, and late-aircraft share; the second compares normalized cause counts. Brushing and highlighting will identify airports with similar profiles. These views explore weather associations without treating the reported weather category as a complete measure of weather impacts.

![v5](pic/v5)


### 6 Delay Propagation Flow Map

A directional flow map centered on Chicago O’Hare will trace connected aircraft journeys. Line width represents journey counts, while color indicates growing, recovering, or stable delays. Connections will require matching tail numbers, airports, and plausible turnaround times. Route selection reveals subsequent flights. If suitable identifiers are unavailable, we will narrow this component rather than infer confirmed aircraft sequences from flight numbers alone.

![v6](pic/v6)

## Team Responsibilities

Yuxuan will lead the airline scatter plot, airport map, and seasonal analysis. Rosa will lead delay-cause analysis and weather profiles. Nora will lead flight-sequence preparation and propagation visualization. All members will contribute to data validation, interface integration, testing, documentation, and presentation preparation, and review the complete analytical workflow.

## Interim Deliverables and Timeline

The interim presentation will include cleaned CSV subsets, a data dictionary, preliminary summaries, finalized research questions, and mockups or prototypes for at least four views. At least two views will demonstrate working interactions, including tooltips and filters.

- **Week 2:** Finalize scope, responsibilities, research questions, and the GitHub repository.
- **Week 3:** Acquire and clean data, calculate metrics, and match airport coordinates.
- **Week 4:** Complete six sketches, interaction plans, and the HTML/CSS interface.
- **Week 5:** Deliver interim prototypes and presentation materials.
- **Week 6:** Complete and connect all six views; test calculations, filters, and browser behavior.
- **Week 7:** Resolve remaining issues, finish documentation, deploy to GitHub Pages, and present findings and limitations.
