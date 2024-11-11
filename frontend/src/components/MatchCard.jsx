import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import Link from "next/link"

export default function MatchCard({
	team1 = "SA",
	team2 = "IND",
	timeLeft = "44h",
	prizePool = "₹28 Crores",
	firstPrize = "₹1.50 Crores",
	spots = { left: "79,46,926", total: "80,48,290" },
	id = "1",
}) {
	return (
		<Card className="w-full min-w-[300px] max-w-md flex-none">
			<CardContent className="p-4">
				<h3 className="mb-4 text-center text-lg font-semibold text-gray-600">{`${team1} vs ${team2} T20I`}</h3>
				<div className="mb-4 flex items-center justify-between">
					<div className="flex items-center gap-2">
						<div className="h-12 w-12 rounded-full bg-gray-100" />
						<span className="text-xl font-bold">{team1}</span>
					</div>
					<div className="rounded-full bg-red-50 px-4 py-2 text-red-600">
						<span className="font-semibold">{timeLeft}</span>
					</div>
					<div className="flex items-center gap-2">
						<span className="text-xl font-bold">{team2}</span>
						<div className="h-12 w-12 rounded-full bg-gray-100" />
					</div>
				</div>
				<div className="mb-4 grid grid-cols-2 gap-4 text-center">
					<div>
						<p className="text-sm text-gray-600">Prize Pool</p>
						<p className="text-xl font-bold">{prizePool}</p>
					</div>
					<div>
						<p className="text-sm text-gray-600">1st Prize</p>
						<p className="text-xl font-bold">{firstPrize}</p>
					</div>
				</div>
				<div className="mb-4 flex justify-between text-sm text-gray-600">
					<span>{spots.left} spots left</span>
					<span>{spots.total} spots</span>
				</div>
				<div className="mb-4 flex items-center justify-between">
					<div>
						<p className="text-sm text-gray-600">Join for</p>
						<p className="text-lg">
							<span className="text-gray-400 line-through">₹49</span>{" "}
							<span className="font-bold">₹1 Only</span>
						</p>
					</div>
					<Link href={`/EachMatch/${id}`} className="w-fit h-fit">
					<Button className="bg-green-600 px-8 hover:bg-green-700" >JOIN NOW</Button>
					</Link>
				</div>
			</CardContent>
		</Card>
	)
}