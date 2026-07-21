async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

let actionFilter = 'all';
const selectedActionIds = new Set();

function setActionStatus(message, isError = false) {
  const status = document.getElementById('action-status');
  status.textContent = message;
  status.classList.toggle('error', isError);
}

function updateBulkCompleteButton() {
  const button = document.getElementById('bulk-complete');
  button.disabled = selectedActionIds.size === 0;
  button.textContent = selectedActionIds.size
    ? `Complete selected (${selectedActionIds.size})`
    : 'Complete selected';
}

async function loadNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  const notes = await fetchJSON('/notes/');
  for (const n of notes) {
    const li = document.createElement('li');
    li.textContent = `${n.title}: ${n.content}`;
    list.appendChild(li);
  }
}

async function loadActions() {
  const list = document.getElementById('actions');
  const query = actionFilter === 'all'
    ? ''
    : `?completed=${actionFilter === 'completed'}`;

  try {
    const items = await fetchJSON(`/action-items/${query}`);
    list.innerHTML = '';
    const visibleIds = new Set(items.map((item) => item.id));
    for (const id of selectedActionIds) {
      if (!visibleIds.has(id)) selectedActionIds.delete(id);
    }

    for (const a of items) {
      const li = document.createElement('li');
      li.className = 'action-row';

      if (!a.completed) {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = selectedActionIds.has(a.id);
        checkbox.setAttribute('aria-label', `Select ${a.description}`);
        checkbox.onchange = () => {
          if (checkbox.checked) selectedActionIds.add(a.id);
          else selectedActionIds.delete(a.id);
          updateBulkCompleteButton();
        };
        li.appendChild(checkbox);

        const btn = document.createElement('button');
        btn.textContent = 'Complete';
        btn.onclick = async () => {
          btn.disabled = true;
          setActionStatus('');
          try {
            await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
            selectedActionIds.delete(a.id);
            await loadActions();
            setActionStatus(`Completed "${a.description}".`);
          } catch (error) {
            btn.disabled = false;
            setActionStatus(`Could not complete item: ${error.message}`, true);
          }
        };
        li.appendChild(btn);
      }

      const description = document.createElement('span');
      description.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
      li.insertBefore(description, li.lastChild);
      list.appendChild(li);
    }
    updateBulkCompleteButton();
  } catch (error) {
    setActionStatus(`Could not load action items: ${error.message}`, true);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    setActionStatus('');
    try {
      await fetchJSON('/action-items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description }),
      });
      e.target.reset();
      await loadActions();
      setActionStatus('Action item added.');
    } catch (error) {
      setActionStatus(`Could not add action item: ${error.message}`, true);
    }
  });

  document.querySelectorAll('#action-filters button').forEach((button) => {
    button.addEventListener('click', async () => {
      actionFilter = button.dataset.filter;
      selectedActionIds.clear();
      document.querySelectorAll('#action-filters button').forEach((filterButton) => {
        filterButton.setAttribute('aria-pressed', filterButton === button ? 'true' : 'false');
      });
      setActionStatus('');
      updateBulkCompleteButton();
      await loadActions();
    });
  });

  document.getElementById('bulk-complete').addEventListener('click', async () => {
    const ids = [...selectedActionIds];
    if (!ids.length) return;

    const button = document.getElementById('bulk-complete');
    button.disabled = true;
    setActionStatus('');
    try {
      await fetchJSON('/action-items/bulk-complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids }),
      });
      selectedActionIds.clear();
      await loadActions();
      setActionStatus(`Completed ${ids.length} action item${ids.length === 1 ? '' : 's'}.`);
    } catch (error) {
      setActionStatus(`Could not complete selected items: ${error.message}`, true);
    } finally {
      updateBulkCompleteButton();
    }
  });

  loadNotes();
  loadActions();
});
