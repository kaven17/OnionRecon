import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 30000
});

// Dashboard stats endpoint
export const fetchDashboardStats = () => API.get("/stats");

// Matches backend
export const collectNodes = () => API.get("/collect");

export const uploadPCAP = (file) => {
  const form = new FormData();
  form.append("file", file);
  return API.post("/upload_pcap", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};

export const runCorrelation = () => API.get("/correlate");

export const generateReport = () =>
  API.get("/report", { responseType: "blob" });

export const fetchGraphData = () => API.get("/graph");


export default API;