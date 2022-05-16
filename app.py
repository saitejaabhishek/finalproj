from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == "POST":
        file_name = request.form['timelogfile']
        try:
            with open(file_name, "r") as f:
                total_time_spend = 0
                for line in f:
                    if line.find("Time Log:") == 0:
                        continue
                    if 'am' not in line.lower() and 'pm' not in line.lower():
                        continue
                    start_time = datetime.strptime(line.split('-')[0].strip()[-7:].lower().strip(), '%I:%M%p')
                    end_time = datetime.strptime(line.split('-')[1][1:8].lower().strip(), '%I:%M%p')
                    time_spend = end_time - start_time
                    total_time_spend = total_time_spend + (time_spend.seconds / 60)
               
                return render_template('index.html',
                                    file_name = file_name.split('.')[0],
                                    result='{:02d} hours {:02d} minutes'.format(*divmod(int(total_time_spend), 60)))
        except FileNotFoundError:
            error = "Sorry, Choose TimeLog data file."
            return render_template('index.html', file_not_found_error = error)

if __name__ == '__main__':
    app.run(debug=True)
