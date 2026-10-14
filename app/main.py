from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.log_utils import get_daily_logger
from app.client_utils import dequeue_action, enqueue_action, get_client_data, update_client_data, update_client_user_data

logger = get_daily_logger()

app = FastAPI(
    title="Recolector y distribuidor de eventos de sistemas de domótica",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/notify")
async def dompi_cloud_notify_post(request: Request):
    # Leer el POST
    form = await request.form()   # ← parsea x-www-form-urlencoded
    data = dict(form)

    # Campos generales
    system = data.get("System_Key", None)
    estado = data.get("Estado", None)
 
    # Campos de Assign
    ass_id = data.get("ASS_Id", None)
    objeto = data.get("Objeto", None)
    tipo = data.get("Tipo", None)
    icono_apagado = data.get("Icono_Apagado", None)
    icono_encendido = data.get("Icono_Encendido", None)
    grupo_visual = data.get("Grupo_Visual", None)
    planta = data.get("Planta", None)
    cord_x = data.get("Cord_x", None)
    cord_y = data.get("Cord_y", None)
    coeficiente = data.get("Coeficiente", None)
    analog_mult_div = data.get("Analog_Mult_Div", None)
    analog_mult_div_valor = data.get("Analog_Mult_Div_Valor", None)
    flags = data.get("Flags", None)

    # Campos de usuarios
    user_id = data.get("User_Id", None)
    clave = data.get("Clave", None)
    amazon_key = data.get("Amazon_Key", None)
    google_key = data.get("Google_Key", None)
    apple_key = data.get("Apple_Key", None)
    other_key = data.get("Other_Key", None)

    if system != None:
        if ass_id != None:
            update_client_data(system, ass_id, objeto, tipo, estado, icono_apagado, icono_encendido, grupo_visual, planta, cord_x, cord_y, coeficiente, analog_mult_div, analog_mult_div_valor, flags)
        elif user_id != None and clave != None:
            update_client_user_data(user_id, clave, system, amazon_key, google_key, apple_key, other_key, estado)
        else:
            update_client_data(system)
    else:
        logger.info(f"[dompi_cloud_notify_post] No se pudo obtener el System_Key [{data}]")

    return dequeue_action(system)
