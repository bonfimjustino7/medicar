import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
@Injectable({
  providedIn: 'root'
})
export class UserService {

  baseUrl = environment.base_url;
  constructor(private http: HttpClient) { }


  createUser(user: any): Observable<any> {
    return this.http.post<any>(this.baseUrl + 'cadastro/', user);
  }
}
