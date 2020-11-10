import {Component, Input, OnInit} from '@angular/core';

@Component({
    selector: 'app-stocks-list',
    templateUrl: './stocks-list.component.html',
    styleUrls: ['./stocks-list.component.scss'],
})
export class StocksListComponent implements OnInit {
    @Input('labels') labels = [];

    constructor() {
    }

    ngOnInit() {
    }

}
