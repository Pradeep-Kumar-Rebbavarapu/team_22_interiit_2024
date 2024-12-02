import { getPlayerData } from '@/api.js'
import CricketPlayerDashboard from '@/components/CricketPlayerDashBoard'

export default async function Page({ params }) {
  console.log(params)
  const playerStats = await getPlayerData({ player_identifier: params.player_id })
  console.log(playerStats)
  return (
    <div className="container mx-auto ">
      <CricketPlayerDashboard
      playerStats={playerStats}
      player_name={params.player_name}
      />
    </div>
  )
}