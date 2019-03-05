import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {DeviceMotion} from 'expo-sensors';

export default class Sensors extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // array of data points captured from on-board sensors
            motionData: [],
        };
    }

    componentDidMount() {
        this._toggle();
    }

    componentWillUnmount() {
        this._unsubscribe();
    }

    _toggle = () => {
        if (this._subscribe()) {
            this._unsubscribe();
        } else {
            this._subscribe();
        }
    };

    _subscribe = () => {
        this.subscription = DeviceMotion.addListener(motionData => {
            // rate at which sensors update (in ms)
            DeviceMotion.setUpdateInterval(5000);
            // append most recent motion data to past data
            let tmp = this.state.motionData.concat(motionData);
            this.setState({motionData: tmp});
        })
    };

    _unsubscribe = () => {
        this.subscription && this.subscription.remove();
        this.subscription = null;
    };

    render() {
        console.log(this.state.motionData);
        return (
            <View style={{
                flex: 1,
                alignItems: 'center',
                justifyContent: 'center',
            }}>
                <Text>: {JSON.stringify(this.state.motionData)}{'\n'}{'\n'}</Text>
                <TouchableOpacity onPress={this._toggle}>
                    <Text>Toggle</Text>
                </TouchableOpacity>
            </View>
        );
    }
}

// //processes cumulative dataset to determine whether user is exercising or not, every second
// processdata() {
//   console.log("i'm processing!");
//   //Calculate standard deviation of accl and gyro dataset
//   //data SCIENCe! train on datasets where we're still vs not still
//
// }
