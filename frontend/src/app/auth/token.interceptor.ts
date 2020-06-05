import { Injectable } from "@angular/core";
import { HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';


@Injectable()
export class TokenInterceptor implements HttpInterceptor {

    constructor(private router: Router) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<any> {
        console.log('Passou pelo Interceptor');
        const token = localStorage.getItem('token')
        console.log(token)
        if (localStorage.getItem('authenticate')) {
            console.log('Passando token')
            const newRequest = request.clone({ setHeaders: { 'Authorization': `Token ${token}` } })

            return next.handle(newRequest)
        }

        return next.handle(request);
    }

}