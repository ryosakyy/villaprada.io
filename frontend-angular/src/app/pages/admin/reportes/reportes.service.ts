import { environment } from '../../../../environments/environment';
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ReportesService {

    private http = inject(HttpClient);
    private apiUrl = environment.apiUrl + '/reportes';

    constructor() { }

    private getHeaders() {
        const token = localStorage.getItem('access_token');
        return new HttpHeaders({
            'Authorization': `Bearer ${token}`
        });
    }

    // 1. Obtener datos financieros (JSON)
    getReporteFinanzas(inicio: string, fin: string): Observable<any[]> {
        const params = new HttpParams()
            .set('inicio', inicio)
            .set('fin', fin);

        return this.http.get<any[]>(`${this.apiUrl}/finanzas`, {
            headers: this.getHeaders(),
            params
        });
    }

    // 2. Descargar Ingresos (Excel)
    downloadIngresosExcel(inicio: string, fin: string): Observable<Blob> {
        const params = new HttpParams()
            .set('fecha_inicio', inicio)
            .set('fecha_fin', fin);

        return this.http.get(`${this.apiUrl}/ingresos/excel`, {
            headers: this.getHeaders(),
            params,
            responseType: 'blob'
        });
    }

    // 3. Descargar Egresos (Excel)
    downloadEgresosExcel(inicio: string, fin: string): Observable<Blob> {
        const params = new HttpParams()
            .set('fecha_inicio', inicio)
            .set('fecha_fin', fin);

        return this.http.get(`${this.apiUrl}/egresos/excel`, {
            headers: this.getHeaders(),
            params,
            responseType: 'blob'
        });
    }

    // 4. Descargar Contratos (Excel)
    downloadContratosExcel(inicio: string, fin: string): Observable<Blob> {
        const params = new HttpParams()
            .set('fecha_inicio', inicio)
            .set('fecha_fin', fin);

        return this.http.get(`${this.apiUrl}/contratos/excel`, {
            headers: this.getHeaders(),
            params,
            responseType: 'blob'
        });
    }

    // 5. Descargar Flujo de Caja (PDF)
    downloadFlujoCajaPDF(inicio: string, fin: string): Observable<Blob> {
        const params = new HttpParams()
            .set('fecha_inicio', inicio)
            .set('fecha_fin', fin);

        return this.http.get(`${this.apiUrl}/flujo-caja/pdf`, {
            headers: this.getHeaders(),
            params,
            responseType: 'blob'
        });
    }
}
