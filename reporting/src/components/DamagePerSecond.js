import React, { Component } from 'react'
import ReactHighchart from 'react-highcharts'
import theme from './theme'
theme(ReactHighchart.Highcharts)
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
        // let delta = new Date(datetime)
        // delta.setSeconds(delta.getSeconds() + normalizedTime);

        points.push([normalizedTime, d.damage])
      })
    }
    points.sort((a,b) => a[0] > b[0] ? 1 : -1);
    const bucketCount = fightLength
    let buckets = []
    const interval = fightLength / bucketCount

    for(let x = 0; x <= bucketCount - 1; x++) {
      const bucketMin = x * interval
      const bucketMax = (x+1) * interval
      buckets[x] = x === 0 ? 0 : buckets[x-1]
      for(let y = 0; y < points.length; y++) {
        if(points[y] === undefined) { break; }
        if(points[y][0] >= bucketMin && points[y][0] < bucketMax) {
          buckets[x] += points[y][1]
        }
      }
    }
    let result = []
    buckets.forEach((bucket, index) => {
      let amount =  bucket / (index * interval)
      amount = amount === Infinity ? 0 : amount
      result.push([index * interval, amount])
    })
    console.log('result', result)
    return result;
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
            chart: {
              type: 'areaspline'
            },
            title: {
                text: 'Damage Per Second (DPS)'
            },
            smooth: true,
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
    return <ReactHighchart config={this.config()} ref="chart"></ReactHighchart>

  }
}
