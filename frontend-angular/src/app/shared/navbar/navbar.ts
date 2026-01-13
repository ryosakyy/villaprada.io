import { CommonModule } from '@angular/common';
import { Component, Output, EventEmitter } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class NavbarComponent {

  @Output() toggleSidebar = new EventEmitter<void>(); // Added Output

  nombres = '...';
  rol = '';

  constructor(private router: Router, private authService: AuthService) { } // Modified constructor

  onToggleSidebar() { // Added method
    this.toggleSidebar.emit();
  }

  ngOnInit(): void {

    const token = this.authService.getToken(); // Changed auth to authService

    // 🔐 Si no hay token, NO llamamos al backend
    if (!token) return;

    this.authService.perfil().subscribe({
      next: (u: any) => {
        this.nombres = u.nombres;
        this.rol = u.rol;
      },
      error: (err: any) => {
        console.warn('Error al cargar perfil', err);
        // ❌ NO cerrar sesión aquí
      }
    });
  }

  cerrarSesion() {
    this.authService.logout();
  }
}
