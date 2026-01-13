import { environment } from '../../../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Usuario {
  id?: number;
  nombres: string;
  email: string;
  rol: string;
  estado?: boolean;
}

@Injectable({ providedIn: 'root' })
export class UsuariosService {
  private apiUrl = environment.apiUrl + '/usuarios/'; 

  constructor(private http: HttpClient) { }

  private getHeaders() {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  listar(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  crear(data: any): Observable<Usuario> {
    return this.http.post<Usuario>(this.apiUrl, data, { headers: this.getHeaders() });
  }

  actualizar(id: number, data: any): Observable<Usuario> {
    return this.http.put<Usuario>(`${this.apiUrl}${id}`, data, { headers: this.getHeaders() });
  }

  eliminar(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}`, { headers: this.getHeaders() });
  }
}