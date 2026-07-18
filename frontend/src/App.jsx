import { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import axios from "axios";
import { addMessage, clearMessages } from "./crmSlice";

const API_URL = "http://127.0.0.1:8000/chat/";

function App() {
  const dispatch = useDispatch();
  const messages = useSelector((state) => state.crm.messages);

  const [chatInput, setChatInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    hcpId: "1",
    summary: "",
    products: "",
    followUpDate: "",
  });

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    dispatch(
      addMessage({
        sender: "user",
        text: messageText,
      })
    );

    setLoading(true);

    try {
      const response = await axios.post(API_URL, {
        message: messageText,
      });

      dispatch(
        addMessage({
          sender: "ai",
          text: response.data.response,
        })
      );
    } catch (error) {
      dispatch(
        addMessage({
          sender: "ai",
          text: "Backend connection failed. Please check if FastAPI is running.",
        })
      );
    } finally {
      setLoading(false);
    }
  };

  const handleChatSubmit = (e) => {
    e.preventDefault();
    sendMessage(chatInput);
    setChatInput("");
  };

  const handleStructuredSubmit = (e) => {
    e.preventDefault();

    const prompt = `Log an interaction for HCP ID ${formData.hcpId}. Summary: ${formData.summary}. Products discussed: ${formData.products}. Follow up date is ${formData.followUpDate}.`;

    sendMessage(prompt);

    setFormData({
      hcpId: "1",
      summary: "",
      products: "",
      followUpDate: "",
    });
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AI-First HCP CRM</h1>
          <p>Structured and conversational interaction logging for field representatives</p>
        </div>
        <span className="badge">React + Redux + LangGraph</span>
      </header>

      <main className="layout">
        <section className="card">
          <h2>Structured Log Interaction</h2>
          <p className="muted">
            Log Healthcare Professional interaction details using a structured CRM form.
          </p>

          <form onSubmit={handleStructuredSubmit} className="form">
            <label>
              HCP ID
              <input
                value={formData.hcpId}
                onChange={(e) =>
                  setFormData({ ...formData, hcpId: e.target.value })
                }
              />
            </label>

            <label>
              Interaction Summary
              <textarea
                value={formData.summary}
                onChange={(e) =>
                  setFormData({ ...formData, summary: e.target.value })
                }
                placeholder="Discussed diabetes therapy benefits..."
                required
              />
            </label>

            <label>
              Products Discussed
              <input
                value={formData.products}
                onChange={(e) =>
                  setFormData({ ...formData, products: e.target.value })
                }
                placeholder="DiabetesCare RX"
              />
            </label>

            <label>
              Follow-up Date
              <input
                type="date"
                value={formData.followUpDate}
                onChange={(e) =>
                  setFormData({ ...formData, followUpDate: e.target.value })
                }
              />
            </label>

            <button type="submit">Log Interaction</button>
          </form>

          <div className="quick-actions">
            <button onClick={() => sendMessage("Search HCPs named Raj")}>
              Search HCP
            </button>

            <button onClick={() => sendMessage("Show interaction history for HCP ID 1")}>
              View History
            </button>

            <button onClick={() => sendMessage("Suggest next action for HCP ID 1")}>
              Next Action
            </button>
          </div>
        </section>

        <section className="card chat-card">
          <div className="chat-header">
            <div>
              <h2>Conversational AI Assistant</h2>
              <p className="muted">
                Ask the CRM assistant to search, log, edit, or suggest actions.
              </p>
            </div>

            <button className="secondary" onClick={() => dispatch(clearMessages())}>
              Clear
            </button>
          </div>

          <div className="chat-box">
            {messages.length === 0 && (
              <div className="empty">
                Try: “Search HCPs named Raj” or “Suggest next action for HCP ID 1”
              </div>
            )}

            {messages.map((msg, index) => (
              <div
                key={index}
                className={msg.sender === "user" ? "message user" : "message ai"}
              >
                <strong>{msg.sender === "user" ? "You" : "AI Assistant"}</strong>
                <p>{msg.text}</p>
              </div>
            ))}

            {loading && <div className="loading">AI is thinking...</div>}
          </div>

          <form onSubmit={handleChatSubmit} className="chat-input">
            <input
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              placeholder="Ask CRM assistant..."
            />
            <button type="submit">Send</button>
          </form>
        </section>
      </main>
    </div>
  );
}

export default App;