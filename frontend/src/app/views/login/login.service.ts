import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class LoginService {

  base_url = 'http://localhost:8000/'

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
