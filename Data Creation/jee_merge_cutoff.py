import pandas as pd
import glob
import os

df_list = []

required_cols = ['Institute', 'Academic Program Name', 'Quota', 'Seat Type', 
                 'Gender', 'Opening Rank', 'Closing Rank', 'Round', 'Year']

# 2018-2022
for year in range(2018, 2023):
    path = rf"E:\Data Scientist\Project\Project College\Data Creation\Jee_cutoff\{year}.csv"
    df = pd.read_csv(path)
    df['Year'] = year
    # Keep only columns that exist
    existing_cols = [col for col in required_cols if col in df.columns or col == 'Year']
    df = df[existing_cols]
    df_list.append(df)

# 2024
df_2024 = pd.read_csv(r"E:\Data Scientist\Project\Project College\Data Creation\Jee_cutoff\2024.csv")
rounds = [1,2,3,4,5]
rows = []
for _, row in df_2024.iterrows():
    for r in rounds:
        opening_col = f"Round{r}OpeningRank"
        closing_col = f"Round{r}ClosingRank"
        if opening_col in df_2024.columns and closing_col in df_2024.columns:
            rows.append({
                'Institute': row.get('Institute', ''),
                'Academic Program Name': row.get('AcademicProgramName', ''),
                'Quota': row.get('Quota', ''),
                'Seat Type': row.get('SeatType', ''),
                'Gender': row.get('Gender', ''),
                'Opening Rank': row[opening_col],
                'Closing Rank': row[closing_col],
                'Round': r,
                'Year': 2024
            })
df_2024_long = pd.DataFrame(rows)
df_list.append(df_2024_long)

# 2023 & 2025 (Round_1.csv, Round_2.csv, etc.)
for year in [2023, 2025]:
    folder_path = rf"E:\Data Scientist\Project\Project College\Data Creation\Jee_cutoff\{year}"
    files = sorted(glob.glob(os.path.join(folder_path, "Round_*.csv")))
    for f in files:
        df = pd.read_csv(f)
        round_number = int(os.path.basename(f).split('_')[1].split('.')[0])
        df['Year'] = year
        df['Round'] = round_number
        # Keep only columns that exist
        existing_cols = [col for col in required_cols if col in df.columns or col in ['Year', 'Round']]
        df = df[existing_cols]
        df_list.append(df)

# Merge all
final_df = pd.concat(df_list, ignore_index=True)

# Remove rows where Opening or Closing Rank has 'P'
final_df = final_df[~final_df['Opening Rank'].astype(str).str.contains('P', na=False)]
final_df = final_df[~final_df['Closing Rank'].astype(str).str.contains('P', na=False)]

# Convert to numeric
final_df['Opening Rank'] = pd.to_numeric(final_df['Opening Rank'])
final_df['Closing Rank'] = pd.to_numeric(final_df['Closing Rank'])

final_df.to_csv(r"E:\Data Scientist\Project\Project College\Data Creation\Jee_cutoff\merged_jee_cutoff_2018_2025.csv", index=False)
print("Merged CSV created successfully!")
