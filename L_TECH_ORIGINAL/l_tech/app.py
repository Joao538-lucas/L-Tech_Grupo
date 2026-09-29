
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_mail import Mail, Message
import mysql.connector
import random

app = Flask(__name__)
app.secret_key = "chave_secreta"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "joaolucasfroes538@gmail.com"
app.config["MAIL_PASSWORD"] = "SUA_SENHA_DE_APP"

mail = Mail(app)

def conectar_banco():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="l_tech",
        port=3306,
        use_pure=True
    )
    return conn

def criar_notificacao(tipo, mensagem):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notificacao (tipo, mensagem)
        VALUES (%s, %s)
    """, (tipo, mensagem))

    conn.commit()
    cursor.close()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/agenda")
def agenda():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM agenda ORDER BY data_evento ASC")
    eventos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("agenda.html", eventos=eventos)

@app.route("/agenda/salvar", methods=["POST"])
def salvar_agenda():
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")
    data = request.form.get("data")

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agenda (titulo, descricao, data_evento)
        VALUES (%s, %s, %s)
    """, (titulo, descricao, data))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/agenda")

@app.route("/agenda/deletar/<int:id>")
def deletar_agenda(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM agenda WHERE idagenda=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/agenda")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("index.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM cliente WHERE email=%s AND senha=%s LIMIT 1",
        (email, senha)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        session["usuario_id"] = usuario["idcliente"]
        session["usuario_nome"] = usuario["nome"]
        session["usuario_email"] = usuario["email"]

        return redirect("/painel")

    flash("Email ou senha incorretos!")
    return redirect("/")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if request.method == 'POST':

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if len(senha) < 8:
            flash('A senha deve ter no mínimo 8 caracteres!')
            return redirect(url_for('cadastro'))

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO cliente (nome, email, senha) VALUES (%s, %s, %s)",
            (nome, email, senha)
        )

        conexao.commit()
        cursor.close()
        conexao.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route("/empresa", methods=["GET", "POST"])
def empresa():
    if request.method == "POST":
        return redirect("/painel")

    return render_template("empresa.html")

@app.route("/painel")
def painel():
    return render_template("painel.html")

@app.route("/notificacoes")
def notificacoes():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM notificacao
        WHERE lida = FALSE
        ORDER BY data_criacao DESC
    """)

    lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return lista

@app.route("/notificacoes/concluir/<int:id>", methods=["POST"])
def concluir_notificacao(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notificacao
        SET lida = TRUE
        WHERE idnotificacao = %s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return {"sucesso": True}

@app.route("/clientes")
def clientes():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cliente")
    lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("clientes.html", clientes=lista)

@app.route("/clientes/deletar/<int:id>")
def deletar_clientes(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cliente WHERE idcliente=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/clientes")

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_clientes(id):
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        cursor.execute("""
            UPDATE cliente
            SET nome=%s, email=%s, senha=%s
            WHERE idcliente=%s
        """, (nome, email, senha, id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/clientes")

    cursor.execute("SELECT * FROM cliente WHERE idcliente=%s", (id,))
    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("editar_cliente.html", cliente=cliente)

@app.route("/cadastro-produtos")
def cadastro_produtos():
    return render_template("cadastro_produtos.html")

@app.route("/dados-produto")
def dados_produto():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produto ORDER BY idproduto DESC")
    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dados_produto.html", produtos=produtos)

@app.route("/produto/editar/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        estoque = request.form.get("estoque")
        validade = request.form.get("validade")

        try:
            estoque_int = int(estoque or 0)
        except (TypeError, ValueError):
            flash("O estoque deve ser um número inteiro.")
            cursor.close()
            conn.close()
            return redirect(f"/produto/editar/{id}")

        if estoque_int < 0:
            flash("O estoque não pode ser negativo.")
            cursor.close()
            conn.close()
            return redirect(f"/produto/editar/{id}")

        cursor.execute("""
            UPDATE produto
            SET nome=%s,
                preco=%s,
                estoqueatual=%s,
                datasaida=%s
            WHERE idproduto=%s
        """, (nome, preco, estoque_int, validade, id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/dados-produto")

    cursor.execute("SELECT * FROM produto WHERE idproduto=%s", (id,))
    produto = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("editar_produto.html", produto=produto)

@app.route("/produto/deletar/<int:id>")
def deletar_produto(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM produto WHERE idproduto=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/dados-produto")

@app.route("/produto/salvar", methods=["POST"])
def salvar_produto():
    nome = request.form.get("nome_produto")
    preco = request.form.get("preco")
    estoque = request.form.get("unidade")
    validade = request.form.get("validade")

    try:
        estoque_int = int(estoque or 0)
    except (TypeError, ValueError):
        flash("O estoque deve ser um número inteiro.")
        return redirect("/cadastro-produtos")

    if estoque_int < 0:
        flash("O estoque não pode ser negativo.")
        return redirect("/cadastro-produtos")

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO produto
        (nome, preco, estoqueatual, datasaida)
        VALUES (%s, %s, %s, %s)
    """, (nome, preco, estoque_int, validade))

    conn.commit()
    cursor.close()
    conn.close()

    criar_notificacao(
        "produto",
        f"Novo produto cadastrado: {nome}"
    )

    flash("Produto cadastrado com sucesso!")
    return redirect("/dados-produto")

