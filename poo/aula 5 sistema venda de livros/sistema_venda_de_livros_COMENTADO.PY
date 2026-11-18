# ==========================================
# CLASSE 1: LIVRO
# ==========================================
# EXPLICAÇÃO: Criação do "molde" para os livros da nossa loja.
# INTENÇÃO: Agrupar as informações (título, preço, estoque) e as ações (vender) de um livro em um só lugar protegido.
class Livro:
    
    # EXPLICAÇÃO: Método construtor. Chamado automaticamente quando um livro "nasce".
    def __init__(self, titulo, autor, preco, estoque_inicial):
        # EXPLICAÇÃO: Os dois sublinhados (__) tornam os atributos PRIVADOS. 
        # INTENÇÃO: Proteger os dados. Ninguém de fora pode mexer no título e autor diretamente.
        self.__titulo = titulo
        self.__autor = autor
        
        # EXPLICAÇÃO: Repare que aqui NÃO tem os dois sublinhados (__). Estamos chamando os "Setters" que criamos lá embaixo!
        # INTENÇÃO: Garantir que, já na hora de criar o livro, os valores de preço e estoque passem pelas regras de segurança (não podem ser negativos).
        self.preco = preco 
        self.estoque = estoque_inicial

    # --- GETTERS (Acesso aos dados seguros) ---
    
    # EXPLICAÇÃO: O decorador @property transforma esse método numa "janela de leitura".
    # INTENÇÃO: Permitir que o resto do programa VEJA qual é o título, sem poder alterá-lo.
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
    
    # EXPLICAÇÃO: O @preco.setter é o "guarda de segurança" para a variável __preco. 
    # INTENÇÃO: Impedir que alguém cadastre um livro valendo um valor negativo (ex: -50 reais).
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco >= 0:
            self.__preco = novo_preco
        else:
            print(f"ERRO: O preço do livro '{self.__titulo}' não pode ser negativo!")
            self.__preco = 0.0 # Valor padrão de segurança

    # EXPLICAÇÃO: O setter do estoque verifica se o número recebido é válido.
    # INTENÇÃO: Garantir a integridade da loja (não existe estoque negativo no mundo real).
    @estoque.setter
    def estoque(self, novo_estoque):
        if novo_estoque >= 0:
            self.__estoque = novo_estoque
        else:
            print(f"ERRO: O estoque do livro '{self.__titulo}' não pode ser menor que zero!")

    # EXPLICAÇÃO: Método que recebe uma quantidade e tenta diminuir do estoque. Retorna True (deu certo) ou False (deu erro).
    # INTENÇÃO: O próprio livro é quem decide se pode ser vendido ou não. O controle está dentro dele, e não solto no programa principal.
    def vender_unidades(self, quantidade):
        if quantidade <= 0:
            print("Quantidade inválida para venda.")
            return False
        elif self.__estoque >= quantidade:
            self.__estoque -= quantidade  # Reduz o estoque de forma segura
            return True  # Venda autorizada e concluída
        else:
            print(f"ESTOQUE INSUFICIENTE! Temos apenas {self.__estoque} unidades de '{self.__titulo}'.")
            return False


# ==========================================
# CLASSE 2: PEDIDO (CARRINHO DE COMPRAS)
# ==========================================
# EXPLICAÇÃO: Criação do molde para o carrinho de compras do cliente.
# INTENÇÃO: Separar a responsabilidade. O "Livro" cuida de si mesmo, o "Pedido" cuida de agrupar os livros comprados.
class Pedido:
    
    def __init__(self, nome_cliente):
        self.__nome_cliente = nome_cliente
        # EXPLICAÇÃO: Cria uma lista vazia e privada para guardar os livros.
        self.__itens = [] 

    @property
    def nome_cliente(self):
        return self.__nome_cliente

    # EXPLICAÇÃO: Recebe um OBJETO livro e a quantidade desejada.
    # INTENÇÃO: Fazer a comunicação entre objetos. O objeto Pedido interage com o objeto Livro.
    def adicionar_livro(self, livro, quantidade):
        
        # EXPLICAÇÃO: O Pedido "pede permissão" ao Livro para fazer a venda, chamando o método vender_unidades.
        # INTENÇÃO: Encapsulamento prático! O carrinho não mexe no estoque do livro. O próprio livro faz isso e avisa se deu certo (True ou False).
        venda_autorizada = livro.vender_unidades(quantidade)
        
        # EXPLICAÇÃO: Se o livro autorizou (tinha estoque suficiente)...
        if venda_autorizada:
            # Adiciona um dicionário na lista de itens do carrinho.
            self.__itens.append({
                "livro": livro,
                "quantidade": quantidade,
                "subtotal": livro.preco * quantidade
            })
            print(f"-> {quantidade}x '{livro.titulo}' adicionado(s) ao pedido com sucesso!")

    # EXPLICAÇÃO: Método para varrer a lista de compras e imprimir um relatório.
    # INTENÇÃO: Deixar a lógica visual e os cálculos finais (total) a cargo do próprio objeto Pedido.
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

