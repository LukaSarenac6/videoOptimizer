import { useState } from "react";
import { createAthlete } from "../api/athletes";
import Modal from "./Modal";
import "./AddAthleteDialog.css";

interface AddAthleteDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AddAthleteDialog({
  isOpen,
  onClose,
  onSuccess,
}: AddAthleteDialogProps) {
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function resetForm() {
    setName("");
    setSurname("");
    setEmail("");
    setPhoneNumber("");
    setError("");
  }

  function handleClose() {
    resetForm();
    onClose();
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await createAthlete({
        name,
        surname,
        email,
        phone_number: phoneNumber,
      });
      resetForm();
      onSuccess();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create athlete");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Add Athlete">
      <form className="athlete-form" onSubmit={handleSubmit}>
        {error && <div className="athlete-form-error">{error}</div>}

        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Surname"
          value={surname}
          onChange={(e) => setSurname(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="tel"
          placeholder="Phone number"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Adding..." : "Add Athlete"}
        </button>
      </form>
    </Modal>
  );
}