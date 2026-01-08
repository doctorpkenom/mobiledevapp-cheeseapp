import React from 'react';
import { View, Text, StyleSheet, ImageBackground } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/types';
import { PrimaryButton } from '../components/PrimaryButton_react';

type Props = NativeStackScreenProps<RootStackParamList, 'Welcome'>;

export const WelcomeScreen = ({ navigation }: Props) => {
    return (
        <View style={styles.container}>
            {/* Background Image ideally, or simple color */}
            <View style={styles.titleContainer}>
                <Text style={styles.title}>What Cheese</Text>
                <Text style={styles.subtitle}>Are You?</Text>
            </View>

            <View style={styles.centerImage}>
                {/* Placeholder for mascot or main cheese image */}
                <Text style={{ fontSize: 50 }}>🧀</Text>
            </View>

            <Text style={styles.description}>
                An existentially terrifying personality quiz.
            </Text>

            <View style={styles.footer}>
                <PrimaryButton
                    title="Start The Roast"
                    onPress={() => navigation.navigate('Quiz')}
                />
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FFF8E1', // Cream background
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingVertical: 60,
        paddingHorizontal: 20,
    },
    titleContainer: {
        alignItems: 'center',
    },
    title: {
        fontSize: 42,
        fontWeight: 'bold',
        color: '#1a1a1a',
    },
    subtitle: {
        fontSize: 42,
        fontWeight: 'bold',
        color: '#FDD835', // Yellow
        textShadowColor: 'rgba(0, 0, 0, 0.1)',
        textShadowOffset: { width: 2, height: 2 },
        textShadowRadius: 10,
    },
    centerImage: {
        justifyContent: 'center',
        alignItems: 'center',
        height: 200,
    },
    description: {
        fontSize: 18,
        textAlign: 'center',
        fontStyle: 'italic',
        color: '#666',
        marginHorizontal: 40,
    },
    footer: {
        marginBottom: 20,
    },
});
