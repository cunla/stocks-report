import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule} from '@angular/forms';

import {IonicModule} from '@ionic/angular';


import {PortfolioPage} from './portfolio-page.component';
import {PortfolioPageRoutingModule} from "./portfolio-routing.module";
import {HighchartsChartModule} from "highcharts-angular";

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        IonicModule,
        PortfolioPageRoutingModule,
        HighchartsChartModule,
    ],
    declarations: [PortfolioPage]
})
export class PortfolioPageModule {
}
