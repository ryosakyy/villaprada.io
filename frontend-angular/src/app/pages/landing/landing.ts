import { environment } from '../../../environments/environment';
import { CommonModule } from "@angular/common";
import { ChangeDetectorRef, Component, OnInit, inject } from "@angular/core";
import { RouterModule } from "@angular/router";
import { GaleriaService } from "../admin/galeria/galeria.service";
import { DisponibilidadService, DisponibilidadPublica } from "../../core/services/disponibilidad.service";

@Component({
  selector: "app-landing",
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: "./landing.html",
  styleUrls: ["./landing.css"],
})
export class LandingComponent implements OnInit {

  private galeriaService = inject(GaleriaService);
  private disponibilidadService = inject(DisponibilidadService);
  private cdr = inject(ChangeDetectorRef);
  imagenesGaleria: any[] = [];
  fechasOcupadas: DisponibilidadPublica[] = [];
  mobileMenuOpen: boolean = false;

  ngOnInit() {
    this.cargarGaleria();
    this.cargarDisponibilidad();
  }

  cargarDisponibilidad() {
    // Cargar próximos 6 meses por ejemplo, o simplemente todo lo que devuelva el back (filtro por año/mes opcional)
    // Para simplificar, pedimos todo lo que el back mande (el back ya filtra ocupados)
    this.disponibilidadService.getFechasOcupadasPublico().subscribe({
      next: (data) => {
        // Filtrar fechas pasadas si el back no lo hace
        const hoy = new Date().toISOString().split('T')[0];
        this.fechasOcupadas = data.filter(d => d.fecha >= hoy).slice(0, 10); // Mostrar solo las próximas 10 ocupaciones
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error cargando disponibilidad', err)
    });
  }

  cargarGaleria() {
    console.log('[LANDING] Iniciando carga de galería desde:', environment.apiUrl + '/galeria/light-list');
    this.galeriaService.getGaleriaLight().subscribe({
      next: (data) => {
        console.log('[LANDING] ✅ Imágenes recibidas:', data);
        console.log('[LANDING] Total de imágenes:', data.length);
        this.imagenesGaleria = data;
        this.cdr.detectChanges(); // 🔥 FORZAR actualización de UI

        if (data.length === 0) {
          console.warn('[LANDING] ⚠️ La API respondió pero no hay imágenes en la base de datos');
        }
      },
      error: (err) => {
        console.error('[LANDING] ❌ Error cargando galería:', err);
        console.error('[LANDING] Detalles del error:', {
          status: err.status,
          statusText: err.statusText,
          message: err.message,
          url: err.url
        });
        // Si falla, mantener el array vacío
      }
    });
  }

  toggleMobileMenu() {
    this.mobileMenuOpen = !this.mobileMenuOpen;
  }

  closeMobileMenu() {
    this.mobileMenuOpen = false;
  }

  abrirWhatsapp() {
    const phoneNumber = "51987654321"; // Tu número
    const message = "Hola! Me interesa conocer más sobre los servicios de Eventos Villa Prada y reservar mi evento.";
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;

    try {
      const windowRef = window.open(whatsappUrl, "_blank");
      if (!windowRef) {
        window.location.href = whatsappUrl;
      }
    } catch (error) {
      console.error("Error al abrir WhatsApp:", error);
    }
  }
}