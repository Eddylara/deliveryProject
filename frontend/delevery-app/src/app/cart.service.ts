import { Injectable, signal } from '@angular/core';

export interface CartItem {
  comida_id: number;
  nombre: string;
  precio: number;
  cantidad: number;
  foto?: string;
}

@Injectable({ providedIn: 'root' })
export class CartService {
  private storageKey = 'cart-v1';
  items = signal<CartItem[]>(this.load());

  private load(): CartItem[] {
    try {
      const raw = localStorage.getItem(this.storageKey);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) return parsed;
    } catch {}
    return [];
  }

  private persist() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.items()))
    } catch {}
  }

  clear() {
    this.items.set([]);
    this.persist();
  }

  add(item: Omit<CartItem, 'cantidad'>, cantidad = 1) {
    const current = this.items();
    const idx = current.findIndex(x => x.comida_id === item.comida_id);
    if (idx >= 0) {
      current[idx] = { ...current[idx], cantidad: current[idx].cantidad + cantidad };
      this.items.set([...current]);
    } else {
      this.items.set([...current, { ...item, cantidad }]);
    }
    this.persist();
  }

  updateCantidad(comida_id: number, cantidad: number) {
    const current = this.items();
    const idx = current.findIndex(x => x.comida_id === comida_id);
    if (idx >= 0) {
      const next = [...current];
      next[idx] = { ...next[idx], cantidad: Math.max(1, cantidad) };
      this.items.set(next);
      this.persist();
    }
  }

  remove(comida_id: number) {
    this.items.set(this.items().filter(x => x.comida_id !== comida_id));
    this.persist();
  }

  total() {
    return this.items().reduce((acc, it) => acc + it.precio * it.cantidad, 0);
  }
}
