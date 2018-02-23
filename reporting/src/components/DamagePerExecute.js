import React, { Component } from 'react'
import ReactHighcharts from 'react-highcharts'
import theme from './theme'
theme(ReactHighcharts.Highcharts)

export default class DamagePerExecute extends Component {

  processData() {
    let damageBreakdown = []
    for(var key in this.props.data.actions) {
      let totalDamage = 0
      const executeTime = this.props.data.actions[key].execute_time[0].delta
      this.props.data.actions[key].damage.forEach( d => {
        totalDamage = (totalDamage + d.damage) / 2
      })
      if(totalDamage > 0) {
        damageBreakdown.push([
          key.toString().substring(0, key.toString().length - 4),
          totalDamage / executeTime,
        ])
      }
    }
    return damageBreakdown
  }

  config() {
    const data = this.processData().sort(function(a, b) {
      return a[1] > b[1] ? 1 : -1;
    }).reverse()
    return {
       credits: {
            enabled: false
        },
        xAxis: {
            type: 'category',
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Damage Per Execute Time (DPET)'
        },
        series: [{
            name: 'Abilities',
            colorByPoint: true,
            data: data,
        }]
    }
  }

  render() {

    if (!this.props.data) { return null }
    return <ReactHighcharts config={this.config()} ref="chart"></ReactHighcharts>

  }
}
