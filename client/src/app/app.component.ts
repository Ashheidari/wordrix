import { Component } from '@angular/core';
import {ApiService} from "./appService";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  userInput: string = '';
  message: string = '';
  hint: { word: string; score: number; isError: boolean } | null = null;
  showCongratulations: boolean = false;
  winningWord: string = '';
  foreignWord: string = '';
  lastSubmission: { word: string; score: number } | null = null;

  guesses: { word: string; score: number }[] = [];
  guessMap: Map<string, number> = new Map(); // Fast lookup map

  constructor(private apiService: ApiService) {
    this.apiService.getWord().subscribe({
      next: response => {
        console.log('Success:', response);
        this.winningWord = response.english.trim().toLowerCase();
        this.foreignWord = response.spanish.trim().toLowerCase();
      },
      error: error => console.error('getWord Error:', error)
    });
  }

  async guessWord() {
    const trimmedInput = this.userInput.trim().toLowerCase();

    if (!trimmedInput) return; // Prevent empty guesses

    if (this.guessMap.has(trimmedInput)) {
      this.message = `Duplicate word entered: "${trimmedInput}"`;
    } else {
      const score = await this.calculateScore(trimmedInput);

      this.guessMap.set(trimmedInput, score);
      this.lastSubmission = {word: trimmedInput, score};

      if (score === 100 || this.winningWord == trimmedInput) {
        this.showCongratulations = true;
      } else {
        this.guesses.push(this.lastSubmission);
        this.guesses.sort((a, b) => b.score - a.score); // Sort from highest to lowest
      }

      this.message = ''; // Clear error message
    }

    this.userInput = ''; // Reset input field
  }

  getHint(): void {
    if (this.guesses.length === 0) {
      this.hint = { word: "No guesses yet! Try guessing first.", score: -1, isError: true };
      return;
    }

    // Find a word in the list with a higher score than the highest guessed score
    const hint = { word: "hint unavailable", score: -1}
    console.log(`sam hint ${JSON.stringify(hint)}`);

    if (hint) {
      this.hint = { ...hint, isError: false };
    } else {
      this.hint = { word: "No hints available. Keep guessing!", score: -1, isError: true };
    }
  }


  calculateScore(word: string): Promise<number> {
    return new Promise((resolve, reject) => {
      this.apiService.getSimilarity(this.winningWord, word).subscribe({
        next: response => {
          console.log('getSimilarity Success:', response);
          resolve(response.similarity);
        },
        error: error => {
          console.error('getSimilarity Error:', error);
          reject(error);
        }
      });
    });
  }


  resetGame() {
    this.showCongratulations = false;
    this.guesses = [];
    this.lastSubmission = null;
    this.message = '';
    this.userInput = '';
    this.hint = null;
  }
}
