import React, { useEffect, useState, useMemo } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/types';
import { QuizEngine, Question } from '../logic/QuizEngine';
import { QuestionCard } from '../components/QuestionCard_react';
import { AnswerButton } from '../components/AnswerButton_react';
import { BackButton } from '../components/BackButton_react';

type Props = NativeStackScreenProps<RootStackParamList, 'Quiz'>;

export const QuizScreen = ({ navigation }: Props) => {
    const engine = useMemo(() => new QuizEngine(), []);
    const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        engine.startNewGame();
        loadNextQuestion();
    }, [engine]);

    const loadNextQuestion = () => {
        const q = engine.getNextQuestion();
        if (q) {
            setCurrentQuestion(q);
            setProgress(engine.getCurrentProgress());
        } else {
            // Quiz Finished
            finishQuiz();
        }
    };

    const finishQuiz = () => {
        const result = engine.calculateResult();
        if (result) {
            navigation.replace('Result', { cheese: result });
        } else {
            Alert.alert("Error", "Could not calculate a result. Use fallback.");
            navigation.goBack();
        }
    };

    const handleAnswer = (value: number | string) => {
        engine.submitAnswer(value);
        loadNextQuestion();
    };

    if (!currentQuestion) {
        return <View style={styles.container} />; // Loading or finished
    }

    const LABELS = ['A', 'B', 'C', 'D'];

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <BackButton onPress={() => navigation.goBack()} />
            </View>

            <ScrollView contentContainerStyle={styles.scrollContent}>
                <QuestionCard text={currentQuestion.text} />

                <View style={styles.optionsContainer}>
                    {currentQuestion.options.map((opt, index) => (
                        <AnswerButton
                            key={index}
                            label={LABELS[index]}
                            text={opt.label}
                            onPress={() => handleAnswer(opt.value)}
                        />
                    ))}
                </View>
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FFF8E1',
    },
    header: {
        paddingTop: 50, // Safe area
        paddingHorizontal: 20,
    },
    scrollContent: {
        alignItems: 'center',
        paddingVertical: 20,
    },
    optionsContainer: {
        marginTop: 20,
    },
});
