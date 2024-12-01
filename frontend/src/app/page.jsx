import { Trophy, Plus } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";
import { getMatches } from "@/api";

export default async function Page() {
  const matches = await getMatches({ limit: 20 });
  console.log(matches);

  return (
    <div className="min-h-screen bg-gradient-to-b from-red-900 to-red-800">
      <header className="flex items-center justify-between p-4 bg-red-900">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-white flex items-center justify-center">
            <Trophy className="h-5 w-5 text-red-900" />
          </div>
          <span className="text-white text-lg font-bold">Dream11</span>
        </div>
        <Link href="/AddMatch">
          <Button className="bg-green-600 hover:bg-green-700 text-white text-sm px-4 py-2 transition-all duration-300 ease-in-out hover:shadow-md active:scale-95">
            <Plus className="mr-2 h-4 w-4" />
            Add Match
          </Button>
        </Link>
      </header>

      <main className="px-4 py-6">
        <h1 className="mb-6 text-center text-2xl font-bold text-white">
          UPCOMING CRICKET MATCHES
        </h1>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {matches.map((match) => (
            <Card
              key={match.id}
              className="bg-white/90 backdrop-blur-sm transition-all duration-300 ease-in-out hover:shadow-lg hover:scale-105"
            >
              <CardContent className="p-4">
                <h3 className="mb-3 text-center text-lg font-semibold text-gray-800">
                  {`${match.team_a.name} vs ${match.team_b.name}`}
                </h3>
                <div className="mb-3 flex items-center justify-between text-sm">
                  <span className="font-medium">{match.team_a.name}</span>
                  <span className="rounded-full bg-red-100 px-3 py-1 text-red-600 font-semibold">
                    {match.date}
                  </span>
                  <span className="font-medium">{match.team_b.name}</span>
                </div>
                <div className="mb-3 flex justify-between text-center">
                  <div>
                    <p className="text-xs text-gray-600">Prize Pool</p>
                    <p className="text-sm font-bold">{match.prize_pool}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">1st Prize</p>
                    <p className="text-sm font-bold">{match.first_prize}</p>
                  </div>
                </div>
                <div className="mb-3 flex justify-between text-xs text-gray-600">
                  <span>{match.teama_spots_left} spots left</span>
                  <span>{match.teamb_spots_left} spots</span>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs text-gray-600">Join for</p>
                    <p>
                      <span className="text-xs text-gray-400 line-through">
                        ₹49
                      </span>{" "}
                      <span className="text-sm font-bold">
                        ₹{match.amount_to_be_paid}
                      </span>
                    </p>
                  </div>
                  <Link href={`/EachMatch/${match.id}`}>
                    <Button className="bg-green-600 hover:bg-green-700 text-white text-sm px-4 py-2 transition-all duration-300 ease-in-out hover:shadow-md active:scale-95">
                      JOIN NOW
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
}

