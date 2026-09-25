let precoPizza = 45;
let quantidade = 2;

let valorTotal = precoPizza * quantidade;

console.log(`Valor do pedido: R$ ${valorTotal}`);
console.log(`Se rachar com um amigo (metade): R$ ${valorTotal / 2}`);
console.log(`Se pedir o dobro de pizzas: R$ ${valorTotal * 2}`);

let temDesconto = true;
let temBordaGratis = false;

if (temDesconto && temBordaGratis) {
    console.log("Combo completo: Você ganhou desconto E borda recheada grátis!");
} else if (temDesconto) {
    console.log("Benefício aplicado: Desconto de 10%!");
} else if (temBordaGratis) {
    console.log("Benefício aplicado: Borda recheada grátis!");
} else {
    console.log("Nenhum benefício aplicado nesta compra.");
}