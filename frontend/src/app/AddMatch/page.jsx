import React from 'react'
import {getAllPlayers,getAllTeams} from '@/api'
import AddMatchPage from '../../components/AddMatchPage';
export default async function page() {
    const all_teams = await getAllTeams();
  return (
    <div><AddMatchPage all_teams={all_teams} /></div>
  )
}
