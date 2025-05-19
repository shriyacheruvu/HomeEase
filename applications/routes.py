
from flask import render_template, request, session,flash,redirect,url_for
from main import app
import os
from applications.models import *
from datetime import datetime

app.config['SERVICER_FILE'] = 'static/servicer_files'
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)

        if not email or not password:
            flash('Please enter email and password')
            return render_template('login.html')  
             
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User does not exist')
            return render_template('login.html')
            
        if user.password != password:
            flash('Incorrect password')
            return render_template('login.html')
                       
        session['user_email'] = user.email
        session['user_role'] = user.roles[0].name
        
        if 'customer' in session['user_role']:
            if user.customer:
                session['customer_id']=user.customer[0].id              
            return redirect(url_for('customer_dashboard'))
        
        if 'admin' in session['user_role']:
            return redirect(url_for('admin_dashboard'))
        
        if 'servicer' in session['user_role']:
            if user.servicer:
                session['servicer_id']=user.servicer[0].id
            return redirect(url_for('servicer_dashboard'))
        
        flash('Login successful')

        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_role', None)
    flash('Logged out')
    return render_template('home.html')

@app.route('/register_customer', methods=['GET','POST'])
def register_customer():
    if request.method == 'GET':
        return render_template('register_customer.html') 
    
    if request.method == 'POST':
        name = request.form.get('name',None)
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        confirmpassword = request.form.get('confirmpassword',None)
        address = request.form.get('address',None)
        state = request.form.get('state',None)
        pincode = request.form.get('pincode',None)
        phone=request.form.get('phone',None)

        if not name or not email or not password or not confirmpassword  or not address or not state or not pincode :
            flash('Please enter all fields')
            return render_template('register_customer.html')
        
        if password != confirmpassword:
            flash('Passwords do not match')
            return render_template('register_customer.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return render_template('register_customer.html')
        
        if len(pincode) != 6:
            flash('Pincode must be 6 characters long')
            return render_template('register_customer.html')
        if phone and (len(phone)) !=10:
            flash('Phone number must be 10 characters long')
            return render_template('register_customer.html')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists')
            return render_template('register_customer.html')
        
        customer_role = Role.query.filter_by(name='customer').first()
        if not customer_role:
            flash("Role 'customer' does not exist")
            return redirect(url_for('register_customer'))
               
        user = User(name=name,
                    email= email,
                    password = password,
                    address = address,
                    state=state,
                    pincode=pincode,
                    phone=phone)
        user.roles.append(customer_role)
        db.session.add(user)
        db.session.commit()
        customer = Customer(user_id=user.id)
        db.session.add(customer)
        db.session.commit()
        flash('User registered successfully')
        return redirect('/login')

@app.route('/register_servicer', methods=['GET','POST'])    
def register_servicer():
    if request.method == 'GET':
        services=Service.query.all()
        return render_template('register_servicer.html',services=services) 
    
    if request.method == 'POST':
        name=request.form.get('name',None)
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        confirmpassword = request.form.get('confirmpassword',None)
        service_id=request.form.get('service_id',None)
        address = request.form.get('address',None)
        state = request.form.get('state',None)
        pincode = request.form.get('pincode',None)
        phone = request.form.get('phone',None)
        experience= request.form.get('experience',None)
        doc_path = None
        doc_file = request.files.get('doc_path',None)
        
        if not name or not email or not password or not confirmpassword  or not service_id or not address or not state or not pincode or not experience or not doc_file:
            flash('Please enter all fields')
            return render_template('register_servicer.html')
        
        if password != confirmpassword:
            flash('Passwords do not match')
            return render_template('register_servicer.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return render_template('register_servicer.html')
        
        if len(pincode) != 6:
            flash('Pincode must be 6 characters long')
            return render_template('register_servicer.html')
        if phone and (len(phone)) !=10 :          
            flash('Phone number must be 10 characters long')
            return render_template('register_servicer.html')
        
        if doc_file and doc_file.filename:
            servicer_file_path = app.config['SERVICER_FILE']
            if not os.path.exists(servicer_file_path):
                os.makedirs(servicer_file_path)
            doc_filename = doc_file.filename
            doc_path = os.path.join('servicer_files', doc_filename).replace(os.sep, '/') 
            file_doc_path = os.path.join(servicer_file_path, doc_filename)  
            doc_file.save(file_doc_path)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists')
            return render_template('register_servicer.html')
        
        servicer_role = Role.query.filter_by(name='servicer').first()
        if not servicer_role:
            flash("Role 'servicer' does not exist")
            return redirect(url_for('register_servicer'))
        
        user = User(name=name,
                    email= email,
                    password = password,
                    address = address,
                    state=state,
                    pincode=pincode,
                    phone=phone)
        user.roles.append(servicer_role)
        db.session.add(user)       
        db.session.commit()

        servicer = Servicer(
                user_id=user.id,
                service_id=service_id,
                experience=experience,
                doc_path=doc_path)
        db.session.add(servicer)
        db.session.commit() 

        flash('User registered successfully')
        return redirect('/login')
    
@app.route('/add_service', methods=['GET','POST'])
def add_service():
    if request.method == 'GET':
        return render_template('add_service.html')
    
    if request.method == 'POST':
        name = request.form.get('name',None)
        description = request.form.get('description',None)
        base_price = request.form.get('base_price',None)

        if not name:
            flash('Please enter service name')
            return render_template('add_service.html')
        if not base_price:
            flash('Please enter price')
            return render_template('add_service.html')
        
        service = Service.query.filter_by(name=name).first()
        if service:
            flash('Service already exists')
            return render_template('add_service.html')
        
        service = Service(name=name, description=description,base_price=base_price)
        db.session.add(service)
        db.session.commit()

        flash('Service added successfully')
        return redirect(url_for('admin_dashboard')) 
    
@app.route('/admin_dashboard', methods=['GET','POST'])
def admin_dashboard():
    if request.method == 'GET':
        services = Service.query.all()
        servicers=Servicer.query.all()
        requests=NewServiceRequest.query.all()
               
        return render_template('admin_dashboard.html',services=services,servicers=servicers,requests=requests)
    
@app.route('/servicer/<int:servicer_id>', methods=['GET', 'POST'])
def servicer_details(servicer_id):
    servicer = Servicer.query.get(servicer_id)
    if request.method == 'POST':
        action = request.form.get('action', None)
        
        if action == 'approve' or action == 'unblock':
            servicer.ver_doc = 'Approved'
        elif action == 'reject':
            servicer.ver_doc = 'Rejected'
        elif action == 'block':
            servicer.ver_doc = 'Blocked'
        
        db.session.commit()
        flash(f"Servicer status updated to {servicer.ver_doc}")
        return redirect(url_for('servicer_details', servicer_id=servicer_id))  
    return render_template('servicer_details.html',servicer=servicer)

@app.route('/customer_dashboard', methods=['GET','POST'])
def customer_dashboard():
    if request.method == 'GET':
        services = Service.query.all()
        service_requests=ServiceRequest.query.all()
        
        return render_template('customer_dashboard.html',services=services,service_requests=service_requests)

@app.route('/add_new_service_request', methods=['GET','POST'])
def add_new_service_request():
    if request.method == 'GET':
        return render_template('add_new_service_request.html')
    
    if request.method == 'POST':
        customer_id = session.get('customer_id')
        
        new_service_name = request.form.get('new_service_name',None)
        new_service_description= request.form.get('new_service_description',None)
        request_date = datetime.now()

        if not new_service_name:
            flash('Please enter service name')
            return render_template('add_new_servicerequest.html')
             
        service = Service.query.filter_by(name=new_service_name).first()
        if service:
            flash('Service already exists')
            return render_template('add_new_service_request.html')
        
        new_service = NewServiceRequest( customer_id=customer_id,
                                    new_service_name=new_service_name,
                                    new_service_description=new_service_description,
                                    request_date=request_date,
                                    status='Pending')
        db.session.add(new_service)
        db.session.commit()

        flash('Service requested submitted successfully')
        return redirect(url_for('customer_dashboard')) 
    
@app.route('/edit_service/<int:id>',methods=['GET','POST'])
def edit_service(id):
    service = Service.query.get(id)
    if not service:
        flash('Service does not exist')
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('edit_service.html', service=service)
    
    if request.method == 'POST':
        name = request.form.get('name',None)
        description = request.form.get('description',None)
        base_price=request.form.get('base_price',None)
        service.name = name
        service.description = description
        service.base_price = base_price
        db.session.commit()

        flash('Service updated successfully')
        return redirect(url_for('admin_dashboard'))
    
@app.route('/delete_service/<int:id>', methods=['POST'])
def delete_service(id):
    service = Service.query.get(id)
    if not service:
        flash('Service does not exist')

    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully')
    return redirect(url_for('admin_dashboard'))
 
@app.route('/add_service_request', methods=['GET', 'POST'])
def add_service_request():
    if request.method == 'GET':
        services = Service.query.all() 
        return render_template('add_service_request.html', services=services)
    
    if request.method == 'POST':
        customer_id = session.get('customer_id')
        service_id = request.form.get('service_id', None)
        request_date = datetime.now()
        status = 'Open'
        if not service_id:
            flash('Please select a service')
            services = Service.query.all()
            return render_template('add_service_request.html', services=services)

        service_request = ServiceRequest(
            customer_id=customer_id,
            service_id=service_id,
            request_date=request_date,
            status=status)
        db.session.add(service_request)
        db.session.commit()

        flash('Service request added successfully')
        return redirect(url_for('customer_dashboard'))

@app.route('/edit_service_request/<int:request_id>', methods=['GET', 'POST'])
def edit_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    
    if request.method == 'GET':
        services = Service.query.all()
        return render_template('edit_service_request.html', service_request=service_request, services=services)
    
    if request.method == 'POST':
        service_request.service_id = request.form.get('service_id', service_request.service_id)
        service_request.status = request.form.get('status', service_request.status)
        service_request.completion_date = datetime.now() if service_request.status == 'Closed' else None

        db.session.commit()

        flash('Service request updated successfully')
        return redirect(url_for('customer_dashboard'))
    
@app.route('/close_service_request/<int:request_id>', methods=['POST'])
def close_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    service_request.status = 'Closed'
    service_request.completion_date = datetime.now()

    db.session.commit()

    flash('Service request closed successfully')
    return redirect(url_for('customer_dashboard'))

@app.route('/approve_new_service/<int:request_id>', methods=['POST'])
def approve_new_service(request_id):
    request = NewServiceRequest.query.get(request_id)
    if not request:
        flash('Service request not found')
        return redirect(url_for('admin_dashboard'))
    
    request.status = 'Approved'
    db.session.commit()
    flash('Service request approved')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_new_service/<int:request_id>', methods=['POST'])
def reject_new_service(request_id):
    request = NewServiceRequest.query.get(request_id)
    if not request:
        flash('Service request not found')
        return redirect(url_for('admin_dashboard'))
    
    request.status = 'Rejected'
    db.session.commit()
    flash('Service request rejected')
    return redirect(url_for('admin_dashboard'))

@app.route('/servicer_dashboard', methods=['GET', 'POST'])
def servicer_dashboard():
    servicer_id = session.get('servicer_id')
    servicer =Servicer.query.get(servicer_id)
    if request.method == 'GET': 
        service_requests=ServiceRequest.query.all()
        reviews=Review.query.all()
        return render_template('servicer_dashboard.html',service_requests=service_requests,reviews=reviews,servicer=servicer)

@app.route('/accept_service_request/<int:request_id>', methods=['POST'])
def accept_service_request(request_id):
    request = ServiceRequest.query.get(request_id)
    servicer_id = session.get('servicer_id') 
    if not request:
        flash('Service request not found')
        return redirect(url_for('admin_dashboard'))
    request.servicer_id = servicer_id
    request.status = 'Accepted'
    db.session.commit()
    flash('Service request accepted')
    return redirect(url_for('servicer_dashboard'))

@app.route('/reject_service_request/<int:request_id>', methods=['POST'])
def reject_service_request(request_id):
    request = ServiceRequest.query.get(request_id)
    if not request:
        flash('Service request not found')
        return redirect(url_for('admin_dashboard'))
    
    request.status = 'Rejected'
    db.session.commit()
    flash('Service request rejected')
    return redirect(url_for('servicer_dashboard'))

@app.route('/complete_service_request/<int:request_id>', methods=['POST'])
def complete_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    service_request.status = 'Completed'
    service_request.completion_date = datetime.now()

    db.session.commit()

    flash('Service request completed successfully')
    return redirect(url_for('servicer_dashboard'))

@app.route('/review_servicer/<int:request_id>', methods=['GET', 'POST'])
def review_servicer(request_id):
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        flash('Service request not found')
        return redirect(url_for('servicer_dashboard'))
    
    if request.method == 'POST':
        rating = int(request.form.get('rating', None))
        review = request.form.get('review', None)
        if not rating:
            flash('Please give your rating')
            return render_template('review_servicer.html')
        
        review = Review(
            customer_id=service_request.customer_id,
            servicer_id=service_request.servicer_id,
            service_request_id=request_id,
            rating=rating,
            review=review)
        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully', 'success')
        return redirect(url_for('customer_dashboard'))
    
    return render_template('review_servicer.html', service_request=service_request)


@app.route('/customer_search', methods=['GET'])
def customer_search():
    query = request.args.get('query', None)  
    if not query:
        flash('Please enter in search')
    else:
        services = Service.query.filter(Service.name.ilike(f'%{query}%')).all()
    
    return render_template('customer_search.html', services=services)

@app.route('/admin_search', methods=['GET'])
def admin_search():
    query = request.args.get('query', None)    
    if not query:
        flash('Please enter in search')
    
    servicers = Servicer.query.join(User).filter(User.name.ilike(f'%{query}%')).all()

    return render_template('admin_search.html', servicers=servicers)
