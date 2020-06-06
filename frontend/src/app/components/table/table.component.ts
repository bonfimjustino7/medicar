import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css']
})
export class TableComponent implements OnInit {

  @Input() consultas: Array<any> = []
  @Output() selecionado = new EventEmitter();

  constructor() { }

  ngOnInit(): void {

  }

  escolher(consulta): void {
    this.selecionado.emit(consulta);
  }

}
