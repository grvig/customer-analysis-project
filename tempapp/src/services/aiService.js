import axios from "axios";
import { API_BASE_URL } from "./api";

export const askQuestion = async (question) => {
  const response = await axios.post(
    `${API_BASE_URL}/ask`,
    {
      question,
    }
  );

  return response.data;
};