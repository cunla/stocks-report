import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {PortfolioService} from '../services/portfolio.service';
import {DateTime} from 'luxon';
import * as Highcharts from 'highcharts';
import HC_data from 'highcharts/modules/data';
import theme from 'highcharts/themes/dark-unica';
import {LoadingController} from '@ionic/angular';

HC_data(Highcharts);
theme(Highcharts);


export interface PortfolioResult {
    csv: string;
    startDate: string;
    endDate: string;
}

@Component({
    selector: 'app-portfolio',
    templateUrl: './portfolio-page.component.html',
    styleUrls: ['./portfolio-page.component.scss'],
})
export class PortfolioPage implements OnInit {
    private id;
    public title: string;
    isDataLoaded = false;
    Highcharts: typeof Highcharts = Highcharts;
    chartOptions: Highcharts.Options = {
        credits: {enabled: false},
        title: {text: 'Portfolio'},
        legend: {enabled: false,},
        series: [{type: 'spline', color: 'cyan', opacity: 0.7, lineWidth: 1,},
            {type: 'spline', color: 'orange', opacity: 0.2, lineWidth: 1,},
            {type: 'spline', color: 'orange', opacity: 0.2, lineWidth: 1,},
        ],
        tooltip: {shared: true,},
        plotOptions: {series: {marker: {enabled: false}}},
        data: {csv: '',},
        yAxis: {gridLineColor: '#383838',},
    };

    constructor(
        private activatedRoute: ActivatedRoute,
        private portfolioService: PortfolioService,
        private loadingController: LoadingController,) {

    }

    async ngOnInit() {
        const startDate = DateTime.local().minus({days: 90}).toISODate();
        const endDate = DateTime.local().toISODate();
        const id = this.activatedRoute.snapshot.paramMap.get('id').toUpperCase();
        const loading = await this.loadingController.create({
            message: 'Please wait...',
        });
        loading.present();
        if (isNaN(+id)) { // One symbol
            this.id = id;
            const portfolio = {};
            portfolio[this.id] = 1;
            this.portfolioService.getSymbols(this.id)
                .subscribe((res) => {
                    this.title = `${res[this.id]} (${this.id})`;
                    this.chartOptions.title.text = this.title;
                });
            this.portfolioService.portfolioReport(startDate, endDate, portfolio)
                .subscribe((res: PortfolioResult) => {
                    this.chartOptions.data.csv = res.csv;
                    this.isDataLoaded = true;
                    loading.dismiss();
                });
        } else { // Portfolio id number
            this.id = +id;
            this.portfolioService.getPortfolio(this.id).subscribe((portfolio) => {
                this.title = `${portfolio.name} `;
                this.chartOptions.title.text = this.title;
                this.portfolioService.portfolioReport(startDate, endDate, portfolio.mix)
                    .subscribe((res: PortfolioResult) => {
                        this.chartOptions.data.csv = res.csv;
                        this.isDataLoaded = true;
                        loading.dismiss();
                    });
            });
        }

    }

}