# EXPLICAÇÃO: Lista vazia criada de forma procedural para simular nossa prateleira.
catalogo = [] 

print("=== BEM-VINDO AO SISTEMA DA LIVRARIA ===")

# --- PASSO 1: CADASTRAR O ESTOQUE DA LOJA ---
print("\n--- PASSO 1: CADASTRAR LIVROS NO ESTOQUE ---")
while True:
    # EXPLICAÇÃO: Coleta de dados usando input padrão.
    titulo_dig = input("Título do livro: ")
    autor_dig = input("Autor do livro: ")
    preco_dig = float(input("Preço de venda (R$): "))
    estoque_dig = int(input("Quantidade em estoque: "))
    
    # EXPLICAÇÃO: O comando 'Livro(...)' executa o def __init__ da Classe Livro.
    # INTENÇÃO: Instanciar (criar) um objeto real na memória contendo as variáveis digitadas.
    novo_livro = Livro(titulo_dig, autor_dig, preco_dig, estoque_dig)
    
    # EXPLICAÇÃO: Guarda o objeto inteiro na lista.
    catalogo.append(novo_livro)
    
    continuar = input("Deseja cadastrar outro livro? (s/n): ").strip().lower()
    if continuar != 's':
        break # Sai do laço while

# --- PASSO 2: REALIZAR UMA VENDA ---
print("\n--- PASSO 2: FRENTE DE CAIXA (NOVA VENDA) ---")
nome_cliente = input("Qual o nome do cliente? ")

# EXPLICAÇÃO: Instanciamos a classe Pedido, criando um carrinho vazio para o cliente.
meu_pedido = Pedido(nome_cliente)

while True:
    print("\n[ CATÁLOGO DE LIVROS DISPONÍVEIS ]")
    
    # EXPLICAÇÃO: O enumerate gera um número 'i' para cada 'livro' dentro da lista 'catalogo'.
    # INTENÇÃO: Criar um menu fácil para o usuário escolher o livro digitando apenas um número.
    for i, livro in enumerate(catalogo):
        print(f"{i} - {livro.titulo} (R$ {livro.preco:.2f}) | Estoque: {livro.estoque} un.")
    
    escolha = int(input("\nDigite o número do livro que o cliente quer comprar (ou -1 para finalizar): "))
    
    if escolha == -1:
        break # Encerra a venda
    
    # EXPLICAÇÃO: Verifica se o número digitado existe na nossa lista de livros (no catálogo).
    if 0 <= escolha < len(catalogo):
        # Capturamos o objeto Livro que o usuário escolheu
        livro_escolhido = catalogo[escolha]
        qtd_comprada = int(input(f"Quantas unidades de '{livro_escolhido.titulo}'? "))
        
        # EXPLICAÇÃO: Mandamos o objeto Pedido agir. Ele vai tentar adicionar o Livro escolhido.
        # INTENÇÃO: Aqui brilha a POO! O fluxo principal não mexe em estoque, não calcula nada. Ele apenas junta as peças e manda os objetos trabalharem.
        meu_pedido.adicionar_livro(livro_escolhido, qtd_comprada)
    else:
        print("Opção de livro inválida!")

# --- PASSO 3: IMPRIMIR O RECIBO FINAL ---

# EXPLICAÇÃO: Chamamos o método exibir_recibo do próprio objeto Pedido.
meu_pedido.exibir_recibo()

# --- BÔNUS: VERIFICAÇÃO DO ENCAPSULAMENTO ---

print("\n[ ESTOQUE ATUALIZADO DA LOJA APÓS A VENDA ]")
# EXPLICAÇÃO: Percorremos novamente o catálogo original para ver como ficou.
# INTENÇÃO: Provar para o aluno que, graças à comunicação entre as Classes, o estoque dos livros foi descontado corretamente, mesmo a operação tendo acontecido dentro da Classe Pedido.
for livro in catalogo:
    print(f"-> {livro.titulo}: Restam {livro.estoque} unidades.")