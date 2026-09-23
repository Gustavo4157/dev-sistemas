const CORES_MAPEADAS = new Map([
  ['caixa1', { nome: 'Amarelo', hex: 'yellow' }],
  ['caixa2', { nome: 'Roxo', hex: 'purple' }],
  ['caixa3', { nome: 'Laranja', hex: 'orange' }]
]);

const alterarCorCaixa = (evento) => {
  const elemento = evento.currentTarget;
  const dadosCor = CORES_MAPEADAS.get(elemento.id);

  if (!dadosCor) return;

  elemento.style.backgroundColor = dadosCor.hex;
  
  setTimeout(() => {
    alert(`A cor foi alterada para: ${dadosCor.nome}`);
  }, 50);
};

document.querySelectorAll('.caixa').forEach(caixa => {
  caixa.addEventListener('dblclick', alterarCorCaixa);
});