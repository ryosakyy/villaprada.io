import { environment } from '../../../environments/environment';
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface DisponibilidadPublica {
    fecha: string; // YYYY-MM-DD
    hora_inicio: string | null;
    hora_fin: string | null;
    estado: string;
}

@Injectable({
    providedIn: 'root'
})
export class DisponibilidadService {
    private http = inject(HttpClient);
    private apiUrl = environment.apiUrl;

    getFechasOcupadasPublico(anio?: number, mes?: number): Observable<DisponibilidadPublica[]> {
        let params = new HttpParams();
        if (anio) params = params.set('anio', anio);
        if (mes) params = params.set('mes', mes);

        return this.http.get<DisponibilidadPublica[]>(`${this.apiUrl}/disponibilidad/publico/fechas-ocupadas`, { params });
    }
}
