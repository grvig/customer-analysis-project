import axios from "axios";
import { API_BASE_URL } from "./api";

export const login = async (username, password) => {
  const response = await axios.post(
    `${API_BASE_URL}/login`,
    {
      username,
      password,
    }
  );

  return response.data;
};
export const register = async (username, password) => {
  const response = await axios.post(
    `${API_BASE_URL}/register`,
    {
      username,
      password,
    }
  );

  return response.data;
};
export const logout = () => {
  localStorage.removeItem("user");
};