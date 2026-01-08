import React from 'react';
import { Text, View, StyleSheet } from 'react-native';
import Svg, { Path } from 'react-native-svg';

interface QuestionCardProps {
    text: string;
}

export const QuestionCard = ({ text }: QuestionCardProps) => {
    return (
        <View style={styles.container}>
            <View style={styles.svgContainer}>
                <Svg width="350" height="150" viewBox="0 0 350 150">
                    <Path d="M10 10C5 10 2 15 2 25V125C2 135 5 145 20 145H330C345 145 348 135 348 125V25C348 15 345 10 330 10H20C15 10 10 10 10 10Z" fill="#FFF8E1" stroke="#1a1a1a" strokeWidth="3" />
                </Svg>
            </View>
            <View style={styles.content}>
                <Text style={styles.text} adjustsFontSizeToFit>{text}</Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        width: 350,
        height: 150,
        justifyContent: 'center',
        alignItems: 'center',
        marginVertical: 20,
    },
    svgContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
    },
    content: {
        padding: 20,
        width: '100%',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
    },
    text: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#1a1a1a',
        textAlign: 'center',
    },
});
