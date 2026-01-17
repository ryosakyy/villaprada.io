import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Paquete, PaqueteDataService } from './paquete-data';

@Component({
  selector: 'app-paquetes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './paquetes.page.html',
  styleUrls: ['./paquetes.page.css']
})
export class PaquetesPage implements OnInit {
  paquetes: Paquete[] = [];
  paquetesOriginales: Paquete[] = [];
  showModal = false;
  modoEditar = false;
  textoBusqueda: string = '';

  // Paginación
  paginaActual: number = 1;
  pageSize: number = 10;
  paquetesPaginados: Paquete[] = [];

  formPaquete: Paquete = {
    nombre: '',
    descripcion: '',
    precio: 0,
    capacidad: 1,
    servicios: '',
    estado: 'activo'
  };

  constructor(
    private service: PaqueteDataService,
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit() { this.cargarPaquetes(); }

  cargarPaquetes() {
    this.service.listar().subscribe({
      next: (res) => {
        this.paquetes = res;
        this.paquetesOriginales = res;
        this.actualizarPaginacion();
        this.cd.detectChanges();
      },
      error: (err) => console.error("Error al cargar", err)
    });
  }

  // Búsqueda de paquetes
  buscarPaquete() {
    if (!this.textoBusqueda || this.textoBusqueda.trim() === '') {
      this.paquetes = [...this.paquetesOriginales];
    } else {
      const texto = this.textoBusqueda.toLowerCase();
      this.paquetes = this.paquetesOriginales.filter(p => {
        const nombre = p.nombre ? p.nombre.toLowerCase() : '';
        const descripcion = p.descripcion ? p.descripcion.toLowerCase() : '';
        const servicios = p.servicios ? p.servicios.toLowerCase() : '';
        return nombre.includes(texto) || descripcion.includes(texto) || servicios.includes(texto);
      });
    }
    this.paginaActual = 1;
    this.actualizarPaginacion();
  }

  abrirModalCrear() {
    this.modoEditar = false;
    this.formPaquete = { nombre: '', descripcion: '', precio: 0, capacidad: 1, servicios: '', estado: 'activo' };
    this.showModal = true;
  }

  abrirModalEditar(p: Paquete) {
    this.modoEditar = true;
    this.formPaquete = { ...p };
    this.showModal = true;
  }

  guardar() {
    if (this.modoEditar && this.formPaquete.id) {
      this.service.actualizar(this.formPaquete.id, this.formPaquete).subscribe({
        next: () => { this.cargarPaquetes(); this.showModal = false; },
        error: () => alert('Error al actualizar')
      });
    } else {
      this.service.crear(this.formPaquete).subscribe({
        next: () => { this.cargarPaquetes(); this.showModal = false; },
        error: () => alert('Error al crear')
      });
    }
  }

  borrar(p: Paquete) {
    if (p.id && confirm(`¿Eliminar ${p.nombre}?`)) {
      this.service.eliminar(p.id).subscribe({
        next: () => this.cargarPaquetes(),
        error: () => alert('Error al eliminar')
      });
    }
  }

  // Lógica de Paginación
  actualizarPaginacion() {
    const inicio = (this.paginaActual - 1) * this.pageSize;
    const fin = inicio + this.pageSize;
    this.paquetesPaginados = this.paquetes.slice(inicio, fin);
  }

  cambiarPagina(nuevaPagina: number) {
    this.paginaActual = nuevaPagina;
    this.actualizarPaginacion();
    this.cd.detectChanges();
  }

  get totalPaginas(): number {
    return Math.ceil(this.paquetes.length / this.pageSize) || 1;
  }
}