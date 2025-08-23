import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# --- Configuration ---
COLUMN_NAMES = ["Timestamp", "Registry", "SizeMB", "PushTime", "ColdPullTime", "WarmPullTime"]
MAIN_DATA_FILE = 'results/data.csv'
NEW_RESULTS_DIR = 'all-results/'
PUSH_CHART_FILE = 'chart-push-performance.svg'
PULL_CHART_FILE = 'chart-cold-pull-performance.svg'

def generate_plot(df, output_path, y_col, title):
    """Groups data, calculates the average, and generates a plot."""
    # Group by Registry and Size, then calculate the mean time.
    df_agg = df.groupby(['Registry', 'SizeMB'])[y_col].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the aggregated (averaged) data
    for group_name, group_data in df_agg.groupby('Registry'):
        ax.plot(group_data['SizeMB'], group_data[y_col], marker='o', linestyle='-', label=group_name)
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Image Size (MB)', fontsize=12)
    ax.set_ylabel('Average Time (ms)', fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend(title='Registry')
    plt.tight_layout()
    fig.savefig(output_path, format='svg')
    print(f"Chart saved to {output_path}")

def main():
    # 1. Load existing data
    if os.path.exists(MAIN_DATA_FILE):
        try:
            old_df = pd.read_csv(MAIN_DATA_FILE)
        except pd.errors.EmptyDataError:
            old_df = pd.DataFrame(columns=COLUMN_NAMES)
    else:
        old_df = pd.DataFrame(columns=COLUMN_NAMES)

    # 2. Load all new results
    new_files = glob.glob(os.path.join(NEW_RESULTS_DIR, '**/*.csv'), recursive=True)
    if not new_files:
        print("No new result files found.")
        all_data_df = old_df
    else:
        list_of_new_dfs = [pd.read_csv(f, header=None, names=COLUMN_NAMES) for f in new_files]
        new_df = pd.concat(list_of_new_dfs, ignore_index=True)
        all_data_df = pd.concat([old_df, new_df], ignore_index=True)

    # 3. VITAL FIX: Convert data to numeric types for correct sorting and math
    for col in ['SizeMB', 'PushTime', 'ColdPullTime', 'WarmPullTime']:
        all_data_df[col] = pd.to_numeric(all_data_df[col])

    # 4. Clean and sort the combined data
    all_data_df.drop_duplicates(inplace=True)
    all_data_df.sort_values(by=["Timestamp", "Registry", "SizeMB"], inplace=True)

    # 5. Save the updated master data file
    os.makedirs(os.path.dirname(MAIN_DATA_FILE), exist_ok=True)
    all_data_df.to_csv(MAIN_DATA_FILE, index=False)
    print(f"Updated data saved to {MAIN_DATA_FILE}. Total rows: {len(all_data_df)}")

    # 6. Generate charts if there's data
    if not all_data_df.empty:
        generate_plot(all_data_df, PUSH_CHART_FILE, 'PushTime', 'Push Performance (Time vs. Image Size)')
        generate_plot(all_data_df, PULL_CHART_FILE, 'ColdPullTime', 'Cold Pull Performance (Time vs. Image Size)')
    else:
        print("Dataframe is empty, skipping chart generation.")

if __name__ == "__main__":
    main()