@app.route("/cadastro-fornecedor")
def cadastro_fornecedor():
    return render_template("cadastro_fornecedor.html")

@app.route("/fornecedores")
def fornecedores():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM fornecedor")
    lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("fornecedores.html", fornecedores=lista)

@app.route("/fornecedor/salvar", methods=["POST"])
def salvar_fornecedor():
    nome = request.form.get("nome_fornecedor")
    cnpj = request.form.get("cnpj")
    telefone = request.form.get("telefone")
    email = request.form.get("email")
    endereco = request.form.get("endereco")
    produto = request.form.get("produto_fornecido")

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fornecedor
        (nome, cnpj, telefone, email, endereco, produto_fornecido)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        nome,
        cnpj,
        telefone,
        email,
        endereco,
        produto
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/fornecedores")

@app.route("/fornecedor/editar/<int:id>", methods=["GET", "POST"])
def editar_fornecedor(id):
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form.get("nome_fornecedor")
        cnpj = request.form.get("cnpj")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        endereco = request.form.get("endereco")
        produto = request.form.get("produto_fornecido")

        cursor.execute("""
            UPDATE fornecedor
            SET
                nome=%s,
                cnpj=%s,
                telefone=%s,
                email=%s,
                endereco=%s,
                produto_fornecido=%s
            WHERE idfornecedor=%s
        """, (
            nome,
            cnpj,
            telefone,
            email,
            endereco,
            produto,
            id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/fornecedores")

    cursor.execute("""
        SELECT * FROM fornecedor
        WHERE idfornecedor=%s
    """, (id,))

    fornecedor = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "editar_fornecedor.html",
        fornecedor=fornecedor
    )

@app.route("/fornecedor/deletar/<int:id>")
def deletar_fornecedor(id):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM fornecedor WHERE idfornecedor=%s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/fornecedores")

@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_clientes FROM cliente")
    clientes = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_produtos FROM produto")
    produtos = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM produto
        ORDER BY idproduto DESC
        LIMIT 5
    """)
    ultimos_produtos = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM produto
        WHERE estoqueatual <= 5
    """)
    estoque_baixo = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "relatorios.html",
        clientes=clientes,
        produtos=produtos,
        ultimos_produtos=ultimos_produtos,
        estoque_baixo=estoque_baixo
    )

@app.route("/pedido_saida")
def pedido_saida():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ps.idsaida,
            ps.produto_idproduto AS produto,
            ps.quantidade,
            ps.datasaida AS data_saida
        FROM pedido_saida ps
        ORDER BY ps.idsaida DESC
    """)

    saidas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("pedido_saida.html", saidas=saidas)

@app.route("/pedido_saida/criar", methods=["POST"])
def criar_saida():
    produto_id = request.form.get("produto")

    try:
        quantidade = int(request.form.get("quantidade"))
    except (TypeError, ValueError):
        return "Quantidade inválida"

    if quantidade <= 0:
        return "A quantidade deve ser maior que zero"

    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT nome, estoqueatual
        FROM produto
        WHERE idproduto = %s
    """, (produto_id,))

    produto = cursor.fetchone()

    if not produto:
        cursor.close()
        conn.close()
        return "Produto não encontrado"

    try:
        estoque_atual = int(produto["estoqueatual"])
    except (TypeError, ValueError):
        cursor.close()
        conn.close()
        return "O estoque atual do produto é inválido"

    if quantidade > estoque_atual:
        cursor.close()
        conn.close()
        return f"Estoque insuficiente! Disponível: {estoque_atual}"

    novo_estoque = estoque_atual - quantidade

    cursor.execute("""
        INSERT INTO pedido_saida
        (produto_idproduto, quantidade, datasaida)
        VALUES (%s, %s, NOW())
    """, (produto_id, quantidade))

    cursor.execute("""
        UPDATE produto
        SET estoqueatual = %s
        WHERE idproduto = %s
    """, (novo_estoque, produto_id))

    conn.commit()

    cursor.close()
    conn.close()

    criar_notificacao(
        "pedido",
        f"Nova saída: {quantidade} unidade(s) de {produto['nome']}."
    )

    if novo_estoque <= 5:
        criar_notificacao(
            "estoque",
            f"Estoque baixo: {produto['nome']} possui {novo_estoque} unidade(s)."
        )

    return redirect("/pedido_saida")


