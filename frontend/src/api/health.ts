import { apiClient } from "./client";

export interface HealthData {
  status: string;
  db: boolean;
}

export async function getHealth(): Promise<HealthData> {
  const res = await apiClient.get("/health");
  return res.data.data;
}
