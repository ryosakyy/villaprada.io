import { environment } from '../../../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Paquete {
  id?: number;
  nombre: string;
  descripcion?: string;
  precio: number;
  capacidad: number;
  servicios?: string;
  estado?: string;
}

@Injectable({ providedIn: 'root' })
export class PaqueteDataService {
  private apiUrl = environment.apiUrl + '/paquetes/';

  constructor(private http: HttpClient) { }

  private getHeaders() {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({ 'Authorization': `Bearer ${token}` });
  }

  listar(): Observable<Paquete[]> {
    return this.http.get<Paquete[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  crear(data: Paquete): Observable<Paquete> {
    return this.http.post<Paquete>(this.apiUrl, data, { headers: this.getHeaders() });
  }

  actualizar(id: number, data: any): Observable<Paquete> {
    return this.http.put<Paquete>(`${this.apiUrl}${id}`, data, { headers: this.getHeaders() });
  }

  eliminar(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}`, { headers: this.getHeaders() });
  }
}