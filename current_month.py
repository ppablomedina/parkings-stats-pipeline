import pandas as pd


# Diccionario de months
months_n = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo',       4: 'Abril',    5: 'Mayo',       6: 'Junio', 
    7: 'Julio', 8: 'Agosto',  9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

months_w = {
    'Enero': '01', 'Febrero': '02', 'Marzo':      '03', 'Abril':   '04', 'Mayo':      '05', 'Junio':     '06',
    'Julio': '07', 'Agosto':  '08', 'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'
}

# Fecha del mes anterior
n_month_int = pd.Timestamp.now() - pd.DateOffset(months=1)
year       = n_month_int.year
date       = n_month_int.strftime("%Y%m")


# # Ajustar formato de número de mes (por ejemplo, '09' en lugar de '9')
# n_month_str = f'{n_month_int:02}'

# # Obtener el nombre del mes anterior
# w_month = months_n[n_month_int]
