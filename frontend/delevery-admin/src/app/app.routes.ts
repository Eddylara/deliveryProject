import { Routes } from '@angular/router';

export const routes: Routes = [
	{ path: '', redirectTo: 'login', pathMatch: 'full' },
	{ path: 'login', loadComponent: () => import('./login/login.component').then(m => m.LoginComponent) },
	{ path: 'panel', loadComponent: () => import('./admin-panel/admin-panel.component').then(m => m.AdminPanelComponent) },
	{ path: 'pedidos', loadComponent: () => import('./orders/orders.component').then(m => m.OrdersComponent) }
];
