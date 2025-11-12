from gcp.paths import n_month, path_abonos_lpa_y_qr as ss
from gcp.utils import read, parkings_current_info
import pandas as pd

def main():

    events = []

    sheet_map = {'Pagos': 'LPA PARK', 'QR': 'QR'}

    for parking_name, [parking_id, _, _, _] in parkings_current_info.items():

        pairs = {}
        
        for sheet_name in ['Pagos', 'QR']:

            try: df = read(ss, 'excel_sheet', sheet_name)
            except: continue
            
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

            df = df[df['Fecha'].dt.month == n_month]

            mask = df['Descripción'].str.contains(parking_name.upper(), na=False)
            df_parking = df[mask].copy()

            operaciones = len(df_parking)
            if operaciones == 0: continue

            df_parking['Importe'] = (
                df_parking['Importe']
                .astype(str)
                .str.replace(r'[^0-9,.-]', '', regex=True)  # elimina €, espacios, etc.
                .str.replace(',', '.', regex=False)         # convierte comas decimales a punto
                .astype(float)
            )
            recaudacion = df_parking['Importe'].sum()
            
            pairs[f'Operaciones {sheet_map.get(sheet_name)}'] = operaciones
            pairs[f'Recaudación {sheet_map.get(sheet_name)}'] = recaudacion

        if pairs: events.append([parking_id, pairs])

    return events
