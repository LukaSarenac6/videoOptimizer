import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Layout.css";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  function handleNavClick() {
    setSidebarOpen(false);
  }

  // Close sidebar on route change (mobile)
  const navClassName = ({ isActive }: { isActive: boolean }) =>
    isActive ? "nav-link active" : "nav-link";

  return (
    <div className="layout">
      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <h1>HPL</h1>
          <p className="sidebar-user">{user?.name} {user?.surname}</p>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/" end className={navClassName} onClick={handleNavClick}>
            Dashboard
          </NavLink>
          <NavLink to="/sessions" className={navClassName} onClick={handleNavClick}>
            Training Sessions
          </NavLink>
          <NavLink to="/videos" className={navClassName} onClick={handleNavClick}>
            Videos
          </NavLink>
        </nav>

        <button className="sidebar-logout" onClick={handleLogout}>
          Log Out
        </button>
      </aside>

      <div className="main-wrapper">
        <header className="mobile-header">
          <button className="hamburger" onClick={() => setSidebarOpen(true)}>
            <span /><span /><span />
          </button>
          <span className="mobile-title">HPL</span>
        </header>
        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}