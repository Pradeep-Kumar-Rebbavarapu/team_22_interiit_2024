'use client'
import { useToast } from "@/hooks/use-toast"
import axios from 'axios'
import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"

export default function AddMatchPage({ all_teams }) {
	const { toast } = useToast()
	const router = useRouter()
	const [formData, setFormData] = useState({
		team_a: 0, // Now this will be the integer team ID
		team_b: 0, // Now this will be the integer team ID
		team_a_players: [],
		team_b_players: [],
		date: '',
		match_type: ''
	})
	const [errors, setErrors] = useState({})
	const [isLoading, setIsLoading] = useState(false)

	const handleInputChange = (e) => {
		const { name, value } = e.target
		setFormData(prev => ({ ...prev, [name]: value }))
	}

	const handleTeamSelect = (team, teamId) => {
		setFormData(prev => ({
			...prev,
			[`team_${team}`]: Number(teamId),
			[`team_${team}_players`]: []
		}))

		const otherTeam = team === 'a' ? 'b' : 'a'
		if (formData[`team_${otherTeam}`] === Number(teamId)) {
			setFormData(prev => ({
				...prev,
				[`team_${otherTeam}`]: 0,
				[`team_${otherTeam}_players`]: []
			}))
		}
	}

	const handlePlayerSelect = (team, playerId) => {
		setFormData(prev => {
			const playerList = prev[`team_${team}_players`]
			if (playerList.includes(playerId)) {
				return { ...prev, [`team_${team}_players`]: playerList.filter(id => id !== playerId) }
			} else if (playerList.length < 11) {
				return { ...prev, [`team_${team}_players`]: [...playerList, playerId] }
			}
			return prev
		})
	}

	const validateForm = () => {
		const newErrors = {}
		if (formData.team_a_players.length !== 11) {
			newErrors.team_a_players = 'Team A must have exactly 11 players'
		}
		if (formData.team_b_players.length !== 11) {
			newErrors.team_b_players = 'Team B must have exactly 11 players'
		}
		if (formData.team_a <= 0) {
			newErrors.team_a = 'Team A is required'
		}
		if (formData.team_b <= 0) {
			newErrors.team_b = 'Team B is required'
		}
		if (!formData.date) {
			newErrors.date = 'Match date is required'
		}
		if (!formData.match_type) {
			newErrors.match_type = 'Match type is required'
		}
		setErrors(newErrors)
		return Object.keys(newErrors).length === 0
	}

	const handleSubmit = async (e) => {
		e.preventDefault()
		if (!validateForm()) return
		console.log(formData)
		setIsLoading(true)
		axios.post('http://localhost:8000/backend/api/v1/add-match/', formData).then((response) => {
			console.log(response);
			toast({
				title: "Success",
				description: "Match added successfully!",
			})
			router.push('/')
			setIsLoading(false)
		}).catch((error) => {
			console.error('Error adding match:', error)
			toast({
				title: "Error",
				description: "Failed to add match. Please try again.",
				variant: "destructive",
			})
			setIsLoading(false)
		})
	}

	return (
		<div className="min-h-screen bg-gradient-to-b from-red-900 to-red-800 py-8 px-4 sm:px-6 lg:px-8">
			<Card className="max-w-2xl mx-auto">
				<CardHeader>
					<CardTitle className="text-2xl font-bold text-center">Add New Match</CardTitle>
				</CardHeader>
				<CardContent>
					<form onSubmit={handleSubmit} className="space-y-6">
						<div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
							{['a', 'b'].map(team => (
								<div key={team} className="space-y-4">
									<Label htmlFor={`team_${team}`}>Team {team.toUpperCase()} Name</Label>
									<Select
										value={formData[`team_${team}`] ? formData[`team_${team}`].toString() : ''}
										onValueChange={(teamId) => handleTeamSelect(team, teamId)}
									>
										<SelectTrigger id={`team_${team}`}>
											<SelectValue placeholder="Select team">
												{formData[`team_${team}`]
													? all_teams.find(t => t.id === formData[`team_${team}`])?.name
													: "Select team"}
											</SelectValue>
										</SelectTrigger>
										<SelectContent>
											{all_teams
												.filter(t => t.id !== formData[`team_${team === 'a' ? 'b' : 'a'}`])
												.map(t => (
													<SelectItem key={t.id} value={t.id.toString()}>{t.name}</SelectItem>
												))
											}
										</SelectContent>
									</Select>
									{errors[`team_${team}`] && (
										<Alert variant="destructive">
											<AlertTitle>Error</AlertTitle>
											<AlertDescription>{errors[`team_${team}`]}</AlertDescription>
										</Alert>
									)}

									<div>
										<Label>Team {team.toUpperCase()} Players ({formData[`team_${team}_players`].length}/11)</Label>
										<ScrollArea className="h-[200px] w-full border rounded-md p-4">
											{all_teams.find(t => t.id === formData[`team_${team}`])?.players.map(player => (
												<div key={player.id} className="flex items-center space-x-2 mb-2">
													<Checkbox
														id={`player-${team}-${player.id}`}
														checked={formData[`team_${team}_players`].includes(player.id)}
														onCheckedChange={() => handlePlayerSelect(team, player.id)}
														disabled={formData[`team_${team}_players`].length >= 11 && !formData[`team_${team}_players`].includes(player.id)}
													/>
													<Label htmlFor={`player-${team}-${player.id}`} className="flex-1 cursor-pointer">
														<span className="font-medium">{player.name}</span>
														<span className="ml-2 text-sm text-gray-500">({player.role})</span>
													</Label>
												</div>
											))}
										</ScrollArea>
										{errors[`team_${team}_players`] && (
											<Alert variant="destructive">
												<AlertTitle>Error</AlertTitle>
												<AlertDescription>{errors[`team_${team}_players`]}</AlertDescription>
											</Alert>
										)}
									</div>
								</div>
							))}
						</div>

						<div className="space-y-4">
							<div>
								<Label htmlFor="date">Match Date</Label>
								<Input
									id="date"
									name="date"
									type="date"
									required
									value={formData.date}
									onChange={handleInputChange}
								/>
								{errors.date && (
									<Alert variant="destructive">
										<AlertTitle>Error</AlertTitle>
										<AlertDescription>{errors.date}</AlertDescription>
									</Alert>
								)}
							</div>

							<div>
								<Label htmlFor="match_type">Match Type</Label>
								<Select
									value={formData.match_type}
									onValueChange={(value) => setFormData(prev => ({ ...prev, match_type: value }))}
								>
									<SelectTrigger id="match_type">
										<SelectValue placeholder="Select match type" />
									</SelectTrigger>
									<SelectContent>
										<SelectItem value="t20">T20</SelectItem>
										<SelectItem value="odi">ODI</SelectItem>
										<SelectItem value="test">Test</SelectItem>
									</SelectContent>
								</Select>
								{errors.match_type && (
									<Alert variant="destructive">
										<AlertTitle>Error</AlertTitle>
										<AlertDescription>{errors.match_type}</AlertDescription>
									</Alert>
								)}
							</div>
						</div>

						<Button type="submit" className="w-full" disabled={isLoading}>
							{isLoading ? 'Adding Match...' : 'Add Match'}
						</Button>
					</form>
				</CardContent>
			</Card>
		</div>
	)
}