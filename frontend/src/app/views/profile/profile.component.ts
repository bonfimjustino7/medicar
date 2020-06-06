import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../login/login.service';
import { ProfileService } from './profile.service';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { DialogComponent } from 'src/app/components/dialog/dialog.component';
import { environment } from 'src/environments/environment';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  consultas: Array<any> = []

  name: string;

  constructor(private router: Router, private loginService: LoginService,
    private profileServise: ProfileService, private dialog: MatDialog, private title: Title) { }

  ngOnInit(): void {
    this.name = localStorage.getItem('name');
    this.profileServise.list().subscribe(consultas => {

      this.consultas = [...consultas]
    });
    this.title.setTitle('Home - ' + environment.title_base);
  }

  logout(): void {

    this.loginService.desconectar();
    localStorage.removeItem('name');
    localStorage.removeItem('token');
    this.router.navigate([''])
  }

  desmarcar(consulta): void {
    this.profileServise.desmarcarConsulta(consulta.id).subscribe(e => {

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
