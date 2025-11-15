import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterModule],
  templateUrl: './app.shell.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('delevery-app');
}
