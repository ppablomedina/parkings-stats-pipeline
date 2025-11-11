from current_month import w_month, year
from gcp.paths import path_recaudacion as ss
from gcp.utils import read, parkings_current_info


def main():

    events = []

    excel = read(ss, 'excel_sheets')

    for parking_name, [parking_id, _, _, _] in parkings_current_info.items():

        for sheet_name in excel.sheet_names:

            if parking_name.upper() not in sheet_name.upper(): continue

            df = excel.parse(sheet_name)

            row = find_cell(df, w_month.upper())
            col = find_cell(df, year)

            value = df.iloc[row, col]
            if value == '-': continue

            events.append([parking_id, {'Recaudación Total Real': value}])

    return events

def find_cell(df, value):
    result = (df == value)
    if result.any().any():
        row_idx, col_label = result.stack()[result.stack()].index[0]
        col_idx = df.columns.get_loc(col_label)
        return row_idx if isinstance(value, str) else col_idx
    return None
