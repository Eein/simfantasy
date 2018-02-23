import React, { Component } from 'react'
import { Tag } from 'reactbulma'
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
    return (
      <div>
        <Tag dark>Name: {data.name}</Tag>
        <Tag dark>Race: {data.race}</Tag>
        <Tag dark>DPS: {Math.round(dps)}</Tag>
        <Tag dark>Damage: {damage}</Tag>
      </div>
    )

  }
}
