import { getMatches } from "@/api";
import MatchDetailClient from "@/components/MatchDetailClient";
import Dream11AIChat from "@/components/chatbot";

export default async function Page({ params }) {
  const { id } = await params;
  const matchData = await getMatches({id:id})

  return (
    <>
      <MatchDetailClient matchData={matchData[0]}  />
      <Dream11AIChat match_id = {matchData[0].id}/>
    </>
  );
}
