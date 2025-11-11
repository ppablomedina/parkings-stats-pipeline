import pandas as pd
from gcp_paths import path_informes_filtrados
from gcp_utils import read, parkings_current_info


def main():

    events = []

    for parking_name, [parking_id, _, _, parking_norm] in parkings_current_info.items():

        ss = path_informes_filtrados.replace('&', parking_norm)

        lines = get_lines(ss)

        pasos_apertura_manual, apertura_manual, apertura_permanente = get_informe_aperturas(lines)

        recaudacion_r, recaudacion_a, operaciones_r, operaciones_a  = get_recaudacion_y_operaciones(lines, parking_name)

        events.append([parking_id, {
            'Pasos apertura manual': pasos_apertura_manual,
            'Apertura manual':       apertura_manual,
            'Apertura permanente':   apertura_permanente,
            'Recaudación Rotación':  recaudacion_r,
            'Recaudación Abonados':  recaudacion_a,
            'Operaciones Rotación':  operaciones_r,
            'Operaciones Abonados':  operaciones_a
        }])

    return events

def get_indices_de_secciones(documnet_lines, titulo, subtitulo, hasta=None, es_para_salidas=False):
    """
    documnet_lines: todas las líneas del informe
    titulo: título de la sección
    subtitulo: subtítulo de la sección
    hasta: lista de palabras que detienen la búsqueda
    es_para_salidas: si es para obtener las salidas, no pone total ni todos al final, por lo que cuando pongan esos valores acaba

    """

    lines = []

    i_init = None

    for i in range(len(documnet_lines)):
        if titulo in documnet_lines[i]:
            for j in range(i+1, len(documnet_lines)):
                if subtitulo in documnet_lines[j]:
                    i_init = j+1
                    break
            break

    for i in range(i_init, len(documnet_lines)):

        if   titulo in documnet_lines[i]: continue
        elif subtitulo in documnet_lines[i]: continue

        if hasta != None:
            if any([h in documnet_lines[i] for h in hasta]): break

        lines.append(documnet_lines[i])

        if es_para_salidas:
            if len(documnet_lines[i].split(' ')) == 3: break

        if 'Total' in documnet_lines[i] or 'Todos' in documnet_lines[i]: break

    return lines

def get_informe_indices(lineas):

    lines = get_indices_de_secciones(lineas, 'Informe de índices: To', 'Circulación con', es_para_salidas=True)

    ticket_aparc_limitado = 0
    ticket_por_extravio = 0
    ta_perm = 0
    ta_perm_renov = 0
    ab_perm = 0

    total = int(lines[-1].split(' ')[-2])

    for line in lines:
        if   'TA. Permanente renov.'  in line:                             ta_perm_renov         += int(line.split(' ')[-2])
        elif 'TA.Permanente'          in line or 'TA. Permanente' in line: ta_perm               += int(line.split(' ')[-2])
        elif 'Ab. Permanente'         in line:                             ab_perm               += int(line.split(' ')[-2])
        elif 'Ticket Aparc. Limitado' in line:                             ticket_aparc_limitado += int(line.split(' ')[-2])
        elif 'Ticket por Extravío'    in line:                             ticket_por_extravio   += int(line.split(' ')[-2])

    return ticket_por_extravio, ticket_aparc_limitado, ta_perm, ta_perm_renov, ab_perm, total

def get_informe_ventas(lineas, parking):
    
    lines = get_indices_de_secciones(lineas, 'Informe de Ventas: To', 'Artículos')
    recaudacion_tickets_rotacion = 0

    if parking != 'rincon':
        for line in lines:
            if 'ticket por extrav' in line.lower():
                recaudacion_tickets_rotacion += str_to_float(line.split(' ')[-2])
                break

    else:
        for line in lines:
            if 'bono guagua' in line.lower():
                recaudacion_tickets_rotacion += str_to_float(line.split(' ')[-2])
            elif 'prepago 24h' in line.lower():
                recaudacion_tickets_rotacion += str_to_float(line.split(' ')[-2])

    total = str_to_float(lines[-1].split(' ')[-2])

    return recaudacion_tickets_rotacion, total

def get_informe_aperturas(lineas):

    document_lines = get_indices_de_secciones(lineas, 'Informe de índices: To', 'Nombre', ['Circulación con'])

    aperturas = {
        'Paso por apertura manual':           'Pasos apertura manual',
        'Pasos c/apertura permanente/manual': 'Pasos apertura manual',

        'Barrera con apertura manual':        'Apertura manual',
        'Apertura manual':                    'Apertura manual',

        'Apertura Permanente':                'Apertura permanente'
    }
    
    data = []

    for line in document_lines:
        for key, nombre in aperturas.items():
            if key in line:
                ocasiones = encontrar_el_numero(line)
                data.append({'Nombre': nombre, 'Ocasiones': ocasiones})
                break
    
    df = pd.DataFrame(data)

    if len(df) != 3:
        estan = set([d['Nombre'] for d in data])
        faltan = set(aperturas.values()) - estan
        print(f"ERROR: faltan las aperturas {faltan}")

    return [
        int(df.loc[df['Nombre'] == 'Pasos apertura manual', 'Ocasiones'].iloc[0]), 
        int(df.loc[df['Nombre'] == 'Apertura manual',       'Ocasiones'].iloc[0]), 
        int(df.loc[df['Nombre'] == 'Apertura permanente',   'Ocasiones'].iloc[0])
    ]

def get_recaudacion_y_operaciones(lineas, parking):

    """                                       RECAUDACIÓN                                       """
    transacciones_con_importe = str_to_float(lineas[2].split(' ')[-2])

    recaudacion_tickets_rotacion, total_ventas = get_informe_ventas(lineas, parking) 

    recaudacion_r = transacciones_con_importe + recaudacion_tickets_rotacion
    
    recaudacion_a = total_ventas - recaudacion_tickets_rotacion

    """                                       OPERACIONES                                       """

    _, _, ta_perm, ta_perm_renov, ab_perm, total = get_informe_indices(lineas)

    operaciones_a = ta_perm + ta_perm_renov + ab_perm
    
    operaciones_r = total - operaciones_a

    return recaudacion_r, recaudacion_a, operaciones_r, operaciones_a

def get_lines(path):
    pdf_reader = read(path, 'pdf')
    text = ""
    for page in pdf_reader.pages: 
        lineas = page.extract_text()
        lineas = lineas.split('\n')[2:-2]
        text += '\n'.join(lineas) + '\n'
    return text.split('\n')

def str_to_float(txt):
    return float(txt.replace('.', '').replace(',', '.'))

def encontrar_el_numero(line):
    line = line.split(' ')
    for i in range(len(line)):
        if line[i].isdigit():
            return line[i]
