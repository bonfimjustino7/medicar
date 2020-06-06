import { Injectable } from "@angular/core";
import { HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';


@Injectable()
export class TokenInterceptor implements HttpInterceptor {

    constructor(private router: Router) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<any> {

        const token = localStorage.getItem('token')

        if (localStorage.getItem('authenticate')) {

            const newRequest = request.clone({ setHeaders: { 'Authorization': `Token ${token}` } })

            return next.handle(newRequest)
        }

        return next.handle(request);
    }

}