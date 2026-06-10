import { mockAIResponse } from "../mock/aiMock";

export const askQuestion = async (question) => {
  console.log(question);

  return mockAIResponse;
};