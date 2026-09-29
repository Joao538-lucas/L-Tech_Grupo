from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class PedidoCliente(CrudBase):
    table = "pedido_cliente"
    fields = [
        "cliente_id",
        "data_pedido",
        "data_entrega",
        "status",
        "valor_total",
        "observacao"
    ]

    def __init__(self, cliente_id, data_pedido, data_entrega,
                 status, valor_total, observacao):
        self.cliente_id = cliente_id
        self.data_pedido = data_pedido
        self.data_entrega = data_entrega
        self.status = status
        self.valor_total = valor_total
        self.observacao = observacao

    def validate(self):
        erros = [
            Validator.required(self.cliente_id, "cliente"),
            Validator.required(self.data_pedido, "data do pedido"),
            Validator.required(self.status, "status"),
            Validator.non_negative(self.valor_total, "valor total")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def listar_pedidos(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM pedido_cliente
                ORDER BY data_pedido DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def pedidos_pendentes(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM pedido_cliente
                WHERE status = 'Pendente'
                ORDER BY data_pedido ASC
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
            sql = "SELECT COUNT(*) FROM item_pedido_cliente WHERE pedido_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        pedido = cls.find_by_id(id)

        if not pedido:
            raise ValueError("Pedido do cliente não encontrado.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o pedido porque ele possui itens vinculados.")

        cls.delete(id)