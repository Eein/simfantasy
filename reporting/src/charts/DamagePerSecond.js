import React, { Component } from 'react'
import ReactHighstock from 'react-highcharts/ReactHighstock'
export default class DamageBreakdown extends Component {

  processData() {
    let points = []
    let times = []
    for(let key in this.props.data.actions) {
      this.props.data.actions[key].damage.forEach( d => {
        times.push(d.time)
      })
    }
    const minTime = Math.min(...times)
    const maxTime = Math.max(...times)
    const fightLength = 300
    // snapshots the current time
    const datetime = new Date();
    // get the times to calc min and max
    for(let key in this.props.data.actions) {
      this.props.data.actions[key].damage.forEach( d => {
        let normalizedTime = ((d.time - minTime) / (maxTime - minTime) * fightLength);
        let delta = new Date(datetime)
        delta.setSeconds(delta.getSeconds() + normalizedTime);

        points.push([delta.getTime(), d.damage])
      })
    }
    points.sort((a,b) => a[0] > b[0] ? 1 : -1);
    console.log(points)

    return points;
  }

  config() {
    const data = this.processData()
    let times = []
    for(let key in this.props.data.actions) {
      this.props.data.actions[key].damage.forEach( d => {
        times.push(d.time)
      })
    }
    return {
            credits: false,
            title: {
                text: 'Damage Per Second (DPS)'
            },
            navigator: { enabled: false },
            scrollbar: { enabled: false },
            rangeSelector: {
                selected: 4,
                inputEnabled: false,
                buttonTheme: {
                    visibility: 'hidden'
                },
                labelStyle: {
                    visibility: 'hidden'
                }
            },
            xAxis: {
              dateTimeLabelFormats: {
                  millisecond: '%M:%S',
                  second: '%M:%S',
                  minute: '%M:%S',
                  hour: '%M:%S',
                  day: '%M:%S',
                  week: '%M:%S',
                  month: '%M:%S',
                  year: '%M:%S'
              },
            },
            yAxis: {
                title: {
                    text: 'DPS'
                }
            },
            plotOptions: {
              series: {
                dataGrouping: {
                  enabled: true,
                  forced: true,
                  approximation: 'average',
                  smoothed: true,
                  units: [[
                    'second', [1]
                  ]]
                },
              },
            },
            series: [{
                name: 'Damage Per Second',
                data: this.processData()
            }]
        }  }

  render() {

    if (!this.props.data) { return null }
    return <ReactHighstock config={this.config()} ref="chart"></ReactHighstock>

  }
}
