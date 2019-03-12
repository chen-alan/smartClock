import React from 'react';
import {
    Text,
    View,
    StyleSheet,
    DatePickerIOS,
    TouchableOpacity,
} from 'react-native';
import {DeviceMotion} from 'expo-sensors';


export default class Sensors extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            status: false, // data capture on/off toggle
            motionData: [], // array of data points captured from phone sensors
            alarm: new Date()
        };

        this._setDate = this._setDate.bind(this)
    }

    componentDidMount() {
        this._toggle();
    }

    componentWillUnmount() {
        this._unsubscribe();
    }

    _toggle = () => {
        if (this.subscription) {
            this._unsubscribe();
            console.log('toggle off');
            this.setState({status: false});
        } else {
            this._subscribe();
            console.log('toggle on');
            this.setState({status: true});
        }
    };

    _subscribe = () => {
        this.subscription = DeviceMotion.addListener(motionData => {
            // rate at which sensors update (in ms)
            DeviceMotion.setUpdateInterval(100);

            // append most recent motion data to past data
            let tmp = this.state.motionData.concat(motionData);
            this.setState({motionData: tmp});
        })
    };

    _unsubscribe = () => {
        this.subscription && this.subscription.remove();
        this.subscription = null;

        console.log(JSON.stringify(this.state.motionData))

        this.setState({motionData: []})
    };

    _setDate(newDate) {
        this.setState({alarm: newDate})
    }

    render() {
        return (
            <View style={styles.container}>
                <DatePickerIOS
                    date={this.state.alarm}
                    onDateChange={this._setDate}
                    mode={'time'}
                />
                <TouchableOpacity onPress={this._toggle}>
                    <Text>Toggle</Text>
                </TouchableOpacity>
            </View>
        );
    }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center'
  },
})

// //processes cumulative dataset to determine whether user is exercising or not, every second
// processdata() {
//   console.log("i'm processing!");
//   //Calculate standard deviation of accl and gyro dataset
//   //data SCIENCe! train on datasets where we're still vs not still
//
// }
