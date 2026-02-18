import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Layout.css";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>HPL</h1>
          <p className="sidebar-user">{user?.name} {user?.surname}</p>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/" end className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Dashboard
          </NavLink>
          <NavLink to="/sessions" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Training Sessions
          </NavLink>
          <NavLink to="/videos" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Videos
          </NavLink>
        </nav>

        <button className="sidebar-logout" onClick={handleLogout}>
          Log Out
        </button>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}