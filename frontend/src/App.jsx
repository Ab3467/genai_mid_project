import React, { useState } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setReview(null);
    try {
      const response = await axios.post("http://127.0.0.1:8000/review", {
        code,
        language,
        depth: "medium",
        context: "",
      });
      setReview(response.data);
    } catch (err) {
      console.error(err);
      alert("Error fetching review");
    } finally {
      setLoading(false);
    }
  };

  const renderReview = (reviewData) => {
    if (!reviewData?.ok) {
      return (
        <div className="error-box">
          ❌ Error: {reviewData.error || "Unknown error occurred."}
        </div>
      );
    }

    const data = reviewData.review;
    return (
      <div className="review-box">
        <h2>🧾 Summary</h2>
        <p>{data.summary}</p>

        {data.potential_issues && data.potential_issues.length > 0 && (
          <>
            <h3>⚠️ Potential Issues</h3>
            <ul>
              {data.potential_issues.map((issue, i) => (
                <li key={i} className="issue">
                  <strong>{issue.issue}</strong> —{" "}
                  <em>Severity:</em> {issue.severity || "N/A"}
                  <p>{issue.explanation}</p>
                  {issue.suggested_fix && (
                    <p className="fix">
                      💡 Suggested fix: {issue.suggested_fix}
                    </p>
                  )}
                </li>
              ))}
            </ul>
          </>
        )}

        {data.suggestions && data.suggestions.length > 0 && (
          <>
            <h3>💡 Suggestions</h3>
            <ul>
              {data.suggestions.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </>
        )}

        {data.score && (
          <p className="score">
            🧮 Overall Score: <strong>{data.score}</strong> / 100
          </p>
        )}
      </div>
    );
  };

  return (
    <div className="container">
      <h1>🧠 AI Code Reviewer</h1>

      <label>Language:</label>
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        style={{ marginLeft: "10px" }}
      >
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="cpp">C++</option>
      </select>

      <br />
      <br />

      <textarea
        placeholder="Paste your code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      ></textarea>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "🔍 Reviewing..." : "Review Code"}
      </button>

      {loading && <p style={{ marginTop: "10px" }}>⏳ Analyzing your code...</p>}

      {review && <div style={{ marginTop: "20px" }}>{renderReview(review)}</div>}
    </div>
  );
}

export default App;
