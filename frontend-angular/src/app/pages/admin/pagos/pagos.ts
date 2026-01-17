import { environment } from '../../../../environments/environment';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Pago, PagoCreate, PagoResumen, PagosService } from './pagos.service';

@Component({
  selector: 'app-pagos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './pagos.html',
  styleUrls: ['./pagos.css']
})
export class Pagos implements OnInit {

  listaContratos: any[] = [];
  listaClientes: any[] = [];
  listaPagos: Pago[] = [];
  resumen: PagoResumen | null = null;

  cargando: boolean = false;

  // Paginación
  paginaActual: number = 1;
  pageSize: number = 10;
  pagosPaginados: Pago[] = [];

  apiClientes = environment.apiUrl + '/clientes/';
  apiUrl = environment.apiUrl;

  nuevoPago: PagoCreate = {
    contrato_id: 0,
    fecha_pago: new Date().toISOString().split('T')[0],
    monto: 0,
    metodo: 'Efectivo',
    observacion: ''
  };

  archivoSeleccionado: File | null = null;

  constructor(
    private pagosService: PagosService,
    private http: HttpClient,
    private route: ActivatedRoute,
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.cargarDatosCompletos();

    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.nuevoPago.contrato_id = +idParam;
      setTimeout(() => this.alSeleccionarContrato(), 500);
    }
  }

  getHeaders() {
    const token = localStorage.getItem('token');
    return { headers: new HttpHeaders({ 'Authorization': `Bearer ${token}` }) };
  }

  cargarDatosCompletos() {
    this.http.get<any[]>(this.apiClientes, this.getHeaders()).subscribe({
      next: (clientes) => {
        this.listaClientes = clientes;
        this.cargarListaContratos();
      },
      error: () => {
        console.error("No se pudieron cargar clientes, cargando contratos igual...");
        this.cargarListaContratos();
      }
    });
  }

  cargarListaContratos() {
    this.pagosService.obtenerListaContratos().subscribe({
      next: (data) => {
        this.listaContratos = data;
        this.listaContratosFiltrados = data; // Inicializar filtrados
        this.cd.detectChanges();
      },
      error: (e) => console.error('Error cargando contratos:', e)
    });
  }

  // --- FILTRO DE CONTRATOS ---
  textoBusqueda: string = '';
  listaContratosFiltrados: any[] = [];

  buscarContrato() {
    const term = this.textoBusqueda.toLowerCase();
    if (!term) {
      this.listaContratosFiltrados = this.listaContratos;
    } else {
      this.listaContratosFiltrados = this.listaContratos.filter(c => {
        const nombreCliente = this.getNombreCliente(c).toLowerCase();
        const id = c.id.toString();
        // Buscar por nombre o ID
        return nombreCliente.includes(term) || id.includes(term);
      });
    }
  }

  getNombreCliente(c: any): string {
    if (c.cliente && typeof c.cliente === 'object') {
      return (c.cliente.nombres || c.cliente.nombre || '') + ' ' + (c.cliente.apellidos || c.cliente.apellido || '');
    }
    if (c.cliente_id && this.listaClientes.length > 0) {
      const found = this.listaClientes.find(cli => cli.id == c.cliente_id);
      if (found) {
        return (found.nombres || found.nombre || '') + ' ' + (found.apellidos || found.apellido || '');
      }
    }
    return c.cliente_nombre || 'Cliente Desconocido';
  }

  alSeleccionarContrato() {
    const id = this.nuevoPago.contrato_id;

    if (!id || id == 0) {
      this.resumen = null;
      this.listaPagos = [];
      return;
    }

    this.cargando = true;

    // A. Resumen
    this.pagosService.obtenerResumen(id).subscribe({
      next: (res) => this.resumen = res,
      error: (e) => console.error('Error resumen:', e)
    });

    // B. Historial
    this.pagosService.listarPagosPorContrato(id).subscribe({
      next: (pagos) => {
        this.listaPagos = pagos;
        this.paginaActual = 1;
        this.actualizarPaginacion();
        this.cargando = false;
      },
      error: (e) => this.cargando = false
    });
  }

  // --- LÓGICA DE ARCHIVO ---
  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
      this.archivoSeleccionado = event.target.files[0];
    }
  }

  // --- REGISTRAR PAGO (MODIFICADO) ---
  registrarPago() {
    if (this.nuevoPago.contrato_id == 0) {
      alert("⚠️ Por favor selecciona un contrato/cliente primero.");
      return;
    }
    if (this.nuevoPago.monto <= 0) {
      alert("⚠️ El monto debe ser mayor a 0.");
      return;
    }
    if (this.resumen && this.nuevoPago.monto > this.resumen.saldo) {
      if (!confirm(`⚠️ El monto (S/ ${this.nuevoPago.monto}) excede el saldo (S/ ${this.resumen.saldo}). ¿Continuar?`)) return;
    }

    // CREAR FORM DATA
    const formData = new FormData();
    formData.append('contrato_id', this.nuevoPago.contrato_id.toString());
    formData.append('monto', this.nuevoPago.monto.toString());
    formData.append('fecha_pago', this.nuevoPago.fecha_pago);
    formData.append('metodo', this.nuevoPago.metodo);
    formData.append('observacion', this.nuevoPago.observacion || '');

    if (this.archivoSeleccionado) {
      formData.append('file', this.archivoSeleccionado);
    }

    this.pagosService.crearPago(formData).subscribe({
      next: () => {
        alert("✅ Pago registrado con éxito");

        // Resetear campos
        this.nuevoPago.monto = 0;
        this.nuevoPago.observacion = '';
        this.archivoSeleccionado = null;

        // Limpiar input file visualmente
        const fileInput = document.getElementById('fileInput') as HTMLInputElement;
        if (fileInput) fileInput.value = '';

        this.alSeleccionarContrato();
      },
      error: (err) => {
        console.error(err);
        alert("❌ Error al registrar pago.");
      }
    });
  }

  eliminarPago(id: number) {
    if (confirm('¿Seguro que deseas eliminar este pago? La deuda volverá a subir.')) {
      this.pagosService.eliminarPago(id).subscribe({
        next: () => {
          this.alSeleccionarContrato();
        },
        error: () => alert('Error al eliminar')
      });
    }
  }

  // Lógica de Paginación
  actualizarPaginacion() {
    const inicio = (this.paginaActual - 1) * this.pageSize;
    const fin = inicio + this.pageSize;
    this.pagosPaginados = this.listaPagos.slice(inicio, fin);
  }

  cambiarPagina(nuevaPagina: number) {
    this.paginaActual = nuevaPagina;
    this.actualizarPaginacion();
    this.cd.detectChanges();
  }

  get totalPaginas(): number {
    return Math.ceil(this.listaPagos.length / this.pageSize) || 1;
  }
}