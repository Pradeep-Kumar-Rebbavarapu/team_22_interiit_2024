import { getMatches } from "@/api"
import MatchDetailClient from "@/components/MatchDetailClient"

export default async function MatchDetailPage({ params }) {
  const matchData = await getMatches({id:params.id})
  console.log(matchData)

  return <MatchDetailClient matchData={matchData[0]} id={params.id} />
}