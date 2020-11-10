import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {MenuComponent} from "./menu.component";
import {StocksListComponent} from "./stocks-list/stocks-list.component";
import {IonicModule} from "@ionic/angular";
import {RouterModule} from "@angular/router";


@NgModule({
    declarations: [
        MenuComponent,
        StocksListComponent,
    ],
    imports: [
        CommonModule,
        IonicModule,
        RouterModule
    ],
    exports:[
      MenuComponent,
    ],
})
export class MenuModule {
}
