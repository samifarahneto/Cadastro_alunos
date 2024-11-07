import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QMainWindow, QHeaderView, QFrame
from PyQt5.QtGui import QFont, QColor
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
        self.setGeometry(100, 100, 1000, 500)  # Largura 1000px, altura 500px

        # Variável para armazenar o ID do aluno selecionado
        self.aluno_id = None

        # Layout principal com duas colunas
        self.main_layout = QHBoxLayout()
        main_widget = QWidget(self)
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

        # Criar o layout de cadastro à esquerda
        self.layout_cadastro = QVBoxLayout()

        # Botão de Novo Aluno (sem ícone)
        self.button_adicionar_aluno = QPushButton("+ Novo Aluno")
        self.button_adicionar_aluno.setStyleSheet("font-size: 14px;")
        self.button_adicionar_aluno.clicked.connect(self.limpar_campos)

        # Labels e entradas com estilos personalizados
        self.label_nome = QLabel("Nome:")
        self.label_nome.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nome = QLineEdit(self)
        self.input_nome.setFixedHeight(30)
        self.input_nome.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")

        self.label_cpf = QLabel("CPF:")
        self.label_cpf.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_cpf = QLineEdit(self)
        self.input_cpf.setPlaceholderText("000.000.000-00")  # Placeholder com formato visível
        self.input_cpf.setFixedHeight(30)
        self.input_cpf.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")
        self.input_cpf.textChanged.connect(self.formatar_cpf)

        self.label_nota1 = QLabel("Nota Av 1:")
        self.label_nota1.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nota1 = QLineEdit(self)
        self.input_nota1.setFixedHeight(30)
        self.input_nota1.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")

        self.label_nota2 = QLabel("Nota Av 2:")
        self.label_nota2.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nota2 = QLineEdit(self)
        self.input_nota2.setFixedHeight(30)
        self.input_nota2.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")

        self.label_nota3 = QLabel("Nota Av 3:")
        self.label_nota3.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_nota3 = QLineEdit(self)
        self.input_nota3.setFixedHeight(30)
        self.input_nota3.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")

        # Botão de Salvar
        self.button_salvar = QPushButton("Salvar", self)
        self.button_salvar.clicked.connect(self.salvar_aluno)

        # Adicionar widgets ao layout de cadastro
        self.layout_cadastro.addWidget(self.button_adicionar_aluno)  # Adicionando o botão Novo Aluno
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

        # Criar um widget e adicionar o layout nele para a coluna esquerda
        cadastro_widget = QWidget()
        cadastro_widget.setLayout(self.layout_cadastro)

        # Criar o layout de consulta à direita
        self.layout_consulta = QVBoxLayout()

        # Label "Alunos Cadastrados" centralizado
        self.label_alunos = QLabel("Alunos Cadastrados")
        self.label_alunos.setFont(QFont('Arial', 14, QFont.Bold))
        self.label_alunos.setAlignment(Qt.AlignCenter)  # Centralizar o label

        # Campos de Busca
        self.label_busca_nome = QLabel("Buscar por Nome:")
        self.label_busca_nome.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_busca_nome = QLineEdit(self)
        self.input_busca_nome.setFixedHeight(30)
        self.input_busca_nome.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")
        self.input_busca_nome.textChanged.connect(self.filtrar_alunos)

        self.label_busca_cpf = QLabel("Buscar por CPF:")
        self.label_busca_cpf.setFont(QFont('Arial', 10, QFont.Bold))
        self.input_busca_cpf = QLineEdit(self)
        self.input_busca_cpf.setFixedHeight(30)
        self.input_busca_cpf.setStyleSheet("border: 1px solid black; border-radius: 10px; padding: 5px;")
        self.input_busca_cpf.textChanged.connect(self.filtrar_alunos)

        self.table_alunos = QTableWidget()
        self.table_alunos.setColumnCount(7)  # Remove a coluna do rótulo "Selecionar"
        self.table_alunos.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Av 1", "Av 2", "Av 3", "Média"])
        self.table_alunos.setSelectionBehavior(QTableWidget.SelectRows)  # Seleciona a linha inteira
        self.table_alunos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Colunas ajustam-se dinamicamente
        self.table_alunos.cellClicked.connect(self.selecionar_linha)

        # Tornar a coluna de ID oculta
        self.table_alunos.setColumnHidden(0, True)

        # Definir fonte negrito para o cabeçalho
        header_font = QFont('Arial', 10, QFont.Bold)
        for i in range(self.table_alunos.columnCount()):
            self.table_alunos.horizontalHeaderItem(i).setFont(header_font)

        # Ativar a ordenação da tabela pelo cabeçalho (coluna Nome)
        self.table_alunos.setSortingEnabled(True)

        # Botão de Apagar
        self.button_apagar = QPushButton("Apagar", self)
        self.button_apagar.clicked.connect(self.apagar_aluno)

        # Adicionar widgets ao layout de consulta
        self.layout_consulta.addWidget(self.label_alunos)  # Adicionando o label "Alunos Cadastrados"
        self.layout_consulta.addWidget(self.label_busca_nome)
        self.layout_consulta.addWidget(self.input_busca_nome)
        self.layout_consulta.addWidget(self.label_busca_cpf)
        self.layout_consulta.addWidget(self.input_busca_cpf)
        self.layout_consulta.addWidget(self.table_alunos)
        self.layout_consulta.addWidget(self.button_apagar)

        # Criar um widget e adicionar o layout nele para a coluna direita
        consulta_widget = QWidget()
        consulta_widget.setLayout(self.layout_consulta)

        # Adicionar um divisor vertical entre as colunas
        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)
        vertical_line.setFrameShadow(QFrame.Sunken)

        # Adicionar os widgets ao layout principal com proporções 25% para o cadastro e 75% para a consulta
        self.main_layout.addWidget(cadastro_widget)
        self.main_layout.addWidget(vertical_line)
        self.main_layout.addWidget(consulta_widget)

        # Definir as proporções de largura (25% para o cadastro e 75% para a consulta)
        self.main_layout.setStretch(0, 25)  # Cadastro
        self.main_layout.setStretch(1, 0)   # Linha vertical
        self.main_layout.setStretch(2, 75)  # Consulta

        # Carregar dados ao iniciar
        self.carregar_alunos()

    # Função para formatar CPF com a máscara "000.000.000-00"
    def formatar_cpf(self):
        texto = ''.join([c for c in self.input_cpf.text() if c.isdigit()])  # Manter apenas os números
        if len(texto) > 11:  # Limitar a 11 dígitos
            texto = texto[:11]

        # Adicionar a máscara de CPF
        if len(texto) <= 3:
            self.input_cpf.setText(texto)
        elif len(texto) <= 6:
            self.input_cpf.setText(f"{texto[:3]}.{texto[3:]}")
        elif len(texto) <= 9:
            self.input_cpf.setText(f"{texto[:3]}.{texto[3:6]}.{texto[6:]}")
        else:
            self.input_cpf.setText(f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}")

    # Função para selecionar a linha e carregar os dados nos campos
    def selecionar_linha(self, row):
        self.aluno_id = self.table_alunos.item(row, 0).text()  # Captura o ID do aluno
        self.input_nome.setText(self.table_alunos.item(row, 1).text())
        self.input_cpf.setText(self.table_alunos.item(row, 2).text())
        self.input_nota1.setText(self.table_alunos.item(row, 3).text())
        self.input_nota2.setText(self.table_alunos.item(row, 4).text())
        self.input_nota3.setText(self.table_alunos.item(row, 5).text())

    # Função para validar o CPF (verificar se contém exatamente 11 dígitos)
    def validar_cpf(self, cpf):
        cpf_somente_numeros = cpf.replace(".", "").replace("-", "")
        if len(cpf_somente_numeros) != 11:
            QMessageBox.warning(self, "CPF inválido", "O CPF deve conter exatamente 11 dígitos.")
            return False
        return True

    # Função para validar se o nome foi informado
    def validar_nome(self, nome):
        if not nome.strip():
            QMessageBox.warning(self, "Nome não informado", "Por favor, informe o nome.")
            return False
        return True

    # Função para salvar aluno no banco de dados
    def salvar_aluno(self):
        nome = self.input_nome.text()
        cpf = self.input_cpf.text()

        # Validar o nome e o CPF
        if not self.validar_nome(nome):
            return
        if not self.validar_cpf(cpf):
            return

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

    # Função para carregar alunos na tabela e colorir texto de acordo com a média
    def carregar_alunos(self):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, cpf, nota1, nota2, nota3 FROM alunos")
            resultados = cursor.fetchall()
            self.table_alunos.setRowCount(len(resultados))
            for row_num, row_data in enumerate(resultados):
                for col_num, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)  # Centralizar o texto nas colunas
                    self.table_alunos.setItem(row_num, col_num, item)

                # Calcular e exibir a média
                media = (row_data[3] + row_data[4] + row_data[5]) / 3
                media_item = QTableWidgetItem(f"{media:.2f}")
                media_item.setTextAlignment(Qt.AlignCenter)

                # Adicionar o item da média na tabela
                self.table_alunos.setItem(row_num, 6, media_item)

                # Definir cor com base na média
                if media < 6:
                    for col in range(self.table_alunos.columnCount()):
                        item = self.table_alunos.item(row_num, col)
                        if item:  # Certificar que o item não é None
                            item.setForeground(QColor(Qt.red))
                else:
                    for col in range(self.table_alunos.columnCount()):
                        item = self.table_alunos.item(row_num, col)
                        if item:  # Certificar que o item não é None
                            item.setForeground(QColor(Qt.blue))

            conn.close()

    # Função para apagar aluno
    def apagar_aluno(self):
        if self.aluno_id is None:
            QMessageBox.warning(self, "Nenhum aluno selecionado", "Por favor, selecione um aluno para apagar.")
            return

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM alunos WHERE id = %s", (self.aluno_id,))
                conn.commit()
                QMessageBox.information(self, "Sucesso", "Aluno apagado com sucesso!")
                self.carregar_alunos()
                self.limpar_campos()
                self.aluno_id = None  # Resetar ID do aluno
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Erro", f"Erro ao apagar aluno: {err}")
            finally:
                conn.close()

    # Função para limpar os campos após cadastro ou quando o usuário clica em "Novo Aluno"
    def limpar_campos(self):
        self.input_nome.clear()
        self.input_cpf.clear()
        self.input_nota1.clear()
        self.input_nota2.clear()
        self.input_nota3.clear()
        self.aluno_id = None  # Resetar ID após limpar

    # Função para filtrar alunos na tabela
    def filtrar_alunos(self):
        nome_busca = self.input_busca_nome.text().lower()
        cpf_busca = self.input_busca_cpf.text()
        for row in range(self.table_alunos.rowCount()):
            nome_item = self.table_alunos.item(row, 1).text().lower()  # Coluna 1 é o nome
            cpf_item = self.table_alunos.item(row, 2).text()  # Coluna 2 é o CPF
            if nome_busca in nome_item and cpf_busca in cpf_item:
                self.table_alunos.setRowHidden(row, False)
            else:
                self.table_alunos.setRowHidden(row, True)

if __name__ == "__main__":
    create_table()

    app = QApplication(sys.argv)
    window = AlunoApp()
    window.show()
    sys.exit(app.exec_())
