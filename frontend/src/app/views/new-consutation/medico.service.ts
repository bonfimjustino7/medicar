import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MedicoService {

  base_url = environment.base_url;

  constructor(private http: HttpClient) { }


  listar(filters: any): Observable<any> {
    let params = new HttpParams({
      fromObject: { ...filters }
    });

    return this.http.get(this.base_url + 'medicos/', {
      params: params
    })
  }
}
