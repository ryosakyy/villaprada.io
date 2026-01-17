import { environment } from '../../../environments/environment';
import { CommonModule } from "@angular/common";
import { ChangeDetectorRef, Component, OnInit, inject } from "@angular/core";
import { RouterModule } from "@angular/router";
import { GaleriaService } from "../admin/galeria/galeria.service";
import { DisponibilidadService, DisponibilidadPublica } from "../../core/services/disponibilidad.service";
import { FormsModule } from '@angular/forms';

@Component({
  selector: "app-landing",
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: "./landing.html",
  styleUrls: ["./landing.css"],
})
export class LandingComponent implements OnInit {

  private galeriaService = inject(GaleriaService);
  private disponibilidadService = inject(DisponibilidadService);
  private cdr = inject(ChangeDetectorRef);
  imagenesGaleria: any[] = [];
  imagenesSeccionGaleria: any[] = []; // Imágenes exclusivas para la sección Galería
  fechasOcupadas: DisponibilidadPublica[] = [];
  mobileMenuOpen: boolean = false;

  // Propiedades para el Calendario
  hoy = new Date();
  currentMonth = this.hoy.getMonth();
  currentYear = this.hoy.getFullYear();
  daysInMonth: { day: number, fullDate: string, isPast: boolean, events: any[] }[] = [];
  weekDays = ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'];
  monthNames = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];

  // Formulario de contacto
  contactoForm = {
    nombre: '',
    email: '',
    telefono: '',
    mensaje: ''
  };

  ngOnInit() {
    this.cargarGaleria();
    this.cargarDisponibilidad();
    this.generateCalendar();
  }

  cargarDisponibilidad() {
    this.disponibilidadService.getFechasOcupadasPublico().subscribe({
      next: (data) => {
        const hoyIso = new Date().toISOString().split('T')[0];
        // Conservamos todo para el calendario, pero filtramos para la lista rápida
        this.fechasOcupadas = data.filter(d => d.fecha >= hoyIso).slice(0, 10);

        // Mapeamos los datos para facilitar la búsqueda por fecha en el calendario
        this.eventosPorFecha = data;
        this.generateCalendar();
        this.cdr.detectChanges();
      },
      error: (err) => console.error('Error cargando disponibilidad', err)
    });
  }

  eventosPorFecha: any[] = [];

  generateCalendar() {
    this.daysInMonth = [];
    const firstDay = new Date(this.currentYear, this.currentMonth, 1).getDay();
    const totalDays = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();

    // Rellenar días vacíos al inicio (offset)
    for (let i = 0; i < firstDay; i++) {
      this.daysInMonth.push({ day: 0, fullDate: '', isPast: true, events: [] });
    }

    const hoyStr = new Date().toISOString().split('T')[0];

    for (let day = 1; day <= totalDays; day++) {
      const dateObj = new Date(this.currentYear, this.currentMonth, day);
      const dateStr = dateObj.toISOString().split('T')[0];
      const isPast = dateStr < hoyStr;

      // Buscar eventos para este día
      const events = this.eventosPorFecha.filter(e => e.fecha === dateStr);

      this.daysInMonth.push({
        day,
        fullDate: dateStr,
        isPast,
        events
      });
    }
  }

  prevMonth() {
    this.currentMonth--;
    if (this.currentMonth < 0) {
      this.currentMonth = 11;
      this.currentYear--;
    }
    this.generateCalendar();
  }

  nextMonth() {
    this.currentMonth++;
    if (this.currentMonth > 11) {
      this.currentMonth = 0;
      this.currentYear++;
    }
    this.generateCalendar();
  }

  enviarMensaje() {
    const { nombre, email, telefono, mensaje } = this.contactoForm;
    if (!nombre || !mensaje) {
      alert("Por favor, ingresa al menos tu nombre y el mensaje.");
      return;
    }

    const texto = `*Nuevo Mensaje desde Web Villa Prada*\n\n` +
      `👤 *Nombre:* ${nombre}\n` +
      `📧 *Email:* ${email || 'No proporcionado'}\n` +
      `📞 *Teléfono:* ${telefono || 'No proporcionado'}\n` +
      `💬 *Mensaje:* ${mensaje}`;

    const phoneNumber = "51927577215"; // Tu número real
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(texto)}`;

    window.open(whatsappUrl, '_blank');
  }

  cargarGaleria() {
    console.log('[LANDING] Iniciando carga de galería desde:', environment.apiUrl + '/galeria/light-list');
    this.galeriaService.getGaleriaLight().subscribe({
      next: (data) => {
        console.log('[LANDING] ✅ Imágenes recibidas:', data);
        console.log('[LANDING] Total de imágenes:', data.length);
        this.imagenesGaleria = data;

        // 1. Intentamos filtrar por la categoría específica "galeria"
        const fotosGaleria = data.filter(img => img.categoria?.toLowerCase() === 'galeria');

        // 2. Si hay fotos en esa categoría, las usamos.
        if (fotosGaleria.length > 0) {
          this.imagenesSeccionGaleria = fotosGaleria;
        } else {
          // 3. Fallback: Si no hay categoría "galeria", mostramos las últimas 6 fotos de CUALQUIER categoría
          // para que la sección no quede vacía.
          console.warn('[LANDING] No hay fotos en categoría "galeria", mostrando recientes.');
          this.imagenesSeccionGaleria = data.slice(0, 12);
        }

        console.log('[LANDING] Imágenes para Galería Principal:', this.imagenesSeccionGaleria.length);

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

  tiposEventos = [
    { title: 'Bodas', icon: '🍸', desc: 'Tu historia de amor comienza aquí', slug: 'bodas' },
    { title: 'Matrimonios', icon: '👑', desc: 'Momentos únicos e irrepetibles', slug: 'matrimonios' },
    { title: 'Graduaciones', icon: '🎓', desc: 'Celebra tus logros a lo grande', slug: 'graduaciones' },
    { title: 'Cumpleaños', icon: '🎂', desc: 'Festeja un año más de vida', slug: 'cumpleaños' },
    { title: 'Baby Showers', icon: '👶', desc: 'La bienvenida más dulce', slug: 'babyshower' },
    { title: 'Corporativos', icon: '💼', desc: 'Eventos empresariales de nivel', slug: 'corporativo' }
  ];

  getImagenCategoria(slug: string): string {
    const img = this.imagenesGaleria.find(i => i.categoria?.toLowerCase() === slug.toLowerCase());

    // Check multiple possible keys for safety
    if (img) {
      return img.imagen_url || img.imagen || img.secure_url || '';
    }

    // Fallbacks por defecto si no hay imagenes en BD
    const fallbacks: any = {
      'bodas': 'https://images.unsplash.com/photo-1519741497674-611481863552?q=80&w=1000',
      'matrimonios': 'https://images.unsplash.com/photo-1511285560982-1351cdeb9821?q=80&w=1000',
      'graduaciones': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=1000',
      'cumpleaños': 'https://images.unsplash.com/photo-1464349153735-7db50ed83c84?q=80&w=1000',
      'babyshower': 'https://images.unsplash.com/photo-1519834785169-98be25ec3f84?q=80&w=1000',
      'corporativo': 'https://images.unsplash.com/photo-1511578314322-379afb476865?q=80&w=1000'
    };
    return fallbacks[slug.toLowerCase()] || '';
  }

  abrirWhatsapp() {
    const phoneNumber = "51927577215"; // Tu número
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