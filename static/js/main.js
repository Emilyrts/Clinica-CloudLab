const API_BASE_URL = 'http://localhost:5000'; 
const loginEndpoint = '/auth/login';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const statusMessage = document.getElementById('mensagemStatus');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); 
            
            const email = document.getElementById('emailInput').value;
            const senha = document.getElementById('senhaInput').value;
            
            statusMessage.textContent = 'Carregando...';
            statusMessage.style.color = 'blue';

            efetuarLogin(email, senha, statusMessage);
        });
    }
});


function efetuarLogin(email, senha, statusElement) {
    
    const credenciais = {
        identificador: email, 
        senha: senha 
    };

    fetch(loginEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(credenciais) 
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Email ou senha inválidos.');
            }
            throw new Error(`Erro de comunicação com o servidor: ${response.status}`);
        }
        return response.json(); 
    })
    .then(data => {
        console.log('Login bem-sucedido!', data);
        
        if (data.token) { 
            localStorage.setItem('authToken', data.token);
        }

        statusElement.textContent = 'Login realizado com sucesso! Redirecionando...';
        statusElement.style.color = 'green';

        setTimeout(() => {
            window.location.href = '/pacientes/home';
        }, 1000);

    })
    .catch(error => {
        statusElement.textContent = `Erro: ${error.message}`;
        statusElement.style.color = 'red';
        console.error('Falha no login:', error);
    });
}