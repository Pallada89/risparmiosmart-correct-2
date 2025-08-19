const API = process.env.REACT_APP_API_BASE;

async function inviaOCR(file, supermarket) {
  const formData = new FormData();
  formData.append('file', file);
  if (supermarket) formData.append('supermarket', supermarket);

  const res = await fetch(`${API}/ocr`, { method: 'POST', body: formData });
  if (!res.ok) throw new Error('Errore OCR');
  return await res.json(); // { text, offers_extracted }
}
