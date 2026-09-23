document.getElementById('buscar').addEventListener('click', function() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');
    const divResultado = document.getElementById('resultado');

    if (cep.length !== 8) {
        divResultado.innerHTML = "<p>Por favor, digite um CEP válido com 8 dígitos.</p>";
        return;
    }

    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(resposta => {
            if (!resposta.ok) {
                throw new Error("Não foi possível realizar a consulta.");
            }
            return resposta.json();
        })
        .then(dados => {
            if (dados.erro) {
                divResultado.innerHTML = "<p>CEP inválido ou não foi localizado.</p>";
            } else {
                divResultado.innerHTML = `
                    <p><strong>Logradouro:</strong> ${dados.logradouro}</p>
                    <p><strong>Bairro:</strong> ${dados.bairro}</p>
                    <p><strong>Cidade:</strong> ${dados.localidade}</p>
                    <p><strong>UF:</strong> ${dados.uf}</p>
                `;
            }
        })
        .catch(erro => {
            divResultado.innerHTML = `<p>${erro.message}</p>`;
        });
});