import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
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

