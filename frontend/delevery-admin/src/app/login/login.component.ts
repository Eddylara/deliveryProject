import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username = '';
  password = '';
  error = '';
  backendBase = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    this.error = '';
    this.http.post<{ authorized: boolean }>(`${this.backendBase}/admin/login`, {
      username: this.username,
      password: this.password
    }).subscribe({
      next: (res) => {
        if (res?.authorized) {
          localStorage.setItem('isAdmin', '1');
          this.router.navigate(['/panel']);
        } else {
          this.error = 'Credenciales inválidas';
        }
      },
      error: () => {
        this.error = 'Credenciales inválidas';
      }
    });
  }
}
