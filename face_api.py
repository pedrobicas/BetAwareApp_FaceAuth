from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import os
import tempfile
import shutil

app = Flask(__name__)
CORS(app)

USER_FACES_PATH = os.path.join(os.getcwd(), "user_faces")

if not os.path.exists(USER_FACES_PATH):
    os.makedirs(USER_FACES_PATH)
    with open(os.path.join(USER_FACES_PATH, "placeholder.txt"), "w") as f:
        f.write("Placeholder")

print("--- SERVIÇO DE AUTENTICAÇÃO FACIAL (FLUXO SEGURO) INICIANDO ---")
print(f"Banco de dados de rostos em: {USER_FACES_PATH}")

# O ENDPOINT DE CADASTRO CONTINUA O MESMO E ESTÁ CORRETO
@app.route('/api/register-face', methods=['POST'])
def register_face():
    username = request.form.get('username')
    file = request.files.get('file')

    if not username or not file:
        return jsonify({"success": False, "message": "Nome de usuário e arquivo são obrigatórios."}), 400

    file_extension = os.path.splitext(file.filename)[1]
    save_path = os.path.join(USER_FACES_PATH, f"{username.lower()}{file_extension}")
    
    file.save(save_path)
    
    # Remove o arquivo de representações antigas para forçar o DeepFace a reanalisar
    representations_path = os.path.join(USER_FACES_PATH, "representations_vgg_face.pkl")
    if os.path.exists(representations_path):
        os.remove(representations_path)
    
    print(f"Rosto do usuário '{username}' cadastrado com sucesso.")
    return jsonify({"success": True, "message": "Rosto cadastrado com sucesso!"})

# ENDPOINT DE LOGIN CORRIGIDO PARA VERIFICAÇÃO 1-PARA-1
@app.route('/api/face-login', methods=['POST'])
def face_login():
    username = request.form.get('username')
    file = request.files.get('file')

    if not username or not file:
        return jsonify({"success": False, "message": "Nome de usuário e arquivo de imagem são obrigatórios."}), 400

    print(f"Recebida tentativa de login facial para o usuário: '{username}'")

    # Encontra a imagem de referência para este usuário específico (ex: "lucas_vassao.jpg")
    reference_img_path = None
    for ext in ['.jpg', '.jpeg', '.png']:
        path_to_check = os.path.join(USER_FACES_PATH, f"{username.lower()}{ext}")
        if os.path.exists(path_to_check):
            reference_img_path = path_to_check
            break
    
    if not reference_img_path:
        return jsonify({"success": False, "message": "Nenhum rosto cadastrado para este usuário."})

    # Salva a imagem enviada em um arquivo temporário
    temp_dir = tempfile.gettempdir()
    temp_img_path = os.path.join(temp_dir, file.filename)
    file.save(temp_img_path)

    try:
        # USA DeepFace.verify para uma comparação 1-para-1
        print(f"Verificando se o rosto enviado corresponde ao de '{username}'...")
        result = DeepFace.verify(
            img1_path=reference_img_path, 
            img2_path=temp_img_path,
            model_name='VGG-Face',
            enforce_detection=False
        )

        os.remove(temp_img_path)

        if result.get('verified'):
            print(f"--- SUCESSO DE AUTENTICAÇÃO: O rosto corresponde ao usuário '{username}'.")
            return jsonify({"success": True, "message": "Login Facial Bem-sucedido!", "user_name": username})
        else:
            print(f"--- FALHA DE AUTENTICAÇÃO: O rosto NÃO corresponde ao usuário '{username}'.")
            return jsonify({"success": False, "message": "Rosto não corresponde ao do usuário cadastrado."})

    except Exception as e:
        print(f"--- ERRO CRÍTICO DURANTE A VERIFICAÇÃO: {e}")
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        return jsonify({"success": False, "message": "Erro ao processar a imagem."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)