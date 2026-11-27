"""Persiste eventos e os vínculos da equipe de fiscalização."""

from collections.abc import Collection, Mapping

from src.infra.db_handler import DbHandler
from src.infra.logging_utils import log
from src.infra.postgres import conninfo


class EventoHandler(DbHandler):
    """Grava eventos e suas equipes no esquema SC_EVENTOS.

    Args:
        None.

    Returns:
        EventoHandler: Handler configurado para abrir a sessão sob demanda.
    """

    def __init__(self) -> None:
        super().__init__(
            "SC_EVENTOS",
            log("appeventos_db", verbose={"error": True}, target_screen=True),
            conninfo=conninfo(),
            reuse_connection=False,
        )

    def gravar_evento(
        self, dados: Mapping[str, object], equipe: Collection[int]
    ) -> None:
        """Insere um evento e vincula os fiscais da equipe.

        A chave estrangeira diferida exige que o responsável, quando informado,
        apareça na equipe com o papel de coordenação antes do commit.

        Args:
            dados (Mapping[str, object]): Colunas e valores validados de TB_EVENTO.
            equipe (Collection[int]): IDs únicos dos fiscais, incluindo o
                responsável quando informado. Pode ser vazia.

        Returns:
            None.

        Raises:
            psycopg.Error: Se o PostgreSQL rejeitar a gravação ou a transação falhar.
            RuntimeError: Se o insert não devolver o identificador do evento.
        """
        with self._unit_of_work():
            evento = self._insert_row("TB_EVENTO", dados, returning=("ID_EVENTO",))
            if evento is None:
                raise RuntimeError("A inserção do evento não retornou seu identificador.")

            if equipe:
                responsavel = dados.get("ID_FISCAL_RESPONSAVEL")
                self._insert_batch(
                    "TB_EVENTO_FISCAL",
                    [
                        {
                            "ID_EVENTO": evento["ID_EVENTO"],
                            "ID_FISCAL": membro,
                            "IC_COORDENACAO": int(membro == responsavel),
                        }
                        for membro in sorted(equipe)
                    ],
                )
