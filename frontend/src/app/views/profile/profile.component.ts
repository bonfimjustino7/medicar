import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from '../login/login.service';
import { ProfileService } from './profile.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  consultas: Array<any> = [
    {
      especialidade: 'Cardiologia',
      medico: 'Dr. Carlos Ferreira',
      data: '03/06/2020',
      hora: '17:00'
    },
    {
      especialidade: 'Cardiologia',
      medico: 'Dr. Carlos Ferreira',
      data: '03/06/2020',
      hora: '17:00'
    },
    {
      especialidade: 'Cardiologia',
      medico: 'Dr. Carlos Ferreira',
      data: '03/06/2020',
      hora: '17:00'
    },
    {
      especialidade: 'Cardiologia',
      medico: 'Dr. Carlos Ferreira',
      data: '03/06/2020',
      hora: '13:00'
    },
  ]

  name: string;
  constructor(private router: Router, private loginService: LoginService,
    private profileServise: ProfileService) { }

  ngOnInit(): void {
    this.name = localStorage.getItem('name');
    this.profileServise.list().subscribe(e => {
      console.log(e);
      this.consultas = e.data
    })
  }

  logout(): void {
    console.log('Chamou o logout')
    this.loginService.desconectar();
    localStorage.removeItem('name');
    this.router.navigate([''])
  }
}
