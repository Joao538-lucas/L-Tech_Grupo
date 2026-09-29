from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Cliente(CrudBase):
    table = "cliente"
    fields = [
        "nome",
        "cpf_cnpj",
        "telefone",
        "email",
        "endereco",
        "cidade",
        "estado"
    ]

    def __init__(self, nome, cpf_cnpj, telefone, email,
                 endereco, cidade, estado):
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado

    def validate(self):
        erros = [
            Validator.required(self.nome, "nome"),
            Validator.required(self.cpf_cnpj, "cpf/cnpj"),
            Validator.required(self.telefone, "telefone"),
            Validator.required(self.email, "email")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def search_by_name(cls, nome):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM cliente WHERE nome LIKE %s ORDER BY nome"
            cursor.execute(sql, ('%' + nome + '%',))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            queries = [
                "SELECT COUNT(*) FROM pedido WHERE cliente_id = %s",
                "SELECT COUNT(*) FROM venda WHERE cliente_id = %s"
            ]

            total = 0

            for sql in queries:
                cursor.execute(sql, (id,))
                total += cursor.fetchone()[0]

            return total > 0

        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        cliente = cls.find_by_id(id)

        if not cliente:
            raise ValueError("Cliente não encontrado.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o cliente porque ele possui registros vinculados.")

        cls.delete(id)
