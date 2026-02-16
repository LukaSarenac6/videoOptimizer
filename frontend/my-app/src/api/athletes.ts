import { apiRequest } from "./client";

export interface Athlete {
  id: number;
  name: string;
  surname: string;
  email: string;
}

export interface AthleteCreate {
  name: string;
  surname: string;
  email: string;
}

export function getAthletes(): Promise<Athlete[]> {
  return apiRequest<Athlete[]>("/athletes");
}

export function createAthlete(athlete: AthleteCreate): Promise<Athlete> {
  return apiRequest<Athlete>("/athlete", {
    method: "POST",
    body: JSON.stringify(athlete),
  });
}
