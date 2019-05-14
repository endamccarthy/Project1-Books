from core import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


""" 
To run this app using flask enviromnet variables type the following in the command line:

> export FLASK_APP=run.py
> export FLASK_DEBUG=1 (for debug mode)
> flask run

If we wanted to run the app directly instead of using the environment variables we can use the following code:

if __name__ == '__main__':
    app.run(debug=True)

The command line argument for the above will be 'python3 run.py'.  
"""