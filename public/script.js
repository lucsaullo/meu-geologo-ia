// Arquivo: public/script.js

// Seleciona os elementos do HTML com os quais vamos interagir
const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

// Adiciona um "escutador" para o evento de envio do formulário
chatForm.addEventListener('submit', async (e) => {
    // Previne o comportamento padrão do formulário (que é recarregar a página)
    e.preventDefault();

    const userMessage = userInput.value.trim();
    if (!userMessage) return; // Não faz nada se a mensagem estiver vazia

    // 1. Adiciona a mensagem do usuário à tela
    addMessage(userMessage, 'user-message');
    userInput.value = ''; // Limpa o campo de digitação

    // 2. Mostra um indicador de que o bot está "pensando"
    addMessage('Pensando...', 'bot-message', true);

    try {
        // 3. Envia a pergunta para o nosso backend na Netlify
        // O endpoint '/.netlify/functions/ask_geologist' é um caminho padrão da Netlify para a sua função
        const response = await fetch('/.netlify/functions/ask_geologist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: userMessage })
        });

        // 4. Remove a mensagem de "Pensando..."
        removeTypingIndicator();

        if (!response.ok) {
            // Se a resposta do servidor não for bem-sucedida, joga um erro
            throw new Error('Houve um problema com a resposta do servidor.');
        }

        const data = await response.json();
        
        // 5. Formata a resposta do bot com a fonte e a página
        const botResponseHTML = `
            ${data.answer}
            <div class="source">
                <strong>Fonte no Livro:</strong> "${data.source_quote}"
                <br>
                <strong>Página:</strong> ${data.source_page}
            </div>
        `;
        addMessage(botResponseHTML, 'bot-message');

    } catch (error) {
        console.error('Erro ao buscar resposta:', error);
        removeTypingIndicator();
        addMessage('Desculpe, ocorreu um erro ao tentar obter uma resposta. Tente novamente.', 'bot-message');
    }
});

/**
 * Função para adicionar uma nova mensagem ao chat box
 * @param {string} content - O texto ou HTML da mensagem
 * @param {string} className - A classe CSS para estilizar a mensagem (user-message ou bot-message)
 * @param {boolean} isTyping - Se for verdadeiro, adiciona um ID para o indicador de "digitando"
 */
function addMessage(content, className, isTyping = false) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', className);
    if (isTyping) {
        messageElement.id = 'typing-indicator';
    }
    messageElement.innerHTML = content; // Usamos innerHTML para renderizar o HTML da resposta do bot
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Rola automaticamente para a mensagem mais recente
}

/**
 * Função para remover o indicador de "Pensando..."
 */
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}
