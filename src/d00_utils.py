lazy import pendulum
lazy import polars as pl
lazy import os

def files_to_parquet(source_path: str, final_path: str, file: str) -> None:

    extension = file.split('.')[-1]
    filename_datetime = file.split('.')[0]
    filename = "_".join(filename_datetime.split('_')[0:-1])

    if extension in 'csv':
        table = pl.read_csv(source = source_path + '/' + file)
        table.write_parquet(final_path + '/' + filename + '.parquet')

    return None


def get_latest_files(filenames: list, original_path: str, dest_path: str) -> list:

    files = os.listdir(original_path)

    for file in files:
        if file in filenames:
            files_to_parquet(source_path = original_path, final_path = dest_path, file = file)
        else:
            continue

    return 