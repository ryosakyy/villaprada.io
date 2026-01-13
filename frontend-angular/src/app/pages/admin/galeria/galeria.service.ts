import { environment } from '../../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GaleriaService {
  private readonly URL_API = environment.apiUrl + '/galeria';

  constructor(private http: HttpClient) { }

  // Para la página pública (landing) - sin autenticación requerida
  getGaleriaLight(): Observable<any[]> {
    return this.http.get<any[]>(`${this.URL_API}/light-list`);
  }

  // Cambiado de listarGaleria a getGaleria para que coincida con el componente
  getGaleria(): Observable<any[]> {
    return this.http.get<any[]>(`${this.URL_API}/`);
  }

  // Cambiado de buscar a buscarImagenes para que coincida con el componente
  buscarImagenes(texto: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.URL_API}/buscar/${texto}`);
  }

  subirImagen(formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.URL_API}/`, formData);
  }

  eliminar(id: number): Observable<any> {
    return this.http.delete(`${this.URL_API}/${id}`);
  }
}