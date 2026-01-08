import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { PrimaryButton } from '../PrimaryButton_react';
import { AnswerButton } from '../AnswerButton_react';
import { BackButton } from '../BackButton_react';
import { QuestionCard } from '../QuestionCard_react';

describe('UI Components', () => {
    test('PrimaryButton renders and handles press', () => {
        const onPress = jest.fn();
        const { getByText } = render(<PrimaryButton title="Test Btn" onPress={onPress} />);

        expect(getByText('Test Btn')).toBeTruthy();
        fireEvent.press(getByText('Test Btn'));
        expect(onPress).toHaveBeenCalled();
    });

    test('AnswerButton renders text and label', () => {
        const onPress = jest.fn();
        const { getByText } = render(<AnswerButton text="Cheat Code" label="A" onPress={onPress} />);

        expect(getByText('A: ')).toBeTruthy();
        expect(getByText('Cheat Code')).toBeTruthy();
    });

    test('BackButton renders', () => {
        const onPress = jest.fn();
        const { getByText } = render(<BackButton onPress={onPress} />);
        expect(getByText('Back')).toBeTruthy();
    });

    test('QuestionCard renders text', () => {
        const { getByText } = render(<QuestionCard text="Is this a test?" />);
        expect(getByText('Is this a test?')).toBeTruthy();
    });
});
