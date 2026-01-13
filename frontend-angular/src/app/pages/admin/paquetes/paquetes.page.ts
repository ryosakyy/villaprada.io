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
  showModal = false;
  modoEditar = false;

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
        this.cd.detectChanges();
      },
      error: (err) => console.error("Error al cargar", err)
    });
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
}