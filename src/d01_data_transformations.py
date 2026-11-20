lazy import httpx
lazy import pendulum
lazy import csv
lazy import json
lazy import polars as pl
from d00_utils import get_latest_files, change_col_names, write_log

def data_extraction(headers: dict, urls: dict, date:pendulum.datetime) -> None:

    filenames = []

    for dataset, url in urls.items():
        
        filename = f"./grdata/_raw/{dataset}_{date.format('YYYYMMDDHHmmss')}.csv"
        
        with httpx.Client(headers = headers, follow_redirects = True, timeout=60, http2 = True) as client:
            with client.stream("GET", url) as response:
                response.raise_for_status()

                if url.startswith('https://repodatos'):
                    with open(filename, "wb") as f:
                        for chunk in response.iter_bytes():
                            f.write(chunk)
                else:
                    response.read()
                    data = response.json()['result']['records']
                    fieldnames = list(set().union(*data))
                    with open(filename, "wt", newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='') 
                        writer.writeheader()
                        writer.writerows(data)

        filenames.append(filename.split('/')[-1])
        get_latest_files(filenames=filenames, original_path = 'grdata/_raw', dest_path = 'grdata/_processed')
    
    return None

def protected_zones_stantization(mapping: str, mappings: dict[str, dict], dataframes: dict[str, pl.DataFrame]):

    for old, new in mappings[mapping].items():
        dataframes[mapping] = change_col_names(df = dataframes[mapping], old_name = old, new_name = new)

    std_df = (
        dataframes[mapping]
        .with_columns(
            pl.col("municipality").cast(pl.Utf8),
            pl.col("state").cast(pl.Utf8),
            pl.col("place_name").cast(pl.Utf8),
            pl.col("owner_type").cast(pl.Utf8),
            pl.col("certification").cast(pl.Utf8),
            pl.col("owner").cast(pl.Utf8),
            pl.col("surface").cast(pl.Float64),
            pl.col("is_endangered?").cast(pl.Boolean)
        )
        .select( 
            [
                "municipality",
                "state",
                "place_name",
                "owner_type",
                "certification",
                "owner",
                "surface",
                "is_endangered?"
            ]
    )
    )
    return std_df

def protected_zones_concat(path: str,json_path: str = "src/data_mapping.json"):
    # receive the mappings
    with open(json_path) as mappings_file:
        mappings = json.load(mappings_file)

    frames = {name: pl.read_parquet(path + name + '.parquet') for name in mappings}

    protected_zones = pl.DataFrame(schema={
        "municipality": pl.Utf8,
        "state": pl.Utf8,
        "place_name": pl.Utf8,
        "owner_type": pl.Utf8,
        "certification": pl.Utf8,
        "owner": pl.Utf8,
        "surface": pl.Float64,
        "is_endangered?": pl.Boolean
    })  

    # get the standarized versions  
    for frame in frames:

        protected_zones_df = protected_zones_stantization(mappings = mappings,mapping = frame, dataframes= frames)

        # check for columns in same name and length
        if protected_zones_df.shape[0] == 1:
            write_log(cat="Protected zones transformation", info = f"Data loss in std cols in {frame}")
            continue
        elif protected_zones_df.shape[1] != 8:
            write_log(cat="Protected zones transformation", info = f"Column creation missmatch in std cols in {frame}")
            continue
        else:
            # concat
            # print(protected_zones_df.collect_schema)

            protected_zones.vstack(protected_zones_df, in_place= True)
    # return
    return protected_zones



    
NOW_DATETIME = pendulum.now()

BASE = "https://www.datos.gob.mx/api/3/action/datastore_search?resource_id="

PATH = 'grdata/_processed/'
urls = {
    'advc':'https://repodatos.atdt.gob.mx/api_update/conanp/areas_destinadas_voluntariamente_conservacion/relacion_advc.csv',
    'sitios_cont': BASE + 'ae35d5aa-9bdd-4995-b2b7-9be5679b7d08',
    'sitios_remediados': BASE + '5194cd4a-35df-448f-ac83-69298fbc5b85',
    'sitios_cont_tipo': BASE + '70333741-9295-4745-9d88-e58415a461a8',
    'incendios_forestales': BASE + 'b61ec11c-e729-4da0-83f6-09965a49d45a',
    'historico_incendios_forestales': BASE + 'ddf38874-6243-4437-8f76-19f797cafa5c',
    'areas_protegidas': BASE + 'fd923799-1d5b-4a34-91f7-f66d7440a118',
    'generacion_res_pel_tipo': BASE + 'b1443d55-ba9e-4207-bd17-152b347b3be1',
    'biosferas_UNESCO': BASE + 'ded5927d-ace9-4ce1-93c4-aa46bafa2e41',
    'patrimonios': BASE + '69c4d710-fb0e-43cf-910d-0093f85c7726',
    'notas_impacto_ambiental': BASE + '8da5d613-841c-4569-ad1b-4ef557ec933a',
    'notas_impacto_ambiental_resolved': BASE + '144ca659-3699-4c6c-bfe9-c8f846ea7e29'

}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36",
    "Referer": "https://www.datos.gob.mx/",
    "Accept": "text/csv,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}

data_extraction(headers = headers,urls = urls,date = NOW_DATETIME)
a = protected_zones_concat(path = PATH)
print(a)