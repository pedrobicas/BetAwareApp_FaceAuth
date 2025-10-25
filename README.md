# BetAware - Backend de Autenticação Facial

Este é o backend do sistema BetAware responsável pela autenticação facial dos usuários. O serviço utiliza tecnologias de deep learning para reconhecimento facial e fornece uma API REST para cadastro e login de usuários através de suas faces.

## 📋 Visão Geral

O backend de autenticação facial é construído com Flask e utiliza a biblioteca DeepFace para processamento de reconhecimento facial. O sistema permite:

- **Cadastro de usuários** através de fotos faciais
- **Login seguro** usando reconhecimento facial
- **Armazenamento local** de dados biométricos
- **API REST** para integração com aplicações frontend

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Flask** - Framework web para API REST
- **DeepFace** - Biblioteca de reconhecimento facial
- **OpenCV** - Processamento de imagens
- **TensorFlow/Keras** - Modelos de deep learning
- **NumPy & Pandas** - Manipulação de dados
- **Flask-CORS** - Suporte a CORS para requisições cross-origin

## 📁 Estrutura do Projeto

```
BetAwareApp_FaceAuth/
├── face_api.py              # API principal do serviço
├── temp.py                  # Script de teste de dependências
├── user_faces/              # Diretório de armazenamento das faces
│   ├── bryan.jpeg          # Exemplo de face cadastrada
│   └── *.pkl               # Arquivos de representação do DeepFace
├── venv/                   # Ambiente virtual Python
│   └── requirements.txt    # Dependências do projeto
├── dlib-19.24.2.*          # Biblioteca dlib para detecção facial
└── *.jpg, *.jpeg           # Imagens de teste
```

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Webcam ou câmera (para captura de imagens)

### Passo a Passo

1. **Clone ou baixe o projeto**
   ```bash
   cd BetAwareApp_FaceAuth
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r venv/requirements.txt
   ```

4. **Instale o dlib (se necessário)**
   ```bash
   pip install dlib-19.24.2-cp311-cp311-win_amd64.whl
   ```

5. **Execute o servidor**
   ```bash
   python face_api.py
   ```

O servidor estará disponível em `http://localhost:5000`

## 📡 API Endpoints

### 1. Cadastro de Face
**POST** `/api/register-face`

Cadastra uma nova face no sistema.

**Parâmetros:**
- `username` (form-data): Nome do usuário
- `file` (form-data): Arquivo de imagem da face

**Exemplo de uso:**
```bash
curl -X POST http://localhost:5000/api/register-face \
  -F "username=joao" \
  -F "file=@foto_joao.jpg"
```

**Resposta de sucesso:**
```json
{
  "success": true,
  "message": "Rosto cadastrado com sucesso!"
}
```

### 2. Login Facial
**POST** `/api/face-login`

Autentica um usuário através do reconhecimento facial.

**Parâmetros:**
- `file` (form-data): Arquivo de imagem para autenticação

**Exemplo de uso:**
```bash
curl -X POST http://localhost:5000/api/face-login \
  -F "file=@foto_login.jpg"
```

**Resposta de sucesso:**
```json
{
  "success": true,
  "message": "Login Facial Bem-sucedido!",
  "user_name": "joao"
}
```

**Resposta de falha:**
```json
{
  "success": false,
  "message": "Rosto não reconhecido."
}
```

## 🔧 Configuração

### Variáveis de Ambiente

O sistema utiliza as seguintes configurações padrão:
- **Host:** `0.0.0.0` (aceita conexões de qualquer IP)
- **Porta:** `5000`
- **Diretório de faces:** `./user_faces`

### Modelo de Reconhecimento

O sistema utiliza o modelo **VGG-Face** do DeepFace, que oferece:
- Alta precisão no reconhecimento
- Boa performance em diferentes condições de iluminação
- Suporte a múltiplos formatos de imagem

## 🛡️ Segurança

- As imagens são processadas localmente
- Não há envio de dados biométricos para serviços externos
- Arquivos temporários são automaticamente removidos
- CORS configurado para permitir integração segura

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de importação do dlib**
   ```
   Solução: Instale o arquivo .whl fornecido:
   pip install dlib-19.24.2-cp311-cp311-win_amd64.whl
   ```

2. **Erro "No face detected"**
   ```
   Solução: Certifique-se de que a imagem contém uma face visível
   e bem iluminada. O parâmetro enforce_detection=False ajuda
   com imagens de baixa qualidade.
   ```

3. **Erro de memória com TensorFlow**
   ```
   Solução: Reduza o tamanho das imagens ou reinicie o serviço
   periodicamente para liberar memória.
   ```

4. **Porta 5000 já em uso**
   ```
   Solução: Altere a porta no arquivo face_api.py:
   app.run(host='0.0.0.0', port=5001)
   ```

### Teste de Dependências

Execute o script de teste para verificar se todas as bibliotecas estão funcionando:
```bash
python temp.py
```

## 📊 Logs e Monitoramento

O sistema gera logs detalhados no console:
- Inicialização do serviço
- Cadastros realizados
- Tentativas de login (sucesso/falha)
- Erros críticos

## 🤝 Integração com Frontend

Para integrar com aplicações frontend (React Native, Web, etc.):

1. Configure CORS adequadamente
2. Use FormData para envio de imagens
3. Trate as respostas JSON adequadamente
4. Implemente feedback visual para o usuário

## 📝 Notas de Desenvolvimento

- O sistema remove automaticamente arquivos de representação antigos para garantir atualizações
- Suporte a múltiplos formatos de imagem (JPG, JPEG, PNG)
- Processamento assíncrono para melhor performance
- Estrutura preparada para escalabilidade

## 📄 Licença

Este projeto faz parte do sistema BetAware e está sujeito às políticas de uso da aplicação principal.

---

**Desenvolvido para o projeto BetAware - Sistema de Apostas Responsáveis**