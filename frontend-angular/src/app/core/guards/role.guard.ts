import { Injectable, inject } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
    providedIn: 'root'
})
export class RoleGuard implements CanActivate {

    private authService = inject(AuthService);
    private router = inject(Router);

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        const userRole = this.authService.getUserRole();

        // Obtener roles permitidos desde la data de la ruta
        const allowedRoles = route.data['roles'] as Array<string>;

        if (!allowedRoles || allowedRoles.length === 0) {
            return true; // Si no hay roles definidos, permitir acceso (o denegar según política)
        }

        if (allowedRoles.includes(userRole)) {
            return true;
        }

        // Si no tiene permiso, redirigir
        alert('⛔ Acceso denegado. No tienes permisos para ver esta sección.');

        if (userRole === 'empleado') {
            this.router.navigate(['/admin/reservas']);
        } else {
            this.router.navigate(['/admin/dashboard']);
        }

        return false;
    }
}
