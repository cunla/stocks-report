import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'stock/hsbc',
    pathMatch: 'full'
  },
  {
    path: 'portfolio/:id',
    loadChildren: () => import('./portfolio/portfolio.module').then(m => m.PortfolioPageModule)
  },
    {
    path: 'stock/:id',
    loadChildren: () => import('./portfolio/portfolio.module').then(m => m.PortfolioPageModule)
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
