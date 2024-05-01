import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { CurrencyRate } from './currencyRate.interface';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {
  private apiBaseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getCurrentRates(): Observable<CurrencyRate[]>{
    const currentDate = new Date();

    if(this.isWeekend(currentDate.toString())){
      return of([]);
    }
    
    return this.http.get<CurrencyRate[]>(this.apiBaseUrl + '/currency-rates/current');
  }

  getSpecyficDateRates(date: string): Observable<CurrencyRate[]>{
    if(this.isWeekend(date))
      return of([]);

    return this.http.get<CurrencyRate[]>(this.apiBaseUrl + '/currency-rates/date/' + date);
  }

  getDateRangeRates(startDate: string, endDate: string): Observable<CurrencyRate[]>{
    return this.http.get<CurrencyRate[]>(this.apiBaseUrl + '/currency-rates/range/' + startDate
      + '/' + endDate);
  }

  private isWeekend(date: string): boolean{
    const dayOfWeek = new Date(date).getDay();

    return dayOfWeek === 0 || dayOfWeek === 6;
  }
}
