import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, NgForm } from '@angular/forms';
import { LoginService } from './login.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  hide = true;

  center = true;

  constructor(private loginService: LoginService, private snackBar: MatSnackBar, private router: Router, private title: Title) { }

  ngOnInit(): void {
    this.title.setTitle('Login')

  }

  logar(f: NgForm): void {
    const { checked, password } = f.value;
    if (checked) {
      console.log(password)
    }

    if (f.valid) {
      this.loginService.authenticate(f.value).subscribe((user: any) => {
        this.snackBar.open('Usuário Logado com sucesso', 'x', {
          duration: 3000,
          horizontalPosition: 'right',
          verticalPosition: 'top',
        });
        // console.log(token.token)
        localStorage.setItem('token', user.token);
        localStorage.setItem('name', user.name);

        setTimeout(() => {
          this.router.navigate(['/profile']);
        }, 700)

      }, error => {
        const { non_field_errors } = error.error
        this.snackBar.open(non_field_errors[0], 'x', {
          duration: 3000,
          horizontalPosition: 'right',
          verticalPosition: 'top',
        })
      });
    }
  }
}
