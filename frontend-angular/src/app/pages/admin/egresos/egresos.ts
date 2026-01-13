import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Egreso, EgresoCreate, EgresosService } from './egresos.service';

@Component({
  selector: 'app-egresos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './egresos.html',
  styleUrls: ['./egresos.css']
})
export class Egresos implements OnInit {

  listaEgresos: Egreso[] = [];
  listaContratos: any[] = [];

  resumenCategorias: any[] = [];
  totalGeneral: number = 0;

  nuevoEgreso: EgresoCreate = {
    descripcion: '',
    categoria: '',
    monto: 0,
    fecha: new Date().toISOString().split('T')[0],
    observacion: '',
    contrato_id: null
  };

  archivoSeleccionado: File | null = null;

  constructor(
    private egresosService: EgresosService,
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.cargarDatosIniciales();
  }

  cargarDatosIniciales() {
    this.cargarEgresos();
    this.cargarContratos();
  }

  cargarContratos() {
    this.egresosService.listarContratos().subscribe({
      next: (data) => {
        this.listaContratos = data;
        this.cd.detectChanges();
      },
      error: (err) => console.error('Error cargando contratos', err)
    });
  }

  cargarEgresos() {
    this.egresosService.listarEgresos().subscribe({
      next: (data) => {
        this.listaEgresos = data;
        this.calcularResumen();
        this.cd.detectChanges();
      },
      error: (err) => console.error('Error al cargar egresos', err)
    });
  }

  calcularResumen() {
    this.totalGeneral = 0;
    const mapa = new Map<string, { count: number, total: number }>();

    this.listaEgresos.forEach(egreso => {
      this.totalGeneral += egreso.monto;

      const actual = mapa.get(egreso.categoria) || { count: 0, total: 0 };
      actual.count++;
      actual.total += egreso.monto;
      mapa.set(egreso.categoria, actual);
    });

    this.resumenCategorias = Array.from(mapa, ([nombre, datos]) => ({
      nombre,
      count: datos.count,
      total: datos.total
    }));
  }

  // --- LÓGICA DE ARCHIVO ---
  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
      this.archivoSeleccionado = event.target.files[0];
    }
  }

  // --- GUARDAR (Aquí estaba tu error antes) ---
  registrarEgreso() {
    if (!this.nuevoEgreso.descripcion || this.nuevoEgreso.monto <= 0 || !this.nuevoEgreso.categoria) {
      alert("⚠️ Por favor completa la Descripción, Categoría y Monto.");
      return;
    }

    // Usamos FormData para enviar texto + archivo
    const formData = new FormData();
    formData.append('descripcion', this.nuevoEgreso.descripcion);
    formData.append('monto', this.nuevoEgreso.monto.toString());
    formData.append('categoria', this.nuevoEgreso.categoria);
    formData.append('fecha', this.nuevoEgreso.fecha);
    formData.append('observacion', this.nuevoEgreso.observacion || '');

    if (this.nuevoEgreso.contrato_id) {
      formData.append('contrato_id', this.nuevoEgreso.contrato_id.toString());
    }

    // Adjuntar archivo si existe
    if (this.archivoSeleccionado) {
      formData.append('file', this.archivoSeleccionado);
    }

    this.egresosService.crearEgreso(formData).subscribe({
      next: () => {
        alert("✅ Gasto registrado correctamente");
        this.limpiarFormulario();
        this.cargarEgresos();
      },
      error: (err) => {
        console.error(err);
        alert("❌ Ocurrió un error al guardar.");
      }
    });
  }

  eliminarEgreso(id: number) {
    if (confirm('¿Estás seguro de que deseas eliminar este registro?')) {
      this.egresosService.eliminarEgreso(id).subscribe({
        next: () => this.cargarEgresos(),
        error: () => alert("Error al eliminar")
      });
    }
  }

  limpiarFormulario() {
    this.nuevoEgreso = {
      descripcion: '',
      categoria: '',
      monto: 0,
      fecha: new Date().toISOString().split('T')[0],
      observacion: '',
      contrato_id: null
    };

    this.archivoSeleccionado = null;

    // Limpiar input visualmente
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  }
}