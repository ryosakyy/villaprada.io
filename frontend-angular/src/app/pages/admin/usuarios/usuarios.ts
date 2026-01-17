import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Usuario, UsuariosService } from './usuarios.service';

@Component({
  selector: 'app-usuarios',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './usuarios.html',
  styleUrls: ['./usuarios.css']
})
export class Usuarios implements OnInit {
  usuarios: Usuario[] = [];
  showCrear = false;
  showEditar = false;

  // Paginación
  paginaActual: number = 1;
  pageSize: number = 10;
  usuariosPaginados: Usuario[] = [];

  nuevo: any = { nombres: '', email: '', password: '', rol: 'admin' };
  edit: any = { id: null, nombres: '', email: '', rol: 'admin', estado: true };

  constructor(
    private service: UsuariosService,
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit() { this.cargarUsuarios(); }

  cargarUsuarios() {
    this.service.listar().subscribe({
      next: (res) => {
        this.usuarios = res.filter(u => u.estado === true);
        this.actualizarPaginacion();
        this.cd.detectChanges();
      },
      error: (err) => console.error("Error al cargar lista")
    });
  }

  abrirModalCrear() {
    this.nuevo = { nombres: '', email: '', password: '', rol: 'admin' };
    this.showCrear = true;
    this.showEditar = false;
  }

  abrirModalEditar(u: Usuario) {
    this.edit = { ...u, password: '' };
    this.showEditar = true;
    this.showCrear = false;
  }

  registrar() {
    this.service.crear(this.nuevo).subscribe({
      next: () => {
        this.cargarUsuarios();
        this.showCrear = false;
      },
      error: (e) => alert('Error: ' + (e.error?.detail || 'Datos inválidos'))
    });
  }

  actualizar() {
    if (!this.edit.id) return;
    this.service.actualizar(this.edit.id, this.edit).subscribe({
      next: () => {
        this.cargarUsuarios();
        this.showEditar = false;
      },
      error: (e) => alert('Error al actualizar')
    });
  }

  borrarUsuario(u: Usuario) {
    if (u.id && confirm(`¿Desea eliminar permanentemente a ${u.nombres}?`)) {
      this.service.eliminar(u.id).subscribe({
        next: () => {
          this.cargarUsuarios(); // Al recargar, el filtro lo quitará de la vista
        },
        error: (e) => alert('No se pudo eliminar')
      });
    }
  }

  // Lógica de Paginación
  actualizarPaginacion() {
    const inicio = (this.paginaActual - 1) * this.pageSize;
    const fin = inicio + this.pageSize;
    this.usuariosPaginados = this.usuarios.slice(inicio, fin);
  }

  cambiarPagina(nuevaPagina: number) {
    this.paginaActual = nuevaPagina;
    this.actualizarPaginacion();
    this.cd.detectChanges();
  }

  get totalPaginas(): number {
    return Math.ceil(this.usuarios.length / this.pageSize) || 1;
  }
}