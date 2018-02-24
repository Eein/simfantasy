import React, { Component } from 'react'
import { Table } from 'reactbulma'
export default class Abilities extends Component {

  renderAbilities() {
    const { data } = this.props
    const actions = []
    for(var key in this.props.data.actions) {
      let damage = 0
      let damageMean = 0;
      let name = key.toString()
      let casts = 0
      let critical_hits = data.actions[key].critical_hits.length
      let direct_hits = data.actions[key].direct_hits.length
      let critical_direct_hits = data.actions[key].critical_direct_hits.length
      data.actions[key].damage.forEach( d => {
        damage += d.damage
        damageMean = (damageMean + d.damage) / 2
        casts++
      })
      // crit_percent = (len(s['critical_hits']) / casts) * 100
      // direct_hit_percent = (len(s['direct_hits']) / casts) * 100
      // crit_direct_hit_percent = (len(s['critical_direct_hits']) / casts) * 100
      let dpet = damageMean / data.actions[key].execute_time[0].delta
      console.log(data)
      actions.push({
        name: name,
        casts: casts,
        damage: damage,
        damageMean: damageMean,
        dps: Number(damage / data.combatLength).toFixed(2),
        dpet: dpet,
        crit_percent: (critical_hits / casts) * 100,
        direct_hit_percent: (direct_hits / casts) * 100,
        critical_direct_hit_percent: (critical_direct_hits / casts) * 100,
      })
    }
    return actions.map(a => {
      return (
        <Table.Tr>
          <Table.Td>{a.name}</Table.Td>
          <Table.Td>{a.casts}</Table.Td>
          <Table.Td>{a.damage}</Table.Td>
          <Table.Td>{a.damageMean.toFixed(2)}</Table.Td>
          <Table.Td>{a.dps}</Table.Td>
          <Table.Td>{a.dpet.toFixed(2)}</Table.Td>
          <Table.Td>{a.crit_percent.toFixed(2)}</Table.Td>
          <Table.Td>{a.direct_hit_percent.toFixed(2)}</Table.Td>
          <Table.Td>{a.critical_direct_hit_percent.toFixed(2)}</Table.Td>
        </Table.Tr>
      )
    })

  }

  render() {
    const { data } = this.props
    // Name | Casts | Damage  | Damage (Mean) | DPS       | DPET      | Crit % | Direct % | D.Crit %
    return (
      <Table>
        <Table.Head>
          <Table.Tr>
            <Table.Th>Ability</Table.Th>
            <Table.Th>Casts</Table.Th>
            <Table.Th>Damage</Table.Th>
            <Table.Th>Damage (Mean)</Table.Th>
            <Table.Th>DPS</Table.Th>
            <Table.Th>DPET</Table.Th>
            <Table.Th>Crit %</Table.Th>
            <Table.Th>Direct %</Table.Th>
            <Table.Th>D.Crit %</Table.Th>
          </Table.Tr>
        </Table.Head>
        <Table.Body>
          {this.renderAbilities()}
        </Table.Body>
      </Table>
    )
  }
}
