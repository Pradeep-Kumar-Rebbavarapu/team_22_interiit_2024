import { getPlayerData } from '@/api.js'
import CricketPlayerDashboard from '@/components/CricketPlayerDashBoard'

export default async function Page({ params }) {
  console.log(params)
  const playerStats = await getPlayerData({ player_identifier: params.player_id, year:params.year, match_type:params.match_type })

  return (
    <div className="container mx-auto p-4">
      <CricketPlayerDashboard
        initialPlayerStats={playerStats?.data?.statistics[0] || null}
        initialYear={params.year || ""}
        initialPlayerId = {params.player_id}
        initialMatchType={params.match_type || ""}
      />
    </div>
  )
}