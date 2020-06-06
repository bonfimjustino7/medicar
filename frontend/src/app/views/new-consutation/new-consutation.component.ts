import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ConsultaService } from './consulta.service';
import { Location } from '@angular/common';
import { AgendaService } from './agenda.service';
import { MedicoService } from './medico.service';
import { MatSnackBar } from '@angular/material/snack-bar';


@Component({
  selector: 'app-new-consutation',
  templateUrl: './new-consutation.component.html',
  styleUrls: ['./new-consutation.component.css']
})
export class NewConsutationComponent implements OnInit {

  hide = true;
  hide2 = true;

  especialidades: Array<any> = [];
  medicos: Array<any> = [];
  datas: Array<any> = [];
  horarios: Array<any> = [];

  filtros: any = {};

  consulta: any = {};

  constructor(
    private consultaService: ConsultaService,
    private location: Location,
    private agendaService: AgendaService,
    private medicoService: MedicoService,
    private snackBar: MatSnackBar,
  ) { }

  ngOnInit(): void {
    this.consultaService.listEspecialidades().subscribe(r => {
      this.especialidades = [...r];
    })
  }

  listarAgenda(filter: any): void {
    this.agendaService.agendasDisponiveis(filter).subscribe(agenda => {
      agenda.map(a => {
        this.horarios = [...a.horario]
        this.datas.push(a.dia);
      });
    });
  }

  handleEspecialidade(e): void {
    this.horarios = [];
    this.datas = [];
    this.medicoService.listar({ especialidade: e }).subscribe(medicos => {
      this.medicos = [...medicos];
    })
  }

  handleMedicos(e): void {
    this.datas = [];
    this.horarios = [];
    this.filtros.medico = e;

    this.agendaService.agendasDisponiveis({ medico: e }).subscribe(agenda => {
      agenda.map(a => {
        this.datas.push({ id: a.id, data: a.dia });
      });
    });


  }

  handleData(dataObject): void {
    this.consulta.agenda_id = dataObject.id;
    this.filtros.data_inicio = dataObject.data;
    this.filtros.data_final = dataObject.data;

    this.horarios = [];

    this.agendaService.agendasDisponiveis(this.filtros).subscribe(agenda => {
      agenda.map(a => {
        this.horarios = [...a.horario]
      });
    });

  }

  handleHorario(horario): void {
    this.consulta.horario = horario;

  }

  // Actions Buttons
  goBack(): void {
    this.location.back();
  }
  marcarConsulta(f: NgForm) {
    if (f.valid) {

      this.consultaService.marcarConsulta(this.consulta).subscribe(consulta => {
        this.snackBar.open('Consulta marcada com sucesso', 'x', {
          duration: 2000,
          verticalPosition: 'top',
          horizontalPosition: 'right',
        });
        this.goBack();
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
