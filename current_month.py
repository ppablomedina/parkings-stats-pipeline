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

# Mes y year actuales
current_month = pd.Timestamp.now().month
current_year = pd.Timestamp.now().year

# Determinar el mes y año anterior
if current_month == 1:
    n_month_int = 12
    year = current_year - 1
else: 
    n_month_int = current_month - 1
    year = current_year

if n_month_int == 1:
    n_month_to_delete_int = 12
    year_to_delete = year - 1
else:
    n_month_to_delete_int = n_month_int - 1
    year_to_delete = year

# Ajustar formato de número de mes (por ejemplo, '09' en lugar de '9')
n_month_str = f'{n_month_int:02}'
n_month_to_delete_str = f'{n_month_to_delete_int:02}'

# Obtener el nombre del mes anterior
w_month = months_n[n_month_int]

if   n_month_int in [1, 3, 5, 7, 8, 10, 12]: days_in_month = 31
elif n_month_int in [4, 6, 9, 11]:           days_in_month = 30
elif n_month_int == 2:                       days_in_month = 29 if year % 4 == 0 else 28

date = f'{year}{n_month_str}'
date_to_delete = f'{year_to_delete}{n_month_to_delete_str}'
