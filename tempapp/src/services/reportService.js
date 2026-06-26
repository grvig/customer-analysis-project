import api from "./api";

export const generateReport = async (type) => {
  const response = await api.post("/report", { report_type: type });
  return response.data;
};

export const generateCustomReport = async (question) => {
  const response = await api.post("/report/custom", { question });
  return response.data;
};

export const downloadPdfReport = async (type) => {
  const response = await api.post("/report/pdf", { report_type: type });
  return response.data;
};
