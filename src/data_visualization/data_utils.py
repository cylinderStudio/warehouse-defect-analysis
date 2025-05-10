from dotenv import load_dotenv
import os
from supabase import create_client
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=True)
def load_data_package():
    # === Load credentials and connect to Supabase ===
    load_dotenv()
    url = os.getenv('DB_URL')
    key = os.getenv('DB_API_KEY')
    supabase = create_client(url, key)
    
    return_object = {}

    def fetch_table(table):
        try:
            response = (
                supabase.from_(table)   # 'from' is a reserved word in Python
                .select('*')
                .execute()
            )
            
            if not response.data:
                raise ValueError(f"No data returned for table: {table}")

        except Exception as e:
            print(f'An error occured: {e}')
    
        return response.data
    
    # === Load and preprocess ===
    fulfillment_df = pd.DataFrame(fetch_table('order_fulfillment_data'))
    sensor_df = pd.DataFrame(fetch_table('shipdock_environmental_data'))
    fulfillment_df[['timestamp', 'ship_date', 'pack_date']] = fulfillment_df[['timestamp', 'ship_date', 'pack_date']].apply(pd.to_datetime)
    sensor_df['timestamp'] = pd.to_datetime(sensor_df['timestamp'])
    
    # === Merge ===
    merged_df = pd.merge_asof(
        fulfillment_df.sort_values('pack_date'),
        sensor_df.sort_values('timestamp'),
        left_on='pack_date',    # left_on and right_on must be datetime, integer or float and ordered
        right_on='timestamp',
        direction='nearest'     # 'nearest' to search for closest matches, vs prior or subsequent
    )
    
    # === Add features ===
    
    # Add boolean column of defect_reported to do numeric correlations
    merged_df.insert(4, 'defect_reported_bool', merged_df['defect_reported'].notnull(), allow_duplicates=False)
    # Add category column indicating 'pre' and 'post' application of temperature and noise mitigation
    merged_df['mitigation_period'] = merged_df['pack_date'].dt.month.map(
        lambda m: 'pre' if m in [6, 7] else 'post'
    )
    # Create ranges to use in bar plots
    merged_df['temp_range'] = pd.cut(
        merged_df['temperature'],
        bins=[60, 65, 70, 75, 80, 85, 90],
        labels=['60-65', '65-70', '70-75', '75-80', '80-85', '85-90']
    )
    merged_df['noise_level_range'] = pd.cut(
        merged_df['noise_level'],
        bins=[20, 30, 40, 50, 60, 70, 80],
        labels=['20-30', '30-40', '40-50', '50-60', '60-70', '70-80']
    )
    
    return_object['merged'] = merged_df
    
    # === Groupings for bar charts ===
    grouping_ranges = {
        'grouped_temp': {'ranges': ['mitigation_period','temp_range']},
        'grouped_noise': {'ranges': ['mitigation_period','noise_level_range']},
        'grouped_all_defects': {'ranges': ['mitigation_period']}
    }
    
    for x in grouping_ranges:
        return_object[x] = merged_df.groupby(grouping_ranges[x]['ranges'], observed=False).agg(
            total_orders=('order_id', 'count'),
            defect_count=('defect_reported', lambda x: x.notna().sum())
        ).sort_values('mitigation_period', ascending=False)
    
        return_object[x]['defect_rate'] = return_object[x]['defect_count'] / return_object[x]['total_orders'] 

    # Creates:
    # return_object['grouped_temp']
    # return_object['grouped_noise']
    # return_object['grouped_all_defects']
    
    # === Pivot tables for heatmaps ===
    
    pivot_periods = ['pre', 'post'] 

    for period in pivot_periods:
        p_series = merged_df[merged_df['mitigation_period'] == period]
        return_object[f'pivot_{period}'] = p_series.pivot_table(
            index='temp_range',
            columns='noise_level_range',
            values='defect_reported',
            aggfunc=lambda x: x.notna().mean()
        )
    
    # Creates:
    # return_object['pivot_pre']
    # return_object['pivot_post']

    return return_object