import {NgModule} from '@angular/core';

import {PortfolioService} from "./portfolio.service";
import {HttpClientModule} from "@angular/common/http";

@NgModule({
    entryComponents: [],
    imports: [HttpClientModule,],
    providers: [
        PortfolioService,
    ]
})
export class ServicesModule {
}
