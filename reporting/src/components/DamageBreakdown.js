import React, { Component } from 'react'
import ReactHighcharts from 'react-highcharts'
export default class DamageBreakdown extends Component {

  processData() {
    var damageBreakdown = []
    for(var key in this.props.data.actions) {
      var totalDamage = 0
      this.props.data.actions[key].damage.forEach( d => {
        totalDamage += d.damage
      })
      if(totalDamage > 0) {
        damageBreakdown.push({
          name: key.toString(),
          y: totalDamage,
        })
      }
    }
    return damageBreakdown
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
            text: 'Damage Breakdown'
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
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                }
            }
        },
        series: [{
            name: 'Abilities',
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
