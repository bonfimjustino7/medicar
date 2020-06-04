import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  baseUrl = 'http://localhost:8000/'
  constructor(private http: HttpClient) { }


  createUser(user: any): Observable<any> {
    return this.http.post<any>(this.baseUrl + 'cadastro/', user);
  }
}
