import React, { Component } from 'react'
import { Tag, Field, Control } from 'reactbulma'
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
        <Field grouped>
          <Control>
          <Tag dark>Name: {data.name}</Tag>
        </Control>
          <Control>
          <Tag dark>Race: {data.race}</Tag>
        </Control>
          <Control>
          <Tag dark>DPS: {Math.round(dps)}</Tag>
        </Control>
          <Control>
          <Tag dark>Damage: {damage}</Tag>
        </Control>
        </Field>
      </div>
    )
  }
}
