import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';

interface PedidoRow {
  id: number;
  fecha: string;
  nombre: string;
  apellido: string;
  telefono: string;
  direccion: string;
  apto?: string | null;
  estado: 'pendiente' | 'preparando' | 'enviado' | 'entregado' | 'cancelado';
  total: number;
  items_count: number;
}

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule, RouterModule],
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent {
  backendBase = 'http://127.0.0.1:8000';
  pedidos: PedidoRow[] = [];
  loading = false;
  error = '';
  filtroEstado: '' | PedidoRow['estado'] = '';
  estados: PedidoRow['estado'][] = ['pendiente', 'preparando', 'enviado', 'entregado', 'cancelado'];

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    const ok = localStorage.getItem('isAdmin');
    if (!ok) {
      this.router.navigate(['/login']);
      return;
    }
    this.load();
  }

  load() {
    this.loading = true;
    this.error = '';
    const params: any = {};
    if (this.filtroEstado) params.estado = this.filtroEstado;
    this.http.get<PedidoRow[]>(`${this.backendBase}/admin/pedidos`, { params })
      .subscribe({
        next: (rows) => { this.pedidos = rows; this.loading = false; },
        error: (err) => { this.error = 'Error cargando pedidos'; this.loading = false; console.error(err); }
      });
  }

  verDetalle(p: PedidoRow) {
    window.open(`${this.backendBase}/pedido/${p.id}`, '_blank');
  }

  cambiarEstado(p: PedidoRow, nuevo: PedidoRow['estado']) {
    if (p.estado === nuevo) return;
    this.http.put<any>(`${this.backendBase}/admin/pedidos/${p.id}/estado`, { estado: nuevo })
      .subscribe({
        next: () => { p.estado = nuevo; },
        error: (err) => { console.error(err); alert('No se pudo actualizar el estado'); }
      });
  }
}
