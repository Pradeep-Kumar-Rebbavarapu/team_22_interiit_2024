import { getMatches } from "@/api";
import { ShowComponents } from "@/components/home";

export default async function Page() {
  const matches = await getMatches({ limit: 20 });

  return <ShowComponents matches={matches} />;
}
