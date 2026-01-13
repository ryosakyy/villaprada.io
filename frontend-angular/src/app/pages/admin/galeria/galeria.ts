import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subject, debounceTime, distinctUntilChanged } from 'rxjs';
import { GaleriaService } from './galeria.service';

@Component({
  selector: 'app-galeria',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './galeria.html',
  styleUrl: './galeria.css',
})
export class Galeria implements OnInit {
  listaImagenes: any[] = [];
  terminoBusqueda: string = '';
  private buscadorSubject = new Subject<string>();

  mostrarFormulario: boolean = false;
  tituloNuevo: string = '';
  categoriaNueva: string = '';
  archivoSeleccionado: File | null = null;

  constructor(
    private galeriaService: GaleriaService,
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.obtenerImagenes();
    this.buscadorSubject.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(texto => this.ejecutarBusqueda(texto));
  }

  obtenerImagenes(): void {
    this.galeriaService.getGaleria().subscribe({
      next: (data: any[]) => {
        this.listaImagenes = data;
        this.cd.detectChanges();
      },
      error: (err: any) => console.error('Error al cargar galería', err)
    });
  }

  // MÉTODO PARA EL ERROR DE "borrarImagen"
  borrarImagen(id: number): void {
    if (confirm('¿Estás seguro de eliminar esta imagen?')) {
      this.galeriaService.eliminar(id).subscribe({
        next: () => this.obtenerImagenes(),
        error: (err: any) => alert('Error al eliminar')
      });
    }
  }

  // MÉTODO PARA EL ERROR DE "window.open"
  verImagen(url: string): void {
    window.open(url, '_blank');
  }

  onSearchChange(texto: string): void {
    this.buscadorSubject.next(texto);
  }

  ejecutarBusqueda(texto: string): void {
    if (!texto.trim()) {
      this.obtenerImagenes();
      return;
    }
    this.galeriaService.buscarImagenes(texto).subscribe({
      next: (data: any[]) => this.listaImagenes = data,
      error: (err: any) => console.error(err)
    });
  }

  onFileSelected(event: any): void {
    this.archivoSeleccionado = event.target.files[0];
  }

  subirImagen(): void {
    if (!this.archivoSeleccionado || !this.tituloNuevo) {
      alert("Completa los datos");
      return;
    }
    const formData = new FormData();
    formData.append('titulo', this.tituloNuevo);
    formData.append('categoria', this.categoriaNueva);
    formData.append('imagen', this.archivoSeleccionado);

    this.galeriaService.subirImagen(formData).subscribe({
      next: () => {
        this.resetForm();
        this.obtenerImagenes();
      },
      error: (err: any) => alert("Error al subir")
    });
  }

  resetForm(): void {
    this.mostrarFormulario = false;
    this.tituloNuevo = '';
    this.categoriaNueva = '';
    this.archivoSeleccionado = null;
  }
}