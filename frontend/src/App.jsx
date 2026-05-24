import { Moon, Sun, Mic2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";

export default function App() {
  const [dark, setDark] = useState(false);
  const location = useLocation();

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  return (
    <div className="min-h-screen bg-[#f8faf9] text-ink dark:bg-[#101418] dark:text-white">
      <header className="border-b border-black/10 bg-white/90 backdrop-blur dark:border-white/10 dark:bg-[#151b20]/90">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
          <Link to="/" className="flex items-center gap-3 font-semibold">
            <span className="grid h-10 w-10 place-items-center rounded-md bg-mint text-white">
              <Mic2 size={22} />
            </span>
            <span className="leading-tight">English Speaking Test Analyzer</span>
          </Link>
          <div className="flex items-center gap-2">
            <Link
              to="/"
              className={`rounded-md px-3 py-2 text-sm ${location.pathname === "/" ? "bg-black text-white dark:bg-white dark:text-black" : "hover:bg-black/5 dark:hover:bg-white/10"}`}
            >
              Test
            </Link>
            <Link
              to="/dashboard"
              className={`rounded-md px-3 py-2 text-sm ${location.pathname === "/dashboard" ? "bg-black text-white dark:bg-white dark:text-black" : "hover:bg-black/5 dark:hover:bg-white/10"}`}
            >
              Dashboard
            </Link>
            <button
              type="button"
              onClick={() => setDark((value) => !value)}
              className="grid h-10 w-10 place-items-center rounded-md border border-black/10 hover:bg-black/5 dark:border-white/10 dark:hover:bg-white/10"
              title="Toggle theme"
            >
              {dark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
        <Outlet />
      </main>
    </div>
  );
}
