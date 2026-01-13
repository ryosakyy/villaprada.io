import { environment } from '../../../../environments/environment';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

// --- CONFIGURACIÓN DE URLS ---
const API_URL_CONTRATOS = environment.apiUrl + '/contratos/';
const API_URL_CLIENTES = environment.apiUrl + '/clientes/';
const API_URL_PAQUETES = environment.apiUrl + '/paquetes/';
const API_URL_SERVICIOS = environment.apiUrl + '/servicios/';

@Component({
  selector: 'app-contratos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './contratos.html',
  styleUrls: ['./contratos.css']
})
export class ContratosComponent implements OnInit {

  private http = inject(HttpClient);
  private cd = inject(ChangeDetectorRef);

  // --- DATOS ---
  contratos: any[] = [];
  listaClientes: any[] = [];
  listaPaquetes: any[] = [];
  listaServicios: any[] = [];
  cargando: boolean = false;

  // --- MODALES (FLAGS) ---
  mostrarModalCliente: boolean = false;
  mostrarModalPaquete: boolean = false;
  mostrarModalServicio: boolean = false;

  ngOnInit() {
    this.cargarContratos();
    this.cargarListaClientes();
    this.cargarListaPaquetes();
    this.cargarListaServicios();
  }

  getHeaders() {
    const token = localStorage.getItem('token');
    return { headers: new HttpHeaders({ 'Authorization': `Bearer ${token}` }) };
  }

  // ==================== CARGAS DE DATOS ====================
  cargarContratos() {
    this.cargando = true;
    this.http.get<any[]>(API_URL_CONTRATOS, this.getHeaders()).subscribe({
      next: (data) => {
        this.contratos = data;
        this.cargando = false;
        this.cd.detectChanges();
      },
      error: (e) => {
        console.error(e);
        this.cargando = false;
        this.cd.detectChanges();
      }
    });
  }

  cargarListaClientes() {
    this.http.get<any[]>(API_URL_CLIENTES, this.getHeaders()).subscribe({
      next: (data) => {
        this.listaClientes = data;
        this.cd.detectChanges();
      },
      error: (e) => console.error(e)
    });
  }

  cargarListaPaquetes() {
    this.http.get<any[]>(API_URL_PAQUETES, this.getHeaders()).subscribe({
      next: (d) => {
        this.listaPaquetes = d;
        this.cd.detectChanges();
      }
    });
  }

  cargarListaServicios() {
    this.http.get<any[]>(API_URL_SERVICIOS, this.getHeaders()).subscribe({
      next: (d) => {
        console.log('Servicios cargados:', d); // DEBUG
        this.listaServicios = d;
        this.cd.detectChanges();
      },
      error: (e) => console.error('Error cargando servicios:', e)
    });
  }

  // ==================== HELPER VISUAL ====================
  obtenerNombreCliente(id: any): string {
    if (!id) return '---';
    const cliente = this.listaClientes.find(c => c.id == id);
    if (cliente) {
      const nom = cliente.nombres || cliente.nombre || cliente.name || '';
      const ape = cliente.apellidos || cliente.apellido || '';
      return `${nom} ${ape}`;
    }
    return 'Cliente ID: ' + id;
  }

  // ==================== LÓGICA DE NEGOCIO ====================

  // Objeto para el formulario (Binding con ngModel)
  nuevoContrato = {
    clienteId: '',
    paqueteStr: '',
    fecha: '',
    horaIni: '',
    horaFin: '',
    montoTotal: 0,
    adelanto: 0
  };

  // 1. Usar Paquete: Reemplaza nombre y precio base
  usarPaquete(evento: any) {
    const idSeleccionado = evento.target.value;
    if (!idSeleccionado) return;

    const paquete = this.listaPaquetes.find(p => p.id == idSeleccionado);
    if (paquete) {
      this.nuevoContrato.paqueteStr = paquete.nombre;
      this.nuevoContrato.montoTotal = parseFloat(paquete.precio);
    }
  }

  // 2. Agregar Servicio: Concatena nombre y suma precio
  agregarServicio(evento: any) {
    const idSeleccionado = evento.target.value;
    if (!idSeleccionado) return;

    const servicio = this.listaServicios.find(s => s.id == idSeleccionado);

    if (servicio) {
      // Concatenar nombre
      if (this.nuevoContrato.paqueteStr) {
        this.nuevoContrato.paqueteStr += ' + ' + servicio.nombre;
      } else {
        this.nuevoContrato.paqueteStr = servicio.nombre;
      }

      // Sumar precio
      this.nuevoContrato.montoTotal = (this.nuevoContrato.montoTotal || 0) + parseFloat(servicio.precio);

      // Resetear el select
      evento.target.value = "";
    }
  }

