const btnBuscar = document.getElementById('buscar');
const campoUsuario = document.getElementById('usuario');
const divPerfil = document.getElementById('perfil');

const buscarPerfilGithub = async () => {
  const username = campoUsuario.value.trim();

  if (!username) {
    divPerfil.innerHTML = '<p>Digite um nome de usuário!</p>';
    return;
  }

  try {
    const resposta = await fetch(`https://api.github.com/users/${username}`);
    
    if (!resposta.ok) throw new Error('Usuário não encontrado!');

    const { avatar_url, name, bio } = await resposta.json();

    divPerfil.innerHTML = `
      <img src="${avatar_url}" alt="Foto de ${username}" width="150">
      <h3>${name ?? 'Sem nome cadastrado'}</h3>
      <p>${bio ?? 'Sem biografia cadastrada'}</p>
    `;
  } catch (erro) {
    divPerfil.innerHTML = `<p>${erro.message}</p>`;
  }
};

btnBuscar.addEventListener('click', buscarPerfilGithub);