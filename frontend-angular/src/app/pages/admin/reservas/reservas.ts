import { environment } from '../../../../environments/environment';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-reservas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reservas.html',
  styleUrl: './reservas.css'
})
export class Reservas implements OnInit {

  currentDate = new Date();
  displayMonth: string = '';
  daysInMonth: any[] = [];
  userRole: string = ''; // variable para el HTML

  // Datos
  listaContratos: any[] = [];
  listaClientes: any[] = [];

  // Modal
  showModal: boolean = false;
  selectedEvent: any = null;

  // URLs
  apiContratos = environment.apiUrl + '/contratos/';
  apiClientes = environment.apiUrl + '/clientes/';

  nombresMeses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

  constructor(
    private http: HttpClient,
    private router: Router,
    private cd: ChangeDetectorRef,
    private auth: AuthService
  ) { }

  ngOnInit() {
    this.userRole = this.auth.getUserRole(); // Obtenemos el rol
    this.cargarDatosCompletos();
  }

  getHeaders() {
    const token = localStorage.getItem('token');
    return { headers: new HttpHeaders({ 'Authorization': `Bearer ${token}` }) };
  }

  cargarDatosCompletos() {
    this.http.get<any[]>(this.apiClientes, this.getHeaders()).subscribe({
      next: (clientes) => {
        this.listaClientes = clientes;
        this.cargarContratos();
      },
      error: () => {
        console.error("Error cargando clientes, se intentará cargar contratos igual.");
        this.cargarContratos();
      }
    });
  }

  cargarContratos() {
    this.http.get<any[]>(this.apiContratos, this.getHeaders()).subscribe({
      next: (data) => {
        this.listaContratos = Array.isArray(data) ? data : [];
        this.construirCalendario();
        this.cd.detectChanges();
      },
      error: (err) => {
        console.error('Error cargando contratos:', err);
        this.cd.detectChanges();
      }
    });
  }

  // Lógica robusta para obtener nombre del cliente
  private getNombreCliente(c: any): string {
    // 1. Intentar sacar del objeto anidado
    if (c.cliente) {
      return (c.cliente.nombres || c.cliente.nombre || c.cliente.name || '') + ' ' + (c.cliente.apellidos || c.cliente.apellido || '');
    }
    // 2. Si no hay objeto anidado, buscar en la lista de clientes por ID
    if (c.cliente_id && this.listaClientes.length > 0) {
      const found = this.listaClientes.find(cli => cli.id == c.cliente_id);
      if (found) {
        return (found.nombres || found.nombre || found.name || '') + ' ' + (found.apellidos || found.apellido || '');
      }
    }
    return 'Cliente desconocido';
  }

  construirCalendario() {
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    this.displayMonth = `${this.nombresMeses[month]} ${year}`;
    this.daysInMonth = [];

    const firstDay = new Date(year, month, 1);
    let startDayIndex = (firstDay.getDay() + 6) % 7;
    const daysTotal = new Date(year, month + 1, 0).getDate();

    // Días vacíos previos
    for (let i = 0; i < startDayIndex; i++) {
      this.daysInMonth.push({ num: '', eventos: [] });
    }

    // Días del mes
    for (let i = 1; i <= daysTotal; i++) {
      const fechaStr = `${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`;

      const contratosDelDia = this.listaContratos.filter(c => c.fecha_evento === fechaStr);

      const eventosMapeados = contratosDelDia.map(c => {

        // OBTENER NOMBRE
        const nombreCompleto = this.getNombreCliente(c).trim();
        const nombreMostrar = nombreCompleto || "Sin Nombre";

        const total = parseFloat(c.monto_total || 0);
        const adelanto = parseFloat(c.adelanto || 0);
        const deuda = total - adelanto;

        return {
          id: c.id,
          fecha: c.fecha_evento,
          cliente: nombreMostrar, // NOMBRE REAL
          paquete: c.paquete || 'Evento',
          hora_inicio: c.hora_inicio ? c.hora_inicio.substring(0, 5) : '--:--',
          hora_fin: c.hora_fin ? c.hora_fin.substring(0, 5) : '--:--',
          total: total,
          adelanto: adelanto,
          deuda: deuda,
          estado: deuda <= 0 ? 'pagado' : 'pendiente'
        };
      });

      const hoyStr = new Date().toISOString().split('T')[0];
      const esPasado = fechaStr < hoyStr;

      this.daysInMonth.push({
        num: i,
        fechaCompleta: fechaStr,
        eventos: eventosMapeados,
        esPasado: esPasado
      });
    }
  }

  cambiarMes(offset: number) {
    this.currentDate.setMonth(this.currentDate.getMonth() + offset);
    this.construirCalendario();
  }

  abrirModalEvento(evento: any, e: Event) {
    e.stopPropagation();
    this.selectedEvent = evento;
    this.showModal = true;
  }

  cerrarModal() {
    this.showModal = false;
    this.selectedEvent = null;
  }
}