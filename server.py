import flask
from flask import request, jsonify
import DataProcess 

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''Home'''

#Extrai o Json inteiro
@app.route('/audience', methods=['GET'])
def fetch_All_programs():
    return jsonify(dict_final)

'''
    validar se o parametro recebido pelo request do cliente está correto, 
    É utilizado dentro das funções.
'''
def returnRequestsArgs(arg):
    if arg in request.args:    
        return request.args[arg]
    else:
        return None   

'''
    Recebe parametros de requisição program_code e signal 
    e retorna um objeto Json gerado pelo método DataProcess.fetch_by_program_signal
'''
@app.route('/audience/fetch_by_program_signal/')
def fetch_by_program_signal_():
    signal = returnRequestsArgs('signal')
    program = returnRequestsArgs('program')
    
    if (program != None) & (signal != None):
        #Busca sinal e programa
        result_dict = DataProcess.fetch_by_program_signal(DataProcess.dfFinal, signal, program)
        
    return jsonify(result_dict)


'''
    Recebe data inicial e data final como parametros de requisição para buscar um periodo especifico
    dentro do Dataframe. Ao final retorna um objeto Json gerado pelo método DataProcess.fetch_signal_program_by_date
'''
@app.route('/audience/fetch_signal_program_by_date/')
def fetch_signal_program_by_date_():
    initial_date = returnRequestsArgs('initial_date')
    final_date = returnRequestsArgs('final_date')
    
    if (initial_date != None) & (final_date != None):
        #Busca sinal e programa
        result_dict = DataProcess.fetch_signal_program_by_date(DataProcess.dfFinal, initial_date, final_date)
        
    return jsonify(result_dict)

'''
@app.route('/audience/fetch_by_signal/')
def fetch_by_signal_():
    signal = returnRequestsArgs('signal')
    if signal != None:
        result_dict = DataProcess.fetch_by_signal(DataProcess.dict_final, signal)             
    return jsonify(result_dict)

@app.route('/audience/fetch_by_program_code/')
def fetch_by_program_code_():
    program_code = returnRequestsArgs('program_code')
    if program_code != None:
        result_dict = DataProcess.fetch_program(DataProcess.dict_final, program_code)             
    return jsonify(result_dict)
'''

app.run()


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    

