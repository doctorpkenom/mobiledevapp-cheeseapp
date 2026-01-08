import questionsData from '../../assets/questions.json';
import cheesesData from '../../assets/cheeses.json';

export interface QuestionOption {
    label: string;
    value: number | string; // number for score, string for "LACTOSE_YES" logic
}

export interface Question {
    id: number;
    type: string;
    text: string;
    options: QuestionOption[];
}

export interface Cheese {
    name: string;
    score: number;
    description: string;
    image: string;
}

export class QuizEngine {
    private questions: Question[];
    private cheeses: Cheese[];
    private currentSessionQuestions: Question[];
    private currentScore: number;
    private questionIndex: number;

    constructor(questions?: Question[], cheeses?: Cheese[]) {
        // Cast imported JSON to types (assuming JSON structure matches)
        this.questions = (questions || questionsData) as Question[];
        this.cheeses = (cheeses || cheesesData) as Cheese[];
        this.currentSessionQuestions = [];
        this.currentScore = 0;
        this.questionIndex = 0;
    }

    startNewGame(numQuestions = 10) {
        this.currentScore = 0;
        this.questionIndex = 0;

        // 1. Pick 10 random questions
        const shuffled = [...this.questions].sort(() => 0.5 - Math.random());
        this.currentSessionQuestions = shuffled.slice(0, Math.min(numQuestions, shuffled.length));

        // 2. Add Mandatory Lactose Intolerant Question
        const lactoseQuestion: Question = {
            id: 999,
            type: "choice",
            text: "Final Question: Are you lactose intolerant?",
            options: [
                { label: "Yes, sadly.", value: "LACTOSE_YES" },
                { label: "No, I am strong.", value: 0 }
            ]
        };
        this.currentSessionQuestions.push(lactoseQuestion);
    }

    getNextQuestion(): Question | null {
        if (this.questionIndex < this.currentSessionQuestions.length) {
            return this.currentSessionQuestions[this.questionIndex];
        }
        return null;
    }

    submitAnswer(value: number | string) {
        if (value === "LACTOSE_YES") {
            this.currentScore = -100;
        } else {
            if (typeof value === 'number') {
                this.currentScore += value;
            }
        }
        this.questionIndex++;
    }

    getCurrentProgress(): number {
        return this.questionIndex / this.currentSessionQuestions.length;
    }

    calculateResult(): Cheese | null {
        // 1. Handle Special Case
        if (this.currentScore === -100) {
            return this.cheeses.find(c => c.score === -100) || null;
        }

        // 2. Exact Match
        const exact = this.cheeses.find(c => c.score === this.currentScore);
        if (exact) return exact;

        // 3. Find Neighbors
        const sortedCheeses = [...this.cheeses].sort((a, b) => a.score - b.score);
        let lowerCheese: Cheese | null = null;
        let upperCheese: Cheese | null = null;

        for (const cheese of sortedCheeses) {
            if (cheese.score < this.currentScore) {
                lowerCheese = cheese;
            } else if (cheese.score > this.currentScore) {
                upperCheese = cheese;
                break;
            }
        }

        // 4. Coin Flip Logic
        if (lowerCheese && upperCheese) {
            return Math.random() < 0.5 ? lowerCheese : upperCheese;
        }

        if (lowerCheese && !upperCheese) return lowerCheese;
        if (upperCheese && !lowerCheese) return upperCheese;

        return null;
    }
}
