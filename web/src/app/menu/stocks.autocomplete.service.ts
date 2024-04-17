import {Injectable} from '@angular/core';
import {map} from 'rxjs/operators';

import {HttpClient} from '@angular/common/http';

import {AutoCompleteService} from '../autocomplete/auto-complete.service';

const SYMBOLS_API = '/api/symbols-list';

@Injectable()
export class StocksAutocompleteService implements AutoCompleteService {
    labelAttribute = 'name';
    formValueAttribute = 'numericCode';

    constructor(private http: HttpClient) {
    }

    getResults(keyword: string) {
        if (!keyword) {
            return false;
        }
        return this.http.get(`${SYMBOLS_API}?q=${keyword}`);
    }
}
