"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartContainer } from "@/components/ui/chart"
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts"
import { CalendarIcon, TrendingUpIcon, Target, Activity, Percent, Award, Shield, Crosshair, Loader2 } from 'lucide-react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {  Trophy } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { useRouter } from 'next/navigation'
import { Skeleton } from "@/components/ui/skeleton"
import { getPlayerData } from "@/api"

// Monochrome Color Palette
const DREAM11_COLORS = [
  "#000000", "#5C4033", "#8B4513", "#A0522D", "#D2B48C", "#DEB887",
  "#0D0D0D", "#1A1A1A", "#292929", "#404040", "#D3D3D3", "#C0C0C0",
  "#A9A9A9", "#FAFAFA", "#E5E5E5", "#D1D1D1", "#9E9E9E", "#717171",
  "#3F3F3F", "#4B0082", "#708090", "#2F4F4F", "#556B2F", "#483D8B",
]

const MATCH_TYPES = ["Test", "MDM", "ODI", "ODM", "T20", "IT20"]

export default function CricketPlayerDashboard({
  initialPlayerStats,
  initialError,
  initialPlayerId,
  initialYear,
  initialMatchType  
}) {
  const router = useRouter()
  const currentYear = new Date().getFullYear()
  const [year, setYear] = useState(initialYear)
  const [matchType, setMatchType] = useState(initialMatchType)
  const [playerStats, setPlayerStats] = useState(initialPlayerStats)
  const [error, setError] = useState(initialError)
  const [loading, setLoading] = useState(false)

  const years = Array.from({ length: currentYear - 2003 }, (_, i) => (2004 + i).toString())

  useEffect(() => {
    if (Object.keys(playerStats).length === 0) {
      fetchPlayerData()
    }
  }, [])

  const fetchPlayerData = async () => {
    setLoading(true)
    setError(null)
    try {
      window.location.href = `/PlayerData/${initialPlayerId}/${year}/${matchType}`
    } catch (err) {
      setError('Failed to fetch player data. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const isBatsman = Number(playerStats["Innings Batted"]) > 0
  const isBowler = Number(playerStats["Innings Bowled"]) > 0

  const keyStats = [
    { title: "Matches Played", value: playerStats.Games, icon: CalendarIcon, color: DREAM11_COLORS[0] },
    { title: "Win %", value: `${playerStats["Win %"]}%`, icon: Percent, color: DREAM11_COLORS[2] },
    ...(isBatsman ? [
      { title: "Total Runs", value: playerStats.Runs, icon: TrendingUpIcon, color: DREAM11_COLORS[0] },
      { title: "Batting Average", value: Number(playerStats["Batting Avg"])?.toFixed(2), icon: Award, color: DREAM11_COLORS[2] },
      { title: "Batting Strike Rate", value: Number(playerStats["Batting S/R"])?.toFixed(2), icon: Activity, color: DREAM11_COLORS[4] },
    ] : []),
    ...(isBowler ? [
      { title: "Wickets", value: playerStats.Wickets, icon: Target, color: DREAM11_COLORS[0] },
      { title: "Bowling Average", value: Number(playerStats["Bowling Avg"])?.toFixed(2) ?? "N/A", icon: Shield, color: DREAM11_COLORS[2] },
      { title: "Economy Rate", value: Number(playerStats["Economy Rate"])?.toFixed(2), icon: Crosshair, color: DREAM11_COLORS[4] },
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

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-bold text-black">{label}</p>
          <p className="text-black">{`Value: ${payload[0].value}`}</p>
        </div>
      )
    }
    return null
  }

  const Loading = () => {
    return (
      <div className="bg-gradient-to-b from-red-900 to-red-800 min-h-screen p-4 sm:p-6 md:p-8">
      <Card className="w-full bg-white/0 backdrop-blur-sm shadow-2xl">
        <CardHeader className="space-y-1">
          <Skeleton className="h-8 w-3/4 bg-white/20" />
          <Skeleton className="h-4 w-1/2 bg-white/20" />
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <Skeleton className="h-10 w-full sm:w-[180px] bg-white" />
            <Skeleton className="h-10 w-full sm:w-[180px] bg-white" />
            <Skeleton className="h-10 w-full sm:w-[180px] bg-white" />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {Array(6).fill(0).map((_, index) => (
              <Card key={index} className="bg-white backdrop-blur-sm shadow-lg">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <Skeleton className="h-4 w-1/2 bg-gray-200" />
                  <Skeleton className="h-4 w-4 bg-gray-200" />
                </CardHeader>
                <CardContent>
                  <Skeleton className="h-8 w-1/2 bg-gray-200" />
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <Card className="bg-white/100 backdrop-blur-sm shadow-lg">
              <CardHeader className="bg-white/100 border-b">
                <Skeleton className="h-6 w-1/2 bg-gray-200" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[300px] w-full bg-gray-100" />
              </CardContent>
            </Card>
            <Card className="bg-white/100 backdrop-blur-sm shadow-lg">
              <CardHeader className="bg-white/100 border-b">
                <Skeleton className="h-6 w-1/2 bg-gray-200" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[300px] w-full bg-gray-100" />
              </CardContent>
            </Card>
          </div>
          <Card className="mb-8 border-0 border-orange-200">
            <CardHeader>
              <Skeleton className="h-6 w-1/3 bg-orange-100" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-[400px] w-full bg-orange-50" />
            </CardContent>
          </Card>
          <Card className="border-0 border-pink-200">
            <CardHeader>
              <Skeleton className="h-6 w-1/3 bg-pink-100" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-[200px] w-full bg-pink-50" />
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </div>
    )
  }

  if (loading) {
    return <Loading />
  }


  return (
    <div className="bg-gradient-to-b from-red-900 to-red-800 min-h-screen p-4 sm:p-6 md:p-8">
      <Card className="w-full bg-white/0 backdrop-blur-sm shadow-2xl">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl sm:text-3xl font-bold text-white">
            {loading ? 'Loading...' : `${playerStats.Players} - Performance Dashboard`}
          </CardTitle>
          <CardDescription className="text-white/80">
            {matchType} Statistics for {year}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <Select value={year} onValueChange={setYear} disabled={loading}>
              <SelectTrigger className="w-full sm:w-[180px] text-black bg-white">
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
            <Select value={matchType} onValueChange={setMatchType} disabled={loading}>
              <SelectTrigger className="w-full sm:w-[180px] text-black bg-white">
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
            <Button 
              onClick={fetchPlayerData} 
              className="bg-white text-black w-full sm:w-auto hover:bg-white hover:text-black"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Loading
                </>
              ) : (
                'Fetch Player Data'
              )}
            </Button>
          </div>
          {error && <p className="text-red-300 mb-4">{error}</p>}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8 !text-black">
            {loading ? (
              Array(6).fill(0).map((_, index) => (
                <Skeleton key={index} className="h-32 w-full" />
              ))
            ) : (
              keyStats.map((stat, index) => (
                <Card 
                  key={index} 
                  className="!text-black bg-white backdrop-blur-sm /20 shadow-lg"
                >
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium text-black">{stat.title}</CardTitle>
                    <stat.icon className="h-4 w-4 text-black" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-black">{stat.value}</div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {loading ? (
              <>
                <Skeleton className="h-[300px] w-full" />
                <Skeleton className="h-[300px] w-full" />
              </>
            ) : (
              <>
                {isBatsman && (
                  <Card className="bg-white/100 backdrop-blur-sm /20 shadow-lg">
                    <CardHeader className="bg-white/100 border-b /20">
                      <CardTitle className="text-xl font-semibold text-black">Batting Breakdown</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ChartContainer config={Object.fromEntries(battingBreakdown.map((item, index) => [item.name, { label: item.name, color: "black" }]))} className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={battingBreakdown} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                            <CartesianGrid stroke="#FFFFFF33" />
                            <XAxis dataKey="name" stroke="#FFFFFF" />
                            <YAxis stroke="#FFFFFF" />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="value" fill="#000000" radius={[4, 4, 0, 0]} maxBarSize={50} />
                          </BarChart>
                        </ResponsiveContainer>
                      </ChartContainer>
                    </CardContent>
                  </Card>
                )}

                {isBowler && (
                  <Card className="bg-white/100 backdrop-blur-sm /20 shadow-lg">
                    <CardHeader className="bg-white/100 border-b /20">
                      <CardTitle className="text-xl font-semibold text-black">Bowling Breakdown</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ChartContainer config={Object.fromEntries(bowlingBreakdown.map((item, index) => [item.name, { label: item.name, color: DREAM11_COLORS[0] }]))} className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={bowlingBreakdown} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                            <CartesianGrid stroke="#FFFFFF33" />
                            <XAxis dataKey="name" stroke="#FFFFFF" />
                            <YAxis stroke="#FFFFFF" />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="value" fill="#000000" radius={[4, 4, 0, 0]} maxBarSize={50} />
                          </BarChart>
                        </ResponsiveContainer></ChartContainer>
                    </CardContent>
                  </Card>
                )}
              </>
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {loading ? (
              <>
                <Skeleton className="h-[300px] w-full" />
                <Skeleton className="h-[300px] w-full" />
              </>
            ) : (
              <>
                {isBatsman && (
                  <Card className="bg-white/100 backdrop-blur-sm /20 shadow-lg">
                  <CardHeader className="bg-white/100 border-b /20">
                    <CardTitle className="text-xl font-semibold text-black">Dismissal Types</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ChartContainer config={Object.fromEntries(dismissalTypes.map((item, index) => [item.name, { label: item.name, color: DREAM11_COLORS[index % DREAM11_COLORS.length] }]))} className="h-[300px] w-full">
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
                            <Cell key={`cell-${index}`} fill={DREAM11_COLORS[index % DREAM11_COLORS.length]} />
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
                  <Card className="bg-white/100 backdrop-blur-sm /20 shadow-lg">
                    <CardHeader className="bg-white/100 border-b /20">
                      <CardTitle className="text-xl font-semibold text-black">Wicket Types</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ChartContainer config={Object.fromEntries(wicketTypes.map((item, index) => [item.name, { label: item.name, color: DREAM11_COLORS[0] }]))} className="h-[300px] w-full">
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
                              <Cell key={`cell-${index}`} fill={DREAM11_COLORS[index % DREAM11_COLORS.length]} />
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
            </>
          )}
        </div>

        <Card className="mb-8 border-0 border-orange-200">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-orange-600">Performance Radar</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-[400px] w-full" />
            ) : (
              <ChartContainer config={Object.fromEntries(performanceRadar.map((item, index) => [item.subject, { label: item.subject, color: DREAM11_COLORS[index % DREAM11_COLORS.length] }]))} className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={performanceRadar}>
                    <PolarGrid stroke="#E5E7EB" />
                    <PolarAngleAxis dataKey="subject" stroke="#4B5563" />
                    <PolarRadiusAxis stroke="#4B5563" />
                    <Radar name={playerStats.Players} dataKey="A" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.6} />
                  </RadarChart>
                </ResponsiveContainer>
              </ChartContainer>
            )}
          </CardContent>
        </Card>

        <Card className="border-0 border-pink-200">
          <CardHeader>
            <CardTitle className="text-xl font-semibold text-pink-600">All Statistics</CardTitle>
          </CardHeader>
          <CardContent className="overflow-x-auto">
            {loading ? (
              <Skeleton className="h-[200px] w-full" />
            ) : (
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
            )}
          </CardContent>
        </Card>
      </CardContent>
    </Card>
    </div>
  )
}

