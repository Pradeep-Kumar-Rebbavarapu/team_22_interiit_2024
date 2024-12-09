'use client'
import { useState, useEffect } from "react";
import { getMatches } from "@/api";
import { ShowComponents } from "@/components/home";

export default function Page() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    const fetchMatches = async () => {
      const result = await getMatches({ limit: 20 });
      setMatches(result);
      console.log('matches', result);
    };

    fetchMatches();
  }, []);

  return (
    <div>
      <ShowComponents matches={matches} />
    </div>
  );
}
