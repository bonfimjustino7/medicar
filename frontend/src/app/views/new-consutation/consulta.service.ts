import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConsultaService {

  base_url = 'http://localhost:8000/'

  constructor(private http: HttpClient) { }

  listEspecialidades(): Observable<any> {
    return this.http.get(this.base_url + 'especialidades/')
  }

}
