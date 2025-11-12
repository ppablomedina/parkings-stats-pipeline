from gcp.paths import path_ocupacion_ld as ss_ld, path_ocupacion_lv as ss_lv, path_ocupacion_sd as ss_sd
from gcp.utils import read, parkings_current_info


def main():

    events = []

    df_ld = read(ss_ld, 'xls')
    df_lv = read(ss_lv, 'xls')
    df_sd = read(ss_sd, 'xls')

    for _, [parking_id, id_internal, plazas, _] in parkings_current_info.items():

        df_p_ld, df_p_lv, df_p_sd = df_ld[df_ld['ID Aparcamiento'] == id_internal], df_lv[df_lv['ID Aparcamiento'] == id_internal], df_sd[df_sd['ID Aparcamiento'] == id_internal]

        values_ld, values_lv, values_sd = [], [], []

        for hour in range(24):
            values_ld.append(plazas - df_p_ld[df_p_ld['Hora'] == hour]['Media Plazas Libres'].values[0])
            values_lv.append(plazas - df_p_lv[df_p_lv['Hora'] == hour]['Media Plazas Libres'].values[0])
            values_sd.append(plazas - df_p_sd[df_p_sd['Hora'] == hour]['Media Plazas Libres'].values[0])
        
        events.append([parking_id, {
            'Plazas libres LD': [int(v) for v in values_ld],
            'Plazas libres LV': [int(v) for v in values_lv],
            'Plazas libres SD': [int(v) for v in values_sd]
        }])

    return events