  // 3. Limpiar formulario
  limpiarForm() {
    this.nuevoContrato = {
      clienteId: '',
      paqueteStr: '',
      fecha: '',
      horaIni: '',
      horaFin: '',
      montoTotal: 0,
      adelanto: 0
    };
  }

  // ==================== CRUD CONTRATOS ====================
  guardarContrato() {
    const { clienteId, paqueteStr, fecha, horaIni, horaFin, montoTotal, adelanto } = this.nuevoContrato;

    if (!clienteId || !paqueteStr || !fecha || !montoTotal) {
      alert('Faltan datos obligatorios (*).');
      return;
    }

    const payload = {
      cliente_id: parseInt(clienteId),
      paquete: paqueteStr,
      fecha_evento: fecha,
      hora_inicio: horaIni || null,
      hora_fin: horaFin || null,
      monto_total: montoTotal,
      adelanto: adelanto || 0
    };

    this.http.post(API_URL_CONTRATOS, payload, this.getHeaders()).subscribe({
      next: () => {
        alert('Contrato guardado con éxito');
        this.limpiarForm(); // Limpiar después de guardar
        this.cargarContratos();
      },
      error: (e) => alert('Error al guardar. Revisa la consola.')
    });
  }

  eliminar(id: number) {
    if (confirm('¿Eliminar contrato?')) {
      this.http.delete(`${API_URL_CONTRATOS}${id}`, this.getHeaders()).subscribe({
        next: () => this.cargarContratos(),
        error: () => alert('Error al eliminar')
      });
    }
  }

  descargarPDF(id: number) {
    const url = `${API_URL_CONTRATOS}${id}/pdf`;
    const headers = this.getHeaders().headers;
    this.http.get(url, { headers: headers, responseType: 'blob' }).subscribe({
      next: (blob: Blob) => {
        const downloadURL = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadURL;
        link.download = `Contrato_VP_${id}.pdf`;
        link.click();
        window.URL.revokeObjectURL(downloadURL);
      },
      error: (error) => {
        console.error('Error descargando PDF:', error);
        alert('No se pudo descargar el PDF.');
      }
    });
  }

  // ==================== MODALES ====================

  // --- CLIENTE ---
  abrirModalCliente() { this.mostrarModalCliente = true; }
  cerrarModalCliente() { this.mostrarModalCliente = false; }

  guardarClienteRapido(dni: string, nombre: string, tel: string, email: string) {
    if (!dni || !nombre) return alert('DNI y Nombre obligatorios');
    const nuevo = { dni, nombres: nombre, nombre: nombre, telefono: tel, correo: email, direccion: 'Sin direccion' };
    this.http.post(API_URL_CLIENTES, nuevo, this.getHeaders()).subscribe({
      next: () => {
        alert('Cliente creado');
        this.cerrarModalCliente();
        this.cargarListaClientes();
      }
    });
  }

  // --- PAQUETE ---
  abrirModalPaquete() { this.mostrarModalPaquete = true; }
  cerrarModalPaquete() { this.mostrarModalPaquete = false; }

  guardarPaqueteRapido(nombre: string, precio: string, cap: string, serv: string) {
    if (!nombre || !precio) return alert('Nombre y Precio obligatorios');
    const nuevo = { nombre, precio: parseFloat(precio), capacidad: parseInt(cap) || 100, servicios: serv, estado: 'activo' };
    this.http.post(API_URL_PAQUETES, nuevo, this.getHeaders()).subscribe({
      next: () => {
        alert('Paquete creado');
        this.cerrarModalPaquete();
        this.cargarListaPaquetes();
      }
    });
  }

  // --- SERVICIO ---

  // Objeto para el modal de servicio
  nuevoServicio = {
    nombre: '',
    precio: '',
    descripcion: ''
  };

  abrirModalServicio() {
    this.nuevoServicio = { nombre: '', precio: '', descripcion: '' }; // Resetear
    this.mostrarModalServicio = true;
    this.cd.detectChanges();
  }

  cerrarModalServicio() {
    this.mostrarModalServicio = false;
    this.cd.detectChanges();
  }

  guardarServicioRapido() {
    const { nombre, precio, descripcion } = this.nuevoServicio;

    if (!nombre || !precio) {
      alert('El nombre y el precio son obligatorios.');
      return;
    }

    const nuevoServicioPayload = {
      nombre: nombre,
      precio: parseFloat(precio),
      descripcion: descripcion || '',
      estado: 'activo'
    };

    this.http.post(API_URL_SERVICIOS, nuevoServicioPayload, this.getHeaders()).subscribe({
      next: () => {
        alert('✅ Servicio creado correctamente');
        this.cerrarModalServicio();
        // Forzamos recarga y detect changes
        this.cargarListaServicios();
      },
      error: (e) => {
        console.error(e);
        alert('❌ Error al guardar el servicio: ' + (e.error?.detail || e.message));
      }
    });
  }
}