let isLoginMode = true;
let authModal;

document.addEventListener('DOMContentLoaded', () => {
    authModal = new bootstrap.Modal(document.getElementById('authModal'));
    checkAuth();
});

async function checkAuth() {
    const res = await fetch('/api/me');
    const data = await res.json();
    if (data.logged_in) {
        document.getElementById('authBtn').textContent = 'Выйти';
        document.getElementById('userInfo').textContent = data.username;
        if (data.is_admin) {
            document.getElementById('resetBtn').style.display = 'inline-block';
        }
    }
}

function toggleAuth() {
    const btn = document.getElementById('authBtn');
    if (btn.textContent === 'Выйти') {
        fetch('/api/logout').then(() => location.reload());
    } else {
        authModal.show();
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const url = isLoginMode ? '/api/login' : '/api/register';
    const res = await fetch(url, { method: 'POST', body: formData });
    const data = await res.json();
    
    if (res.ok) {
        location.reload();
    } else {
        const err = document.getElementById('authError');
        err.textContent = data.detail || 'Ошибка';
        err.style.display = 'block';
    }
}

function switchAuth() {
    isLoginMode = !isLoginMode;
    document.getElementById('authTitle').textContent = isLoginMode ? 'Вход' : 'Регистрация';
    document.getElementById('authSubmit').textContent = isLoginMode ? 'Войти' : 'Зарегистрироваться';
    document.getElementById('switchToRegister').textContent = isLoginMode ? 'Регистрация' : 'Вход';
}

async function resetVotes() {
    if (confirm('Сбросить все голоса?')) {
        const res = await fetch('/api/reset-votes', { method: 'POST' });
        if (res.ok) location.reload();
        else alert('Нет прав администратора');
    }
}