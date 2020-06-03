import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './views/login/login.component';
import { CreateAccountComponent } from './views/create-account/create-account.component';
import { ProfileComponent } from './views/profile/profile.component';


const routes: Routes = [
  {
    path: "",
    component: LoginComponent,
  },

  {
    path: "account/new",
    component: CreateAccountComponent
  },

  {
    path: "profile",
    component: ProfileComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }