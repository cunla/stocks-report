import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';


const PORTFOLIO_API = '/api/portfolios';
const PORTFOLIO_REPORT_API = '/api/portfolio-report';
const SYMBOLS_API = '/api/symbols';

@Injectable({
    providedIn: 'root'
})
export class PortfolioService {

    constructor(private http: HttpClient) {
    }

    public getPortfolios(q: string): Observable<any> {
        q = q || '';
        return this.http.get(`${PORTFOLIO_API}?q=${q}`);
    }

    public getPortfolio(id: number): Observable<any> {
        return this.http.get(`${PORTFOLIO_API}/${id}`);
    }


    public postPortfolio(name: string, mix: any): Observable<any> {
        const body = {
            name,
            mix,
        };
        return this.http.post(`${PORTFOLIO_API}`, body);
    }

    public getSymbols(q: string): Observable<any> {
        return this.http.get(`${SYMBOLS_API}?q=${q}`);
    }

    public portfolioReport(startDate: string,
                           endDate: string,
                           portfolio: any) {
        const body = {
            startDate,
            endDate,
            portfolio,
        };
        return this.http.post(`${PORTFOLIO_REPORT_API}`, body);
    }

}
