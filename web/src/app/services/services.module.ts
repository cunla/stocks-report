import {NgModule} from '@angular/core';

import {PortfolioService} from "./portfolio.service";
import {HttpClientModule} from "@angular/common/http";

@NgModule({
    imports: [
        HttpClientModule,
    ],
    providers: [
        PortfolioService,
    ]
})
export class ServicesModule {
}
