# ==========================================
# CLASSE 1: LIVRO
# ==========================================
class Livro:
    def __init__(self, titulo, autor, preco, estoque_inicial):
        self.__titulo = titulo
        self.__autor = autor
        # Usamos os setters logo na criação para garantir que 
        # ninguém cadastre um livro com preço ou estoque negativos!
        self.preco = preco 
        self.estoque = estoque_inicial

    # --- GETTERS (Acesso aos dados) ---
    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def preco(self):
        return self.__preco

    @property
    def estoque(self):
        return self.__estoque

    # --- SETTERS (Proteção e Encapsulamento) ---
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco >= 0:
            self.__preco = novo_preco
        else:
            print(f"ERRO: O preço do livro '{self.__titulo}' não pode ser negativo!")
            self.__preco = 0.0

    @estoque.setter
    def estoque(self, novo_estoque):
        if novo_estoque >= 0:
            self.__estoque = novo_estoque
        else:
            print(f"ERRO: O estoque do livro '{self.__titulo}' não pode ser menor que zero!")

    # Método para realizar a baixa no estoque de forma segura
    def vender_unidades(self, quantidade):
        if quantidade <= 0:
            print("Quantidade inválida para venda.")
            return False
        elif self.__estoque >= quantidade:
            self.__estoque -= quantidade  # Reduz o estoque
            return True  # Venda autorizada
        else:
            print(f"ESTOQUE INSUFICIENTE! Temos apenas {self.__estoque} unidades de '{self.__titulo}'.")
            return False


# ==========================================
# CLASSE 2: PEDIDO (CARRINHO DE COMPRAS)
# ==========================================
class Pedido:
    def __init__(self, nome_cliente):
        self.__nome_cliente = nome_cliente
        self.__itens = []  # Vai guardar uma lista de dicionários com o livro e a quantidade comprada

    @property
    def nome_cliente(self):
        return self.__nome_cliente

    def adicionar_livro(self, livro, quantidade):
        # Aqui os objetos conversam! O Pedido pede para o Livro baixar o estoque.
        # Se o livro autorizar (retornar True), adicionamos ao carrinho.
        venda_autorizada = livro.vender_unidades(quantidade)
        
        if venda_autorizada:
            self.__itens.append({
                "livro": livro,
                "quantidade": quantidade,
                "subtotal": livro.preco * quantidade
            })
            print(f"-> {quantidade}x '{livro.titulo}' adicionado(s) ao pedido com sucesso!")

    def exibir_recibo(self):
        print("\n" + "=" * 50)
        print(f"RECIBO DE VENDA - CLIENTE: {self.__nome_cliente.upper()}")
        print("=" * 50)
        
        if not self.__itens:
            print("O carrinho está vazio.")
            print("=" * 50)
            return

        total_geral = 0
        for item in self.__itens:
            livro = item["livro"]
            qtd = item["quantidade"]
            subtotal = item["subtotal"]
            total_geral += subtotal
            
            print(f"{qtd}x {livro.titulo} (R$ {livro.preco:.2f} cada) = R$ {subtotal:.2f}")
            
        print("-" * 50)
        print(f"TOTAL A PAGAR: R$ {total_geral:.2f}")
        print("=" * 50)


# ==========================================
# FLUXO PRINCIPAL DO PROGRAMA (INTERAÇÃO)
# ==========================================

catalogo = []  # Nossa prateleira virtual de livros

print("=== BEM-VINDO AO SISTEMA DA LIVRARIA ===")

# PASSO 1: CADASTRAR O ESTOQUE DA LOJA
print("\n--- PASSO 1: CADASTRAR LIVROS NO ESTOQUE ---")
while True:
    titulo_dig = input("Título do livro: ")
    autor_dig = input("Autor do livro: ")
    preco_dig = float(input("Preço de venda (R$): "))
    estoque_dig = int(input("Quantidade em estoque: "))
    
    # Criamos o objeto Livro e guardamos no catálogo
    novo_livro = Livro(titulo_dig, autor_dig, preco_dig, estoque_dig)
    catalogo.append(novo_livro)
    
    continuar = input("Deseja cadastrar outro livro? (s/n): ").strip().lower()
    if continuar != 's':
        break

# PASSO 2: REALIZAR UMA VENDA
print("\n--- PASSO 2: FRENTE DE CAIXA (NOVA VENDA) ---")
nome_cliente = input("Qual o nome do cliente? ")
meu_pedido = Pedido(nome_cliente)

while True:
    print("\n[ CATÁLOGO DE LIVROS DISPONÍVEIS ]")
    # Mostra os livros disponíveis com um número de identificação (índice)
    for i, livro in enumerate(catalogo):
        print(f"{i} - {livro.titulo} (R$ {livro.preco:.2f}) | Estoque: {livro.estoque} un.")
    
    escolha = int(input("\nDigite o número do livro que o cliente quer comprar (ou -1 para finalizar): "))
    
    if escolha == -1:
        break
    
    if 0 <= escolha < len(catalogo):
        livro_escolhido = catalogo[escolha]
        qtd_comprada = int(input(f"Quantas unidades de '{livro_escolhido.titulo}'? "))
        
        # Tentamos adicionar ao pedido. O encapsulamento vai cuidar de barrar
        # se o cliente pedir mais livros do que temos no estoque.
        meu_pedido.adicionar_livro(livro_escolhido, qtd_comprada)
    else:
        print("Opção de livro inválida!")

# PASSO 3: IMPRIMIR O RECIBO FINAL
meu_pedido.exibir_recibo()

# BÔNUS: Mostrando que o estoque real dos livros foi alterado
print("\n[ ESTOQUE ATUALIZADO DA LOJA APÓS A VENDA ]")
for livro in catalogo:
    print(f"-> {livro.titulo}: Restam {livro.estoque} unidades.")