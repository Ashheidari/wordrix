import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) {}

  getWord(): Observable<any> {
    return this.http.get('http://wordrix.live/api/v1/random_word');
  }

  getSimilarity(targetWord: string, guessWord: string): Observable<any> {
    return this.http.post('http://wordrix.live/api/v1/similarity', {
      "guess_word": guessWord,
      "generated_word": targetWord
    });
  }

  getHint(targetWord: string, highScore: number): Observable<any> {
    return this.http.post('http://wordrix.live/api/v1/hint', {
      "generated_word": targetWord,
      "score": highScore
    });
  }
}