@app.route("/pedido_entrada")
def pedido_entrada():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            pe.identrada,
            pe.quantidade,
            pe.data_entrada,
            p.nome AS nome_produto
        FROM pedido_entrada pe
        LEFT JOIN produto p
        ON pe.produto_id = p.idproduto
        ORDER BY pe.identrada DESC
    """)

    entradas = cursor.fetchall()

    cursor.execute("""
        SELECT idproduto, nome
        FROM produto
    """)

    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "pedido_entrada.html",
        entradas=entradas,
        produtos=produtos
    )
@app.route("/pedido_entrada/criar", methods=["POST"])
def criar_entrada():
    produto_id = request.form.get("produto")
    quantidade = request.form.get("quantidade")

    try:
        quantidade_int = int(quantidade)
    except (TypeError, ValueError):
        return "Quantidade inválida"

    if quantidade_int <= 0:
        return "A quantidade deve ser maior que zero"

    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT nome, estoqueatual
        FROM produto
        WHERE idproduto = %s
    """, (produto_id,))

    produto = cursor.fetchone()

    if not produto:
        cursor.close()
        conn.close()
        return "Produto não encontrado"

    try:
        estoque_atual = int(produto["estoqueatual"])
    except (TypeError, ValueError):
        cursor.close()
        conn.close()
        return "O estoque atual do produto é inválido"

    novo_estoque = estoque_atual + quantidade_int

    cursor.execute("""
        INSERT INTO pedido_entrada
        (produto_id, quantidade, data_entrada)
        VALUES (%s, %s, NOW())
    """, (produto_id, quantidade_int))

    cursor.execute("""
        UPDATE produto
        SET estoqueatual = %s
        WHERE idproduto = %s
    """, (novo_estoque, produto_id))

    conn.commit()

    cursor.close()
    conn.close()

    criar_notificacao(
        "pedido",
        f"Entrada registrada: {quantidade_int} unidade(s) de {produto['nome']}."
    )

    if novo_estoque <= 5:
        criar_notificacao(
            "estoque",
            f"Estoque baixo: {produto['nome']} possui apenas {novo_estoque} unidade(s)."
        )

    return redirect("/pedido_entrada")



@app.route("/estoque")
def estoque():
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT idproduto, nome, estoqueatual
        FROM produto
        ORDER BY idproduto DESC
    """)

    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("estoque.html", produtos=produtos)

@app.route("/perfil")
def perfil():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/")

    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT idcliente, nome, email FROM cliente WHERE idcliente = %s",
        (usuario_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario is None:
        return redirect("/")

    return render_template(
        "perfil.html",
        nome=usuario["nome"],
        email=usuario["email"]
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form.get("email")

        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT idcliente FROM cliente WHERE email=%s",
            (email,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if not usuario:
            flash("E-mail não encontrado!")
            return redirect("/esqueci-senha")

        codigo = str(random.randint(100000, 999999))

        session["codigo_recuperacao"] = codigo
        session["recuperar_id"] = usuario["idcliente"]

        mensagem = Message(
            "Código de recuperação - L-Tech",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )

        mensagem.body = f"""
Olá!

Seu código para redefinir a senha da L-Tech é:

{codigo}

Digite esse código na tela de recuperação de senha.
"""

        mail.send(mensagem)

        return redirect("/verificar-codigo")

    return render_template("esqueci_senha.html")

@app.route("/verificar-codigo", methods=["GET", "POST"])
def verificar_codigo():
    if request.method == "POST":
        codigo = request.form.get("codigo")

        if codigo == session.get("codigo_recuperacao"):
            session["codigo_verificado"] = True
            return redirect("/redefinir-senha")

        flash("Código incorreto!")

    return render_template("verificar_codigo.html")

@app.route("/redefinir-senha", methods=["GET", "POST"])
def redefinir_senha():
    if not session.get("codigo_verificado"):
        return redirect("/esqueci-senha")

    usuario_id = session.get("recuperar_id")

    if not usuario_id:
        return redirect("/esqueci-senha")

    if request.method == "POST":
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")

        if not senha or not confirmar_senha:
            flash("Preencha todos os campos!")
            return redirect("/redefinir-senha")

        if senha != confirmar_senha:
            flash("As senhas não são iguais!")
            return redirect("/redefinir-senha")

        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE cliente
            SET senha=%s
            WHERE idcliente=%s
            """,
            (senha, usuario_id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        session.pop("codigo_recuperacao", None)
        session.pop("codigo_verificado", None)
        session.pop("recuperar_id", None)

        flash("Senha redefinida com sucesso!")

        return redirect("/")

    return render_template("redefinir_senha.html")

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)