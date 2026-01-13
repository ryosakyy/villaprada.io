import { environment } from '../../../../environments/environment';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

const API_URL = environment.apiUrl + '/clientes/';

@Component({
  selector: 'app-clientes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './clientes.html',
  styleUrls: ['./clientes.css']
})
export class ClientesComponent implements OnInit {

  private http = inject(HttpClient);
  private cd = inject(ChangeDetectorRef); // Inyectamos CDR

  clientes: any[] = [];
  clientesOriginales: any[] = [];
  cargando: boolean = true;
  mostrarModal: boolean = false;
  textoBusqueda: string = '';

  nuevoCliente: any = {
    id: null,
    dni: '',
    nombre: '',
    telefono: '',
    correo: '',
    direccion: ''
  };

  ngOnInit() {
    this.cargarClientes();
  }

  cargarClientes() {
    this.cargando = true;
    console.log('Cargando clientes...'); // Debug
    this.http.get<any[]>(API_URL).subscribe({
      next: (data) => {
        console.log('Datos recibidos:', data);
        const datosMapeados = data.map(c => ({
          id: c.id,
          dni: c.dni,
          nombre: c.nombres || c.nombre,
          telefono: c.telefono,
          correo: c.email || c.correo,
          direccion: c.direccion
        }));
        this.clientes = datosMapeados;
        this.clientesOriginales = datosMapeados;
        this.cargando = false;
        this.cd.detectChanges(); // Forzamos actualización de la vista
      },
      error: (err) => {
        console.error('Error al cargar clientes:', err);
        this.cargando = false;
        this.cd.detectChanges();
      }
    });
  }

  buscarCliente() {
    if (!this.textoBusqueda || this.textoBusqueda.trim() === '') {
      this.clientes = [...this.clientesOriginales];
      return;
    }
    const texto = this.textoBusqueda.toLowerCase();
    this.clientes = this.clientesOriginales.filter(c => {
      const dni = c.dni ? c.dni.toString().toLowerCase() : '';
      const nombre = c.nombre ? c.nombre.toLowerCase() : '';
      return dni.includes(texto) || nombre.includes(texto);
    });
  }

  abrirModal() {
    this.nuevoCliente = { id: null, dni: '', nombre: '', telefono: '', correo: '', direccion: '' };
    this.mostrarModal = true;
  }

  cerrarModal() {
    this.mostrarModal = false;
  }

  editarCliente(cliente: any) {
    this.nuevoCliente = { ...cliente };
    this.mostrarModal = true;
  }

  guardarManual(dniVal: string, nombreVal: string, telVal: string, correoVal: string, dirVal: string) {

    // 1. Forzamos la actualización de la variable con lo que viene del HTML
    this.nuevoCliente.dni = dniVal;
    this.nuevoCliente.nombre = nombreVal;
    this.nuevoCliente.telefono = telVal;
    this.nuevoCliente.correo = correoVal;
    this.nuevoCliente.direccion = dirVal;

    // 2. Ahora validamos
    if (!this.nuevoCliente.dni || this.nuevoCliente.dni === '') {
      alert('Escribe el DNI.');
      return;
    }
    if (!this.nuevoCliente.nombre || this.nuevoCliente.nombre === '') {
      alert('Escribe el Nombre.');
      return;
    }

    const datosEnviar = {
      dni: this.nuevoCliente.dni,
      nombre: this.nuevoCliente.nombre,
      telefono: this.nuevoCliente.telefono || null,
      correo: this.nuevoCliente.correo || null,
      direccion: this.nuevoCliente.direccion || null
    };

    const finalizar = () => {
      this.cerrarModal();
      this.cargarClientes();
    };

    if (this.nuevoCliente.id) {
      this.http.put(`${API_URL}${this.nuevoCliente.id}`, datosEnviar).subscribe({
        next: () => finalizar(),
        error: (e) => alert('Error al actualizar: ' + JSON.stringify(e))
      });
    } else {
      this.http.post(API_URL, datosEnviar).subscribe({
        next: () => finalizar(),
        error: (e) => alert('Error al registrar: ' + JSON.stringify(e))
      });
    }
  }

  eliminarCliente(id: number) {
    if (confirm('¿Eliminar?')) {
      this.http.delete(`${API_URL}${id}`).subscribe({
        next: () => this.cargarClientes()
      });
    }
  }
}