from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Saida(CrudBase):
    table = "saida"
    fields = [
        "produto_id",
        "quantidade",
        "data_saida",
        "destino",
        "responsavel",
        "observacao"
    ]

    def __init__(self, produto_id, quantidade, data_saida,
                 destino, responsavel, observacao):
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.data_saida = data_saida
        self.destino = destino
        self.responsavel = responsavel
        self.observacao = observacao

    def validate(self):
        erros = [
            Validator.required(self.produto_id, "produto"),
            Validator.required(self.quantidade, "quantidade"),
            Validator.non_negative(self.quantidade, "quantidade"),
            Validator.required(self.data_saida, "data de saída"),
            Validator.required(self.destino, "destino"),
            Validator.required(self.responsavel, "responsável")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def listar_saidas(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM saida
                ORDER BY data_saida DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def total_saidas_produto(cls, produto_id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT SUM(quantidade) FROM saida WHERE produto_id = %s"
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
            sql = "SELECT COUNT(*) FROM pedido_saida WHERE saida_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        saida = cls.find_by_id(id)

        if not saida:
            raise ValueError("Saída não encontrada.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir a saída porque ela possui registros vinculados.")

        cls.delete(id)