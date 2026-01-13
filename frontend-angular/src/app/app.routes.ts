import { Routes } from '@angular/router';
import { RoleGuard } from './core/guards/role.guard';
import { AuthGuard } from './core/guards/auth.guard';

import { LoginComponent } from './pages/auth/login/login';
import { LandingComponent } from './pages/landing/landing';
import { AdminLayout } from './shared/layout/admin-layout/admin-layout';

import { ClientesComponent } from './pages/admin/clientes/clientes';
import { ContratosComponent } from './pages/admin/contratos/contratos';
import { Dashboard } from './pages/admin/dashboard/dashboard';
import { Disponibilidad } from './pages/admin/disponibilidad/disponibilidad';
import { Egresos } from './pages/admin/egresos/egresos';
import { Galeria } from './pages/admin/galeria/galeria';
import { Pagos } from './pages/admin/pagos/pagos';
import { PaquetesPage } from './pages/admin/paquetes/paquetes.page';
import { Reportes } from './pages/admin/reportes/reportes';
import { Reservas } from './pages/admin/reservas/reservas';
import { Usuarios } from './pages/admin/usuarios/usuarios';
import { AdminRedirectComponent } from './shared/components/admin-redirect.component';

export const routes: Routes = [
  // 1. PÁGINA PRINCIPAL (Lo que ve el cliente al entrar a la web)
  { path: '', component: LandingComponent },

  // 2. ACCESO AL PANEL (Para el admin)
  { path: 'login', component: LoginComponent },

  // 3. PANEL DE ADMINISTRACIÓN
  {
    path: 'admin',
    component: AdminLayout,
    canActivate: [AuthGuard],
    children: [
      {
        path: 'dashboard',
        component: Dashboard,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'clientes',
        component: ClientesComponent,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'contratos',
        component: ContratosComponent,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'reservas',
        component: Reservas,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin', 'empleado'] }
      },
      {
        path: 'pagos',
        component: Pagos,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'paquetes',
        component: PaquetesPage,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'usuarios',
        component: Usuarios,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'egresos',
        component: Egresos,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin', 'empleado'] }
      },
      {
        path: 'galeria',
        component: Galeria,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'disponibilidad',
        component: Disponibilidad,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      {
        path: 'reportes',
        component: Reportes,
        runGuardsAndResolvers: 'always',
        canActivate: [RoleGuard],
        data: { roles: ['admin'] }
      },
      { path: '', component: AdminRedirectComponent, pathMatch: 'full' },
    ],
  },

  // 4. COMODÍN (Si escriben cualquier cosa, los manda a la landing)
  { path: '**', redirectTo: '' },
];