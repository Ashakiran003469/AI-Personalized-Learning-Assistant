import React, { useState } from "react";

function App() {
  const [level, setLevel] = useState("");
  const [subject, setSubject] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askAI = async () => {
    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        level,
        subject,
        question,
      }),
    });

    const data = await res.json();
    setAnswer(data.answer || "No response");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>SDG 4 – AI Education Tutor</h1>

      <input
        placeholder="Level (e.g. Class 10)"
        value={level}
        onChange={(e) => setLevel(e.target.value)}
      />
      <br /><br />

      <input
        placeholder="Subject (e.g. Math)"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
      />
      <br /><br />

      <textarea
        placeholder="Ask your question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <br /><br />

      <button onClick={askAI}>Ask AI</button>

      <h3>Answer:</h3>
      <p>{answer}</p>
    </div>
  );
}

export default App;
