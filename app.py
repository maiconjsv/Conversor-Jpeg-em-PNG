#importando flask e o render_template
from flask import Flask, render_template, request, send_file
from PIL import Image
import os

#iniciando o flask  
app = Flask(__name__)

#pasta de upload
UPLOAD_FOLDER = 'temp_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#cria uma pasta de upload caso não exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    

#criando uma rota
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/link1')
def link1():
    return render_template('link1.html')

@app.route('/converter', methods=['POST'])
def converter():
    if 'imagem_original' not in request.files:
        return "Nenhum arquivo enviado", 400
    
    file = request.files['imagem_original']

    #se o nome do arquivo for vazio
    if file.filename == '': 
        return "Nenhum arquivo selecionado", 400
    
    if file:
        # pega a extensão do arquivo
        originl_ext = file.filename.rsplit('.', 1)[1].lower()
        if originl_ext not in ['jpg', 'jpeg']:
            return 'Por favor, somente jpgs', 400
        
        #salva o arquivo temporariamente
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)
    
        try:
            with Image.open(temp_path) as img:
                #define novo caminho para imagem png
                nome_base = os.path.splitext(os.path.basename(temp_path))[0]
                png_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{nome_base}.png')            
                #salva o arquivo em imagem png
                img.save(png_path, 'PNG')
                #devolve o arquivo pro user
                return send_file(png_path, as_attachment=True, download_name=f'{nome_base}.png')
        except Exception as e:
            return f'Erro ao processar o arquivo: {e}', 500
        finally:
            #limpar arquivos temporarios
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(png_path):
                os.remove(png_path)
            





if __name__ == '__main__':
    app.run(debug=True)



