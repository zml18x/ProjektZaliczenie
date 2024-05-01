import { Routes } from '@angular/router';
import { CurrencyComponent } from './currency/currency.component';

export const routes: Routes = [
    {path: '', redirectTo: 'currency', pathMatch: 'full'},
    {path: 'currency', component: CurrencyComponent}
];
