"use client";
import { useState } from "react";
import axios from "axios";

export default function UploadForm() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !description || !file) {
      setStatus("⚠ Please fill all fields and select a PDF.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append(
      "json",
      JSON.stringify({
        name,
        description,
      })
    );

    try {
      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus("✅ Upload successful! " + res.data.message);
    } catch (err) {
      setStatus("❌ Upload failed: " + (err.response?.data?.error || err.message));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      <label>Book Name:</label>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />

      <label>Description:</label>
      <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />

      <label>PDF File:</label>
      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} required />

      <button type="submit">Upload</button>
      {status && <p>{status}</p>}

      <style jsx>{`
        .upload-form {
          display: flex;
          flex-direction: column;
          width: 100%;
          max-width: 500px;
          gap: 12px;
          margin-top: 24px;
        }
        input, textarea {
          padding: 8px;
          border: 1px solid #ccc;
          border-radius: 8px;
        }
        button {
          padding: 10px;
          background: #0070f3;
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
        }
        button:hover {
          background: #005bbb;
        }
        p {
          margin-top: 10px;
          font-weight: bold;
        }
      `}</style>
    </form>
  );
}
