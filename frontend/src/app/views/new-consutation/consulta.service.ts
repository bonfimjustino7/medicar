import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ConsultaService {

  base_url = environment.base_url;

  constructor(private http: HttpClient) { }

  listEspecialidades(): Observable<any> {
    return this.http.get(this.base_url + 'especialidades/');
  }
  marcarConsulta(data): Observable<any> {
    return this.http.post(this.base_url + 'consultas/', data);
  }

}
