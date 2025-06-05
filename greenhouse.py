import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

data = pd.read_csv('dataset_greenhouse_fuzzy.csv')
print("Data sample:")
print(data.head())

suhu = ctrl.Antecedent(np.arange(0, 51, 1), 'suhu')
kelembaban = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembaban')
pendingin = ctrl.Consequent(np.arange(0, 101, 1), 'pendingin')
penyiram = ctrl.Consequent(np.arange(0, 101, 1), 'penyiram')

suhu['Dingin'] = fuzz.trimf(suhu.universe, [0, 0, 15])
suhu['Hangat'] = fuzz.trimf(suhu.universe, [10, 25, 35])
suhu['Panas'] = fuzz.trimf(suhu.universe, [30, 50, 50])

kelembaban['Rendah'] = fuzz.trimf(kelembaban.universe, [0, 0, 40])
kelembaban['Sedang'] = fuzz.trimf(kelembaban.universe, [30, 50, 70])
kelembaban['Tinggi'] = fuzz.trimf(kelembaban.universe, [60, 100, 100])

pendingin['Rendah'] = fuzz.trimf(pendingin.universe, [0, 0, 50])
pendingin['Sedang'] = fuzz.trimf(pendingin.universe, [30, 50, 70])
pendingin['Tinggi'] = fuzz.trimf(pendingin.universe, [60, 100, 100])

penyiram['Rendah'] = fuzz.trimf(penyiram.universe, [0, 0, 50])
penyiram['Sedang'] = fuzz.trimf(penyiram.universe, [30, 50, 70])
penyiram['Tinggi'] = fuzz.trimf(penyiram.universe, [60, 100, 100])

suhu.view()
kelembaban.view()
pendingin.view()
penyiram.view()
plt.show()

rules = [
    ctrl.Rule(suhu['Dingin'] & kelembaban['Rendah'], pendingin['Rendah']),
    ctrl.Rule(suhu['Dingin'] & kelembaban['Sedang'], pendingin['Rendah']),
    ctrl.Rule(suhu['Dingin'] & kelembaban['Tinggi'], pendingin['Rendah']),
    ctrl.Rule(suhu['Hangat'] & kelembaban['Rendah'], pendingin['Sedang']),
    ctrl.Rule(suhu['Hangat'] & kelembaban['Sedang'], pendingin['Sedang']),
    ctrl.Rule(suhu['Hangat'] & kelembaban['Tinggi'], pendingin['Sedang']),
    ctrl.Rule(suhu['Panas'] & kelembaban['Rendah'], pendingin['Tinggi']),
    ctrl.Rule(suhu['Panas'] & kelembaban['Sedang'], pendingin['Tinggi']),
    ctrl.Rule(suhu['Panas'] & kelembaban['Tinggi'], pendingin['Tinggi']),

    ctrl.Rule(suhu['Dingin'] & kelembaban['Rendah'], penyiram['Tinggi']),
    ctrl.Rule(suhu['Dingin'] & kelembaban['Sedang'], penyiram['Sedang']),
    ctrl.Rule(suhu['Dingin'] & kelembaban['Tinggi'], penyiram['Rendah']),
    ctrl.Rule(suhu['Hangat'] & kelembaban['Rendah'], penyiram['Tinggi']),
    ctrl.Rule(suhu['Hangat'] & kelembaban['Sedang'], penyiram['Sedang']),
    ctrl.Rule(suhu['Hangat'] & kelembaban['Tinggi'], penyiram['Rendah']),
    ctrl.Rule(suhu['Panas'] & kelembaban['Rendah'], penyiram['Tinggi']),
    ctrl.Rule(suhu['Panas'] & kelembaban['Sedang'], penyiram['Tinggi']),
    ctrl.Rule(suhu['Panas'] & kelembaban['Tinggi'], penyiram['Sedang'])
]

sistem_kontrol = ctrl.ControlSystem(rules)
sistem = ctrl.ControlSystemSimulation(sistem_kontrol)

def kontrol_greenhouse(input_suhu, input_kelembaban):
    sistem.input['suhu'] = input_suhu
    sistem.input['kelembaban'] = input_kelembaban
    sistem.compute()
    
    output_pendingin = sistem.output['pendingin']
    output_penyiram = sistem.output['penyiram']
    
    if output_pendingin <= 40:
        kategori_pendingin = "Rendah"
    elif 40 < output_pendingin <= 70:
        kategori_pendingin = "Sedang"
    else:
        kategori_pendingin = "Tinggi"
        
    if output_penyiram <= 40:
        kategori_penyiram = "Rendah"
    elif 40 < output_penyiram <= 70:
        kategori_penyiram = "Sedang"
    else:
        kategori_penyiram = "Tinggi"
    
    return {
        'pendingin': output_pendingin,
        'kategori_pendingin': kategori_pendingin,
        'penyiram': output_penyiram,
        'kategori_penyiram': kategori_penyiram
    }

print("\nEvaluasi dengan data dari dataset:")
for i in range(5):
    sample = data.iloc[i]
    hasil = kontrol_greenhouse(sample['Suhu (°C)'], sample['Kelembaban (%)'])
    print(f"\nSample {i+1}:")
    print(f"Suhu: {sample['Suhu (°C)']}°C ({sample['Kategori Suhu']})")
    print(f"Kelembaban: {sample['Kelembaban (%)']}% ({sample['Kategori Kelembaban']})")
    print(f"Pendingin: {hasil['pendingin']:.2f} ({hasil['kategori_pendingin']})")
    print(f"Penyiram: {hasil['penyiram']:.2f} ({hasil['kategori_penyiram']})")
    print(f"Kategori sebenarnya - Pendingin: {sample['Level Pendingin']}, Penyiram: {sample['Level Penyiram']}")

while True:
    print("\nMasukkan nilai untuk simulasi (atau 'exit' untuk keluar):")
    input_suhu = input("Suhu (°C, 0-50): ")
    if input_suhu.lower() == 'exit':
        break
    input_kelembaban = input("Kelembaban (%, 0-100): ")
    
    try:
        input_suhu = float(input_suhu)
        input_kelembaban = float(input_kelembaban)
        
        if 0 <= input_suhu <= 50 and 0 <= input_kelembaban <= 100:
            hasil = kontrol_greenhouse(input_suhu, input_kelembaban)
            print("\nHasil Sistem Fuzzy:")
            print(f"Pendingin: {hasil['pendingin']:.2f} ({hasil['kategori_pendingin']})")
            print(f"Penyiram: {hasil['penyiram']:.2f} ({hasil['kategori_penyiram']})")
            
            suhu.view(sim=sistem)
            kelembaban.view(sim=sistem)
            pendingin.view(sim=sistem)
            penyiram.view(sim=sistem)
            plt.show()
        else:
            print("Input di luar range yang valid!")
    except ValueError:
        print("Input tidak valid! Masukkan angka.")