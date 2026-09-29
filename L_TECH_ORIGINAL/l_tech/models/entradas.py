from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Entrada(CrudBase):
    table = "entrada"
    fields = [
        "produto_id",
        "fornecedor_id",
        "quantidade",
        "data_entrada",
        "valor_unitario",
        "numero_nota",
        "observacao"
    ]

    def __init__(self, produto_id, fornecedor_id, quantidade,
                 data_entrada, valor_unitario, numero_nota, observacao):
        self.produto_id = produto_id
        self.fornecedor_id = fornecedor_id
        self.quantidade = quantidade
        self.data_entrada = data_entrada
        self.valor_unitario = valor_unitario
        self.numero_nota = numero_nota
        self.observacao = observacao

    def validate(self):
        erros = [
            Validator.required(self.produto_id, "produto"),
            Validator.required(self.fornecedor_id, "fornecedor"),
            Validator.required(self.quantidade, "quantidade"),
            Validator.non_negative(self.quantidade, "quantidade"),
            Validator.required(self.data_entrada, "data de entrada"),
            Validator.non_negative(self.valor_unitario, "valor unitário")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def listar_entradas(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM entrada
                ORDER BY data_entrada DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def total_entradas_produto(cls, produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT SUM(quantidade) FROM entrada WHERE produto_id = %s"
            cursor.execute(sql, (produto_id,))
            resultado = cursor.fetchone()[0]
            return resultado if resultado else 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM pedido_entrada WHERE entrada_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        entrada = cls.find_by_id(id)

        if not entrada:
            raise ValueError("Entrada não encontrada.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir a entrada porque ela possui registros vinculados.")

        cls.delete(id)
