import React, { Component } from 'react'
import ReactHighcharts from 'react-highcharts'
import theme from './theme'
theme(ReactHighcharts.Highcharts)

export default class TimeSpent extends Component {

  processData() {
    var timeBreakdown = []
    for(var key in this.props.data.actions) {
      var totalTime = 0
      this.props.data.actions[key].execute_time.forEach( d => {
        totalTime += d.delta
      })
      if(totalTime > 0) {
        timeBreakdown.push({
          name: key.toString().substring(0, key.toString().length - 4),
          y: totalTime,
        })
      }
    }
    let abilityTime = 0
    timeBreakdown.forEach(t => { abilityTime += t.y })
    timeBreakdown.push({
      name: 'Waiting',
      y: this.props.data.combatLength - abilityTime,
    })
    return timeBreakdown
  }

  config() {
    return {
       credits: {
            enabled: false
        },
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Time Spent'
        },
        // tooltip: {
        //     pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        // },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.y:.2f}s',
                }
            }
        },
        series: [{
            name: 'Time Spent',
            colorByPoint: true,
            data: this.processData(),
        }]
    }
  }

  render() {

    if (!this.props.data) { return null }
    return <ReactHighcharts config={this.config()} ref="chart"></ReactHighcharts>

  }
}
