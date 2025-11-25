// A URL base da sua API (ajuste conforme o seu servidor Python)
const API_BASE_URL = 'http://localhost:5000'; 
const loginEndpoint = '/auth/login'; // Exemplo: /login ou /paciente/login

document.addEventListener('DOMContentLoaded', () => {
    // 1. Pega a referência do formulário HTML
    const loginForm = document.getElementById('loginForm');
    const statusMessage = document.getElementById('mensagemStatus');

    if (loginForm) {
        // 2. Adiciona um "ouvinte" para o evento de SUBMISSÃO do formulário
        loginForm.addEventListener('submit', function(event) {
            // Previne o comportamento padrão (recarregar a página)
            event.preventDefault(); 
            
            // Pega os valores dos campos de input
            const email = document.getElementById('emailInput').value;
            const senha = document.getElementById('senhaInput').value;
            
            // Limpa mensagens anteriores
            statusMessage.textContent = 'Carregando...';
            statusMessage.style.color = 'blue';

            // Chama a função que fará a comunicação com a API
            efetuarLogin(email, senha, statusMessage);
        });
    }
});

/**
 * Envia as credenciais para a API e lida com a resposta.
 * @param {string} email - E-mail do usuário.
 * @param {string} senha - Senha do usuário.
 * @param {HTMLElement} statusElement - Elemento onde exibir a mensagem de status.
 */
function efetuarLogin(email, senha, statusElement) {
    
    const credenciais = {
        // As chaves devem corresponder ao que sua API (Python) espera
        identificador: email, 
        senha: senha 
    };

    fetch(loginEndpoint, {
        method: 'POST',
        headers: {
            // CRÍTICO: Informa que o corpo da requisição é JSON
            'Content-Type': 'application/json' 
        },
        // Converte o objeto JavaScript em uma string JSON para envio
        body: JSON.stringify(credenciais) 
    })
    .then(response => {
        // Se a API retornar um status de erro (ex: 401 Unauthorized)
        if (!response.ok) {
            // Lança um erro para ser capturado no .catch()
            if (response.status === 401) {
                throw new Error('Email ou senha inválidos.');
            }
            throw new Error(`Erro de comunicação com o servidor: ${response.status}`);
        }
        // Se for sucesso, processa o JSON
        return response.json(); 
    })
    .then(data => {
        // Sucesso: A API geralmente retorna um token JWT ou dados do usuário
        console.log('Login bem-sucedido!', data);
        
        // 🔑 3. PASSO DE AUTENTICAÇÃO: Armazena o token
        // Use o nome da chave que sua API retorna (ex: data.access_token)
        if (data.token) { 
            localStorage.setItem('authToken', data.token);
        }

        statusElement.textContent = 'Login realizado com sucesso! Redirecionando...';
        statusElement.style.color = 'green';

        // 4. Redireciona o usuário para a página inicial ou área restrita
        setTimeout(() => {
            window.location.href = '/pacientes/home'; // Redireciona para a página principal
        }, 1000);

    })
    .catch(error => {
        // Trata erros de rede, CORS, ou falha de login (401)
        statusElement.textContent = `Erro: ${error.message}`;
        statusElement.style.color = 'red';
        console.error('Falha no login:', error);
    });
}