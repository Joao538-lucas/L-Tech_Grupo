from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Entrega(CrudBase):
    table = "entrega"
    fields = [
        "pedido_cliente_id",
        "cliente_id",
        "data_saida",
        "data_entrega",
        "transportadora",
        "status",
        "observacao"
    ]

    def __init__(self, pedido_cliente_id, cliente_id, data_saida,
                 data_entrega, transportadora, status, observacao):
        self.pedido_cliente_id = pedido_cliente_id
        self.cliente_id = cliente_id
        self.data_saida = data_saida
        self.data_entrega = data_entrega
        self.transportadora = transportadora
        self.status = status
        self.observacao = observacao

    def validate(self):
        erros = [
            Validator.required(self.pedido_cliente_id, "pedido do cliente"),
            Validator.required(self.cliente_id, "cliente"),
            Validator.required(self.data_saida, "data de saída"),
            Validator.required(self.transportadora, "transportadora"),
            Validator.required(self.status, "status")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def listar_entregas(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM entrega
                ORDER BY data_saida DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def entregas_pendentes(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM entrega
                WHERE status = 'Em Transporte'
                ORDER BY data_saida ASC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM rastreamento_entrega WHERE entrega_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        entrega = cls.find_by_id(id)

        if not entrega:
            raise ValueError("Entrega não encontrada.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir a entrega porque ela possui registros vinculados.")

        cls.delete(id)