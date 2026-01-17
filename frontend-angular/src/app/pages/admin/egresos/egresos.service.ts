import { environment } from '../../../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Egreso {
  id: number;
  descripcion: string;
  monto: number;
  categoria: string;
  fecha: string;
  observacion?: string;
  contrato_id?: number;
  comprobante_url?: string; // Nuevo campo para la imagen

  // Campos para mostrar quién registró el egreso
  usuario_id?: number;
  usuario_nombre?: string;
  usuario_rol?: string;
}

// Para crear, usamos una interfaz base, pero el envío será via FormData
export interface EgresoCreate {
  descripcion: string;
  categoria: string;
  monto: number;
  fecha: string;
  observacion: string;
  contrato_id: number | null;
}

@Injectable({
  providedIn: 'root'
})
export class EgresosService {
  // Asegúrate de que este puerto coincida con tu backend (8000)
  private apiUrl = environment.apiUrl + '/egresos/';
  private apiContratos = environment.apiUrl + '/contratos/';

  constructor(private http: HttpClient) { }

  private getHeaders() {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({ 'Authorization': `Bearer ${token}` })
    };
  }

  listarEgresos(): Observable<Egreso[]> {
    return this.http.get<Egreso[]>(this.apiUrl, this.getHeaders());
  }

  // CAMBIO PRINCIPAL: Recibe FormData en lugar de JSON simple
  crearEgreso(datos: FormData): Observable<any> {
    return this.http.post(this.apiUrl, datos, this.getHeaders());
  }

  eliminarEgreso(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}`, this.getHeaders());
  }

  listarContratos(): Observable<any[]> {
    return this.http.get<any[]>(this.apiContratos, this.getHeaders());
  }
}