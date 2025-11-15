import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CartService } from '../cart.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule, RouterModule],
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.css']
})
export class CheckoutComponent {
  backendBase = 'http://127.0.0.1:8000';

  // Formulario
  nombre = '';
  apellido = '';
  documento = '';
  direccion = '';
  apto = '';
  telefono = '';
  notas = '';

  sending = false;
  error = '';
  successId: number | null = null;

  constructor(public cart: CartService, private http: HttpClient, private router: Router) {}

  total() { return this.cart.total(); }
  subtotal() { return this.cart.total(); }
  envio() { return this.subtotal() > 0 ? 5000 : 0; }
  totalFinal() { return this.subtotal() + this.envio(); }

  remove(id: number) { this.cart.remove(id); }

  updateCantidad(id: number, qty: string) {
    const n = Number(qty);
    if (Number.isFinite(n)) this.cart.updateCantidad(id, Math.max(1, Math.floor(n)));
  }

  incQty(id: number, current: number) {
    const next = (Number(current) || 0) + 1;
    this.cart.updateCantidad(id, next);
  }

  decQty(id: number, current: number) {
    const next = Math.max(1, (Number(current) || 1) - 1);
    this.cart.updateCantidad(id, next);
  }

  submit() {
    this.error = '';
    if (!this.cart.items().length) {
      this.error = 'Agrega productos al carrito primero';
      return;
    }
    if (!this.nombre || !this.apellido || !this.documento || !this.direccion || !this.telefono) {
      this.error = 'Completa los campos requeridos';
      return;
    }

    const payload = {
      nombre: this.nombre,
      apellido: this.apellido,
      documento: this.documento,
      direccion: this.direccion,
      apto: this.apto || null,
      telefono: this.telefono,
      notas: this.notas || null,
      items: this.cart.items().map(it => ({ comida_id: it.comida_id, cantidad: it.cantidad }))
    };

    this.sending = true;
    this.http.post<{ id: number, total: number, estado: string }>(`${this.backendBase}/pedido`, payload)
      .subscribe({
        next: (res) => {
          this.successId = res?.id ?? null;
          this.cart.clear();
          this.sending = false;
        },
        error: (err) => {
          console.error(err);
          this.error = err?.error?.detail || 'No se pudo crear el pedido';
          this.sending = false;
        }
      });
  }
}
