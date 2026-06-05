import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/auth";
import { LogOut } from "lucide-react";
import { logout as apiLogout } from "@/api/auth";

export default function Header() {
  const { logout, refreshToken } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      if (refreshToken) await apiLogout(refreshToken);
    } catch {
      // ignore
    }
    logout();
    navigate("/login");
  };

  return (
    <header className="bg-white border-b border-gray-100 h-12 flex items-center justify-end px-6">
      <button
        onClick={handleLogout}
        className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-700 px-3 py-1.5 rounded-md hover:bg-gray-50 transition-colors"
      >
        <LogOut size={15} />
        Sign out
      </button>
    </header>
  );
}
