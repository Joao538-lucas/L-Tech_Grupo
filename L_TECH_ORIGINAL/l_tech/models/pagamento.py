from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Pagamento(CrudBase):
    table = "pagamento"
    fields = [
        "pedido_cliente_id",
        "cliente_id",
        "data_pagamento",
        "forma_pagamento",
        "valor_pago",
        "status",
        "observacao"
    ]

    def __init__(self, pedido_cliente_id, cliente_id, data_pagamento,
                 forma_pagamento, valor_pago, status, observacao):
        self.pedido_cliente_id = pedido_cliente_id
        self.cliente_id = cliente_id
        self.data_pagamento = data_pagamento
        self.forma_pagamento = forma_pagamento
        self.valor_pago = valor_pago
        self.status = status
        self.observacao = observacao

    def validate(self):
        erros = [
            Validator.required(self.pedido_cliente_id, "pedido do cliente"),
            Validator.required(self.cliente_id, "cliente"),
            Validator.required(self.data_pagamento, "data de pagamento"),
            Validator.required(self.forma_pagamento, "forma de pagamento"),
            Validator.required(self.status, "status"),
            Validator.non_negative(self.valor_pago, "valor pago")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def listar_pagamentos(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM pagamento
                ORDER BY data_pagamento DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def pagamentos_pendentes(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM pagamento
                WHERE status = 'Pendente'
                ORDER BY data_pagamento ASC
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
            sql = "SELECT COUNT(*) FROM comprovante_pagamento WHERE pagamento_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        pagamento = cls.find_by_id(id)

        if not pagamento:
            raise ValueError("Pagamento não encontrado.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o pagamento porque ele possui comprovantes vinculados.")

        cls.delete(id)