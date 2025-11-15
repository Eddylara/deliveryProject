import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  carouselImages = [
    'https://images.unsplash.com/photo-1600891964599-f61ba0e24092?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=2f2b3d0a6b4b2a5b4b0f3b0f3b0f3b0f',
    'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=6c9f6d4c6c6b6b6b6b6b6b6b6b6b6b6b',
    'https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3&s=1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d'
  ];

  active = 0;

  next() {
    this.active = (this.active + 1) % this.carouselImages.length;
  }

  prev() {
    this.active = (this.active - 1 + this.carouselImages.length) % this.carouselImages.length;
  }
}
