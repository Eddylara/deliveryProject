import { Component, computed, signal } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { CartService } from './cart.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterModule, CommonModule],
  templateUrl: './app.shell.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('delevery-app');

  constructor(public cart: CartService) {}

  cartCount = computed(() => this.cart.items().reduce((n, it) => n + it.cantidad, 0));
  cartSubtotal = computed(() => this.cart.total());
}
