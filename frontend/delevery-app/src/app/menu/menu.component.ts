import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface MenuItem {
  id?: number;
  name: string;
  description?: string;
  price?: number;
  imageUrl?: string; // URL completa hacia la imagen servida por el backend
}

interface MenuSection {
  title: string;
  items: MenuItem[];
}

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
  restaurantName = 'Sabor y Mar Cartagena';

  sections: MenuSection[] = [];

  // Cambia si tu backend corre en otra dirección
  backendBase = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadMenuFromBackend();
  }

  private loadMenuFromBackend() {
    const url = `${this.backendBase}/menu`;
    this.http.get<Record<string, Array<any>>>(url).subscribe({
      next: (data) => {
        this.sections = Object.keys(data).map((cat) => ({
          title: this.formatTitle(cat),
          items: (data[cat] || []).map((it) => ({
            id: it.id,
            name: it.nombre,
            price: it.precio,
            imageUrl: this.normalizeImageUrl(it.foto)
          }))
        }));
      },
      error: (err) => {
        console.error('No se pudo cargar el menú desde el backend:', err);
        this.sections = [
          { title: 'SUSHI (offline)', items: [{ name: 'California Roll' }, { name: 'Philadelphia Roll' }] }
        ];
      }
    });
  }

  private normalizeImageUrl(foto: string | undefined): string | undefined {
    if (!foto) return undefined;
    const f = String(foto).trim();
    if (f.length === 0) return undefined;
    // Si ya es una URL absoluta, usarla tal cual
    if (/^https?:\/\//i.test(f)) return f;
    // Quitar barras iniciales y construir URL hacia el backend
    const cleaned = f.replace(/^\/+/, '');
    return `${this.backendBase}/${cleaned}`;
  }

  private formatTitle(cat: string) {
    if (!cat) return cat;
    // Reemplazar guiones/underscores por espacios y capitalizar
    const s = cat.replace(/[-_]+/g, ' ');
    return s.charAt(0).toUpperCase() + s.slice(1);
  }
}
