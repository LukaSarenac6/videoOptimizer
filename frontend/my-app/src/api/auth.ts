import { apiRequest, setToken } from "./client";

const BASE_URL = "http://localhost:8000";

interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function login(email: string, password: string): Promise<void> {
  // OAuth2 expects form data with "username" field (even though we use email)
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${BASE_URL}/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(error.detail || "Login failed");
  }

  const data: TokenResponse = await response.json();
  setToken(data.access_token);
}

export interface UserCreate {
  name: string;
  surname: string;
  email: string;
  password: string;
}

export interface UserRead {
  id: number;
  name: string;
  surname: string;
  email: string;
  is_admin: boolean;
}

export function registerUser(user: UserCreate): Promise<UserRead> {
  return apiRequest<UserRead>("/register", {
    method: "POST",
    body: JSON.stringify(user),
  });
}
