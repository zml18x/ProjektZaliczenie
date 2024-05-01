import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CurrencyService } from '../currency.service';
import { CurrencyRate } from '../currencyRate.interface';

@Component({
  selector: 'app-currency',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './currency.component.html',
  styleUrl: './currency.component.css'
})
export class CurrencyComponent {
  currencyRates: CurrencyRate[] = [];
  selectedDate: string = '';
  selectedStartDate: string = '';
  selectedEndDate: string = '';

  constructor(private currencyService: CurrencyService){}

  fetchCurrentRates(){
    this.currencyService.getCurrentRates().subscribe((
      rates: CurrencyRate[]) => {
        this.currencyRates = rates;
      })
  };

  fetchSpecyficDateRates(){
    this.currencyService.getSpecyficDateRates(this.selectedDate).subscribe((
      rates: CurrencyRate[]) => {
        this.currencyRates = rates;
      })
  };

  fetchDateRangeRates(){
    this.currencyService.getDateRangeRates(this.selectedStartDate, this.selectedEndDate).subscribe((
      rates: CurrencyRate[]) => {
        this.currencyRates = rates;
      });
  }
}
