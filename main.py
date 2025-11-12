# main.py
from flask import Flask, request, jsonify

import processes.ocupacion
import processes.abonados_en_banco
import processes.abonados_lpa_y_qr
import processes.recaudacion
import processes.rincon_estadisticas
import processes.abonados_y_rotacion
import processes.informes_filtrados
import processes.ratios

from gcp.utils import insert_events

app = Flask(__name__)  # <-- ESTO es lo que Gunicorn importa (main:app)


def run_etl():
    modules = [
        processes.ocupacion,
        processes.abonados_en_banco,
        processes.recaudacion,
        processes.rincon_estadisticas,
        processes.abonados_lpa_y_qr,
        processes.informes_filtrados,
        processes.abonados_y_rotacion,
    ]

    all_events = []
    for module in modules:
        feeds = module.main()
        # Por si algún módulo devuelve None
        if feeds:
            all_events.extend(feeds)

    insert_events(processes.ratios.main(all_events))
    return "ETL ejecutado correctamente\n", 200


# Mantengo tu firma por compatibilidad con Cloud Functions (opcional)
def entry_point(_request):
    msg, code = run_etl()
    return msg, code


# --- Rutas HTTP para Cloud Run / cualquier contenedor web ---
@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/", methods=["GET", "POST"])
@app.route("/run", methods=["GET", "POST"])
def run_route():
    msg, code = run_etl()
    # Si quieres JSON:
    # return jsonify(message=msg.strip()), code
    return msg, code


if __name__ == "__main__":
    # Útil para correr localmente sin Gunicorn: python main.py
    app.run(host="0.0.0.0", port=8080)
