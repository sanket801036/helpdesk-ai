import { useQuery } from "@tanstack/react-query";
import { getHealth } from "../api/health";

export default function HomePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
    retry: false,
  });

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Welcome to Helpdesk AI</h1>
      <p className="text-slate-600">
        Frontend skeleton (Phase 4). Backend connection status:
      </p>

      <div className="rounded-lg border p-4 bg-white shadow-sm">
        {isLoading && <span className="text-slate-500">Checking backend…</span>}

        {isError && (
          <span className="text-red-600 font-medium">
            ❌ Backend se connect nahi ho paya (kya backend chal raha hai?)
          </span>
        )}

        {data && (
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 rounded-full bg-green-500" />
            <span className="font-medium">
              ✅ Backend connected — status: {data.status}, db:{" "}
              {String(data.db)}
            </span>
          </div>
        )}
      </div>

      <p className="text-sm text-slate-400">
        Aage: Phase 5 — Authentication (login / register / RBAC).
      </p>
    </div>
  );
}
