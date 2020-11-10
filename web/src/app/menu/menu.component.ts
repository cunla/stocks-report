import {Component, OnInit} from '@angular/core';

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

    constructor() {
    }

    ngOnInit() {
        const path = window.location.pathname;
        this.selectedIndex = this.appPages.findIndex(page => page.url.toLowerCase() === path.toLowerCase());
    }

}
