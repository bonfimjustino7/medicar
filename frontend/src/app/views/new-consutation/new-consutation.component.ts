import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ConsultaService } from './consulta.service';

@Component({
  selector: 'app-new-consutation',
  templateUrl: './new-consutation.component.html',
  styleUrls: ['./new-consutation.component.css']
})
export class NewConsutationComponent implements OnInit {

  hide = true;
  hide2 = true;

  especialidades: Array<any>;

  constructor(private consultaService: ConsultaService) { }

  ngOnInit(): void {
    this.consultaService.listEspecialidades().subscribe(r => {
      this.especialidades = [...r];
    })
  }

  marcar(f: NgForm) {
    if (f.valid) {
      console.log(f.value);
    }
  }

  has_medico(): boolean {
    return false;
  }

  has_data(): boolean {
    return false;
  }

  has_horario(): boolean {
    return false;
  }
}
