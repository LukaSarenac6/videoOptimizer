import { useState } from "react";
import AddAthleteDialog from "../components/AddAthleteDialog";
import "./HomePage.css";

export default function HomePage() {
  const [showAddAthlete, setShowAddAthlete] = useState(false);

  return (
    <div className="home-container">
      <h1 className="home-title">Dashboard</h1>

      <div className="home-actions">
        <button className="btn-action" onClick={() => setShowAddAthlete(true)}>
          Add Athlete
        </button>
      </div>

      <AddAthleteDialog
        isOpen={showAddAthlete}
        onClose={() => setShowAddAthlete(false)}
        onSuccess={() => {}}
      />
    </div>
  );
}