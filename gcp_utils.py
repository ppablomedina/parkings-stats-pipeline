from gcp_paths import BUCKET_NAME, PATH_INBOX, TABLE_EVENTS, TABLE_SUBJECTS, TABLE_STATES
from google.cloud import storage, bigquery
from current_month import date, year, n_month_int, date_to_delete
from PyPDF2 import PdfReader
import pandas as pd
import io


def read(blob_path, type, sheet_name=None):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_path)  
    data = blob.download_as_bytes()
    if   type == 'csv':          return pd.read_csv(io.BytesIO(data), sep=';')
    elif type == 'xls':          return pd.read_html(io.BytesIO(data))[0]  
    elif type == 'excel':        return pd.read_excel(io.BytesIO(data), engine='openpyxl')
    elif type == 'excel_sheet':  return pd.read_excel(io.BytesIO(data), sheet_name=sheet_name)
    elif type == 'excel_sheets': return pd.ExcelFile(io.BytesIO(data))
    elif type == 'pdf':          return PdfReader(io.BytesIO(data))

def upload_files_to_gcs(files_map):
    """Sube archivos a Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    for blob_path, local_path in files_map.items():
        bucket.blob(blob_path).upload_from_filename(local_path)

def move_blob(bucket, from_inbox, to_datalake):
    """Copia y borra un archivo en GCS (simula un rename)."""
    blob = bucket.blob(from_inbox)
    bucket.copy_blob(blob, bucket, to_datalake)
    blob.delete()

def delete_previous_version(bucket, path, yearly=False):
    """Elimina la versión del mes anterior del archivo (si existe)."""
    prev_path = path.replace(date, date_to_delete)
    prev_blob = bucket.blob(prev_path)

    if prev_blob.exists():
        if not (yearly and n_month_int == 1):
            prev_blob.delete()

def insert_events(events):
    client = bigquery.Client()

    rows = []
    for i, (parking_id, pairs) in enumerate(events):
        for metric, value in pairs.items():
            row = {
                'date': f'{year}-{n_month_int:02}-01 00:00:00',
                'subjects_id': parking_id,
                'metric': metric,
                'value': round(value, 2) if isinstance(value, (int, float)) else None,
                'value_array': str(value) if not isinstance(value, (int, float)) else None
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    job = client.load_table_from_dataframe(df, TABLE_EVENTS)
    job.result()

def get_current_info():
    client = bigquery.Client()

    query = f"""
    SELECT 
        p.name, p.id AS id_subjects, a.sagulpa_id, a.num_spaces, p.name_norm
    FROM `{TABLE_SUBJECTS}` p
    JOIN `{TABLE_STATES}` a
      ON p.states_id = a.id
    WHERE a.is_open = true
    """
    df = client.query(query).to_dataframe()

    return {
        row['name']: [row['id_subjects'], row['sagulpa_id'], row['num_spaces'], row['name_norm']]
        for _, row in df.iterrows()
    }

def get_bucket():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    return bucket

def get_blobs(bucket):
    """Devuelve una lista de blobs en el bucket."""
    blobs = [blob for blob in bucket.list_blobs(prefix=PATH_INBOX) if blob.size > 0]
    return blobs

parkings_current_info = get_current_info()
