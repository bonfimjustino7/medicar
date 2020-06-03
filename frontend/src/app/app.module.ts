import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatFormFieldModule } from '@angular/material/form-field'
import { MatInputModule } from '@angular/material/input'
import { MatToolbarModule } from '@angular/material/toolbar';
import { LoginComponent } from './views/login/login.component';
import { FormComponent } from './components/form/form.component'
import { MatCheckboxModule } from '@angular/material/checkbox'
import { MatButtonModule } from '@angular/material/button'
import { MatIconModule } from '@angular/material/icon';
import { CreateAccountComponent } from './views/create-account/create-account.component';
import { ProfileComponent } from './views/profile/profile.component';
import { MatCardModule } from '@angular/material/card';
import { TableComponent } from './components/table/table.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    FormComponent,
    CreateAccountComponent,
    ProfileComponent,
    TableComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatToolbarModule,
    MatCheckboxModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }