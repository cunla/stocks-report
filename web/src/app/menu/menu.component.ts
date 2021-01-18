import {Component, OnInit} from '@angular/core';
import {StocksAutocompleteService} from "./stocks.autocomplete.service";
import {Router} from "@angular/router";
import {MenuController} from "@ionic/angular";

@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.scss'],
})
export class MenuComponent implements OnInit {
    public selectedIndex = 0;
    public appPages = [
        {
            title: 'HSBC',
            url: '/stock/HSBC',
            icon: 'mail'
        },
    ];
    public labels = ['HSBC', 'AAPL', 'TSLA', 'VYMI', 'AMZN'];

    constructor(private menu: MenuController,
                private router: Router,
                public stocksService: StocksAutocompleteService,) {
    }

    ngOnInit() {
        const path = window.location.pathname;
        this.selectedIndex = this.appPages.findIndex(page => page.url.toLowerCase() === path.toLowerCase());
    }

    itemSelected(stock: any) {
        this.labels.push(stock.symbol);
        this.menu.close().then();
        this.router.navigateByUrl(`/stock/${stock.symbol}`).then();
    }
}
