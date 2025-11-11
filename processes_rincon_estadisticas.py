from current_month import w_month, year
from gcp_paths import path_rincon_estadisticas as ss
from gcp_utils import read


def main():

    sheet = read(ss, 'excel_sheet', f'{w_month.upper()} {str(year)[2:]}')
    
    # Búsqueda del índice de la fila donde la primera columna sea 'Totales'
    totales_row = sheet[sheet.iloc[:, 0] == 'Totales']

    value = totales_row['Bono2'].values[0]

    return [
        [3, {'Operaciones Bono2': value}  ],
        [3, {'Recaudación Bono2': value*3}]
    ]
