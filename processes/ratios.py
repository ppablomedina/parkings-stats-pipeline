from gcp.utils import parkings_current_info


def main(all_events):

    events_calculated = []

    for _, [parking_id, _, plazas, _] in parkings_current_info.items():
        
        dias_de_servicio           = get_metric(all_events, parking_id, "Días de servicio")
        oferta_servicio_plazas_año = dias_de_servicio  * plazas
        oferta_servicio_horas_año  = dias_de_servicio  * plazas * 24

        operaciones_r = get_metric(all_events, parking_id, "Operaciones Rotación")
        operaciones_a = get_metric(all_events, parking_id, "Operaciones Abonados")
        operaciones_t = operaciones_r + operaciones_a

        horas_r       = get_metric(all_events, parking_id, "Horas Rotación")
        horas_a       = get_metric(all_events, parking_id, "Horas Abonados")
        horas_t       = horas_r + horas_a

        recaudacion_r = get_metric(all_events, parking_id, "Recaudación Rotación")        
        recaudacion_a = get_metric(all_events, parking_id, "Recaudación Abonados")
        recaudacion_t = recaudacion_r + recaudacion_a

        events_calculated.append([parking_id, {
            'Plazas':                         plazas,
            'Operaciones Total':              operaciones_t,
            'Horas Total':                    horas_t,
            'Recaudación Total Estadística':  recaudacion_t,           
            'Recaudación Total Diferencia':   get_metric(all_events, parking_id, 'Recaudación Total Real') - recaudacion_t,
            'Índice Rotación Rotación':       operaciones_r / oferta_servicio_plazas_año, 
            'Índice Rotación Abonados':       operaciones_a / oferta_servicio_plazas_año, 
            'Índice Rotación Total':          operaciones_t / oferta_servicio_plazas_año,
            'Recaudación por plaza Rotación': recaudacion_r / plazas, 
            'Recaudación por plaza Abonados': recaudacion_a / plazas, 
            'Recaudación por plaza Total':    recaudacion_t / plazas, 
            'Índice Ocupación Rotación':      horas_r / oferta_servicio_horas_año, 
            'Índice Ocupación Abonados':      horas_a / oferta_servicio_horas_año, 
            'Índice Ocupación Total':         horas_t / oferta_servicio_horas_año,
            'Permanencia Media Rotación':     horas_r / operaciones_r,      
            'Permanencia Media Abonados':     horas_a / operaciones_a,      
            'Permanencia Media Total':        horas_t / operaciones_t,     
        }])

    return all_events + events_calculated

def get_metric(all_events, parking_id, label):
    for pid, labels_dict in all_events:
        if pid == parking_id and label in labels_dict:
            return labels_dict[label]
    return None
