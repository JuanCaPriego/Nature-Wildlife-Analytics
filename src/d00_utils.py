lazy import pendulum
lazy import polars as pl
lazy import os
lazy import csv

def files_to_parquet(source_path: str, final_path: str, file: str) -> None:

    extension = file.split('.')[-1]
    filename_datetime = file.split('.')[0]
    filename = "_".join(filename_datetime.split('_')[0:-1])

    if extension in 'csv':
        table = pl.read_csv(source = source_path + '/' + file)
        table.write_parquet(final_path + '/' + filename + '.parquet')

    return None

def change_col_names(df: pl.DataFrame, old_name: str, new_name: str) -> pl.DataFrame:
    if old_name not in df.columns:
        return df.with_columns(pl.lit(None).alias(new_name))
    else:
        return df.rename({old_name: new_name}, strict=False)
    
def get_latest_files(filenames: list, original_path: str, dest_path: str) -> list:

    files = os.listdir(original_path)

    for file in files:
        if file in filenames:
            files_to_parquet(source_path = original_path, final_path = dest_path, file = file)
        else:
            continue

    return None

def write_log(cat: str, info: str, timestamp: pendulum.datetime = pendulum.now()):

    filename = 'logs/app_logs.txt'
    file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
    headers = ['Category','Info','Timestamp']

    with open('logs/app_logs.txt', 'a', newline = '') as log_file:
        writer = csv.writer(log_file, delimiter = ',')
        
        if not file_exists:
            writer.writerow(headers)
        writer.writerow([cat, info, timestamp.format('YYYY-MM-DD HH:mm:ss')])
    return None