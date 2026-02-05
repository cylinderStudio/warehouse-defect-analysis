from data_utils import load_data_package
import plots
import streamlit as st

data = load_data_package()

st.set_page_config(page_title='Warehouse Defect Analysis')

st.title("Warehouse Defect Analysis")
st.markdown("Compare defect rates by temperature, noise, and mitigation period.")
st.markdown("""
This interactive dashboard explores the correlation between environmental conditions — specifically **temperature** and **noise** — and order fulfillment defects in a warehouse packing area.

The data powering this analysis is **fully synthetic**, designed to mimic real-world warehouse operations and conditions across a four-month period (June–September 2024). It includes a pre/post intervention split simulating the introduction of fans, portable AC units, and noise-dampening curtains in August.

Use the selector in the sidebar to explore visualizations of:
- Defect rate by **temperature** and **noise level**
- Overall defect rate before and after intervention
- Heatmaps showing joint effects of temperature and noise across time periods

For full context and source code, visit the [GitHub repository](https://github.com/YOUR-REPO-HERE).
""")

st.sidebar.title("Chart Selector")
st.sidebar.caption("Visualize temperature, noise, and defect patterns.")

chart_choice = st.sidebar.selectbox(
    "Choose a chart to display:",
    [
        "Temperature Defect Rate",
        "Noise Defect Rate",
        "Total Defect Rate",
        "Pre-Mitigation Heatmap",
        "Post-Mitigation Heatmap"
    ]
)

if chart_choice == "Temperature Defect Rate":
    st.pyplot(plots.temperature_bar(data['grouped_temp'], (8,5)))
elif chart_choice == "Noise Defect Rate":
    st.pyplot(plots.noise_bars(data['grouped_noise'], (8,5)))
elif chart_choice == "Total Defect Rate":
    st.pyplot(plots.alldefects_bars(data['grouped_all_defects'], (8,5)))
elif chart_choice == "Pre-Mitigation Heatmap":
    st.pyplot(plots.heatmap(data['pivot_pre'], (8,5), 'Defect Rate Heatmap (Pre-Mitigation)'))
elif chart_choice == "Post-Mitigation Heatmap":
    st.pyplot(plots.heatmap(data['pivot_post'], (8,5), 'Defect Rate Heatmap (Post-Mitigation)'))