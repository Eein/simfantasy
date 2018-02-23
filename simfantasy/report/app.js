(function() {
  var damageBreakdown = []
  for(k in window.actor_data.actions) {
    var totalDamage = 0
    window.actor_data.actions[k].damage.forEach(function(d) {
      console.log('damage', d)
      totalDamage += d.damage
    })
    console.log('totalDamage', totalDamage)
    if(totalDamage > 0) {
      damageBreakdown.push({
        name: k.toString(),
        y: totalDamage,
      })
    }
  }
  console.log(damageBreakdown)

  Highcharts.chart('damage-breakdown', {
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
                  style: {
                      color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                  }
              }
          }
      },
      series: [{
          name: 'Abilities',
          colorByPoint: true,
          data: damageBreakdown,
      }]
  });
})()
