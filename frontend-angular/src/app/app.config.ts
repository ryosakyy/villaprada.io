import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { ApplicationConfig } from '@angular/core';
import { provideRouter, withRouterConfig } from '@angular/router';
import { routes } from './app.routes'; // Asegúrate que la ruta sea correcta
import { authInterceptor } from './core/interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      withRouterConfig({
        onSameUrlNavigation: 'reload'
      })
    ),
    // AQUÍ SE CONECTA EL INTERCEPTOR:
    provideHttpClient(
      withFetch(),
      withInterceptors([authInterceptor])
    )
  ]
};