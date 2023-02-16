from flask import Flask, render_template, request # Importa o Flask e o render_template
import speech_recognition as sr     # Importa o speech_recognition

app = Flask(__name__) # Instancia o Flask

@app.route('/') # Define a rota
def index(): # Define a função
    return render_template('index.html') # Renderiza o template

@app.route('/', methods=['POST']) # Define a rota
def process(): # Define a função
    rec = sr.Recognizer() # Instancia o Recognizer
    cpf_comum = ""
    with sr.Microphone() as mic: # Define o microfone como fonte de áudio
        rec.adjust_for_ambient_noise(mic) # Ajusta o ruído ambiente
        audio = rec.listen(mic) # Grava a fala

    try: # Tenta reconhecer a fala
        cpf = rec.recognize_google(audio, language='pt-BR', show_all=True) # Reconhece a fala

        # Deixa o cpf apenas com números, tira os pontos, traços, espaços e letras
        if len(cpf) > 0:
            for i in cpf['alternative']:
                cpf = i['transcript'].replace(".", "").replace("-", "").replace(" ", "").replace("um", "1").replace("dois", "2").replace("três", "3").replace("quatro", "4").replace("cinco", "5").replace("seis", "6").replace("sete", "7").replace("oito", "8").replace("nove", "9").replace("zero", "0")
                print(cpf)
                if len(cpf) == 11:
                    cpf_comum = cpf
                    break

            cpf = cpf_comum
            cpf_formatado = "{}.{}.{}-{}".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]) # Coloca o ponto e o traço no CPF
        
        if cpf_formatado != "" and len(cpf_formatado) == 14:
            return render_template('index.html', cpf=cpf_formatado) # Renderiza o template
        else:
            return render_template('index.html', error='Desculpe, não consegui reconhecer o CPF')
    
    except sr.UnknownValueError: # Caso não consiga reconhecer a fala
        return render_template('index.html', error='Desculpe, não consegui reconhecer o CPF') # Renderiza o template
    
    except sr.RequestError as e: # Caso não consiga se conectar ao Google
        return render_template('index.html', error=f"Não foi possível processar a sua solicitação: {e}") # Renderiza o template

if __name__ == '__main__':
    app.run(debug=True)
