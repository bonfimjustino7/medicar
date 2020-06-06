import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../login/login.service';
import { ProfileService } from './profile.service';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { DialogComponent } from 'src/app/components/dialog/dialog.component';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  consultas: Array<any> = []

  name: string;

  constructor(private router: Router, private loginService: LoginService,
    private profileServise: ProfileService, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.name = localStorage.getItem('name');
    this.profileServise.list().subscribe(consultas => {
      console.log(consultas);
      this.consultas = [...consultas]
    })
  }

  logout(): void {
    console.log('Chamou o logout')
    this.loginService.desconectar();
    localStorage.removeItem('name');
    this.router.navigate([''])
  }

  desmarcar(consulta): void {
    this.profileServise.desmarcarConsulta(consulta.id).subscribe(e => {
      console.log('Desmarcando...');
      const consultas = this.consultas.filter(c => {
        return consulta.id != c.id
      });
      this.consultas = [...consultas];

    });
  }

  confirmar(consulta): void {
    let dialogRef = this.dialog.open(DialogComponent);

    dialogRef.afterClosed().subscribe(resposta => {
      if (resposta) {
        this.desmarcar(consulta);
      }
    })
  }
}
