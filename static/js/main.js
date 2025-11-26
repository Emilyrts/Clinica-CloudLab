const API_BASE_URL = 'http://localhost:5000'; 
const loginEndpoint = '/auth/login';

// ===============================================
// 1. LÓGICA DE LOGIN
// ===============================================

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
    
    // 🚨 AJUSTE 1: Usa a API_BASE_URL completa na chamada fetch
    const urlCompleta = API_BASE_URL + loginEndpoint;

    fetch(urlCompleta, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(credenciais) 
    })
    .then(response => {
        // Verifica se a resposta HTTP indica sucesso (2xx)
        if (!response.ok) {
            // Se for 401 (Não Autorizado), lança erro específico
            if (response.status === 401) {
                throw new Error('Email ou senha inválidos.');
            }
            // Para outros erros (404, 500, etc.)
            throw new Error(`Erro de comunicação com o servidor: ${response.status}`);
        }
        return response.json(); 
    })
    .then(data => {
        console.log('Login bem-sucedido!', data);
        
        // 🚨 O seu backend pode retornar 'access_token' ou 'token'
        const token = data.token || data.access_token;

        if (token) { 
            localStorage.setItem('authToken', token);
        }

        statusElement.textContent = 'Login realizado com sucesso! Redirecionando...';
        statusElement.style.color = 'green';

        setTimeout(() => {
            // 🚨 Use o URL completo ou relativo conforme a estrutura do Flask
            window.location.href = '/agendamentos/'; // Exemplo: Redireciona para a página de agendamentos
        }, 1000);

    })
    .catch(error => {
        statusElement.textContent = `Erro: ${error.message}`;
        statusElement.style.color = 'red';
        console.error('Falha no login:', error);
    });
}

// ===============================================
// 2. LÓGICA DE AGENDAMENTO E VALOR
// ===============================================

// 🚨 AJUSTE 2: Função de formatação de moeda fora do escopo de DOMContentLoaded
function formatarMoeda(valor) {
    // Garante que o valor é um número
    const num = parseFloat(valor);
    if (isNaN(num)) return 'R$ 0,00';
    // Adiciona uma camada de segurança contra números muito grandes
    return 'R$ ' + num.toFixed(2).replace('.', ',');
}

// 🚨 AJUSTE 3: Função de atualização de valor agora usa o valor formatado corretamente
function atualizarValor() {
    // 1. Obtém o elemento <select> de exames pelo ID
    const selectExame = document.getElementById('exame');
    
    // 2. Obtém o campo de input "Total a pagar" pelo ID
    const inputValor = document.getElementById('valor');
    
    // 3. Pega a opção que está selecionada
    const selectedOption = selectExame.options[selectExame.selectedIndex];
    
    // 4. Extrai o valor numérico do atributo 'data-valor'
    const valorExame = selectedOption.getAttribute('data-valor');
    
    if (valorExame && parseFloat(valorExame) >= 0) {
        // Converte para número e formata para a moeda brasileira (R$)
        // Ex: 55.5 vira R$ 55,50
        const valorFormatado = parseFloat(valorExame).toLocaleString('pt-BR', { 
            style: 'currency', 
            currency: 'BRL' 
        });
        
        // 5. Atualiza o input "Total a pagar"
        inputValor.value = valorFormatado;
    } else {
        // Define o valor padrão R$ 0,00 se a opção "Selecionar" for escolhida
        inputValor.value = "R$ 0,00";
    }
}


document.addEventListener('DOMContentLoaded', () => {
    // Garante que o valor inicial seja R$ 0,00 ao carregar
    atualizarValor(); 
    
    const form = document.getElementById('agendamento-form');
    
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
    
            // Cria um objeto FormData
            const formData = new FormData(form);
    
            // Adiciona dados que não têm 'name' no HTML, como a data/hora combinada
            
            const dataAgendamento = document.getElementById('data_agendamento').value;
            const horaAgendamento = document.getElementById('hora_agendamento').value;
            const cpfPaciente = document.getElementById('cpf-paciente').value;
    
            // 🚨 Combina data e hora no formato esperado pelo Flask
            const data_hora_combinada = `${dataAgendamento} ${horaAgendamento}:00`; 
            
            // Adiciona os campos para o Flask buscar com request.form.get()
            formData.append('data_agendamento', dataAgendamento);
            formData.append('hora_agendamento', horaAgendamento);
            formData.append('cpf_paciente', cpfPaciente);
            formData.append('data_hora', data_hora_combinada); // Campo que você usa no Flask para datetime.strptime
            
            // 🚨 Remove os campos individuais do FormData para evitar duplicidade no envio
            // formData.delete('data_agendamento'); // Já corrigido ao usar 'data_agendamento' no JS de forma seletiva
            // formData.delete('hora_agendamento'); // Já corrigido
            
            // 🚨 AJUSTE 4: Envia os dados e processa a resposta!
            try {
                const response = await fetch('/agendamentos/criar_agendamento', {
                    method: 'POST',
                    body: formData 
                });

                const resultado = await response.json();
    
                if (response.ok) {
                    alert('✅ Agendamento criado com sucesso!');
                    // Redireciona ou limpa o formulário
                    window.location.href = '/agendamentos/historico';
                } else {
                    alert('❌ Falha ao agendar: ' + resultado.erro);
                    console.error('Erro no servidor:', resultado.erro);
                }

            } catch (error) {
                alert('❌ Erro de conexão ou processamento.');
                console.error('Erro na requisição:', error);
            }
        });
    }
    
    // 🚨 Adiciona um listener para atualizar o valor quando o select mudar
    const selectExame = document.getElementById('fk_exame');
    if (selectExame) {
        selectExame.addEventListener('change', atualizarValor);
    }
});