import { HashRouter, Routes, Route, Navigate } from "react-router-dom";
import LandingPage from "./LandingPage";
import ChatPage from "./ChatPage";

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </HashRouter>
  );
}
