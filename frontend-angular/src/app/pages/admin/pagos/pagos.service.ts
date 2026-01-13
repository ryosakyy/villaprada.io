import { environment } from '../../../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Pago {
  id: number;
  contrato_id: number;
  fecha_pago: string;
  monto: number;
  metodo: string;
  observacion?: string;
  comprobante_url?: string; // Nuevo campo
}

// Mantenemos la interfaz base para el formulario, pero enviaremos FormData
export interface PagoCreate {
  contrato_id: number;
  fecha_pago: string;
  monto: number;
  metodo: string;
  observacion?: string;
}

export interface PagoResumen {
  contrato_id: number;
  monto_total: number;
  total_pagado: number;
  saldo: number;
  estado: string;
}

@Injectable({
  providedIn: 'root'
})
export class PagosService {

  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  private getHeaders() {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({ 'Authorization': `Bearer ${token}` })
    };
  }

  // 1. Obtener lista de contratos
  obtenerListaContratos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/contratos/`, this.getHeaders());
  }

  // 2. Obtener Resumen Financiero
  obtenerResumen(contratoId: number): Observable<PagoResumen> {
    return this.http.get<PagoResumen>(`${this.baseUrl}/pagos/resumen/${contratoId}`, this.getHeaders());
  }

  // 3. Obtener Lista de Pagos por Contrato
  listarPagosPorContrato(contratoId: number): Observable<Pago[]> {
    return this.http.get<Pago[]>(`${this.baseUrl}/pagos/contrato/${contratoId}`, this.getHeaders());
  }

  // 3.5 Obtener TODOS los pagos (Para el Dashboard)
  obtenerTodosLosPagos(): Observable<Pago[]> {
    return this.http.get<Pago[]>(`${this.baseUrl}/pagos/`, this.getHeaders());
  }

  // 4. Registrar Pago (AHORA RECIBE FORM DATA)
  crearPago(datos: FormData): Observable<any> {
    // Angular maneja el Content-Type multipart automáticamente cuando ve FormData
    return this.http.post(`${this.baseUrl}/pagos/`, datos, this.getHeaders());
  }

  // 5. Eliminar Pago
  eliminarPago(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/pagos/${id}`, this.getHeaders());
  }
}