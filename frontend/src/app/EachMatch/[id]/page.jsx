'use client'
import { useState, useEffect } from "react";
import { getMatches } from "@/api";
import EachMatchCard from "@/components/EachMatchCard";
import { useParams } from "next/navigation";
import Loading from "./loading"; // Adjust the path if necessary

export default function Page() {
  const { id } = useParams();
  const [match, setMatch] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatch = async () => {
      const result = await getMatches({ id:id });
      setMatch(result);
      setLoading(false); // Set loading to false once data is fetched
    };

    fetchMatch();
  }, [id]); // Dependency array ensures the effect runs whenever `id` changes

  if (loading) {
    return <Loading />; // Show the loading component while fetching data
  }

  return <EachMatchCard match={match} id={id} />;
}
