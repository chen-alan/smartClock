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
            alarm_time: new Date(),
            alarm_armed: false,
            alarm_ringing: false,
            alarm_offed: false,
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

            if (this.state.alarm_armed) {
                let cur_date = new Date();
                const cur_hrs = cur_date.getUTCHours();
                const cur_min = cur_date.getUTCMinutes();
                let alm_date = this.state.alarm_time;
                const alm_hrs = alm_date.getUTCHours();
                const alm_min = alm_date.getUTCMinutes();

                if ((cur_hrs === alm_hrs) && (cur_min === alm_min)) {
                    if (!this.state.alarm_offed) {
                        console.log("alarm ringing");
                        this._alarmRing();
                    }
                }
            }
        })
    };

    _unsubscribe = () => {
        this.subscription && this.subscription.remove();
        this.subscription = null;

        console.log(JSON.stringify(this.state.motionData));

        this.setState({motionData: []});
    };

    _alarmOn = () => {
        this.setState({alarm_armed: true});
        this.setState({alarm_offed: false});
        console.log("on");
    };

    _alarmOff = () => {
        this.setState({alarm_armed: false});
        this.setState({alarm_ringing: false});
        console.log("off");
    };

    _setDate(newDate) {
        this.setState({alarm_time: newDate});
    };

    _alarmRing = () => {
        this.setState({alarm_ringing: true});
    };

    _alarmRingOff = () => {
        this.setState({alarm_ringing: false});
        this.setState({alarm_offed: true});
    };

    render() {
        console.log("ALARM: ", this.state.alarm_ringing);
        return (
            <View style={styles.container}>
                <DatePickerIOS
                    date={this.state.alarm_time}
                    onDateChange={this._setDate}
                    mode={'time'}
                />
                <TouchableOpacity onPress={this._toggle}>
                    <Text>Toggle{'\n'}</Text>
                </TouchableOpacity>

                <TouchableOpacity onPress={this._alarmOn}>
                    <Text>Alarm On{'\n'}</Text>
                </TouchableOpacity>

                <TouchableOpacity onPress={this._alarmOff}>
                    <Text>Alarm Off{'\n'}</Text>
                </TouchableOpacity>

                {this.state.alarm_ringing === true ?
                    <TouchableOpacity onPress={this._alarmRingOff}>
                        <Text>Ringer Off{'\n'}</Text>
                    </TouchableOpacity>
                    :
                    <Text></Text>}
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center'
    },
});
