import { Component, OnInit } from '@angular/core';

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

  constructor() { }

  ngOnInit(): void {
  }

}
