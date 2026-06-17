import axios from "axios";
import { API_BASE_URL } from "./api";

export const getDashboardData = async () => {
  const response = await axios.get(
    `${API_BASE_URL}/dashboard`
  );

  return response.data;
};