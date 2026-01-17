import { environment } from '../../../environments/environment';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

const API_URL = environment.apiUrl; // Sincronizado con tu puerto de FastAPI

export interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: {
    id: number;
    nombres: string;
    email: string;
    rol: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);

  // 1. LOGIN (Corregido a JSON estándar)
  login(email: string, pass: string): Observable<LoginResponse> {
    const url = `${API_URL}/usuarios/login`;

    // Enviamos como JSON (más robusto)
    return this.http.post<LoginResponse>(url, { email, password: pass });
  }

  // 2. GUARDAR SESIÓN
  saveSession(data: LoginResponse) {
    if (data && data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('usuario', JSON.stringify(data.usuario));
    }
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getUser(): any {
    const usuario = localStorage.getItem('usuario');
    return usuario ? JSON.parse(usuario) : null;
  }

  getUserRole(): string {
    const user = this.getUser();
    return user && user.rol ? user.rol.toLowerCase() : '';
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  logout() {
    localStorage.clear();
    window.location.href = '/auth/login';
  }

  perfil(): Observable<any> {
    return this.http.get(`${API_URL}/usuarios/perfil`);
  }
}