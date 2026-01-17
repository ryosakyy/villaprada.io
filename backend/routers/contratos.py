from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import io
import os
from datetime import date

# Librerías para PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Importaciones de tu proyecto
from core.database import get_db
import models.contratos as models_contratos
import schemas.contratos as schemas

router = APIRouter(prefix="/contratos", tags=["Contratos"])

# --- FUNCIÓN AUXILIAR: Fecha en Español ---
def fecha_espanol(fecha: date):
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    return f"{fecha.day} de {meses[fecha.month]} de {fecha.year}"

# --- ENDPOINTS CRUD ---

@router.get("/", response_model=List[schemas.ContratoResponse])
def listar_contratos(db: Session = Depends(get_db)):
    return db.query(models_contratos.Contrato).all()

@router.post("/", response_model=schemas.ContratoResponse, status_code=status.HTTP_201_CREATED)
def crear_contrato(contrato: schemas.ContratoCreate, db: Session = Depends(get_db)):
    # --- CAMBIO IMPORTANTE ---
    # Se eliminó la validación "if existente". 
    # Ahora permite crear múltiples contratos el mismo día.
    
    nuevo_contrato = models_contratos.Contrato(**contrato.dict())
    db.add(nuevo_contrato)
    db.commit()
    db.refresh(nuevo_contrato)
    return nuevo_contrato

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_contrato(id: int, db: Session = Depends(get_db)):
    contrato = db.query(models_contratos.Contrato).filter(models_contratos.Contrato.id == id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

    # --- CASCADE DELETE MANUAL ---
    # 1. Eliminar Pagos asociados
    from models.pagos import Pago
    db.query(Pago).filter(Pago.contrato_id == id).delete()

    # 2. Desvincular o Eliminar Egresos asociados
    # (En este caso eliminamos la asociación o el egreso completo si es específico del evento. 
    #  Para evitar dejar basura, los eliminamos si están ligados estrictamente al contrato)
    from models.egresos import Egreso
    db.query(Egreso).filter(Egreso.contrato_id == id).delete()

    # 3. Eliminar el contrato
    db.delete(contrato)
    db.commit()
    return None

# --- ENDPOINT GENERAR PDF ---
@router.get("/{id}/pdf")
def descargar_pdf_contrato(id: int, db: Session = Depends(get_db)):
    # 1. Obtener datos
    contrato = db.query(models_contratos.Contrato).filter(models_contratos.Contrato.id == id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

    # Manejo seguro de nombres/apellidos
    nom_cliente = "CLIENTE NO REGISTRADO"
    dni_cliente = "S/N"
    
    if contrato.cliente:
        c_nom = getattr(contrato.cliente, 'nombre', getattr(contrato.cliente, 'nombres', ''))
        c_ape = getattr(contrato.cliente, 'apellido', getattr(contrato.cliente, 'apellidos', ''))
        
        nom_cliente = f"{c_nom} {c_ape}".strip().upper()
        dni_cliente = getattr(contrato.cliente, 'dni', 'S/N')

    # Cálculos Matemáticos
    total = contrato.monto_total
    adelanto = contrato.adelanto
    
    # Nuevo cálculo: Porcentajes sobre el SALDO (Total - Adelanto)
    saldo_pendiente = total - adelanto
    monto_80 = saldo_pendiente * 0.80
    monto_20 = saldo_pendiente * 0.20

    # 2. Configurar PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    # --- LOGO Y ENCABEZADO ---
    logo_path = "static/logo.png"
    if os.path.exists(logo_path):
        try:
            # Dibujar logo (ajusta tamaño y posición) - BAJADO 1.5 cm
            c.drawImage(logo_path, 2.5*cm, h - 5.0*cm, width=2.5*cm, preserveAspectRatio=True, mask='auto')
        except:
            pass

    c.setFont("Times-Bold", 14)
    # Movemos el título un poco a la derecha/abajo si hay logo - BAJADO 1.5 cm
    c.drawCentredString(w/2 + 1*cm, h - 4.0*cm, "CONTRATO DE PRESTACIÓN DE")
    c.drawCentredString(w/2 + 1*cm, h - 4.7*cm, "SERVICIOS DE PRODUCCIÓN DE EVENTO")

    # --- TEXTO PRINCIPAL ---
    c.setFont("Times-Roman", 11)
    texto_inicio = c.beginText(2.5*cm, h - 6.5*cm)
    texto_inicio.setLeading(14)

    intro = f"""
Conste por el presente documento el contrato de prestación de servicios que celebran de
una parte SALÓN DE EVENTOS VILLA PRADA, con RUC N.° 20608255738,
representado por John Grober Orosco Prada, identificado con DNI N.° 44353304, a
quien en adelante se le denominará EL PRESTADOR; y de la otra parte el Sr./Sra.
{nom_cliente}, identificado con DNI N.° {dni_cliente}, a quien en adelante se le
denominará EL CLIENTE; bajo las siguientes cláusulas:
    """
    for linea in intro.split('\n'):
        texto_inicio.textLine(linea.strip())
    c.drawText(texto_inicio)

    # --- PRIMERA: OBJETO ---
    y = h - 12*cm  # BAJADO de 9cm a 12cm para evitar superposición
    c.setFont("Times-Bold", 11)
    c.drawString(2.5*cm, y, "PRIMERA: OBJETO DEL CONTRATO")
    
    y -= 0.7*cm
    c.setFont("Times-Roman", 11)
    c.drawString(2.5*cm, y, "El PRESTADOR se compromete a brindar el servicio integral de producción del evento")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, f"denominado '{contrato.paquete}' para EL CLIENTE, conforme a la propuesta")
    y -= 0.5*cm
    c.drawString(2.5*cm, y, f"aceptada para la fecha: {fecha_espanol(contrato.fecha_evento)}.")

    # --- SEGUNDA: MONTO Y PAGO ---
    y -= 1.5*cm
    c.setFont("Times-Bold", 11)
    c.drawString(2.5*cm, y, "SEGUNDA: MONTO Y FORMA DE PAGO")
    
    y -= 0.7*cm
    c.setFont("Times-Roman", 11)
    c.drawString(2.5*cm, y, f"El monto total por los servicios contratados asciende a la suma de S/ {total:,.2f}.")
    y -= 0.7*cm
    c.drawString(2.5*cm, y, "El pago se efectuará de la siguiente manera:")

    y -= 0.8*cm
    c.drawString(3*cm, y, f"•  S/ {adelanto:,.2f} entregados en calidad de adelanto para la separación de la fecha.")
    y -= 0.6*cm
    c.drawString(3*cm, y, f"•  80% del saldo (S/ {monto_80:,.2f}) deberá ser cancelado antes del evento.")
    y -= 0.6*cm
    c.drawString(3*cm, y, f"•  20% restante del saldo (S/ {monto_20:,.2f}) será cancelado el mismo día del evento.")

    # --- TERCERA: SERVICIOS ---
    y -= 1.5*cm
    c.setFont("Times-Bold", 11)
    c.drawString(2.5*cm, y, "TERCERA: SERVICIOS INCLUIDOS")
    y -= 0.7*cm
    c.setFont("Times-Roman", 11)
    c.drawString(2.5*cm, y, "Los servicios incluyen, de manera enunciativa y no limitativa:")
    y -= 0.7*cm
    c.drawString(3*cm, y, f"•  Producción integral del evento: {contrato.paquete}")

    # --- FIRMAS ---
    y_firma = 3*cm
    c.setLineWidth(1)

    c.line(2.5*cm, y_firma, 8.5*cm, y_firma)
    c.setFont("Times-Roman", 10)
    c.drawCentredString(5.5*cm, y_firma - 0.5*cm, "John Grober Orosco Prada")
    c.drawCentredString(5.5*cm, y_firma - 1.0*cm, "VILLA PRADA (EL PRESTADOR)")

    c.line(11.5*cm, y_firma, 17.5*cm, y_firma)
    c.drawCentredString(14.5*cm, y_firma - 0.5*cm, nom_cliente)
    c.drawCentredString(14.5*cm, y_firma - 1.0*cm, f"DNI: {dni_cliente}")
    c.drawCentredString(14.5*cm, y_firma - 1.5*cm, "(EL CLIENTE)")

    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer, 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Contrato_VP_{id}.pdf"}
    )