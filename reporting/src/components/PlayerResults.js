import React, { Component } from 'react'
export default class PlayerResults extends Component {

  totalDamage() {
    const { data } = this.props
    let damage = 0.0
    for(let action in data.actions) {
      for(let d in data.actions[action].damage) {
        damage += data.actions[action].damage[d].damage
      }
    }
    return damage
  }

  render() {
    const { data } = this.props
    const damage = this.totalDamage()
    const dps = damage / data.combatLength
    return `Name: ${data.name} Race: ${data.race} - DPS: ${dps} - Damage: ${damage}`

  }
}
