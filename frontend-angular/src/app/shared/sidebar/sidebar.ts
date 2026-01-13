import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { CommonModule } from '@angular/common';

interface MenuItem {
  route: string;
  label: string;
  icon: string;
  roles: string[]; // 'admin' o 'empleado'
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class SidebarComponent implements OnInit {

  allMenuItems: MenuItem[] = [
    { route: '/admin/dashboard', label: 'Dashboard', icon: '📊', roles: ['admin'] },
    { route: '/admin/clientes', label: 'Clientes', icon: '👥', roles: ['admin'] },
    { route: '/admin/contratos', label: 'Contratos', icon: '📄', roles: ['admin'] },
    { route: '/admin/reservas', label: 'Reservas', icon: '📅', roles: ['admin', 'empleado'] },
    { route: '/admin/paquetes', label: 'Paquetes', icon: '📦', roles: ['admin'] },
    { route: '/admin/pagos', label: 'Pagos', icon: '💳', roles: ['admin'] },
    { route: '/admin/egresos', label: 'Egresos', icon: '💸', roles: ['admin', 'empleado'] },
    { route: '/admin/reportes', label: 'Reportes', icon: '📈', roles: ['admin'] },
    { route: '/admin/galeria', label: 'Galería', icon: '🖼️', roles: ['admin'] },
    { route: '/admin/usuarios', label: 'Usuarios', icon: '👤', roles: ['admin'] },
  ];

  visibleMenuItems: MenuItem[] = [];
  userRole: string = '';

  constructor(private authService: AuthService) { }

  ngOnInit() {
    this.userRole = this.authService.getUserRole();
    this.visibleMenuItems = this.allMenuItems.filter(item =>
      item.roles.includes(this.userRole)
    );
  }
}
