import React from 'react';
import { TouchableOpacity, Text, View, StyleSheet, GestureResponderEvent } from 'react-native';
import Svg, { Path } from 'react-native-svg';

interface BackButtonProps {
    onPress: (event: GestureResponderEvent) => void;
}

export const BackButton = ({ onPress }: BackButtonProps) => {
    return (
        <TouchableOpacity onPress={onPress} activeOpacity={0.8} style={styles.container}>
            <View style={styles.svgContainer}>
                <Svg width="100" height="50" viewBox="0 0 100 50">
                    <Path d="M5 10C2 10 2 15 2 25C2 35 5 45 15 45H85C95 45 98 35 98 25C98 15 95 5 85 5H15C10 5 8 10 5 10Z" fill="#FDD835" stroke="#1a1a1a" strokeWidth="3" />
                </Svg>
            </View>
            <Text style={styles.text}>Back</Text>
        </TouchableOpacity>
    );
};

const styles = StyleSheet.create({
    container: {
        width: 100,
        height: 50,
        justifyContent: 'center',
        alignItems: 'center',
        margin: 10,
    },
    svgContainer: {
        position: 'absolute',
        top: 0,
        left: 0,
    },
    text: {
        color: '#1a1a1a',
        fontSize: 16,
        fontWeight: 'bold',
    },
});
