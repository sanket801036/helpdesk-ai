import { Outlet, Link } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="bg-slate-900 text-white px-6 py-4 flex items-center gap-3">
        <span className="text-xl font-bold">🎧 Helpdesk AI</span>
        <nav className="ml-auto flex gap-4 text-sm">
          <Link to="/" className="hover:underline">
            Home
          </Link>
        </nav>
      </header>
      <main className="p-6 max-w-4xl mx-auto">
        <Outlet />
      </main>
    </div>
  );
}
