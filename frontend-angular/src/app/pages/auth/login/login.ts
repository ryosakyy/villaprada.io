import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css'] // Asegúrate que el archivo css exista
})
export class LoginComponent { // Ojo: A veces se llama 'Login' a secas, revisa tu router

  private auth = inject(AuthService);
  private router = inject(Router);

  email = '';
  password = '';
  cargando = false;
  error = '';

  // Función llamada desde el HTML
  ingresar() {
    this.error = '';
    this.cargando = true;

    console.log('Intentando login con:', this.email);

    this.auth.login(this.email, this.password).subscribe({
      next: (data) => {
        console.log('Respuesta Server:', data);

        // 1. Guardamos el token
        this.auth.saveSession(data);

        // 2. Verificamos que se guardó (Depuración)
        if (this.auth.isAuthenticated()) {
          console.log('Login exitoso. Redirigiendo...');
          this.router.navigate(['/admin']);  // Dejamos que el Router decida a dónde ir (Dashboard o Reservas) 
        } else {
          this.error = 'Login exitoso pero no se recibió token.';
        }
      },
      error: (err) => {
        console.error(err);
        this.error = 'Credenciales incorrectas o error de servidor.';
        this.cargando = false;
      },
      complete: () => {
        this.cargando = false;
      }
    });
  }
}