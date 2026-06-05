import { NavLink } from "react-router-dom";
import { useAuthStore } from "@/store/auth";
import {
  LayoutDashboard,
  Calendar,
  UserCheck,
  FileText,
  MessageSquare,
  BookOpen,
  StickyNote,
} from "lucide-react";
import { clsx } from "clsx";

const navItems = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/timetable", icon: Calendar, label: "Timetable" },
  { to: "/attendance", icon: UserCheck, label: "Attendance" },
  { to: "/materials", icon: FileText, label: "Materials" },
  { to: "/chat", icon: MessageSquare, label: "Chat" },
  { to: "/assignments", icon: BookOpen, label: "Assignments" },
  { to: "/notes", icon: StickyNote, label: "Notes" },
];

export default function Sidebar() {
  const user = useAuthStore((s) => s.user);

  return (
    <aside className="w-56 bg-white border-r border-gray-100 flex flex-col">
      <div className="p-5 border-b border-gray-100">
        <h1 className="text-base font-semibold text-gray-900">EduPageKiller</h1>
      </div>

      <nav className="flex-1 py-3 overflow-y-auto">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              clsx(
                "flex items-center gap-2.5 px-3 py-2 mx-2 rounded-md text-sm transition-colors",
                isActive
                  ? "bg-gray-100 text-gray-900 font-medium"
                  : "text-gray-500 hover:bg-gray-50 hover:text-gray-800"
              )
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="p-3 border-t border-gray-100">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 text-xs font-medium">
            {user?.full_name?.charAt(0) ?? "?"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user?.full_name}</p>
            <p className="text-xs text-gray-400 capitalize">{user?.role}</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
