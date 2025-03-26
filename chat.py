import React, { useState } from "react";

export default function ChatBox() {
  const [messages, setMessages] = useState([
    { user: "LeFan", text: "LeBron is the GOAT." },
    { user: "HoopsLover", text: "Facts only." },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (input.trim() === "") return;
    setMessages([...messages, { user: "You", text: input.trim() }]);
    setInput("");
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>💬 LeDiscussion</h2>
      <div style={styles.chatArea}>
        {messages.map((msg, idx) => (
          <div key={idx} style={styles.bubble}>
            <strong style={styles.user}>{msg.user}</strong>: {msg.text}
          </div>
        ))}
      </div>
      <div style={styles.inputRow}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={styles.input}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage} style={styles.button}>Send</button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "sans-serif",
    maxWidth: 500,
    margin: "auto",
    padding: 20,
    backgroundColor: "#f9f9f9",
    borderRadius: 12,
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
  },
  title: {
    textAlign: "center",
    marginBottom: 10,
  },
  chatArea: {
    maxHeight: 300,
    overflowY: "auto",
    marginBottom: 10,
    padding: 10,
    backgroundColor: "#fff",
    borderRadius: 8,
    border: "1px solid #ddd",
  },
  bubble: {
    padding: 8,
    borderBottom: "1px solid #eee",
  },
  user: {
    color: "#4b0082",
  },
  inputRow: {
    display: "flex",
    gap: 8,
  },
  input: {
    flex: 1,
    padding: 8,
    borderRadius: 6,
    border: "1px solid #ccc",
  },
  button: {
    padding: "8px 16px",
    backgroundColor: "purple",
    color: "white",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
  },
};
