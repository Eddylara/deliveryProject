import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-admin-panel',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.css']
})
export class AdminPanelComponent {
  backendBase = 'http://127.0.0.1:8000';
  menu: Record<string, any[]> = {};
  categories: { id: number; nombre: string }[] = [];

  // Estado modal crear
  showAddModal = false;
  // Estado modal editar
  showEditModal = false;
  editingItem: any = null;

  // Nuevo item
  newNombre = '';
  newPrecio: number | null = null;
  newCategoriaId: number | null = null;
  newFotoFile: File | null = null;

  // Edit item
  editNombre = '';
  editPrecio: number | null = null;
  editCategoriaId: number | null = null;
  editFotoFile: File | null = null;

  constructor(private router: Router, private http: HttpClient) {}

  ngOnInit(): void {
    const ok = localStorage.getItem('isAdmin');
    if (!ok) {
      this.router.navigate(['/login']);
    }
    this.loadMenu();
    this.loadCategories();
  }

  logout() {
    localStorage.removeItem('isAdmin');
    this.router.navigate(['/login']);
  }

  loadMenu() {
    this.http.get<any>(`${this.backendBase}/menu`).subscribe({
      next: (res) => this.menu = res,
      error: (err) => console.error('Error cargando menú', err)
    });
  }

  loadCategories() {
    this.http.get<{ id: number; nombre: string }[]>(`${this.backendBase}/admin/categories`).subscribe({
      next: (res) => this.categories = res,
      error: (err) => console.error('Error cargando categorías', err)
    });
  }

  onFileChange(ev: Event) {
    const input = ev.target as HTMLInputElement;
    if (input.files && input.files.length) {
      this.newFotoFile = input.files[0];
    } else {
      this.newFotoFile = null;
    }
  }

  onEditFileChange(ev: Event) {
    const input = ev.target as HTMLInputElement;
    if (input.files && input.files.length) {
      this.editFotoFile = input.files[0];
    } else {
      this.editFotoFile = null;
    }
  }

  addItem() {
    if (!this.newNombre || this.newPrecio == null || this.newCategoriaId == null) {
      alert('Rellena nombre, precio y categoría');
      return;
    }

    const fd = new FormData();
    fd.append('nombre', this.newNombre);
    fd.append('precio', String(this.newPrecio));
    fd.append('categoria_id', String(this.newCategoriaId));
    if (this.newFotoFile) {
      fd.append('foto', this.newFotoFile, this.newFotoFile.name);
    }

    this.http.post<any>(`${this.backendBase}/admin/menu`, fd).subscribe({
      next: (res) => {
        alert('Elemento creado');
        this.resetAddForm();
        this.closeAddModal();
        this.loadMenu();
      },
      error: (err) => {
        console.error(err);
        alert('Error creando elemento');
      }
    });
  }

  openAddModal() { this.showAddModal = true; }
  closeAddModal() { this.showAddModal = false; }
  resetAddForm() {
    this.newNombre = '';
    this.newPrecio = null;
    this.newCategoriaId = null;
    this.newFotoFile = null;
    const fiA = document.getElementById('file-input-add') as HTMLInputElement | null;
    if (fiA) fiA.value = '';
  }

  editItem(item: any) {
    this.editingItem = item;
    this.editNombre = item?.nombre ?? '';
    this.editPrecio = item?.precio ?? null;
    this.editCategoriaId = item?.categoria_id ?? null;
    this.editFotoFile = null;
    this.showEditModal = true;
  }

  deleteItem(item: any) {
    if (!item?.id) return;
    const ok = confirm(`¿Eliminar "${item.nombre}" (ID ${item.id})?`);
    if (!ok) return;
    this.http.delete<any>(`${this.backendBase}/admin/menu/${item.id}`).subscribe({
      next: () => {
        this.loadMenu();
      },
      error: (err) => {
        console.error(err);
        alert('Error eliminando elemento');
      }
    });
  }

  closeEditModal() { this.showEditModal = false; }

  updateItem() {
    if (!this.editingItem?.id) return;
    const fd = new FormData();
    if (this.editNombre) fd.append('nombre', this.editNombre);
    if (this.editPrecio != null) fd.append('precio', String(this.editPrecio));
    if (this.editCategoriaId != null) fd.append('categoria_id', String(this.editCategoriaId));
    if (this.editFotoFile) fd.append('foto', this.editFotoFile, this.editFotoFile.name);

    this.http.put<any>(`${this.backendBase}/admin/menu/${this.editingItem.id}`, fd).subscribe({
      next: () => {
        this.closeEditModal();
        const fiE = document.getElementById('file-input-edit') as HTMLInputElement | null;
        if (fiE) fiE.value = '';
        this.loadMenu();
      },
      error: (err) => {
        console.error(err);
        alert('Error actualizando elemento');
      }
    });
  }

  imageSrcFor(item: any) {
    if (!item?.foto) return '';
    // Si ya viene con protocolo/ruta completa
    if (/^https?:\/\//i.test(item.foto)) return item.foto;
    // No forzar extensión: el backend resuelve si falta
    const file = String(item.foto).replace(/^\/+/, '');
    return `${this.backendBase}/${file}`;
  }
}
