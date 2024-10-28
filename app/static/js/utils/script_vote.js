$(document).ready(function() {
    console.log("Script de voto carregado");

    // Configura o token CSRF para requisições AJAX
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Intercepta o evento de envio do formulário de votação
    $('.vote-section form').on('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        const form = $(this);
        const url = form.attr('data-url');
        const button = form.find('.vote-button');  // Seleciona o botão de voto

        if (!url) {
            console.error("URL de destino não encontrada");
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function(response) {
                if (response.success) {
                    alert('Voto registrado com sucesso!');
                    button.addClass('voted').removeClass('unvoted');
                    createParticles(button);
                } else {
                    alert('Voto removido com sucesso!');
                    button.addClass('unvoted').removeClass('voted');
                }

                // Atualizar a contagem de votos
                let voteCountElement = form.find('.vote-count');
                let currentVotes = parseInt(voteCountElement.text()) || 0;
                voteCountElement.text(response.success ? currentVotes + 1 : currentVotes - 1);
            },
            error: function(xhr, status, error) {
                console.error("Erro na requisição AJAX:", status, error);
                alert('Ocorreu um erro ao processar seu voto. Tente novamente.');
            }
        });
    });
});

function createParticles(button) {
    const particles = $('<div>').addClass('particles'); // Cria o contêiner de partículas usando jQuery

    // Criar 8 partículas
    for (let i = 0; i < 8; i++) {
        const particle = $('<div>').addClass('particle'); // Cria cada partícula usando jQuery

        // Calcular posição aleatória para cada partícula
        const angle = (i * Math.PI * 2) / 8;
        const distance = 20 + Math.random() * 20;
        const tx = Math.cos(angle) * distance;
        const ty = Math.sin(angle) * distance;

        particle.css('--tx', `${tx}px`);
        particle.css('--ty', `${ty}px`);

        particles.append(particle); // Anexa cada partícula ao contêiner
    }

    button.append(particles); // Anexa o contêiner de partículas ao botão

    // Remover as partículas após a animação
    setTimeout(() => {
        particles.remove();
    }, 1000);
}

