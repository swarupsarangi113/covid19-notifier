from flask import Flask,render_template,request
from main_script import main_function


# instantiated Flask application in this app variable
app = Flask(__name__)

# creating route for home page
@app.route('/',methods = ['GET','POST'])
def home_page() :

	if request.method == 'POST' :	
		name = ' '.join([i.capitalize() for i in request.form.get('name').capitalize().split()])
		email = request.form.get('email').lower()
		state = ' '.join([i.capitalize() for i in request.form.get('state').split() if i != 'and'])
		district = ' '.join([i.capitalize() for i in request.form.get('district').split() if i != 'and'])

		try :
		# calling the main function from the covid_script.py to get in the inputs and send email
			main_function(name,email,state,district)

			return render_template('thankyou.html',name=name.split()[0],state=state,district=district)
		except :
			return render_template('invalid.html')


	return render_template('home.html')


if __name__ == '__main__' :

	app.run(debug=True)