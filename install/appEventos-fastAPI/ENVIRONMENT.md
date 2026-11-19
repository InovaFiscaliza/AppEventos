# Ambiente do appEventos FastAPI

O host do deploy precisa de Podman, rede `podman`, portas `9087` e `9088`
disponíveis e diretório `/appEventos` acessível pelo operador.
Execute o deploy como o usuário proprietário dos containers.

O runtime é o container `appEventos-fastAPI`, com Debian 12 e Python em
`/opt/appeventos/venv/bin/python`. O código montado fica em `/appEventos`.
Instalações de dependências pertencem ao build da imagem. Para testar código
da aplicação, use esse interpretador dentro do container; não instale suas
dependências nos containers do RF.Fusion.

A validação estática dos scripts Bash pode ser feita no checkout com `bash -n`.
O build e os testes de integração de NGINX, SSH e FastAPI exigem o host Podman.
