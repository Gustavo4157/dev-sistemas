
const nomePlayer = "Gustavo";
let idade = 17;
let statusAtivo = true; 
const jogoFavorito = { nome: nomePlayer, jogo: "God of War" };
const pontuacoes = [70, 56, 76];
 

console.log("=== DADOS DO PLAYER ===");
console.log(`Nome: ${nomePlayer} | Tipo: ${typeof nomePlayer}`);
console.log(`Idade: ${idade} | Tipo: ${typeof idade}`);
console.log(`Status: ${statusAtivo} | Tipo: ${typeof statusAtivo}`);
console.log(`Jogo Favorito:`, jogoFavorito, `| Tipo: ${typeof jogoFavorito}`);
console.log(`Pontuações:`, pontuacoes, `| Tipo: ${typeof pontuacoes}`);

idade = 18;
statusAtivo = false

console.log("\n=== DADOS ALTERADOS ===");
console.log(`Nova Idade: ${idade} (${typeof idade})`);
console.log(`Novo Status: ${statusAtivo} (${typeof statusAtivo})`);

const soma = pontuacoes.reduce((acc, curr) => acc + curr, 0);
const media = soma / pontuacoes.length;

console.log("\n=== ESTATÍSTICAS ===");
console.log(`Média das pontuações: ${media.toFixed(2)}`);