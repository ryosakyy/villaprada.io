import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Egreso, EgresoCreate, EgresosService } from './egresos.service';
import { AuthService } from '../../../core/services/auth.service';
import { environment } from '../../../../environments/environment';

@Component({
  selector: 'app-egresos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './egresos.html',
  styleUrls: ['./egresos.css']
})
export class Egresos implements OnInit {

  listaEgresos: Egreso[] = [];
  listaContratos: any[] = [];

  // Paginación
  paginaActual: number = 1;
  pageSize: number = 10;
  egresosPaginados: Egreso[] = [];

  resumenCategorias: any[] = [];
  totalGeneral: number = 0;

  nuevoEgreso: EgresoCreate = {
    descripcion: '',
    categoria: '',
    monto: 0,
    fecha: new Date().toISOString().split('T')[0],
    observacion: '',
    contrato_id: null
  };

  archivoSeleccionado: File | null = null;
  isAdmin: boolean = false;
  isEmpleado: boolean = false;

  constructor(
    private egresosService: EgresosService,
    public authService: AuthService,
    private cd: ChangeDetectorRef
  ) { }

  apiUrl = environment.apiUrl;

  getNombreCliente(c: any): string {
    if (c.cliente && typeof c.cliente === 'object') {
      return (c.cliente.nombres || c.cliente.nombre || '') + ' ' + (c.cliente.apellidos || c.cliente.apellido || '');
    }
    // Si el backend devuelve nombres planos (ej. cliente_nombre)
    if (c.cliente_nombre) return c.cliente_nombre;

    // Fallback por si solo tenemos ID
    return 'Cliente #' + (c.cliente_id || c.id);
  }

  getNombreClientePorId(contratoId: number | null): string {
    if (!contratoId) return 'Gasto General';

    const contrato = this.listaContratos.find(c => c.id === contratoId);
    if (contrato) {
      return this.getNombreCliente(contrato);
    }
    return '#' + contratoId;
  }

  ngOnInit(): void {
    const role = this.authService.getUserRole();
    this.isAdmin = role === 'admin';
    this.isEmpleado = role === 'empleado';

    // Permitir acceso a admin y empleado
    if (this.isAdmin || this.isEmpleado) {
      this.cargarDatosIniciales();
    }
  }

  cargarDatosIniciales() {
    this.cargarEgresos();
    this.cargarContratos();
  }

  cargarContratos() {
    this.egresosService.listarContratos().subscribe({
      next: (data) => {
        this.listaContratos = data;
        this.cd.detectChanges();
      },
      error: (err) => console.error('Error cargando contratos', err)
    });
  }

  cargarEgresos() {
    this.egresosService.listarEgresos().subscribe({
      next: (data) => {
        this.listaEgresos = data;
        this.egresosFiltrados = data; // Inicializar filtrados
        this.actualizarPaginacion();
        this.calcularResumen();
        this.cd.detectChanges();
      },
      error: (err) => console.error('Error al cargar egresos', err)
    });
  }

  calcularResumen() {
    this.totalGeneral = 0;
    const mapa = new Map<string, { count: number, total: number }>();

    this.listaEgresos.forEach(egreso => {
      this.totalGeneral += egreso.monto;

      const actual = mapa.get(egreso.categoria) || { count: 0, total: 0 };
      actual.count++;
      actual.total += egreso.monto;
      mapa.set(egreso.categoria, actual);
    });

    this.resumenCategorias = Array.from(mapa, ([nombre, datos]) => ({
      nombre,
      count: datos.count,
      total: datos.total
    }));
  }

  // --- LÓGICA DE ARCHIVO ---
  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
      this.archivoSeleccionado = event.target.files[0];
    }
  }

  // --- GUARDAR (Aquí estaba tu error antes) ---
  registrarEgreso() {
    if (!this.nuevoEgreso.descripcion || this.nuevoEgreso.monto <= 0 || !this.nuevoEgreso.categoria) {
      alert("⚠️ Por favor completa la Descripción, Categoría y Monto.");
      return;
    }

    // Usamos FormData para enviar texto + archivo
    const formData = new FormData();
    formData.append('descripcion', this.nuevoEgreso.descripcion);
    formData.append('monto', this.nuevoEgreso.monto.toString());
    formData.append('categoria', this.nuevoEgreso.categoria);
    formData.append('fecha', this.nuevoEgreso.fecha);
    formData.append('observacion', this.nuevoEgreso.observacion || '');

    if (this.nuevoEgreso.contrato_id) {
      formData.append('contrato_id', this.nuevoEgreso.contrato_id.toString());
    }

    // Adjuntar archivo si existe
    if (this.archivoSeleccionado) {
      formData.append('file', this.archivoSeleccionado);
    }

    console.log("Enviando egreso:", this.nuevoEgreso);
    this.egresosService.crearEgreso(formData).subscribe({
      next: (res) => {
        console.log("Respuesta servidor:", res);
        alert("✅ Gasto registrado correctamente");
        this.limpiarFormulario();
        this.cargarEgresos();
      },
      error: (err) => {
        console.error(err);
        alert("❌ Ocurrió un error al guardar.");
      }
    });
  }

  eliminarEgreso(id: number) {
    if (confirm('¿Estás seguro de que deseas eliminar este registro?')) {
      this.egresosService.eliminarEgreso(id).subscribe({
        next: () => this.cargarEgresos(),
        error: () => alert("Error al eliminar")
      });
    }
  }

  limpiarFormulario() {
    this.nuevoEgreso = {
      descripcion: '',
      categoria: '',
      monto: 0,
      fecha: new Date().toISOString().split('T')[0],
      observacion: '',
      contrato_id: null
    };

    this.archivoSeleccionado = null;

    // Limpiar input visualmente
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  }

  // --- FILTROS Y BÚSQUEDA ---
  textoBusqueda: string = '';
  egresosFiltrados: Egreso[] = [];

  filtrarEgresos() {
    const term = this.textoBusqueda.toLowerCase();

    if (!term) {
      this.egresosFiltrados = this.listaEgresos;
    } else {
      this.egresosFiltrados = this.listaEgresos.filter(e => {
        const desc = e.descripcion.toLowerCase();
        const cat = e.categoria.toLowerCase();
        const cliente = e.contrato_id ? this.getNombreClientePorId(e.contrato_id).toLowerCase() : '';
        const user = e.usuario_nombre ? e.usuario_nombre.toLowerCase() : '';

        return desc.includes(term) || cat.includes(term) || cliente.includes(term) || user.includes(term);
      });
    }

    this.paginaActual = 1;
    this.actualizarPaginacion();
  }

  // Lógica de Paginación
  actualizarPaginacion() {
    const inicio = (this.paginaActual - 1) * this.pageSize;
    const fin = inicio + this.pageSize;
    // IMPORTANTE: Paginar sobre los FILTRADOS, no sobre la lista completa original
    this.egresosPaginados = this.egresosFiltrados.slice(inicio, fin);
  }

  cambiarPagina(nuevaPagina: number) {
    this.paginaActual = nuevaPagina;
    this.actualizarPaginacion();
    this.cd.detectChanges();
  }

  get totalPaginas(): number {
    return Math.ceil(this.egresosFiltrados.length / this.pageSize) || 1;
  }
}