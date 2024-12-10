import pandas as pd
import os
import hashlib
from supabase import create_client, Client
from helper_functions import csv_to_dataframe
from my_secrets import url, key

supabase: Client = create_client(url, key)

DATA_DIR = "./data"
FILTER_IDS = {
    "V": 1,
    "B": 2,
    "U": 3,
    "UVW1": 4,
    "UVM2": 5,
    "UVW2": 6
}


def check_errors(result) -> None:
    """
    Check for errors in the result of a Supabase query
    :param result: dict: the result of a Supabase query
    :return: None
    """
    if hasattr(result, "status_code") and result.status_code != 200:
        print(f"Something happened during upsert: HTTP status {result.status_code}")
    elif hasattr(result, "error") and result.error:
        print(f"Error during upsert: {result.error.message}")


def populate_filters():
    """
    Populate the filters table in the database with the filters used in the data
    """
    for filter_name, filter_id in FILTER_IDS.items():
        result = supabase.table("filters").upsert({"filter_id": filter_id, "filter_name": filter_name}, on_conflict="filter_id").execute()
        check_errors(result)
    
    print("Filters populated.")


def populate_supernovae():
    df = csv_to_dataframe("./data/csv/updated_master.csv", ["name", "type", "redshift", "modulus"])

    # Step 1: Aggregate unique types from CSV data
    unique_types_from_csv = set(df['type'].dropna().unique())

    # Step 2: Fetch existing types from the database
    existing_types_result = supabase.table("sn_types").select("type_id", "type_name").execute()
    existing_types = {type['type_name']: type['type_id'] for type in existing_types_result.data}

    # Step 3: Find which types need to be inserted
    missing_types = unique_types_from_csv - existing_types.keys()

    # Step 4: Insert missing types in a batch
    if missing_types:
        missing_types_data = [{"type_name": type_name} for type_name in missing_types]
        supabase.table("sn_types").insert(missing_types_data).execute()

        # Step 5: Optionally, re-fetch the updated types list
        updated_types_result = supabase.table("sn_types").select("type_id", "type_name").execute()
        existing_types.update({type['type_name']: type['type_id'] for type in updated_types_result.data})

    # Step 6: Create a map from type names to IDs
    type_name_to_id = {type_name: existing_types[type_name] for type_name in unique_types_from_csv}

    # Step 7: Prepare your supernovae batch with correct `type_id`, ensuring no duplicates
    supernovae_batch_temp = {}
    for _, row in df.iterrows():
        sn_name = row['name']
        if sn_name not in supernovae_batch_temp:
            type_id = type_name_to_id.get(row['type'])
            supernovae_batch_temp[sn_name] = {
                "sn_name": sn_name,
                "type_id": type_id if type_id else None,
                "redshift": row['redshift'] if pd.notna(row['redshift']) else None,
                "distance_modulus": row['modulus'] if pd.notna(row['modulus']) else None
            }

    supernovae_batch = list(supernovae_batch_temp.values())

    # Step 8: Upsert supernovae batch
    if supernovae_batch:
        result = supabase.table("supernovae").upsert(supernovae_batch, on_conflict="sn_name").execute()
        check_errors(result)
        print("Supernovae populated.")
    else:
        print("No data to upsert.")


def populate_light_curves():
    file_names = [f for f in os.listdir(DATA_DIR) if f.endswith(".dat")]
    existing_sn_names_result = supabase.table("supernovae").select("sn_id", "sn_name").execute().data
    existing_sn_names_lower = {sn['sn_name'].lower(): sn['sn_id'] for sn in existing_sn_names_result}
    
    unique_sn_names = []
    ignored_sn_names = []
    updated_file_names = []
    
    for f in file_names:
        supernova_name = f.split('_')[0].lower()
        if supernova_name not in existing_sn_names_lower:
            print(f"Supernova {supernova_name} not found in the database. Ignoring photometry data.")
            ignored_sn_names.append(supernova_name)
            continue
        
        if supernova_name not in unique_sn_names:
            unique_sn_names.append(supernova_name)
            updated_file_names.append(f)
    
    batch = []
    
    for f in updated_file_names:
        with open(os.path.join(DATA_DIR, f), 'r') as file:
            lines = file.readlines()
            for idx, line in enumerate(lines):
                if line.startswith('# Filter'):
                    header_line = idx
                    break
            else:
                print(f"File {f} is malformed. Ignoring.")
                continue
        
        data = pd.read_csv(os.path.join(DATA_DIR, f), skiprows=header_line + 1, sep=r'\s+', comment='#', engine='python', header=None)
        data.columns = lines[header_line].replace("# ", "").split()
        
        for _, row in data.iterrows():
            sn_name = f.split('_')[0].lower()
            sn_id = existing_sn_names_lower[sn_name]
            filter_id = FILTER_IDS.get(row['Filter'])
            mjd = row['MJD[days]']
            mag = row['Mag'] if pd.notna(row['Mag']) else None
            mag_err = row['MagErr'] if pd.notna(row['MagErr']) else None
            hash_value = hashlib.sha256(f"{sn_id}-{filter_id}-{mjd}-{mag}-{mag_err}".encode('utf-8')).hexdigest()
            
            batch.append({
                "sn_id": sn_id,
                "filter_id": filter_id,
                "mjd": mjd,
                "magnitude": mag,
                "magnitude_error": mag_err,
                "hash": hash_value,
            })
    
    # Upsert light curve batch based on the hash
    if batch:
        hashes = [item['hash'] for item in batch]
        if len(hashes) != len(set(hashes)):
            print("Duplicate hashes found in the batch.")
            # print conflicting rows
            # print("Conflicting rows: ")
            # for item in batch:
            #     if hashes.count(item['hash']) > 1:
            #         print(item)
            remove_duplicates = input("Do you want to remove duplicates before upserting? (y/n): ")
            if remove_duplicates.lower() == "y":
                batch = [dict(t) for t in {tuple(d.items()) for d in batch}]
                print("Duplicates removed.")
            else:
                print("Duplicates not removed, upsert aborted.")
                return
        result = supabase.table("light_curves").upsert(batch, on_conflict="hash").execute()
        check_errors(result)
        print("Light curves populated.")
    else:
        print("No data to upsert.")
    print(f"Ignored supernovae due to missing supernova names/id: {ignored_sn_names}")
