'use client'
import { useState, useEffect } from "react";
import { getPlayerData } from "@/api.js";
import { useParams } from "next/navigation";
import CricketPlayerDashboard from "@/components/CricketPlayerDashBoard";

export default function Page({ params }) {
  const { player_id, player_name } = useParams();
  const [playerStats, setPlayerStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPlayerData = async () => {
      try {
        const data = await getPlayerData({ player_identifier: player_id });
        setPlayerStats(data);
      } catch (error) {
        console.error("Error fetching player data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayerData();
  }, [player_id]);

  return (
    <div className="container">
      <CricketPlayerDashboard playerStats={playerStats} player_name={player_name} />
    </div>
  );
}
