import { useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./HomePage.css";

export default function HomePage() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const { logout } = useAuth();

  function addCategory() {
    console.log("cat");
  }

  function addSubCategory() {
    console.log("sub-cat");
  }

  function addVideo() {
    fileInputRef.current?.click();
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Video Optimizer</h1>
        <button className="btn-logout" onClick={handleLogout}>
          Log Out
        </button>
      </header>

      <div className="home-actions">
        <button className="btn-action" onClick={addCategory}>
          Add Category
        </button>
        <button className="btn-action" onClick={addSubCategory}>
          Add Sub-Category
        </button>
        <button className="btn-action" onClick={addVideo}>
          Add Video
        </button>
        <input
          type="file"
          style={{ display: "none" }}
          ref={fileInputRef}
        />
      </div>
    </div>
  );
}
