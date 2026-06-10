import { sampleReport } from "../mock/reportMock";

export const generateReport = async (type) => {
  console.log(type);

  return {
    success: true,
    report_type: type,
    report: sampleReport,
  };
};