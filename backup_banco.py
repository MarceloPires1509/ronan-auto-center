import os
import shutil
import datetime
import glob

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
BACKUP_DIR = os.path.expanduser('~/backups_oficina')
MAX_BACKUPS = 15  # Manter os últimos 15 dias de backup

def realizar_backup():
    if not os.path.exists(DB_PATH):
        print(f"Banco de dados não encontrado em: {DB_PATH}")
        return

    # Criar diretório de backups se não existir
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Diretório de backups criado em: {BACKUP_DIR}")

    # Gerar nome do arquivo com data e hora
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_filename = f"backup_db_{data_atual}.sqlite3"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    # Copiar o arquivo
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup realizado com sucesso: {backup_filename}")

    # Limpar backups antigos
    limpar_backups_antigos()

def limpar_backups_antigos():
    # Listar todos os arquivos de backup ordenados por data de modificação (mais antigos primeiro)
    arquivos = glob.glob(os.path.join(BACKUP_DIR, 'backup_db_*.sqlite3'))
    arquivos.sort(key=os.path.getmtime)

    # Se tiver mais que o limite, apaga os mais antigos
    if len(arquivos) > MAX_BACKUPS:
        arquivos_para_apagar = arquivos[:-MAX_BACKUPS]
        for arquivo in arquivos_para_apagar:
            try:
                os.remove(arquivo)
                print(f"Backup antigo removido: {os.path.basename(arquivo)}")
            except Exception as e:
                print(f"Erro ao remover {arquivo}: {e}")

if __name__ == '__main__':
    print("Iniciando rotina de backup...")
    realizar_backup()
    print("Rotina finalizada.")
