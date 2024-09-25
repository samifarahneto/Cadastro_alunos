import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QMainWindow, QHeaderView, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import mysql.connector

# Função para conectar ao banco de dados
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Seu host MySQL
            user="root",  # Seu usuário MySQL
            password="Neto010185!",  # Sua senha MySQL
            database="alunos_cadastro_db"  # Nome do banco de dados MySQL
        )
        return conn
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Erro de Conexão", f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para criar a tabela (caso não exista)
def create_table():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            cpf VARCHAR(14),
            nota1 FLOAT,
            nota2 FLOAT,
            nota3 FLOAT
        )
        """)
        conn.close()

# Classe principal da interface
class AlunoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cadastro de Alunos")
        self.setGeometry(100, 100, 800, 500)

        # Variável para armazenar o ID do aluno selecionado
        self.aluno_id = None

        # Criar o widget de abas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Aba de Cadastro
        self.cadastro_tab = QWidget()
        self.tabs.addTab(self.cadastro_tab, "Cadastro")

        # Layout da aba de cadastro
        self.layout_cadastro = QVBoxLayout()

        # Labels e entradas com estilos personalizados
        self.label_nome = QLabel("Nome:")
        self.label_nome.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nome = QLineEdit(self)
        self.input_nome.setFixedHeight(30)
        self.input_nome.setStyleSheet("border-radius: 10px; padding: 5px;")

        self.label_cpf = QLabel("CPF:")
        self.label_cpf.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_cpf = QLineEdit(self)
        self.input_cpf.setPlaceholderText("000.000.000-00")
        self.input_cpf.setFixedHeight(30)
        self.input_cpf.setStyleSheet("border-radius: 10px; padding: 5px;")
        self.input_cpf.textChanged.connect(self.formatar_cpf)

        self.label_nota1 = QLabel("Nota 1:")
        self.label_nota1.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nota1 = QLineEdit(self)
        self.input_nota1.setFixedHeight(30)
        self.input_nota1.setStyleSheet("border-radius: 10px; padding: 5px;")

        self.label_nota2 = QLabel("Nota 2:")
        self.label_nota2.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nota2 = QLineEdit(self)
        self.input_nota2.setFixedHeight(30)
        self.input_nota2.setStyleSheet("border-radius: 10px; padding: 5px;")

        self.label_nota3 = QLabel("Nota 3:")
        self.label_nota3.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nota3 = QLineEdit(self)
        self.input_nota3.setFixedHeight(30)
        self.input_nota3.setStyleSheet("border-radius: 10px; padding: 5px;")

        # Botão de Salvar
        self.button_salvar = QPushButton("Salvar", self)
        self.button_salvar.clicked.connect(self.salvar_aluno)

        # Adicionar widgets ao layout
        self.layout_cadastro.addWidget(self.label_nome)
        self.layout_cadastro.addWidget(self.input_nome)
        self.layout_cadastro.addWidget(self.label_cpf)
        self.layout_cadastro.addWidget(self.input_cpf)
        self.layout_cadastro.addWidget(self.label_nota1)
        self.layout_cadastro.addWidget(self.input_nota1)
        self.layout_cadastro.addWidget(self.label_nota2)
        self.layout_cadastro.addWidget(self.input_nota2)
        self.layout_cadastro.addWidget(self.label_nota3)
        self.layout_cadastro.addWidget(self.input_nota3)
        self.layout_cadastro.addWidget(self.button_salvar)
        self.cadastro_tab.setLayout(self.layout_cadastro)

        # Aba de Consulta
        self.consulta_tab = QWidget()
        self.tabs.addTab(self.consulta_tab, "Consulta")

        self.layout_consulta = QVBoxLayout()

        # Campos de Busca
        self.label_busca_nome = QLabel("Buscar por Nome:")
        self.label_busca_nome.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_busca_nome = QLineEdit(self)
        self.input_busca_nome.setFixedHeight(30)
        self.input_busca_nome.setStyleSheet("border-radius: 10px; padding: 5px;")
        self.input_busca_nome.textChanged.connect(self.filtrar_alunos)

        self.label_busca_cpf = QLabel("Buscar por CPF:")
        self.label_busca_cpf.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_busca_cpf = QLineEdit(self)
        self.input_busca_cpf.setFixedHeight(30)
        self.input_busca_cpf.setStyleSheet("border-radius: 10px; padding: 5px;")
        self.input_busca_cpf.textChanged.connect(self.filtrar_alunos)

        self.table_alunos = QTableWidget()
        self.table_alunos.setColumnCount(8)  # Adicionar coluna para o ID
        self.table_alunos.setHorizontalHeaderLabels(["Selecionar", "ID", "Nome", "CPF", "Nota 1", "Nota 2", "Nota 3", "Média"])
        self.table_alunos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_alunos.cellDoubleClicked.connect(self.mostrar_detalhes_aluno)

        # Tornar a coluna de ID oculta
        self.table_alunos.setColumnHidden(1, True)

        # Botões de Editar e Apagar
        self.button_editar = QPushButton("Editar", self)
        self.button_editar.clicked.connect(self.editar_aluno)

        self.button_apagar = QPushButton("Apagar", self)
        self.button_apagar.clicked.connect(self.apagar_aluno)

        # Adicionar widgets ao layout de consulta
        self.layout_consulta.addWidget(self.label_busca_nome)
        self.layout_consulta.addWidget(self.input_busca_nome)
        self.layout_consulta.addWidget(self.label_busca_cpf)
        self.layout_consulta.addWidget(self.input_busca_cpf)
        self.layout_consulta.addWidget(self.table_alunos)
        self.layout_consulta.addWidget(self.button_editar)
        self.layout_consulta.addWidget(self.button_apagar)
        self.consulta_tab.setLayout(self.layout_consulta)

        # Carregar dados ao iniciar
        self.carregar_alunos()

    # Função para salvar aluno no banco de dados
    def salvar_aluno(self):
        nome = self.input_nome.text()
        cpf = self.input_cpf.text()
        try:
            nota1 = float(self.input_nota1.text())
            nota2 = float(self.input_nota2.text())
            nota3 = float(self.input_nota3.text())
        except ValueError:
            QMessageBox.warning(self, "Entrada inválida", "Por favor, insira valores numéricos para as notas.")
            return

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            try:
                if self.aluno_id:  # Atualizar aluno existente
                    cursor.execute(
                        "UPDATE alunos SET nome = %s, cpf = %s, nota1 = %s, nota2 = %s, nota3 = %s WHERE id = %s",
                        (nome, cpf, nota1, nota2, nota3, self.aluno_id))
                    QMessageBox.information(self, "Sucesso", "Aluno atualizado com sucesso!")
                else:  # Inserir novo aluno
                    cursor.execute(
                        "INSERT INTO alunos (nome, cpf, nota1, nota2, nota3) VALUES (%s, %s, %s, %s, %s)",
                        (nome, cpf, nota1, nota2, nota3))
                    QMessageBox.information(self, "Sucesso", "Aluno salvo com sucesso!")
                
                conn.commit()
                self.limpar_campos()
                self.carregar_alunos()
                self.aluno_id = None  # Resetar ID do aluno após salvar
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar aluno: {err}")
            finally:
                conn.close()

    # Função para formatar o CPF
    def formatar_cpf(self):
        texto = self.input_cpf.text().replace(".", "").replace("-", "")
        if len(texto) > 3:
            texto = texto[:3] + "." + texto[3:]
        if len(texto) > 7:
            texto = texto[:7] + "." + texto[7:]
        if len(texto) > 11:
            texto = texto[:11] + "-" + texto[11:]
        self.input_cpf.setText(texto)

    # Função para carregar alunos na tabela
    def carregar_alunos(self):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cpf, nota1, nota2, nota3 FROM alunos")
            resultados = cursor.fetchall()
            self.table_alunos.setRowCount(len(resultados))
            for row_num, row_data in enumerate(resultados):
                checkbox_item = QCheckBox()
                checkbox_item.stateChanged.connect(self.uncheck_other_checkboxes)  # Conectar sinal para desmarcar outros checkboxes
                self.table_alunos.setCellWidget(row_num, 0, checkbox_item)
                
                # Definir o ID oculto e os dados na tabela
                self.table_alunos.setItem(row_num, 1, QTableWidgetItem(str(row_data[0])))  # Armazenar ID
                for col_num, data in enumerate(row_data[1:]):  # Ignorar o ID
                    self.table_alunos.setItem(row_num, col_num + 2, QTableWidgetItem(str(data)))
                
                # Calcular e exibir a média
                media = (row_data[3] + row_data[4] + row_data[5]) / 3
                self.table_alunos.setItem(row_num, 7, QTableWidgetItem(f"{media:.2f}"))

            conn.close()

    # Função para desmarcar outros checkboxes
    def uncheck_other_checkboxes(self):
        sender = self.sender()
        for row in range(self.table_alunos.rowCount()):
            checkbox = self.table_alunos.cellWidget(row, 0)
            if checkbox is not sender:
                checkbox.setChecked(False)

    # Função para filtrar alunos na tabela
    def filtrar_alunos(self):
        nome_busca = self.input_busca_nome.text().lower()
        cpf_busca = self.input_busca_cpf.text()
        for row in range(self.table_alunos.rowCount()):
            nome_item = self.table_alunos.item(row, 2).text().lower()  # Ajuste para a nova posição da coluna Nome
            cpf_item = self.table_alunos.item(row, 3).text()  # Ajuste para a nova posição da coluna CPF
            self.table_alunos.setRowHidden(row, not (nome_busca in nome_item and cpf_busca in cpf_item))

    # Função para mostrar detalhes do aluno
    def mostrar_detalhes_aluno(self, row, column):
        nome = self.table_alunos.item(row, 2).text()
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM alunos WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()
            if resultado:
                media = (resultado['nota1'] + resultado['nota2'] + resultado['nota3']) / 3
                QMessageBox.information(self, "Dados do Aluno",
                                        f"Nome: {resultado['nome']}\nCPF: {resultado['cpf']}\n"
                                        f"Nota 1: {resultado['nota1']}\nNota 2: {resultado['nota2']}\nNota 3: {resultado['nota3']}\n"
                                        f"Média: {media:.2f}")
            conn.close()

    # Função para editar aluno
    def editar_aluno(self):
        for row in range(self.table_alunos.rowCount()):
            checkbox = self.table_alunos.cellWidget(row, 0)
            if checkbox.isChecked():
                aluno_id_item = self.table_alunos.item(row, 1).text()  # Use o ID oculto da coluna 1
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM alunos WHERE id = %s", (aluno_id_item,))
                    resultado = cursor.fetchone()
                    if resultado:
                        self.aluno_id = resultado[0]  # Armazenar ID do aluno
                        self.input_nome.setText(resultado[1])
                        self.input_cpf.setText(resultado[2])
                        self.input_nota1.setText(str(resultado[3]))
                        self.input_nota2.setText(str(resultado[4]))
                        self.input_nota3.setText(str(resultado[5]))
                        self.tabs.setCurrentIndex(0)  # Voltar para a aba de cadastro para edição
                    conn.close()
                break

    # Função para apagar aluno
    def apagar_aluno(self):
        for row in range(self.table_alunos.rowCount()):
            checkbox = self.table_alunos.cellWidget(row, 0)
            if checkbox.isChecked():
                aluno_id_item = self.table_alunos.item(row, 1).text()  # Use o ID da coluna oculta
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM alunos WHERE id = %s", (aluno_id_item,))
                    conn.commit()
                    conn.close()
                self.carregar_alunos()
                QMessageBox.information(self, "Sucesso", "Aluno apagado com sucesso!")
                break

    # Função para limpar os campos após cadastro
    def limpar_campos(self):
        self.input_nome.clear()
        self.input_cpf.clear()
        self.input_nota1.clear()
        self.input_nota2.clear()
        self.input_nota3.clear()
        self.aluno_id = None  # Resetar ID após limpar

if __name__ == "__main__":
    create_table()

    app = QApplication(sys.argv)
    window = AlunoApp()
    window.show()
    sys.exit(app.exec_())
