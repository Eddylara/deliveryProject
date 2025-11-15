import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface MenuItem {
  name: string;
  description?: string;
  imageUrl?: string; // Dejar vacío para que el usuario agregue la imagen manualmente
}

interface MenuSection {
  title: string;
  items: MenuItem[];
}

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  restaurantName = 'Sabor y Mar Cartagena';

  sections: MenuSection[] = [
    {
      title: '🍣 SUSHI',
      items: [
        { name: 'California Roll', imageUrl: '' },
        { name: 'Philadelphia Roll', imageUrl: '' },
        { name: 'Kani Roll (cangrejo)', imageUrl: '' }
      ]
    },
    {
      title: '🍔 Hamburguesas',
      items: [
        { name: 'Clásica con queso', imageUrl: '' },
        { name: 'Doble carne/doble queso', imageUrl: '' },
        { name: 'BBQ Bacon', imageUrl: '' }
      ]
    },
    {
      title: 'Perros calientes',
      items: [
        { name: 'Perro americano', imageUrl: '' },
        { name: 'Perro costeño (con papitas y cebolla)', imageUrl: '' }
      ]
    },
    {
      title: 'Pizzas personales',
      items: [
        { name: 'Margarita', imageUrl: '' },
        { name: 'Hawaiana', imageUrl: '' },
        { name: 'Pepperoni', imageUrl: '' }
      ]
    },
    {
      title: '🥤 BEBIDAS',
      items: [
        { name: 'Gaseosas', imageUrl: '' },
        { name: 'Jugos naturales', imageUrl: '' },
        { name: 'Limonada de coco', imageUrl: '' },
        { name: 'Té frío', imageUrl: '' }
      ]
    },
    {
      title: '🍰 POSTRES',
      items: [
        { name: 'Cheesecake', imageUrl: '' },
        { name: 'Rollo de banana frito', imageUrl: '' },
        { name: 'Helado artesanal', imageUrl: '' }
      ]
    }
  ];

  /** Genera una sugerencia de nombre de archivo para la imagen del plato */
  getSuggestedFilename(sectionTitle: string, itemIndex: number) {
    const safe = (sectionTitle || '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 10);
    return `assets/menu/imagen-${safe}-${itemIndex + 1}.jpg`;
  }
}
