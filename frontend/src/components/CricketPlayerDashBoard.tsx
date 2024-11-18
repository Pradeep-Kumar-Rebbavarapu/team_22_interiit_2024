"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer, ChartTooltip } from "@/components/ui/chart"
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts"
import { CalendarIcon, TrendingUpIcon, Target, Activity, Percent, Award, Shield, Crosshair } from 'lucide-react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useRouter } from 'next/navigation'

type PlayerStats = {
  [key: string]: number | string | null
}

const COLORS = [
  "#FF3B30", // Red
  "#007AFF", // Blue
  "#FF2D55", // Pink
  "#5856D6", // Purple
  "#FF9500", // Orange
  "#4CD964", // Green
  "#5AC8FA", // Light Blue
]

const MATCH_TYPES = ["Test", "MDM", "ODI", "ODM", "T20", "IT20"]

type CricketPlayerDashboardProps = {
  initialPlayerStats: PlayerStats | null
  initialError: string | null
  initialPlayer: string | undefined
  initialYear: string
  initialMatchType: string
}

export default function CricketPlayerDashboard({
  initialPlayerStats,
  initialError,
  initialPlayerId,
  initialYear,
  initialMatchType
}: CricketPlayerDashboardProps) {
  const router = useRouter()
  const currentYear = new Date().getFullYear()
  const [year, setYear] = useState(initialYear)
  const [matchType, setMatchType] = useState(initialMatchType)
  const [playerStats, setPlayerStats] = useState<PlayerStats | null>(initialPlayerStats)
  const [error, setError] = useState<string | null>(initialError)

  const years = Array.from({ length: currentYear - 2003 }, (_, i) => (2004 + i).toString())

  const fetchPlayerData = () => {
    router.push(`/PlayerData/${ initialPlayerId}/${year}/${matchType}`)
  }


  const isBatsman = Number(playerStats["Innings Batted"]) > 0
  const isBowler = Number(playerStats["Innings Bowled"]) > 0

  const keyStats = [
    { title: "Matches Played", value: playerStats.Games, icon: CalendarIcon, color: COLORS[0] },
    { title: "Win %", value: `${playerStats["Win %"]}%`, icon: Percent, color: COLORS[1] },
    ...(isBatsman ? [
      { title: "Total Runs", value: playerStats.Runs, icon: TrendingUpIcon, color: COLORS[2] },
      { title: "Batting Average", value: Number(playerStats["Batting Avg"])?.toFixed(2), icon: Award, color: COLORS[3] },
      { title: "Batting Strike Rate", value: Number(playerStats["Batting S/R"])?.toFixed(2), icon: Activity, color: COLORS[4] },
    ] : []),
    ...(isBowler ? [
      { title: "Wickets", value: playerStats.Wickets, icon: Target, color: COLORS[5] },
      { title: "Bowling Average", value: Number(playerStats["Bowling Avg"])?.toFixed(2) ?? "N/A", icon: Shield, color: COLORS[6] },
      { title: "Economy Rate", value: Number(playerStats["Economy Rate"])?.toFixed(2), icon: Crosshair, color: COLORS[0] },
    ] : []),
  ]

  const battingBreakdown = isBatsman ? [
    { name: "Singles", value: Number(playerStats.Singles) },
    { name: "Fours", value: Number(playerStats.Fours) },
    { name: "Sixes", value: Number(playerStats.Sixes) },
    { name: "Dot Balls", value: Number(playerStats["Dot Balls"]) },
  ] : []

  const bowlingBreakdown = isBowler ? [
    { name: "Dot Balls", value: Number(playerStats["Dot Balls Bowled"]) },
    { name: "Singles", value: Number(playerStats.Singlesgiven) },
    { name: "Fours", value: Number(playerStats.Foursgiven) },
    { name: "Sixes", value: Number(playerStats.Sixesgiven) },
  ] : []

  const dismissalTypes = isBatsman ? [
    { name: "Bowled", value: Number(playerStats["Bowled Outs"]) },
    { name: "LBW", value: Number(playerStats["LBW Outs"]) },
    { name: "Caught", value: Number(playerStats["Caught Outs"]) },
    { name: "Stumped", value: Number(playerStats["Stumped Outs"]) },
    { name: "Run Out", value: Number(playerStats["Run Outs"]) },
    { name: "Hit Wicket", value: Number(playerStats["Hitwicket Outs"]) },
    { name: "Caught & Bowled", value: Number(playerStats["Caught and Bowled Outs"]) },
  ] : []

  const wicketTypes = isBowler ? [
    { name: "Bowled", value: Number(playerStats.Bowleds) },
    { name: "LBW", value: Number(playerStats.LBWs) },
    { name: "Caught", value: Number(playerStats.Caughts) },
    { name: "Stumped", value: Number(playerStats.Stumpeds) },
    { name: "Caught & Bowled", value: Number(playerStats["Caught and Bowleds"]) },
  ] : []

  const performanceRadar = [
    ...(isBatsman ? [
      { subject: "Batting Avg", A: Number(playerStats["Batting Avg"]), fullMark: 50 },
      { subject: "Scoring Consistency", A: Number(playerStats["Scoring Consistency"]), fullMark: 50 },
      { subject: "Boundary %", A: Number(playerStats["Boundary %"]), fullMark: 20 },
      { subject: "Strike Rate", A: Number(playerStats["Batting S/R"]) / 2, fullMark: 100 },
    ] : []),
    ...(isBowler ? [
      { subject: "Economy Rate", A: Number(playerStats["Economy Rate"]), fullMark: 12 },
      { subject: "Bowling Avg", A: Number(playerStats["Bowling Avg"]), fullMark: 40 },
      { subject: "Dot Ball %", A: Number(playerStats["Dot Ball Bowled %"]), fullMark: 100 },
      { subject: "Bowling S/R", A: Number(playerStats["Bowling S/R"]), fullMark: 30 },
    ] : []),
  ]

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-bold text-gray-900">{label}</p>
          <p className="text-blue-600">{`Value: ${payload[0].value}`}</p>
        </div>
      )
    }
    return null
  }

  return (
    <Card className="w-full border-2 border-gray-200">
      <CardHeader>
        <CardTitle className="text-3xl font-bold text-blue-600">{playerStats.Players} - Performance Dashboard</CardTitle>
        <CardDescription className="text-lg text-gray-600">
          {matchType} Statistics for {year}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col sm:flex-row gap-4 mb-4">
          <Select value={year} onValueChange={setYear}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select year" />
            </SelectTrigger>
            <SelectContent>
              {years.map((y) => (
                <SelectItem key={y} value={y}>
                  {y}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={matchType} onValueChange={setMatchType}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select match type" />
            </SelectTrigger>
            <SelectContent>
              {MATCH_TYPES.map((type) => (
                <SelectItem key={type} value={type}>
                  {type}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button onClick={fetchPlayerData}>
            Fetch Player Data
          </Button>
        </div>
        {error && <p className="text-red-600 mb-4">{error}</p>}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {keyStats.map((stat, index) => (
            <Card key={index} className="border-2" style={{ borderColor: stat.color }}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-700">{stat.title}</CardTitle>
                <stat.icon className="h-4 w-4" style={{ color: stat.color }} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold" style={{ color: stat.color }}>{stat.value}</div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {isBatsman && (
            <Card className="border-2 border-blue-200">
              <CardHeader>
                <CardTitle className="text-xl font-semibold text-blue-600">Batting Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer config={Object.fromEntries(battingBreakdown.map((item, index) => [item.name, { label: item.name, color: COLORS[index % COLORS.length] }]))} className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={battingBreakdown} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                      <XAxis dataKey="name" stroke="#4B5563" />
                      <YAxis stroke="#4B5563" />
                      <Tooltip content={<CustomTooltip />} />
                      <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]} maxBarSize={50} />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartContainer>
              </CardContent>
            </Card>
          )}
          
          {isBowler && (
            <Card className="border-2 border-green-200">
              <CardHeader>
                <CardTitle className="text-xl font-semibold text-green-600">Bowling Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer config={Object.fromEntries(bowlingBreakdown.map((item, index) => [item.name, { label: item.name, color: COLORS[index % COLORS.length] }]))} className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={bowlingBreakdown} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                      <XAxis dataKey="name" stroke="#4B5563" />
                      <YAxis stroke="#4B5563" />
                      <Tooltip content={<CustomTooltip />} />
                      <Bar dataKey="value" fill="#10B981" radius={[4, 4, 0, 0]} maxBarSize={50} />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartContainer>
              </CardContent>
            </Card>
          )}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {isBatsman && (
            <Card className="border-2 border-red-200">
              <CardHeader>
                <CardTitle className="text-xl font-semibold text-red-600">Dismissal Types</CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer config={Object.fromEntries(dismissalTypes.map((item, index) => [item.name, { label: item.name, color: COLORS[index % COLORS.length] }]))} className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={dismissalTypes}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {dismissalTypes.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </ChartContainer>
              </CardContent>
            </Card>
          )}
          
          {isBowler && (
            <Card className="border-2 border-purple-200">
              <CardHeader>
                <CardTitle className="text-xl font-semibold text-purple-600">Wicket Types</CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer config={Object.fromEntries(wicketTypes.map((item, index) => [item.name, { label: item.name, color: COLORS[index % COLORS.length] }]))} className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={wicketTypes}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {wicketTypes.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </ChartContainer>
              </CardContent>
            </Card>
          )}
        </div>
        
        <Card className="mb-8 border-2 border-orange-200">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-orange-600">Performance Radar</CardTitle>
          </CardHeader>
          <CardContent>
            <ChartContainer config={Object.fromEntries(performanceRadar.map((item, index) => [item.subject, { label: item.subject, color: COLORS[index % COLORS.length] }]))} className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={performanceRadar}>
                  <PolarGrid stroke="#E5E7EB" />
                  <PolarAngleAxis dataKey="subject" stroke="#4B5563" />
                  <PolarRadiusAxis stroke="#4B5563" />
                  <Radar name={playerStats.Players} dataKey="A" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.6} />
                </RadarChart>
              </ResponsiveContainer>
            </ChartContainer>
          </CardContent>
        </Card>
        
        <Card className="border-2 border-pink-200">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-pink-600">All Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-gray-900">Statistic</TableHead>
                  <TableHead className="text-gray-900">Value</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {Object.entries(playerStats).map(([key, value]) => (
                  <TableRow key={key}>
                    <TableCell className="text-gray-700">{key}</TableCell>
                    <TableCell className="text-gray-900">{value !== null ? value : 'N/A'}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </CardContent>
    </Card>
  )
}