import { Cheese } from '../logic/QuizEngine';

export type RootStackParamList = {
    Welcome: undefined;
    Quiz: undefined;
    Result: { cheese: Cheese };
};
