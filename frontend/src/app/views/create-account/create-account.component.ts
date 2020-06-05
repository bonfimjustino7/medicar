import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, NgForm } from '@angular/forms';
import { UserService } from './user.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-account',
  templateUrl: './create-account.component.html',
  styleUrls: ['./create-account.component.css']
})
export class CreateAccountComponent implements OnInit {

  hide = true;
  hide2 = true;

  email = new FormControl('', [Validators.required, Validators.email]);

  constructor(private userService: UserService, private snackBar: MatSnackBar, private router: Router) { }

  ngOnInit(): void {
  }

  create(f: NgForm) {
    if (f.valid) {

      this.userService.createUser(f.value).subscribe((user) => {
        localStorage.setItem('token', user.token);
        localStorage.setItem('name', user.first_name);
        localStorage.setItem('authenticate', 'true');

        this.snackBar.open('Usuário criado com sucesso', 'X', {
          duration: 3000,
          horizontalPosition: 'right',
          verticalPosition: 'top',
        });
        this.router.navigate(['/profile']);
      }, error => {

        if (error.error) {
          Object.values(error.error).map((e: string) => {
            this.snackBar.open(e, 'X', {
              duration: 3000,
              horizontalPosition: 'right',
              verticalPosition: 'top',
            });
          })
        }
      });

    }
  }

}
