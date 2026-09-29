from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class Fornecedor(CrudBase):
    table = "fornecedor"
    fields = [
        "nome",
        "cnpj",
        "telefone",
        "email",
        "endereco",
        "cidade",
        "estado"
    ]

    def __init__(self, nome, cnpj, telefone, email, endereco, cidade, estado):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado

    def validate(self):
        erros = [
            Validator.required(self.nome, "nome"),
            Validator.required(self.cnpj, "cnpj"),
            Validator.required(self.telefone, "telefone"),
            Validator.required(self.email, "email")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def search_by_name(cls, nome):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = "SELECT * FROM fornecedor WHERE nome LIKE %s ORDER BY nome"
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
            sql = "SELECT COUNT(*) FROM produto WHERE fornecedor_id = %s"
            cursor.execute(sql, (id,))
            total = cursor.fetchone()[0]
            return total > 0
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def safe_delete(cls, id):
        fornecedor = cls.find_by_id(id)

        if not fornecedor:
            raise ValueError("Fornecedor não encontrado.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir o fornecedor porque ele possui produtos vinculados.")

        cls.delete(id)