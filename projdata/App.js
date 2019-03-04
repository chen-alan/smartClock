import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {Accelerometer, Gyroscope} from 'expo';
import TimerMixin from 'react-timer-mixin';

export default class Sensors extends React.Component {
    state = {
        accelerometerData: {},
        gyroscopeData: {},
        data: [0],
    }

    mixins: [TimerMixin];

    componentDidMount() {
        this._toggle();
        this.update = this.update.bind(this);
        this.add = setInterval(() => {this.update();}, 100);
        this.processdata = this.processdata.bind(this);
        this.interval = setInterval(() => {this.processdata();}, 1000);
    }

    componentWillUnmount() {
        this._unsubscribe();
        clearInterval(this.add);
        clearInterval(this.interval);

    }

    _toggle = () => {
        Accelerometer.setUpdateInterval(100);
        Gyroscope.setUpdateInterval(100);

        if (this._acclsubscription) {
            this._unsubscribe();
        } else {
            this._subscribe();
        }
    }

    _subscribe = () => {
        this._acclsubscription = Accelerometer.addListener(accelerometerData => {
            this.setState({accelerometerData});
        });
        this._gyrosubscription = Gyroscope.addListener(gyroscopeData => {
            this.setState({gyroscopeData});
        });
    }

    //adds accelerometer data to dataset
    update() {
      let {x, y, z} = this.state.accelerometerData;
      let {gx, gy, gz} = this.state.gyroscopeData;
      var currdata = {
        "ax": x, "ay": y, "az": z, "gx": gx, "gy": gy, "gz": gz
      };
      var temparr = this.state.data.slice();
      temparr.push(currdata);
      this.setState({data: temparr});
    }

    //processes cumulative dataset to determine whether user is exercising or not, every second
    processdata() {
      console.log("i'm processing!");
      //Calculate standard deviation of accl and gyro dataset
      //data SCIENCe! train on datasets where we're still vs not still

    }

    _unsubscribe = () => {
        this._acclsubscription && this._acclsubscription.remove();
        this._gyrosubscription && this._gyrosubscription.remove();
        this._acclsubscription = null;
        this._gyrosubscription = null;
    }

    render() {
        let {x, y, z} = this.state.accelerometerData;
        let {gx, gy, gz} = this.state.gyroscopeData;
        return (
            <View style={{
                flex: 1,
                flexDirection: 'column',
                justifyContent: 'center',
            }}>
                <Text>x: {round(x)}{"\n"}</Text>
                <Text>y: {round(y)}{"\n"}</Text>
                <Text>z: {round(z)}{"\n\n"}</Text>
                <Text>x: {round(gx)}{"\n"}</Text>
                <Text>y: {round(gy)}{"\n"}</Text>
                <Text>z: {round(gz)}{"\n\n"}</Text>
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
