import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})

export class LoginService {

  base_url = environment.base_url;


  // private has_authenticate = false;

  constructor(private http: HttpClient) { }


  authenticate(credenials: any): Observable<Object> {
    delete credenials.checked;
    const response = this.http.post<Object>(this.base_url + 'api-token-auth/', credenials);

    response.subscribe(_ => {
      localStorage.setItem('authenticate', 'true');

    }, _ => localStorage.removeItem('authenticate'))

    return response
  }

  is_authenticate(): boolean {

    if (localStorage.getItem('authenticate'))
      return true

    return false
  }

  desconectar(): void {
    localStorage.removeItem('authenticate')
  }
}
