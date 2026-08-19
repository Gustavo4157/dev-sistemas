document.getElementById('buscar').addEventListener('click', function() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');
    const divResultado = document.getElementById('resultado');

    if (cep.length !== 8) {
        divResultado.innerHTML = "<p>Por favor, digite um CEP válido com 8 dígitos.</p>";
        return;
    }

    const xhr = new XMLHttpRequest();
    const url = `https://viacep.com.br/ws/${cep}/json/`;

    xhr.open('GET', url, true);

    xhr.onload = function() {
        if (xhr.status === 200) {
            const dados = JSON.parse(xhr.responseText);

            if (dados.erro) {
                divResultado.innerHTML = "<p>CEP não encontrado!</p>";
            } else {
                divResultado.innerHTML = `
                    <p><strong>Logradouro:</strong> ${dados.logradouro}</p>
                    <p><strong>Bairro:</strong> ${dados.bairro}</p>
                    <p><strong>Cidade:</strong> ${dados.localidade}</p>
                    <p><strong>UF:</strong> ${dados.uf}</p>
                `;
            }
        } else {
            divResultado.innerHTML = "<p>Erro ao consultar o servidor.</p>";
        }
    };

    xhr.onerror = function() {
        divResultado.innerHTML = "<p>Erro de conexão com a API do ViaCEP.</p>";
    };

    xhr.send();
});