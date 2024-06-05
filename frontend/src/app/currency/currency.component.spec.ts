import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { CurrencyComponent } from './currency.component';
import { CurrencyService } from '../currency.service';
import { CurrencyRate } from '../currencyRate.interface';
import { of } from 'rxjs';
import { By } from '@angular/platform-browser';

describe('CurrencyComponent', () => {
  let component: CurrencyComponent;
  let fixture: ComponentFixture<CurrencyComponent>;
  let currencyService: CurrencyService;
  let mockRates: CurrencyRate[];

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, FormsModule, CurrencyComponent],
      providers: [CurrencyService]
    }).compileComponents();

    fixture = TestBed.createComponent(CurrencyComponent);
    component = fixture.componentInstance;
    currencyService = TestBed.inject(CurrencyService);

    mockRates = [
      { date: new Date('2024-06-01'), currency: 'USD', rate: '1.1' },
      { date: new Date('2024-06-01'), currency: 'EUR', rate: '0.9' }
    ];

    spyOn(currencyService, 'getCurrentRates').and.returnValue(of(mockRates));
    spyOn(currencyService, 'getSpecyficDateRates').and.returnValue(of(mockRates));
    spyOn(currencyService, 'getDateRangeRates').and.returnValue(of(mockRates));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch current rates and update currencyRates', () => {
    component.fetchCurrentRates();
    expect(currencyService.getCurrentRates).toHaveBeenCalled();
    expect(component.currencyRates).toEqual(mockRates);
  });

  it('should fetch specific date rates and update currencyRates', () => {
    component.selectedDate = '2024-06-05';
    component.fetchSpecyficDateRates();
    expect(currencyService.getSpecyficDateRates).toHaveBeenCalledWith('2024-06-05');
    expect(component.currencyRates).toEqual(mockRates);
  });

  it('should fetch date range rates and update currencyRates', () => {
    component.selectedStartDate = '2024-06-01';
    component.selectedEndDate = '2024-06-05';
    component.fetchDateRangeRates();
    expect(currencyService.getDateRangeRates).toHaveBeenCalledWith('2024-06-01', '2024-06-05');
    expect(component.currencyRates).toEqual(mockRates);
  });

  it('should initialize with empty currencyRates and selected dates', () => {
    expect(component.currencyRates).toEqual([]);
    expect(component.selectedDate).toBe('');
    expect(component.selectedStartDate).toBe('');
    expect(component.selectedEndDate).toBe('');
  });

  it('should have required form fields', () => {
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('input[type="date"]')).toBeTruthy();
    const inputs = fixture.debugElement.queryAll(By.css('input[type="date"]'));
    expect(inputs.length).toBe(3);
  });

  it('should call fetchCurrentRates when "Pobierz dzisiejsze kursy" button is clicked', () => {
    spyOn(component, 'fetchCurrentRates');
    fixture.detectChanges();
    const button = fixture.debugElement.query(By.css('.action-container button')).nativeElement;
    button.click();
    expect(component.fetchCurrentRates).toHaveBeenCalled();
  });

  it('should call fetchSpecyficDateRates when "Pobierz kursy dla wybranej daty" button is clicked', () => {
    spyOn(component, 'fetchSpecyficDateRates');
    fixture.detectChanges();
    const button = fixture.debugElement.queryAll(By.css('.action-container button'))[1].nativeElement;
    button.click();
    expect(component.fetchSpecyficDateRates).toHaveBeenCalled();
  });

  it('should call fetchDateRangeRates when "Pobierz kursy dla wybranego okresu" button is clicked', () => {
    spyOn(component, 'fetchDateRangeRates');
    fixture.detectChanges();
    const button = fixture.debugElement.queryAll(By.css('.action-container button'))[2].nativeElement;
    button.click();
    expect(component.fetchDateRangeRates).toHaveBeenCalled();
  });

  it('should display fetched currency rates in table', () => {
    component.currencyRates = mockRates;
    fixture.detectChanges();
    const compiled = fixture.nativeElement;
    const rows = compiled.querySelectorAll('.data-table tbody tr') as NodeListOf<HTMLTableRowElement>;
    const filteredRows = Array.from(rows).filter((row) => row.querySelector('td'));
    expect(filteredRows.length).toBe(mockRates.length);
    expect(filteredRows[0].querySelector('td')?.textContent).toContain('USD');
    expect(filteredRows[0].querySelectorAll('td')[1]?.textContent).toContain('1.1');
  });
});
