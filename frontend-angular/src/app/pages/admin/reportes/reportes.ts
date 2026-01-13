import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ReportesService } from './reportes.service';
import { timeout, catchError, finalize } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-reportes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reportes.html',
  styleUrl: './reportes.css',
})
export class Reportes implements OnInit {

  private reportesService = inject(ReportesService);
  private cd = inject(ChangeDetectorRef);

  fechaInicio: string = '';
  fechaFin: string = '';

  datosFinanzas: any[] = [];
  cargando: boolean = false;

  totalIngresos = 0;
  totalEgresos = 0;
  totalSaldo = 0;

  ngOnInit() {
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth();

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    this.fechaInicio = firstDay.toISOString().split('T')[0];
    this.fechaFin = lastDay.toISOString().split('T')[0];

    // NO cargar automáticamente, esperar a que el usuario haga clic
  }

  generarReporteVisual() {
    if (!this.validarFechas()) return;

    console.log('[REPORTES] Iniciando consulta:', this.fechaInicio, 'a', this.fechaFin);
    this.cargando = true;

    this.reportesService.getReporteFinanzas(this.fechaInicio, this.fechaFin)
      .pipe(
        timeout(15000),
        catchError(err => {
          console.error('[REPORTES] Error completo:', err);
          if (err.name === 'TimeoutError') {
            alert('⏱️ La solicitud tardó más de 15 segundos. Verifique que el servidor esté corriendo.');
          } else if (err.status === 401) {
            alert('🔒 No autorizado. Por favor, inicie sesión nuevamente.');
          } else if (err.status === 0) {
            alert('❌ No se puede conectar al servidor. Verifique que el backend esté corriendo en el puerto 8000.');
          } else {
            alert('❌ Error: ' + (err.error?.detail || err.message || JSON.stringify(err)));
          }
          return of([]);
        }),
        finalize(() => {
          console.log('[REPORTES] Finalizando request...');
          this.cargando = false;
          this.cd.detectChanges(); // Forzar detección de cambios
          console.log('[REPORTES] Estado cargando:', this.cargando);
        })
      )
      .subscribe({
        next: (data) => {
          console.log('[REPORTES] ✅ Datos recibidos:', data);
          this.datosFinanzas = data;
          this.calcularTotales();
        }
      });
  }

  calcularTotales() {
    this.totalIngresos = this.datosFinanzas.reduce((acc, item) => acc + item.ingresos, 0);
    this.totalEgresos = this.datosFinanzas.reduce((acc, item) => acc + item.egresos, 0);
    this.totalSaldo = this.totalIngresos - this.totalEgresos;
    console.log('[REPORTES] Totales calculados - Ingresos:', this.totalIngresos, 'Egresos:', this.totalEgresos);
  }

  // --- DESCARGAS ---

  descargarExcelIngresos() {
    if (!this.validarFechas()) return;
    this.reportesService.downloadIngresosExcel(this.fechaInicio, this.fechaFin).subscribe({
      next: (blob) => this.downloadFile(blob, `Ingresos_${this.fechaInicio}_${this.fechaFin}.xlsx`),
      error: () => alert('Error descargando Excel Ingresos')
    });
  }

  descargarExcelEgresos() {
    if (!this.validarFechas()) return;
    this.reportesService.downloadEgresosExcel(this.fechaInicio, this.fechaFin).subscribe({
      next: (blob) => this.downloadFile(blob, `Egresos_${this.fechaInicio}_${this.fechaFin}.xlsx`),
      error: () => alert('Error descargando Excel Egresos')
    });
  }

  descargarExcelContratos() {
    if (!this.validarFechas()) return;
    this.reportesService.downloadContratosExcel(this.fechaInicio, this.fechaFin).subscribe({
      next: (blob) => this.downloadFile(blob, `Contratos_${this.fechaInicio}_${this.fechaFin}.xlsx`),
      error: () => alert('Error descargando Excel Contratos')
    });
  }

  descargarPDFFlujo() {
    if (!this.validarFechas()) return;
    this.reportesService.downloadFlujoCajaPDF(this.fechaInicio, this.fechaFin).subscribe({
      next: (blob) => this.downloadFile(blob, `FlujoCaja_${this.fechaInicio}_${this.fechaFin}.pdf`),
      error: () => alert('Error descargando PDF Flujo Caja')
    });
  }

  // --- HELPERS ---

  private validarFechas(): boolean {
    if (!this.fechaInicio || !this.fechaFin) {
      alert('Seleccione un rango de fechas válido');
      return false;
    }
    if (this.fechaFin < this.fechaInicio) {
      alert('La fecha fin no puede ser menor a la fecha inicio');
      return false;
    }
    return true;
  }

  private downloadFile(blob: Blob, fileName: string) {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    link.click();
    window.URL.revokeObjectURL(url);
  }
}
