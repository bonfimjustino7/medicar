import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './views/login/login.component';
import { CreateAccountComponent } from './views/create-account/create-account.component';
import { ProfileComponent } from './views/profile/profile.component';
import { NewConsutationComponent } from './views/new-consutation/new-consutation.component';
import { GuardService } from './auth/guard.service';
import { NotFoundComponent } from './components/not-found/not-found.component';


const routes: Routes = [
  {
    path: "account/new",
    component: CreateAccountComponent,
  },

  {
    path: "profile",
    component: ProfileComponent,
    canActivate: [GuardService]
  },

  {
    path: "consultation/new",
    component: NewConsutationComponent,
    canActivate: [GuardService]
  },
  {
    path: "",
    component: LoginComponent,
  },
  {
    path: "**",
    component: NotFoundComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
