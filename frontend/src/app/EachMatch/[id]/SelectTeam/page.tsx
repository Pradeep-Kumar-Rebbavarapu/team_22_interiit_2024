'use client'

import { useState } from 'react'
import { ArrowLeft, Info, Minus, ChevronRight, Trophy } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
// Player component
function PlayerCard({ 
  player, 
  isSelected, 
  onToggle 
}: { 
  player: any
  isSelected: boolean
  onToggle: () => void 
}) {

 
  return (
    <div 
      className={`flex items-center p-4 border-b cursor-pointer transition-colors ${
        isSelected ? 'bg-green-100' : ''
      }`}
      onClick={onToggle}
    >
      <Info className="w-5 h-5 text-gray-400 mr-3" />
      <div className="flex flex-1 items-center">
        <img
          src={`https://ui-avatars.com/api/?name=${player.name}&background=random`}
          alt={player.name}
          className="w-20 h-20 rounded-lg object-cover mr-4"
        />
        <div className="flex-1">
          <h3 className="text-lg font-semibold">{player.name}</h3>
          <p className="text-gray-600">Sel by {player.selectionPercentage}</p>
          <div className="flex items-center mt-1">
            <div className="w-2 h-2 bg-blue-600 rounded-full mr-2" />
            <span className="text-sm text-gray-600">Played last match</span>
          </div>
        </div>
        <div className="flex items-center gap-8 ml-4">
          <span className="text-2xl font-semibold">{player.points}</span>
          <span className="text-2xl font-semibold">{player.credits}</span>
          <Button 
            variant="ghost" 
            size="icon" 
            className="w-10 h-10 rounded-full border-2 border-green-500"
          >
            {isSelected ? <Minus className="w-6 h-6" /> : <span className="text-xl">+</span>}
          </Button>
        </div>
      </div>
    </div>
  )
}

export default function Component() {
  const [selectedPlayers, setSelectedPlayers] = useState<string[]>([])

  const players = [
    { id: '1', name: 'H Klaasen', selectionPercentage: '62.12%', points: 53, credits: 9.0, team: 'SA' },
    { id: '2', name: 'S Samson', selectionPercentage: '86.3%', points: 170, credits: 8.0, team: 'IND' },
    { id: '3', name: 'R Rickelton', selectionPercentage: '29.41%', points: 55, credits: 7.0, team: 'SA' },
    { id: '4', name: 'J Sharma', selectionPercentage: '0.52%', points: 0, credits: 6.0, team: 'IND' },
  ]

  const togglePlayer = (playerId: string) => {
    setSelectedPlayers(prev => 
      prev.includes(playerId) 
        ? prev.filter(id => id !== playerId)
        : [...prev, playerId]
    )
  }

  const selectedTeamCounts = {
    SA: selectedPlayers.filter(id => players.find(p => p.id === id)?.team === 'SA').length,
    IND: selectedPlayers.filter(id => players.find(p => p.id === id)?.team === 'IND').length
  }
  const router = useRouter()
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gradient-to-b from-[#4a0e0e] to-[#1a1f25] text-white p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            className="text-white "
            onClick={() => router.back()}
            aria-label="Go back"
          >
            <ArrowLeft className="w-6 h-6" />
          </Button>
            <div>
              <h1 className="text-xl font-bold">Create Team</h1>
              <p className="text-sm text-gray-400">44h left</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-[#2a3038] px-4 py-2 rounded-lg flex items-center">
              <Trophy className="w-4 h-4 text-yellow-500 mr-1" />
              <span className="text-yellow-500 font-bold">G</span>
              <span className="ml-1">GURUS</span>
            </div>
            <div className="bg-white text-black px-4 py-2 rounded-full font-bold">PTS</div>
          </div>
        </div>

        <p className="text-center mb-4">Maximum of 10 players from one team</p>

        <div className="flex justify-center items-center gap-8 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-full bg-green-600 flex items-center justify-center">
              SA
            </div>
            <span className="text-2xl font-bold">{selectedTeamCounts.SA}</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center">
              IND
            </div>
            <span className="text-2xl font-bold">{selectedTeamCounts.IND}</span>
          </div>
        </div>

        <div className="flex gap-1 mb-4">
          {Array.from({ length: 11 }).map((_, index) => (
            <div 
              key={index}
              className={`flex-1 h-2 ${
                index < selectedPlayers.length ? 'bg-green-500' : 'bg-white'
              }`}
            />
          ))}
        </div>
      </header>

      <div className="bg-[#1a1f25] text-white p-4 flex items-center justify-between">
        <div className="flex items-center">
          <span className="font-bold mr-2">STATS</span>
          <ChevronRight className="w-4 h-4" />
        </div>
        <div className="flex items-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <span className="text-gray-400">Pitch:</span>
            <span>Batting</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-gray-400">Good for:</span>
            <span>Pace</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-gray-400">Avg Score:</span>
            <span>201</span>
          </div>
        </div>
      </div>

      <div className="p-4 bg-white">
        <h2 className="text-center text-gray-600 mb-4">Select Players</h2>
        
        <div className="grid grid-cols-[auto_1fr_auto] items-center p-4 border-b">
          <span className="text-gray-600 font-semibold">SELECTED BY</span>
          <span className="text-center text-gray-600 font-semibold">POINTS</span>
          <span className="text-gray-600 font-semibold">CREDITS</span>
        </div>

        {players.map(player => (
          <PlayerCard
            key={player.id}
            player={player}
            isSelected={selectedPlayers.includes(player.id)}
            onToggle={() => togglePlayer(player.id)}
          />
        ))}
      </div>

      <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4">
        <div className="flex justify-between max-w-3xl mx-auto">
          <Button variant="outline" className="flex-1 mr-2 bg-gray-100">
            PREVIEW
          </Button>
          <Button variant="outline" className="flex-1 ml-2 bg-gray-100">
            NEXT
          </Button>
        </div>
      </div>
    </div>
  )
}