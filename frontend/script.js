const API_BASE = location.origin || 'http://localhost:5000';

const uploadBtn = document.getElementById('uploadBtn');
const resumeFile = document.getElementById('resumeFile');
const resultContainer = document.getElementById('resultContainer');
const loading = document.getElementById('loading');
const searchBtn = document.getElementById('searchBtn');
const searchQuery = document.getElementById('searchQuery');
const searchResults = document.getElementById('searchResults');
const previewPanel = document.getElementById('previewPanel');
const textPreview = document.getElementById('textPreview');
const themeToggle = document.getElementById('themeToggle');

// Theme handling (light/dark)
function setThemeLight(isLight){
  if(isLight){
    document.body.classList.add('light');
    localStorage.setItem('rp_theme','light');
  } else {
    document.body.classList.remove('light');
    localStorage.setItem('rp_theme','dark');
  }
}

// init theme from storage
setThemeLight(localStorage.getItem('rp_theme') === 'light');
themeToggle.checked = localStorage.getItem('rp_theme') === 'light';
themeToggle.addEventListener('change', (e)=> setThemeLight(e.target.checked));

// Upload handler
uploadBtn.addEventListener('click', async () => {
  const file = resumeFile.files[0];
  if (!file) { alert('Please choose a resume file first!'); return; }
  const formData = new FormData();
  formData.append('file', file);
  loading.classList.remove('hidden');
  resultContainer.innerHTML = '';
  textPreview.textContent = 'Loading preview...';

  try {
    const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: formData });
    const data = await res.json();
    loading.classList.add('hidden');
    if (data.error) { resultContainer.innerHTML = `<p style="color:red;">Error: ${data.error}</p>`; textPreview.textContent = 'No preview available.'; return; }
    const parsed = data.parsed;
    resultContainer.innerHTML = `
      <h3>🧠 Parsed Information</h3>
      <p><b>Name:</b> ${parsed.full_name || 'N/A'}</p>
      <p><b>Email:</b> ${parsed.emails?.join(', ') || 'N/A'}</p>
      <p><b>Phone:</b> ${parsed.phones?.join(', ') || 'N/A'}</p>
      <p><b>Skills:</b> ${parsed.skills?.join(', ') || 'N/A'}</p>
      <p><b>Education:</b> ${parsed.education.map(e=> `${e.degree||''} ${e.institution||''}`).join('; ') || 'N/A'}</p>
      <p><b>Experience:</b> ${parsed.experience.map(e=> `${e.title||''} ${e.company||''}`).join('; ') || 'N/A'}</p>
    `;
    // show full text preview
    textPreview.textContent = parsed.full_text || 'No text extracted from document.';
    previewPanel.open = true;
  } catch (err) {
    loading.classList.add('hidden');
    resultContainer.innerHTML = `<p style="color:red;">Upload failed. Check backend logs.</p>`;
    textPreview.textContent = 'No preview available.';
  }
});

// Search handler
searchBtn.addEventListener('click', async () => {
  const q = searchQuery.value.trim();
  if (!q) return;
  searchResults.innerHTML = '🔍 Searching...';
  const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  if (!data.length) { searchResults.innerHTML = '<p>No candidates found.</p>'; return; }
  searchResults.innerHTML = data.map(c => `
    <div class="candidate-card">
      <p><b>${c.full_name}</b></p>
      <p>${c.email || ''}</p>
      <p><small>${c.summary?.slice(0,120) || ''}...</small></p>
    </div>
  `).join('<hr>');
});
