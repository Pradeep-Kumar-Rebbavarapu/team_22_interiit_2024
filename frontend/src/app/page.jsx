'use client'
import { useState, useEffect } from "react";
import { getMatches } from "@/api";
import { ShowComponents } from "@/components/home";
import Loading from "./loading"; // Adjusted import path

export default function Page() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatches = async () => {
      const result = await getMatches({ limit: 20 });
      setMatches(result);
      setLoading(false); // Set loading to false once data is fetched
      console.log('matches', result);
    };

    fetchMatches();
  }, []); // Empty dependency array to run only once after the component mounts

  if (loading) {
    return <Loading />; // Show the loading component while fetching data
  }

  return (
    <div>
      <ShowComponents matches={matches} />
    </div>
  );
}
