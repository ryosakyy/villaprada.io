import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const API = environment.apiUrl;

export interface Cliente {
  id: number;
  dni: string;
  nombre: string;
  telefono?: string | null;
  correo?: string | null;
  direccion?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class ClientesService {

  constructor(private http: HttpClient) {}

  // GET /clientes (PROTEGIDO)
  listar(): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${API}/clientes/`);
  }

  // POST /clientes
  crear(data: Partial<Cliente>): Observable<Cliente> {
    return this.http.post<Cliente>(`${API}/clientes/`, data);
  }

  // PUT /clientes/{id}
  actualizar(id: number, data: Partial<Cliente>): Observable<Cliente> {
    return this.http.put<Cliente>(`${API}/clientes/${id}`, data);
  }

  // DELETE /clientes/{id}
  eliminar(id: number): Observable<any> {
    return this.http.delete(`${API}/clientes/${id}`);
  }
}
