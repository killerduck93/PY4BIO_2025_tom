# dna_reverse_complement.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def reverse_complement():
    if request.method == 'POST':
        input_sequence = request.form['dna_sequence']
        reversed_complement = reverse_complement_sequence(input_sequence)
        return render_template('result_rev_comp.html', input_sequence=input_sequence, reversed_complement=reversed_complement)
    return render_template('index_rev_comp.html')

def reverse_complement_sequence(sequence):
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement_dict.get(base, base) for base in reversed(sequence))

if __name__ == '__main__':
    app.run()

