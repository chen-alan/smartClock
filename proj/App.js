import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {Accelerometer} from 'expo';

export default class AccelerometerSensor extends React.Component {
    state = {
        accelerometerData: {},
    }

    componentDidMount() {
        this._toggle();
    }

    componentWillUnmount() {
        this._unsubscribe();
    }

    _toggle = () => {
        Accelerometer.setUpdateInterval(20);

        if (this._subscription) {
            this._unsubscribe();
        } else {
            this._subscribe();
        }
    }

    _subscribe = () => {
        this._subscription = Accelerometer.addListener(accelerometerData => {
            this.setState({accelerometerData});
        });
    }

    _unsubscribe = () => {
        this._subscription && this._subscription.remove();
        this._subscription = null;
    }

    render() {
        let {x, y, z} = this.state.accelerometerData;

        return (
            <View style={{
                flex: 1,
                flexDirection: 'column',
                justifyContent: 'center',
            }}>
                <Text>x: {round(x)}{"\n"}</Text>
                <Text>y: {round(y)}{"\n"}</Text>
                <Text>z: {round(z)}{"\n\n"}</Text>
                <TouchableOpacity onPress={this._toggle}>
                    <Text>Toggle</Text>
                </TouchableOpacity>
            </View>
        );
    }
}

function round(n) {
    if (!n) {
        return 0;
    }

    return Math.floor(n * 10000) / 10000;
}
