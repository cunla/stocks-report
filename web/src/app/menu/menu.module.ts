import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {MenuComponent} from "./menu.component";
import {StocksListComponent} from "./stocks-list/stocks-list.component";
import {IonicModule} from "@ionic/angular";
import {RouterModule} from "@angular/router";
import {AutoCompleteModule} from "ionic4-auto-complete";
import {StocksAutocompleteService} from "./stocks.autocomplete.service";


@NgModule({
    declarations: [
        MenuComponent,
        StocksListComponent,
    ],
    imports: [
        CommonModule,
        IonicModule,
        RouterModule,
        AutoCompleteModule,
    ],
    exports: [
        MenuComponent,
    ],
    providers: [StocksAutocompleteService,],
})
export class MenuModule {
}
