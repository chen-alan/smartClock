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
            collecting_data: false,
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
            if (this.state.collecting_data) {
                // rate at which sensors update (in ms)
                DeviceMotion.setUpdateInterval(100);

                // append most recent motion data to past data
                let tmp = this.state.motionData.concat(motionData);
                this.setState({motionData: tmp});
            }

            if (this.state.alarm_armed) {
                let cur_date = new Date();
                const cur_hrs = cur_date.getUTCHours();
                const cur_min = cur_date.getUTCMinutes();
                let alm_date = this.state.alarm_time;
                const alm_hrs = alm_date.getUTCHours();
                const alm_min = alm_date.getUTCMinutes();

                if ((cur_hrs === alm_hrs) && (cur_min === alm_min)) {
                    // if (!this.state.collecting_data) {
                    //     this._alarmCollect();
                    // }
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

        this.setState({
            motionData: [],
            alarm_armed: false,
            alarm_ringing: false,
            alarm_offed: false,
            collecting_data: false,
        });
    };

    _alarmOn = () => {
        this.setState({alarm_armed: true});
        this.setState({alarm_offed: false});
        console.log("on");
    };

    _alarmOff = () => {
        this._unsubscribe();
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

    _alarmCollect = () => {
        // 1) render "done" button (state prop [collecting_data])
        this.setState({collecting_data: true});
    };

    _alarmDone = () => {
        // 1) unrender "done" button
        this.setState({collecting_data: false});
        console.log("should start processing data");
        runPyScript();
        console.log("assume jj done");
        this._alarmRingOff();
        // 4) if backend return done: _alarmRingOff; else do nothing
    };

    render() {
        return (
            <View style={styles.container}>
                <DatePickerIOS
                    date={this.state.alarm_time}
                    onDateChange={this._setDate}
                    mode={'time'}
                />
                {/*<TouchableOpacity onPress={this._toggle}>*/}
                {/*<Text>Toggle{'\n'}</Text>*/}
                {/*</TouchableOpacity>*/}

                <TouchableOpacity onPress={this._alarmOn}>
                    <Text>Alarm On{'\n'}</Text>
                </TouchableOpacity>

                <TouchableOpacity onPress={this._alarmOff}>
                    <Text>Alarm Off{'\n'}</Text>
                </TouchableOpacity>

                {this.state.alarm_ringing === true ?
                    <TouchableOpacity onPress={this._alarmCollect}>
                        <Text>Ringer Off{'\n'}</Text>
                    </TouchableOpacity>
                    :
                    <Text></Text>}

                {this.state.collecting_data === true ?
                    <TouchableOpacity onPress={this._alarmDone}>
                        <Text>Done with Jumping Jacks!{'\n'}</Text>
                    </TouchableOpacity>
                    :
                    <Text></Text>}
            </View>
        );
    }
}

function makeHttpObject() {
    try {
        return new XMLHttpRequest();
    } catch (error) {
    }
    try {
        return new ActiveXObject("Msxml2.XMLHTTP");
    } catch (error) {
    }
    try {
        return new ActiveXObject("Microsoft.XMLHTTP");
    } catch (error) {
    }

    throw new Error("Could not create HTTP request object.");
}

function blah() {
    var request = makeHttpObject();
    request.open("GET", "", true);
    request.send(null);
    request.onreadystatechange = function () {
        if (request.readyState == 4)
            alert(request.responseText);
    };
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center'
    },
});
