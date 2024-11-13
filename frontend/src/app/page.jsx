
import { Trophy } from "lucide-react";
import MatchCard from "@/components/MatchCard";
import { getMatches } from "@/api";

export default async function Component() {
  const matches = await getMatches({limit:20});
  return (
    <div className=" h-full bg-gradient-to-b from-red-900 to-red-800">
      {/* Header */}
      <header className="flex items-center justify-between p-4 md:p-6 bg-red-900">
        <div className="flex items-center gap-4">
          <div className="h-10 w-10 rounded-full bg-white flex items-center justify-center">
            <Trophy className="h-6 w-6 text-red-900" />
          </div>
          <span className="text-white text-xl font-bold hidden md:block">
            Dream11
          </span>
        </div>
        <span className="text-white text-xl font-bold md:hidden">Dream11</span>
      </header>

      <main className="px-4 md:px-6">
        {/* Title */}
        <h1 className="my-6 text-center text-2xl font-bold text-white md:text-3xl">
          UPCOMING CRICKET MATCHES
        </h1>

        {/* Matches ScrollArea */}
        <div className="grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-4 pb-4">
          {matches.map((match, index) => {
            return (
              <div key={index}>
                <MatchCard id={index} match={match} />
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
}
