import { environment } from '../../../../environments/environment';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { PagosService } from '../pagos/pagos.service';
import { EgresosService } from '../egresos/egresos.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {

  private http = inject(HttpClient);
  private pagosService = inject(PagosService);
  private egresosService = inject(EgresosService);
  private cd = inject(ChangeDetectorRef);

  totalClientes = 0;
  totalContratos = 0;
  totalIngresos = 0;
  totalEgresos = 0;

  reservasPorDia: any[] = [];

  ngOnInit() {
    this.cargarKPIs();
  }

  cargarKPIs() {
    // 1. Clientes (No tenemos servicio, usamos http directo)
    // El interceptor pone el token
    this.http.get<any[]>(environment.apiUrl + '/clientes/').subscribe({
      next: (data) => {
        this.totalClientes = data.length;
        this.cd.detectChanges();
      }
    });

    // 2. Contratos (Usamos service de Pagos que ya lo tiene)
    this.pagosService.obtenerListaContratos().subscribe({
      next: (data) => {
        this.totalContratos = data.length;
        this.calcularReservas(data);
        this.cd.detectChanges();
      }
    });

    // 3. Ingresos (Todos los pagos)
    this.pagosService.obtenerTodosLosPagos().subscribe({
      next: (data) => {
        this.totalIngresos = data.reduce((acc, p) => acc + (p.monto || 0), 0);
        this.cd.detectChanges();
      }
    });

    // 4. Egresos
    this.egresosService.listarEgresos().subscribe({
      next: (data) => {
        this.totalEgresos = data.reduce((acc, e) => acc + (e.monto || 0), 0);
        this.cd.detectChanges();
      }
    });
  }

  calcularReservas(contratos: any[]) {
    const map: { [key: string]: number } = {};

    // Contar por fecha
    contratos.forEach(c => {
      if (c.fecha_evento) {
        map[c.fecha_evento] = (map[c.fecha_evento] || 0) + 1;
      }
    });

    // Convertir a array y ordenar
    this.reservasPorDia = Object.keys(map)
      .map(fecha => ({ fecha, cantidad: map[fecha] }))
      // Ordenar por fecha ascendente
      .sort((a, b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime())
      // Mostrar solo las próximas (o las últimas 5 si prefieres)
      // Vamos a mostrar las 5 más recientes/próximas
      .filter(item => new Date(item.fecha) >= new Date(new Date().setHours(0, 0, 0, 0))) // Solo futuras o hoy
      .slice(0, 5);
  }

  get balance() {
    return this.totalIngresos - this.totalEgresos;
  }
}

