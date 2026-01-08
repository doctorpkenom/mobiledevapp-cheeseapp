import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/types';
import { PrimaryButton } from '../components/PrimaryButton_react';
import { CheeseImages } from '../utils/imageMap';

type Props = NativeStackScreenProps<RootStackParamList, 'Result'>;

export const ResultScreen = ({ route, navigation }: Props) => {
    const { cheese } = route.params;

    const imageSource = CheeseImages[cheese.image];

    return (
        <View style={styles.container}>
            <ScrollView contentContainerStyle={styles.scrollContent}>
                <Text style={styles.headerText}>You are...</Text>

                <Text style={styles.cheeseName}>{cheese.name}</Text>

                {imageSource && (
                    <Image source={imageSource} style={styles.image} resizeMode="contain" />
                )}

                <View style={styles.card}>
                    <Text style={styles.description}>{cheese.description}</Text>
                </View>

                <PrimaryButton
                    title="Roast Again"
                    onPress={() => navigation.popToTop()}
                />
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#FFF8E1',
    },
    scrollContent: {
        alignItems: 'center',
        paddingVertical: 60,
        paddingHorizontal: 20,
    },
    headerText: {
        fontSize: 24,
        color: '#666',
        marginBottom: 10,
    },
    cheeseName: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#1a1a1a',
        marginBottom: 20,
        textAlign: 'center',
    },
    image: {
        width: 250,
        height: 250,
        marginBottom: 20,
    },
    card: {
        backgroundColor: '#fff',
        padding: 20,
        borderRadius: 15,
        borderWidth: 2,
        borderColor: '#1a1a1a',
        marginBottom: 30,
        width: '100%',
    },
    description: {
        fontSize: 18,
        color: '#1a1a1a',
        lineHeight: 26,
        textAlign: 'center',
    },
});
