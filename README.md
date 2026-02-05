# Shipping Defect Analysis

This project is a fork of a delivered codebase for a freelance client who manufactures and ships a basic line of consumer products. It has been modified to remove anything proprietary.

The end-to-end solution collects sensor data and analyzes the correlation between environmental conditions (temperature and noise) and defect rates in a warehouse fulfillment process. It demonstrates how real-time sensor data combined with operational data can be used to identify and validate environmental stressors contributing to order fulfillment errors.

---

## Project Overview

This project showcases an end-to-end data engineering workflow:

- Environmental data captured via CircuitPython running on an RP2040 Connect microcontroller.
- Fulfillment and sensor data posted to Supabase via REST API.
- Analysis performed in Python using pandas, matplotlib, and seaborn.
- Visualized in an interactive Streamlit dashboard.

Initially, simulated warehouse environmental data was generated to help test the hypothesis and settle on data design.

---

## Tech Stack

- **Device**: Arduino Nano RP2040 Connect
- **Languages**: Python, CircuitPython
- **Cloud Backend**: Supabase (PostgreSQL + REST API)
- **Visualization**: Matplotlib, Seaborn, Streamlit
- **Dev Tools**: Jupyter, VSCode

---

## Repo Structure

```
data/
├── order_fulfillment_data_0607.csv
├── order_fulfillment_data_0809.csv
├── shipdock_environmental_data_0607.csv
├── shipdock_environmental_data_0809.csv
├── weather_data_0607.csv
└── weather_data_0809.csv

src/
├── config/
├── data_collection/
│   ├── code.py               # CircuitPython code for RP2040
│   └── settings.toml         # WiFi + config vars
├── data_ingestion_and_simulation/
│   ├── orderfufillment_data_gen.ipynb
│   └── shipdock_environmental_data_gen.ipynb
└── data_visualization/
    ├── app.py                # Streamlit dashboard
    ├── barchart.mplstyle
    ├── heatmap.mplstyle
    ├── data_utils.py
    ├── plots.py
    └── data_comparison.ipynb
```

---

## Supabase Schema

### Table: `order_fulfillment_data`

| Column          | Type          |
| --------------- | ------------- |
| id              | int4 (PK)     |
| timestamp       | timestamp     |
| ship_date       | timestamp     |
| defect_reported | defect enum   |
| pack_date       | timestamp     |
| order_id        | text          |
| number_of_items | int4          |
| ship_method     | carriers enum |
| box_size        | box_size enum |

### Table: `shipdock_environmental_data`

| Column      | Type      |
| ----------- | --------- |
| id          | int4 (PK) |
| timestamp   | timestamp |
| temperature | float8    |
| noise_level | float8    |

### Enumerated Types

- `box_size`: A, B, C
- `carriers`: usps, fedex, ups, dhl
- `defect`: missing items, wrong items, poorly packed

---

## Data Modeling

- `defect_reported_bool`: boolean flag for analysis
- `mitigation_period`: labeled "pre" (June–July) or "post" (August–September)
- `temp_range`, `noise_level_range`: binned ranges for grouped visualization

---

## Visualizations

- **Bar Charts**
  - Defect rate by `temp_range` (`grouped_temp`)
  - Defect rate by `noise_level_range` (`grouped_noise`)
  - Defect rate by `mitigation_period` (`grouped_all_defects`)
- **Heatmaps**
  - Pivot tables showing `defect_reported` ratio by `temp_range` and `noise_level_range`
  - Pre- and post-mitigation views with consistent scale

---

## Correlation Analysis

The merged dataframe shows weak but visible positive correlation between:

- Higher temperatures and higher defect rates
- Elevated noise levels and defect reports

---

## Results

- Functional simulation of environmental + operational data
- Interactive dashboard to view patterns over time
- Modular pipeline that mirrors real-world industrial analytics

---

## Next Steps

- Test with real IoT sensor data
- Expand schema to track packing employees or shift schedules
- Integrate dashboard into real-time operations UI

---

## Live Dashboard

[Streamlit App (Demo)](https://sensor-to-dashboard-deploy-hdccv4tetxjvauxzm6pvf2.streamlit.app/)

---

## License

MIT © 2025
