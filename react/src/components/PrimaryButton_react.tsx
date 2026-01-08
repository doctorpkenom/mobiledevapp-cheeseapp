import React from 'react';
import { TouchableOpacity, Text, View, StyleSheet, GestureResponderEvent } from 'react-native';
import Svg, { Path } from 'react-native-svg';

interface ButtonProps {
    onPress: (event: GestureResponderEvent) => void;
    title: string;
}

export const PrimaryButton = ({ onPress, title }: ButtonProps) => {
    return (
        <TouchableOpacity onPress={onPress} activeOpacity={0.8} style={styles.container}>
            <View style={styles.svgContainer}>
                <Svg width="300" height="80" viewBox="0 0 300 80">
                    <Path d="M5 15C5 10 10 5 20 5H280C290 5 295 10 295 15V65C295 72 290 75 280 75H20C10 75 5 70 5 65V15Z" fill="#1a1a1a" />
                    <Path d="M5 10C5 5 10 0 20 0H280C290 0 295 5 295 10V60C295 67 290 70 280 70H20C10 70 5 65 5 60V10Z" fill="#FFB74D" stroke="#1a1a1a" strokeWidth="3" />
                </Svg>
            </View>
            <Text style={styles.text}>{title}</Text>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        width: 300,
        height: 80,
        justifyContent: 'center',
        alignItems: 'center',
        marginVertical: 10,
    },
    svgContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
    },
    text: {
        color: '#1a1a1a',
        fontSize: 24,
        fontWeight: 'bold',
        fontFamily: 'System', // Or custom font if added later
        marginBottom: 5, // Visual adjustment for the 3D effect offset
    },
});
