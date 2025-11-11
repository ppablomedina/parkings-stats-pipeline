from gcp.paths import year, n_month, path_abonados_en_banco as ss
from gcp.utils import read, parkings_current_info
import pandas as pd


SHEETS = {
    'Domiciliados':   {'event': 'Recaudación Domiciliados',   'n_parkings': 5, 'column_offset': year - 2012},
    'Otros Ingresos': {'event': 'Recaudación Otros ingresos', 'n_parkings': 3, 'column_offset': year - 2020},
}

def main():

    events = []

    for parking_name, [parking_id, _, _, _] in parkings_current_info.items():

        pairs = {}
        
        for sheet_name, sheet_info in SHEETS.items():
            sheet = read(ss, 'excel_sheet', sheet_name)

            event = sheet_info['event']
            n_parkings = sheet_info['n_parkings']
            column_offset = sheet_info['column_offset']

            for i in range(n_parkings):
                row_p_name = 2 + (i * 15)
                row_value = row_p_name + n_month

                p = sheet.iloc[row_p_name, 1]
                if p != parking_name: continue

                value = sheet.iloc[row_value, column_offset]
                if pd.isna(value) or value == 0: break
                pairs[event] = value
        
        if pairs: events.append([parking_id, pairs])

    return events
