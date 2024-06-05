import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { CurrencyService } from './currency.service';
import { CurrencyRate } from './currencyRate.interface';

describe('CurrencyService', () => {
  let service: CurrencyService;
  let httpMock: HttpTestingController;
  let apiBaseUrl: string;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CurrencyService]
    });
    service = TestBed.inject(CurrencyService);
    httpMock = TestBed.inject(HttpTestingController);
    apiBaseUrl = (service as any).apiBaseUrl;
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return current rates if not a weekend', () => {
    const mockRates: CurrencyRate[] = [{ date: new Date(), currency: 'USD', rate: '1.1' }];
    service.getCurrentRates().subscribe(rates => {
      expect(rates).toEqual(mockRates);
    });

    const req = httpMock.expectOne(apiBaseUrl + '/currency-rates/current');
    expect(req.request.method).toBe('GET');
    req.flush(mockRates);
  });

  it('should return an empty array if current date is a weekend', () => {
    spyOn(service as any, 'isWeekend').and.returnValue(true);
    service.getCurrentRates().subscribe(rates => {
      expect(rates).toEqual([]);
    });
  });

  it('should return rates for a specific date if not a weekend', () => {
    const mockRates: CurrencyRate[] = [{ date: new Date('2024-06-05'), currency: 'USD', rate: '1.2' }];
    const date = '2024-06-05';
    service.getSpecyficDateRates(date).subscribe(rates => {
      expect(rates).toEqual(mockRates);
    });

    const req = httpMock.expectOne(apiBaseUrl + '/currency-rates/date/' + date);
    expect(req.request.method).toBe('GET');
    req.flush(mockRates);
  });

  it('should return an empty array if specific date is a weekend', () => {
    spyOn(service as any, 'isWeekend').and.returnValue(true);
    service.getSpecyficDateRates('2024-06-08').subscribe(rates => {
      expect(rates).toEqual([]);
    });
  });

  it('should return rates for a date range', () => {
    const mockRates: CurrencyRate[] = [{ date: new Date('2024-06-01'), currency: 'USD', rate: '1.3' }];
    const startDate = '2024-06-01';
    const endDate = '2024-06-05';
    service.getDateRangeRates(startDate, endDate).subscribe(rates => {
      expect(rates).toEqual(mockRates);
    });

    const req = httpMock.expectOne(apiBaseUrl + '/currency-rates/range/' + startDate + '/' + endDate);
    expect(req.request.method).toBe('GET');
    req.flush(mockRates);
  });

  it('should correctly identify weekends', () => {
    expect(service['isWeekend']('2024-06-01')).toBe(true);
    expect(service['isWeekend']('2024-06-02')).toBe(true);
    expect(service['isWeekend']('2024-06-03')).toBe(false);
  });
});
