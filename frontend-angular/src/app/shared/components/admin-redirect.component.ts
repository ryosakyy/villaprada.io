import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
    selector: 'app-admin-redirect',
    standalone: true,
    template: '<p>Redirigiendo...</p>'
})
export class AdminRedirectComponent implements OnInit {

    constructor(
        private authService: AuthService,
        private router: Router
    ) { }

    ngOnInit() {
        const role = this.authService.getUserRole();

        if (role === 'empleado') {
            this.router.navigate(['/admin/reservas']);
        } else {
            this.router.navigate(['/admin/dashboard']);
        }
    }
}
