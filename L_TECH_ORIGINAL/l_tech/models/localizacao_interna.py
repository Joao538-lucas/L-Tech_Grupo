from core.crud_base import CrudBase
from core.database import Database
from core.validator import Validator

class LocalizacaoInterna(CrudBase):
    table = "localizacao_pedido_interna"
    fields = [
        "pedido_interno_id",
        "setor",
        "prateleira",
        "corredor",
        "bloco",
        "observacao"
    ]

    def __init__(self, pedido_interno_id, setor, prateleira,
                 corredor, bloco, observacao):
        self.pedido_interno_id = pedido_interno_id
        self.setor = setor
        self.prateleira = prateleira
        self.corredor = corredor
        self.bloco = bloco
        self.observacao = observacao

    def validate(self):
        erros = [
            Validator.required(self.pedido_interno_id, "pedido interno"),
            Validator.required(self.setor, "setor"),
            Validator.required(self.prateleira, "prateleira"),
            Validator.required(self.corredor, "corredor"),
            Validator.required(self.bloco, "bloco")
        ]
        return [erro for erro in erros if erro]

    @classmethod
    def listar_localizacoes(cls):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM localizacao_pedido_interna
                ORDER BY setor ASC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def buscar_por_pedido(cls, pedido_interno_id):
        conexao = Database.connect()
        cursor = conexao.cursor(dictionary=True)

        try:
            sql = """
                SELECT * FROM localizacao_pedido_interna
                WHERE pedido_interno_id = %s
            """
            cursor.execute(sql, (pedido_interno_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def has_related_records(cls, id):
        conexao = Database.connect()
        cursor = conexao.cursor()

        try:
            sql = "SELECT COUNT(*) FROM movimentacao_interna WHERE localizacao_id = %s"
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
            raise ValueError("Localização não encontrada.")

        if cls.has_related_records(id):
            raise ValueError("Não é possível excluir a localização porque ela possui registros vinculados.")

        cls.delete(id)