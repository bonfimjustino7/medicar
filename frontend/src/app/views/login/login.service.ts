import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class LoginService {

  base_url = 'http://localhost:8000/'

  constructor(private snackBar: MatSnackBar, private http: HttpClient) { }


  authenticate(credenials: any): Observable<Object> {
    delete credenials.checked;
    return this.http.post<Object>(this.base_url + 'api-token-auth/', credenials);

  }
}
