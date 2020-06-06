import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  base_url = environment.base_url;

  constructor(private http: HttpClient) { }

  list(): Observable<any> {

    return this.http.get(this.base_url + 'consultas/')

  }

  desmarcarConsulta(idConsulta): Observable<any> {
    return this.http.delete(this.base_url + `consultas/${idConsulta}/`);
  }
}
