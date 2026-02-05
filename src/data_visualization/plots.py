
import matplotlib.pyplot as plt
import seaborn as sns

# === Bar Plots ===
def set_bar_style():
    plt.style.use("barchart.mplstyle")
    sns.set_theme(style="whitegrid", font_scale=1.2)
    palette = {
        "pre": "#1f3b4d",    # dark slate
        "post": "#5ca4a9"    # muted teal
    }
    return palette

# Temperature
def temperature_bar(df, fs):
    palette = set_bar_style()

    fig, ax = plt.subplots(figsize=fs)
    sns.barplot(
        data=df.reset_index(),        # get rid of the multindex from the grouping
        x='temp_range',
        y='defect_rate',
        hue='mitigation_period',
        palette=palette,
        ax=ax
    )
    ax.set(xlabel='Temperature Range (°F)', ylabel='Defect Rate')
    ax.legend(title='Mitigation', bbox_to_anchor=(1,1))
    ax.set_title("Temperature Defect Rate")
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    sns.despine(left=True, bottom=True)
    
    fig.tight_layout()
    
    return fig

# Noise level
def noise_bars(df, fs): 
    palette = set_bar_style()
    
    fig, ax = plt.subplots(figsize=fs)
    sns.barplot(
        data=df.reset_index(),        # get rid of the multindex from the grouping
        x='noise_level_range',
        y='defect_rate',
        hue='mitigation_period', 
        palette=palette,
        ax=ax
    )
    ax.set(xlabel='Noise Level Range (dB)', ylabel='Defect Rate')
    ax.legend(title='Mitigation', bbox_to_anchor=(1,1))
    ax.set_title("Noise Level Defect Rate")
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    sns.despine(left=True, bottom=True)

    fig.tight_layout()

    return fig


# All defects
def alldefects_bars(df, fs): 
    # Set a new column to use in bar plot to force ordering 'pre' before 'post'
    df['period_label'] = df.index.str.capitalize() + '-mitigation'
    
    palette = set_bar_style()

    fig, ax = plt.subplots(figsize=fs) # fs = (6,5)
    sns.barplot( 
        data=df.reset_index(),        # get rid of the multindex from the grouping
        x='period_label',
        y='defect_rate',
        hue='mitigation_period',
        palette=palette,
        legend=False,
        width=0.4,
        ax=ax
    )

    # Add count labels
    for i, val in enumerate(df['defect_count']):
        ax.text(i, df['defect_rate'].iloc[i] + 0.002, f"{val}", ha='center')
    ax.set(xlabel='Total Defects', ylabel='Defect Rate')
    ax.set_title("Total Defect Rate")
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    sns.despine(left=True, bottom=True)
    
    fig.tight_layout()
    
    return fig


# === Heatmaps ===

def set_heatmap_style():
    plt.style.use("heatmap.mplstyle")
    plt.get
    sns.set_theme(style="white", font_scale=1.2)

def heatmap(df, fs, title):
    set_heatmap_style()
    
    fig, ax = plt.subplots(figsize=fs)
    sns.heatmap(
        df, 
        annot=True, 
        cmap='coolwarm', 
        vmin=0, 
        vmax=0.5, 
        fmt='.1%', 
        linewidths=0.5,            # in heatmaps, this applies to Quadmesh, rather than grid, lines, etc.
        ax=ax
    )

    ax.set(xlabel='Noise Level Range (dB)', ylabel='Temperature Range (°F)')
    ax.invert_yaxis()
    ax.set_title(title)
    ax.tick_params(axis='y', labelrotation=0)
    sns.despine(left=True, bottom=True)
    
    fig.tight_layout()
    
    return fig
