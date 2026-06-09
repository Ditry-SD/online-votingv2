/**
 * Система онлайн голосования — клиентская логика
 * Автор: Морозов Д.В., ПИН-б-з-22-1
 */

let currentVotes = {};

document.addEventListener('DOMContentLoaded', async () => {
    await loadCandidates();
    setInterval(updateVotes, 3000);
});

async function loadCandidates() {
    try {
        const response = await fetch('/api/candidates');
        if (!response.ok) throw new Error('Ошибка загрузки');
        const candidates = await response.json();
        candidates.forEach(c => { currentVotes[c.id] = c.votes; });
        displayCandidates(candidates);
        
        // Проверяем, голосовал ли уже пользователь
        const votedRes = await fetch('/api/has-voted');
        const votedData = await votedRes.json();
        if (votedData.voted) {
            disableAllButtons();
        }
    } catch (error) {
        showMessage('Не удалось загрузить список кандидатов.', 'danger');
    }
}

async function updateVotes() {
    try {
        const response = await fetch('/api/candidates');
        if (!response.ok) return;
        const candidates = await response.json();
        
        candidates.forEach(candidate => {
            const oldVotes = currentVotes[candidate.id] || 0;
            const newVotes = candidate.votes;
            
            if (newVotes !== oldVotes) {
                const badge = document.querySelector(`.vote-count[data-id="${candidate.id}"] .badge`);
                if (badge) {
                    badge.style.transform = 'scale(1.3)';
                    badge.style.transition = 'transform 0.2s ease';
                    badge.textContent = newVotes;
                    setTimeout(() => { badge.style.transform = 'scale(1)'; }, 200);
                }
                currentVotes[candidate.id] = newVotes;
            }
        });
    } catch(e) {}
}

function displayCandidates(candidates) {
    const container = document.getElementById('candidates-container');
    container.innerHTML = '';
    
    candidates.forEach(candidate => {
        const cardHTML = `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">${escapeHTML(candidate.name)}</h5>
                        <p class="card-text">${escapeHTML(candidate.description)}</p>
                        <div class="vote-count" data-id="${candidate.id}">
                            Голосов: <span class="badge bg-primary">${candidate.votes}</span>
                        </div>
                        <button class="btn btn-primary vote-btn" 
                                data-id="${candidate.id}"
                                data-name="${escapeHTML(candidate.name)}">
                            Голосовать
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', cardHTML);
    });
    
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', handleVote);
    });
}

async function handleVote(event) {
    const button = event.target;
    const candidateId = button.dataset.id;
    const candidateName = button.dataset.name;
    
    try {
        const response = await fetch(`/api/vote/${candidateId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        
        if (response.ok) {
            showMessage(`✅ ${data.message}`, 'success');
            disableAllButtons();
            await loadCandidates();
            setTimeout(() => {
                document.getElementById('message').style.display = 'none';
            }, 3000);
        } else {
            showMessage(`⚠️ ${data.detail}`, 'warning');
        }
    } catch (error) {
        showMessage('Ошибка при голосовании.', 'danger');
    }
}

function disableAllButtons() {
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.disabled = true;
        btn.textContent = '✓ Голос учтен';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-success');
    });
}

function enableAllButtons() {
    document.querySelectorAll('.vote-btn').forEach(btn => {
        btn.disabled = false;
        btn.textContent = 'Голосовать';
        btn.classList.remove('btn-success');
        btn.classList.add('btn-primary');
    });
}

function showMessage(text, type) {
    // Удаляем старое сообщение если есть
    const old = document.getElementById('popup-message');
    if (old) old.remove();
    
    // Создаём новое с правильными стилями
    const div = document.createElement('div');
    div.id = 'popup-message';
    div.className = `alert alert-${type} text-center`;
    div.textContent = text;
    div.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 9999; min-width: 320px;';
    document.body.appendChild(div);
    
    setTimeout(() => div.remove(), 3000);
}

function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Слушаем сброс голосов админом — разблокируем кнопки
setInterval(async () => {
    try {
        const res = await fetch('/api/candidates');
        const candidates = await res.json();
        const totalVotes = candidates.reduce((sum, c) => sum + c.votes, 0);
        
        if (totalVotes === 0 && Object.values(currentVotes).some(v => v > 0)) {
            location.reload();
        }
    } catch(e) {}
}, 5000);