import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, NgForm } from '@angular/forms';
import { LoginService } from './login.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  hide = true;


  constructor(private loginService: LoginService, private snackBar: MatSnackBar, private router: Router) { }

  ngOnInit(): void {
    localStorage.clear();
  }

  logar(f: NgForm): void {
    const { checked, password } = f.value;
    if (checked) {
      console.log(password)
    }

    if (f.valid) {
      this.loginService.authenticate(f.value).subscribe((user: any) => {
        this.snackBar.open('Usuário Logado com sucesso', 'X', {
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
        this.snackBar.open(non_field_errors[0], 'X', {
          duration: 3000,
          horizontalPosition: 'right',
          verticalPosition: 'top',
        })
      });
    }
  }
}
