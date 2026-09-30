from flask import Flask, render_template, request
import pickle
import numpy as np

# setup application
app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'        # model eka load kirima
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])          # api dipu values  predict kirima- scikit-learn library install kra gata yutui predict use kirimt
    return pred_value

@app.route('/', methods=['POST', 'GET'])   # method ekk
def index():
    # return "Hello World"
    pred_value = 0                            #submit kre nathi avastavata pred_value ekk yaviya yutu nisa
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen') #check box eka tic kloth element 1k list ekk(['on']) labe.nathnm empty list([]) ekk labe
        ips = request.form.getlist('ips')

        #print(ram,weight,company,typename,opsys,cpu,gpu,touchscreen,ips)
        
        feature_list = []   # list ekk hadima

        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['linux','mac','other','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']

        # for item in company_list:
        #     if item == company:
        #         feature_list.append(1)
        #     else:
        #         feature_list.append(0)

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse_list(company_list, company)
        traverse_list(typename_list, typename)
        traverse_list(opsys_list, opsys)
        traverse_list(cpu_list, cpu)
        traverse_list(gpu_list, gpu)

        #print(feature_list)
    
        pred_value = prediction(feature_list)
        #print(pred_value)
        pred_value = np.round(pred_value[0],2)*380     #pred_value eka 1D list ekk vidiyt enne- [20000] vage
                                                       #eka nathi kirimt eke 0 index ekt call krai
                                                       # decimal point 2kta blai

    return render_template('index.html', pred_value=pred_value) #html web page eka access kirima


if __name__ == '__main__':          #condition eka hari nm app eka run kranna kiyl dei
    app.run(debug=True)