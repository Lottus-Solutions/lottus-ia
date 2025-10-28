import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class Banco:
    def __init__(self):
        self.config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

    def executar_query(self, query: str):
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            dados = cursor.fetchall()
            cursor.close()
            conn.close()
            return dados
        except mysql.connector.Error as err:
            print(f"Erro ao executar a query: {err}")
            return []

    def executar_intencao(self, intencao: str):
        queries = {
            "consultar_emprestimos_ativos": """
               SELECT 
                    ag.id, 
                    l.nome AS livro, 
                    al.nome AS aluno, 
                    ag.data_emprestimo, 
                    ag.data_devolucao_prevista
                FROM agendamento ag
                JOIN livro l ON l.id = ag.livro_id
                JOIN aluno al ON al.matricula = ag.aluno_id
                WHERE ag.status_emprestimo = 'ATIVO'
                ORDER BY ag.data_emprestimo DESC
                LIMIT 5
            """,
            "consultar_emprestimos_atrasados": """
                SELECT
                    ag.id,
                    l.nome AS livro,
                    al.nome AS aluno,
                    ag.dias_atrasados,
                    ag.data_devolucao_prevista
                FROM agendamento ag
                JOIN livro l ON l.id = ag.livro_id
                JOIN aluno al ON al.matricula = ag.aluno_id
                WHERE ag.status_emprestimo = 'ATRASADO'
                ORDER BY ag.dias_atrasados DESC
                LIMIT 5
            """,
            "consultar_emprestimos_devolucao_hoje": """
                SELECT 
                    ag.id, 
                    l.nome AS livro, 
                    al.nome AS aluno, 
                    ag.data_devolucao_prevista
                FROM agendamento ag
                JOIN livro l ON l.id = ag.livro_id
                JOIN aluno al ON al.matricula = ag.aluno_id
                WHERE ag.status_emprestimo = 'ATIVO' 
                AND DATE(ag.data_devolucao_prevista) = CURRENT_DATE
                ORDER BY ag.data_emprestimo DESC
                LIMIT 5
            """,
            "consultar_emprestimos_devolucao_amanha": """
               SELECT 
                    ag.id, 
                    l.nome AS livro, 
                    al.nome AS aluno, 
                    ag.data_devolucao_prevista
                FROM agendamento ag
                JOIN livro l ON l.id = ag.livro_id
                JOIN aluno al ON al.matricula = ag.aluno_id
                WHERE ag.status_emprestimo = 'ATIVO'
                AND DATE(ag.data_devolucao_prevista) = DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY)
                ORDER BY ag.data_emprestimo DESC
                LIMIT 5
            """,
            "livros_reservados": """
               SELECT 
                    ag.id, 
                    l.nome AS livro, 
                    al.nome AS aluno, 
                    ag.data_devolucao_prevista
                FROM agendamento ag
                JOIN livro l ON l.id = ag.livro_id
                JOIN aluno al ON al.matricula = ag.aluno_id
                WHERE ag.status_emprestimo = 'ATIVO'
                AND DATE(ag.data_devolucao_prevista) = DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY)
                ORDER BY ag.data_emprestimo DESC
                LIMIT 5
            """,
            "livros_mais_lidos_por_turma": """
                SELECT 
                    l.nome AS livro,
                    c.nome AS categoria,
                    l.quantidade,
                    l.quantidade_disponivel
                FROM livro l
                JOIN categoria c ON c.id = l.fk_categoria
                WHERE l.status = 'RESERVADO'
                ORDER BY l.nome
                LIMIT 5
            """,
            "livros_maior_demanda_semestre": """
                SELECT 
                    l.nome AS livro,
                    c.nome AS categoria,
                    COUNT(*) AS total_emprestimos
                FROM agendamento ag
                JOIN livro l ON l.id = ag.livro_id
                JOIN categoria c ON c.id = l.fk_categoria
                WHERE ag.data_emprestimo >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
                AND ag.status_emprestimo IN ('FINALIZADO', 'ATIVO', 'ATRASADO')
                GROUP BY l.nome, c.nome
                ORDER BY total_emprestimos DESC
                LIMIT 5
            """,
            "livros_totais": """
                SELECT 
                    COUNT(*) AS total_titulos,
                    SUM(quantidade) AS total_exemplares
                FROM livro
            """,
            "alunos_sem_retirada_obrigatoria": """
                SELECT 
                    t.serie AS turma,
                    COUNT(al.matricula) AS alunos_sem_livros_retirados
                FROM aluno al
                JOIN turma t ON t.id = al.fk_turma
                LEFT JOIN agendamento a 
                    ON a.aluno_id = al.matricula 
                    AND a.status_emprestimo = 'ATIVO'
                WHERE a.id IS NULL
                GROUP BY t.serie
                ORDER BY t.serie
            """,
            "alunos_atrasos_frequentes": """
                SELECT 
                    al.nome AS aluno,
                    t.serie AS turma,
                    COUNT(*) AS total_atrasos,
                    MAX(a.dias_atrasados) AS maior_atraso,
                    SUM(a.dias_atrasados) AS total_dias_atrasados
                FROM agendamento a
                JOIN aluno al ON al.matricula = a.aluno_id
                JOIN turma t ON t.id = al.fk_turma
                WHERE a.status_emprestimo = 'ATRASADO'
                GROUP BY al.matricula, al.nome, t.serie
                HAVING COUNT(*) >= 2
                ORDER BY total_atrasos DESC, total_dias_atrasados DESC
                LIMIT 5
            """,
            "bonus_por_turma": """
                SELECT 
                    t.serie AS turma,
                    COUNT(al.matricula) AS total_alunos,
                    SUM(al.qtd_bonus) AS total_bonus,
                    AVG(al.qtd_bonus) AS media_bonus
                FROM aluno al
                JOIN turma t ON t.id = al.fk_turma
                GROUP BY t.serie
                ORDER BY total_bonus DESC
            """,
            "alunos_em_atraso": """
                SELECT 
                    al.nome AS aluno,
                    t.serie AS turma,
                    l.nome AS livro,
                    a.data_devolucao_prevista,
                    a.dias_atrasados
                FROM agendamento a
                JOIN aluno al ON al.matricula = a.aluno_id
                JOIN turma t ON t.id = al.fk_turma
                JOIN livro l ON l.id = a.livro_id
                WHERE a.status_emprestimo = 'ATRASADO'
                ORDER BY a.dias_atrasados DESC
                LIMIT 5
            """,
            "categorias_mais_emprestadas": """
                SELECT 
                    c.nome AS categoria, 
                    COUNT(*) AS total_emprestimos
                FROM agendamento a
                JOIN livro l ON l.id = a.livro_id
                JOIN categoria c ON c.id = l.fk_categoria
                WHERE a.status_emprestimo IN ('FINALIZADO', 'ATIVO', 'ATRASADO')
                GROUP BY c.nome
                ORDER BY total_emprestimos DESC
                LIMIT 10
            """,
            "categorias_menos_procuradas": """
                SELECT 
                    c.nome AS categoria, 
                    COUNT(*) AS total_emprestimos
                FROM agendamento a
                JOIN livro l ON l.id = a.livro_id
                JOIN categoria c ON c.id = l.fk_categoria
                WHERE a.status_emprestimo IN ('FINALIZADO', 'ATIVO', 'ATRASADO')
                GROUP BY c.nome
                ORDER BY total_emprestimos ASC
                LIMIT 10
            """,
            "livros_por_categoria": """
                SELECT 
                    c.nome AS categoria, 
                    COUNT(*) AS total_livros
                FROM livro l
                JOIN categoria c ON c.id = l.fk_categoria
                GROUP BY c.nome
                ORDER BY total_livros DESC
            """,
            "categorias_aumento_emprestimos": """
                SELECT 
                    c.nome AS categoria,
                    COUNT(CASE 
                        WHEN a.data_emprestimo BETWEEN DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH) AND DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
                        THEN 1 END) AS emprestimos_ultimo_ano,
                    COUNT(CASE 
                        WHEN a.data_emprestimo > DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
                        THEN 1 END) AS emprestimos_ultimo_semestre
                FROM agendamento a
                JOIN livro l ON l.id = a.livro_id
                JOIN categoria c ON c.id = l.fk_categoria
                GROUP BY c.nome
                HAVING emprestimos_ultimo_semestre > emprestimos_ultimo_ano
                ORDER BY (emprestimos_ultimo_semestre - emprestimos_ultimo_ano) DESC
                LIMIT 10
            """,
        }

        query = queries.get(intencao)
        if not query:
            return []

        return self.executar_query(query)
