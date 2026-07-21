async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  const text = await res.text();
  if (!res.ok) {
    let message = text || `Request failed (${res.status})`;
    try {
      const payload = JSON.parse(text);
      message = payload.detail || message;
    } catch (_) {
      // Keep the response text when the server did not return JSON.
    }
    throw new Error(message);
  }
  return text ? JSON.parse(text) : null;
}

let notesState = [];

function showNotesError(message = '') {
  const error = document.getElementById('notes-error');
  error.textContent = message;
  error.hidden = !message;
}

function renderNotes() {
  const list = document.getElementById('notes');
  list.replaceChildren();
  for (const note of notesState) {
    const li = document.createElement('li');
    li.className = 'note-item';

    const text = document.createElement('span');
    text.textContent = `${note.title}: ${note.content}`;

    const edit = document.createElement('button');
    edit.type = 'button';
    edit.textContent = 'Edit';
    edit.addEventListener('click', () => showNoteEditor(li, note));

    const remove = document.createElement('button');
    remove.type = 'button';
    remove.textContent = 'Delete';
    remove.addEventListener('click', () => deleteNote(note));

    const controls = document.createElement('span');
    controls.className = 'note-controls';
    controls.append(edit, remove);
    li.append(text, controls);
    list.appendChild(li);
  }
}

function showNoteEditor(li, note) {
  const title = document.createElement('input');
  title.value = note.title;
  title.maxLength = 200;
  title.required = true;

  const content = document.createElement('input');
  content.value = note.content;
  content.maxLength = 10000;
  content.required = true;

  const save = document.createElement('button');
  save.type = 'button';
  save.textContent = 'Save';
  save.addEventListener('click', () => updateNote(note, title.value, content.value));

  const cancel = document.createElement('button');
  cancel.type = 'button';
  cancel.textContent = 'Cancel';
  cancel.addEventListener('click', renderNotes);

  li.replaceChildren(title, content, save, cancel);
  title.focus();
}

async function updateNote(original, title, content) {
  showNotesError();
  const updated = { ...original, title, content };
  notesState = notesState.map((note) => (note.id === original.id ? updated : note));
  renderNotes();

  try {
    const saved = await fetchJSON(`/notes/${original.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    notesState = notesState.map((note) => (note.id === saved.id ? saved : note));
    renderNotes();
  } catch (error) {
    notesState = notesState.map((note) => (note.id === original.id ? original : note));
    renderNotes();
    showNotesError(`Could not update note: ${error.message}`);
  }
}

async function deleteNote(note) {
  showNotesError();
  const previousNotes = [...notesState];
  notesState = notesState.filter((item) => item.id !== note.id);
  renderNotes();

  try {
    await fetchJSON(`/notes/${note.id}`, { method: 'DELETE' });
  } catch (error) {
    notesState = previousNotes;
    renderNotes();
    showNotesError(`Could not delete note: ${error.message}`);
  }
}

async function loadNotes() {
  showNotesError();
  try {
    notesState = await fetchJSON('/notes/');
    renderNotes();
  } catch (error) {
    showNotesError(`Could not load notes: ${error.message}`);
  }
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  const items = await fetchJSON('/action-items/');
  for (const a of items) {
    const li = document.createElement('li');
    li.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    showNotesError();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    try {
      await fetchJSON('/notes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content }),
      });
      e.target.reset();
      await loadNotes();
    } catch (error) {
      showNotesError(`Could not create note: ${error.message}`);
    }
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  loadNotes();
  loadActions();
});
