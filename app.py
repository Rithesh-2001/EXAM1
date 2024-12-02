from flask import Flask, render_template, request, redirect, url_for, flash ,send_file
import os
from database import insert_user,insert_request,tounix,fetch_request,is_valid,delete_request,get_time
from sql_connection import get_sql_connection
from block import store_hash,retrive_hash

connection = get_sql_connection()





question_papers = []

requests_data = {
    'teacher1': ['REQ001', 'REQ002'],  # Example: teacher1 has two requests
    'teacher2': ['REQ003']  # Example: teacher2 has one request
}

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    return render_template('login.html')  # Renders your login page

@app.route('/login', methods=['POST'])
def login():
    role = request.form['role']
    username = request.form['username']
    password = request.form['password']

    if is_valid(connection,username,role,password) :
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher_dashboard', username=username))
        elif role == 'superintendent':
            return redirect(url_for('superintendent_dashboard'))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('index'))
    
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/submit_paper', methods=['POST'])
def submit_paper():
    teacher_id = request.form['teacherId']
    paper_code = request.form['paperCode']
    release_date = request.form['releaseDate']
    release_date = tounix(release_date)

    flash('Question Paper Submitted Successfully!')
    print("######33/n",question_papers)
    insert_request(connection,paper_code,release_date,teacher_id)
    return redirect(url_for('admin_dashboard'))

@app.route('/add_user', methods=['POST'])
def add_user():
    user_id = request.form['userId']
    password = request.form['password']
    role = request.form['role']
    insert_user(connection,user_id,role,password)
    flash(f'User {user_id} with role {role} added successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/teacher_dashboard/<username>')
def teacher_dashboard(username):
    # Check if there are any requests for the teacher
    teacher_requests = fetch_request(connection,username)
    print('techer' ,teacher_requests)
    return render_template('teacher_dashboard.html', requests=teacher_requests, username=username)

@app.route('/upload/<username>/<req_id>', methods=['POST'])
def upload_file(username, req_id):
    # Handle file upload for the specific teacher and request ID
    if 'pdfFile' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['pdfFile']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and file.filename.endswith('.pdf'):
        # Save the PDF file
        filename = f"{username}_{req_id}.pdf"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        hash = '0xbluhhhh'
        release_time = get_time(connection,req_id)
        print('datetime',release_time)
        store_hash(req_id,hash,release_time)
        
        # After upload, remove the request
        delete_request(connection,req_id,username)
        
        flash(f'PDF for request {req_id} uploaded successfully!')
        return redirect(url_for('teacher_dashboard', username=username))

    flash('Invalid file format. Please upload a PDF.')
    return redirect(url_for('teacher_dashboard', username=username))

# Superintendent dashboard
@app.route('/superintendent_dashboard')
def superintendent_dashboard():
    return render_template('superintendent_dashboard.html')

@app.route('/fetch_pdf/<unique_code>')
def fetch_pdf(unique_code):
    # Call the retrieve_hash function to get the result
    print(type(unique_code))
    result = retrive_hash(unique_code)  
    print('Result is:', result)

    # Check if the result is not None, meaning the paper is released
    if result is not None:
        # Assuming the filename is constructed dynamically based on the unique_code
        filename = 't1_2223.pdf'  # or based on the result, depending on how you're storing files
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if the file exists in the uploads folder
        if os.path.exists(file_path):
            # Send the file to the front end for download
            return send_file(file_path, as_attachment=True)
        else:
            flash('Question paper file not found on the server.')
            return "Error: File not found.", 404
    else:
        # Notify the user that the question paper has not been released yet
        flash('The question paper for the given code has not been released yet.')
        return "Error: Question paper not released yet.", 400
if __name__ == '__main__':
    app.run(debug=True)