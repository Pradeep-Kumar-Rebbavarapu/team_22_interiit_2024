'use client'
import { useState, useEffect } from "react";
import { getMatches } from "@/api";
import MatchDetailClient from "@/components/MatchDetailClient";
import Dream11AIChat from "@/components/chatbot";
import Loading from "./loading"; // Adjust the path if necessary
import { useParams } from "next/navigation";

export default function Page() {
  const { id } = useParams();
  const [matchData, setMatchData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatchData = async () => {
      const result = await getMatches({ id });
      setMatchData(result[0]); // Assuming the result is an array and you want the first match
      setLoading(false); // Set loading to false once data is fetched
    };

    fetchMatchData();
  }, [id]); // Dependency array ensures the effect runs whenever `id` changes

  if (loading) {
    return <Loading />; // Show the loading component while fetching data
  }

  return (
    <>
      <MatchDetailClient matchData={matchData} />
      <Dream11AIChat match_id={matchData.id} />
    </>
  );
}
