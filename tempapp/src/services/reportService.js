import axios from "axios";
import { API_BASE_URL } from "./api";

export const generateReport = async (type) => {
  const response = await axios.post(
    `${API_BASE_URL}/report`,
    {
      report_type: type,
    }
  );

  return response.data;
};

export const generateCustomReport = async (question) => {
  const response = await axios.post(
    `${API_BASE_URL}/report/custom`,
    {
      question,
    }
  );

  return response.data;
};
export const downloadPdfReport = async (type) => {
  const response = await axios.post(
    `${API_BASE_URL}/report/pdf`,
    {
      report_type: type,
    }
  );

  return response.data;
};