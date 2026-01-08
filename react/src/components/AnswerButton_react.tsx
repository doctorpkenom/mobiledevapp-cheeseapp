import React from 'react';
import { TouchableOpacity, Text, View, StyleSheet, GestureResponderEvent } from 'react-native';
import Svg, { Path } from 'react-native-svg';

interface AnswerButtonProps {
    onPress: (event: GestureResponderEvent) => void;
    label?: string; // e.g. "A"
    text: string;
}

export const AnswerButton = ({ onPress, label, text }: AnswerButtonProps) => {
    return (
        <TouchableOpacity onPress={onPress} activeOpacity={0.8} style={styles.container}>
            <View style={styles.svgContainer}>
                <Svg width="300" height="70" viewBox="0 0 300 70">
                    <Path d="M10 10C5 10 2 15 2 25V50C2 60 8 68 20 68H280C292 68 298 60 298 50V25C298 15 292 10 280 10C260 8 240 12 220 10C180 6 140 12 100 10C60 8 30 12 10 10Z" fill="#FFF8E1" stroke="#1a1a1a" strokeWidth="3" />
                </Svg>
            </View>
            <View style={styles.content}>
                {label && <Text style={styles.label}>{label}: </Text>}
                <Text style={styles.text} numberOfLines={2} adjustsFontSizeToFit>{text}</Text>
            </View>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        width: 300,
        height: 70,
        justifyContent: 'center',
        alignItems: 'center',
        marginVertical: 5,
    },
    svgContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
    },
    content: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 20,
        width: '100%',
    },
    label: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#1a1a1a',
    },
    text: {
        fontSize: 16,
        color: '#1a1a1a',
        flex: 1,
        flexWrap: 'wrap',
    },
});
