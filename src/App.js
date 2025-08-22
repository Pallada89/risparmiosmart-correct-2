import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Imposta questa variabile su Vercel → Settings → Environment Variables
  const API = process.env.REACT_APP_API_BASE;

  const handleFileChange = (e) => {
    setFile(e.target.files?.[0] ?? null);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Seleziona prima un file!");
      return;
    }
    if (!API) {
      alert("Configura REACT_APP_API_BASE su Vercel (URL del backend OCR).");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fetch(`${API}/ocr`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setResult(data); // data è un oggetto → lo renderizziamo con JSON.stringify (vedi sotto)
    } catch (err) {
      console.error(err);
      alert("Errore durante l'analisi OCR");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: 16, fontFamily: "sans-serif", maxWidth: 800, margin: "0 auto" }}>
      <h1>RisparmioSmart</h1>
      <p>Carica un volantino (immagine) e invialo al backend OCR.</p>

      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Analisi in corso…" : "Carica e analizza"}
        </button>
      </div>

      {!API && (
        <p style={{ color: "crimson", marginTop: 12 }}>
          ⚠️ Variabile non configurata: <code>REACT_APP_API_BASE</code> su Vercel.
        </p>
      )}

      {result && (
        <section style={{ marginTop: 24 }}>
          <h2>Testo estratto</h2>
          <pre style={{ whiteSpace: "pre-wrap", background: "#f6f6f6", padding: 12, borderRadius: 8 }}>
            {result.text || "(nessun testo)"}
          </pre>

          <h3>Risposta completa (debug)</h3>
          <pre style={{ background: "#f6f6f6", padding: 12, borderRadius: 8 }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </section>
      )}
    </main>
  );
}

export default App;
