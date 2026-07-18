import { useState, useRef, useEffect } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const SUGGESTIONS = [
  "I want to learn Python",
  "Teach me Machine Learning",
  "Best courses for Web Development",
  "I'm a beginner in Data Science",
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = Math.min(ta.scrollHeight, 120) + "px";
    }
  }, [input]);

  const sendMessage = async (text) => {
    const trimmed = (text || input).trim();
    if (!trimmed || loading) return;

    const userMsg = { role: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      if (!res.ok) throw new Error(`Server error (${res.status})`);

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: data.response || "No response received." },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: `⚠️ ${err.message}. Make sure the backend is running.` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const isEmpty = messages.length === 0;

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-icon">🎓</div>
        <div className="header-text">
          <h1>Knowledge Navigator</h1>
          <p>AI-powered academic advisor</p>
        </div>
        <div className="header-status">
          <span className="status-dot"></span>
          Online
        </div>
      </header>

      {/* Chat area */}
      <div className="chat-area" id="chat-area">
        {isEmpty ? (
          <div className="welcome">
            <div className="welcome-icon">🎓</div>
            <h2>What do you want to learn?</h2>
            <p>
              I'll find the best courses and build you a personalized learning
              roadmap. Just tell me a topic, your level, and your budget.
            </p>
            <div className="welcome-suggestions">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  className="suggestion-chip"
                  onClick={() => sendMessage(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <div key={i} className={`message-row ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === "user" ? "👤" : "🎓"}
                </div>
                <div className="message-content">
                  <span className="message-label">
                    {msg.role === "user" ? "You" : "Navigator"}
                  </span>
                  <div className="message-bubble">{msg.text}</div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="typing-row">
                <div className="message-avatar" style={{
                  background: "linear-gradient(135deg, #6366f1, #a78bfa)",
                  width: 30, height: 30, borderRadius: "50%",
                  display: "grid", placeItems: "center", fontSize: "0.8rem"
                }}>
                  🎓
                </div>
                <div className="typing-bubble">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </>
        )}
      </div>

      {/* Input area */}
      <div className="input-area">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask what you want to learn…"
            rows={1}
            id="chat-input"
          />
          <button
            className="send-btn"
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
            aria-label="Send message"
            id="send-button"
          >
            ➜
          </button>
        </div>
        <p className="input-hint">
          Press Enter to send · Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}
