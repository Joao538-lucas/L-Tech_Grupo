
from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class LocalizacaoPedido(CrudBase):
    table = "localizacao_pedido"
    fields = [
        "pedido_cliente_id",
        "endereco",
        "numero",
        "bairro",
        "cidade",
        "estado",
        "cep",
        "referencia"
    ]

    def __init__(self, pedido_cliente_id, endereco, numero,
                 bairro, cidade, estado, cep, referencia):
        self.pedido_cliente_id = pedido_cliente_id
        self.endereco = endereco
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.referencia = referencia

    def validate(self):
        erros = [
            Validator.required(self.pedido_cliente_id, "pedido do cliente"),
            Validator.required(self.endereco, "endereço"),
            Validator.required(self.numero, "número"),
            Validator.required(self.bairro, "bairro"),
            Validator.required(self.cidade, "cidade"),
            Validator.required(self.estado, "estado"),
            Validator.required(self.cep, "cep")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def listar_localizacoes(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM localizacao_pedido
                ORDER BY cidade ASC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_por_pedido(cls, pedido_cliente_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM localizacao_pedido
                WHERE pedido_cliente_id = %s
            """
            cursor.execute(sql, (pedido_cliente_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM entrega WHERE localizacao_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        localizacao = cls.find_by_id(id)

        if not localizacao:
            raise ValueError("Localização do pedido não encontrada.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir a localização porque ela possui entregas vinculadas.")

        cls.delete(id)