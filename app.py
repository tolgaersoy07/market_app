from flask import Flask,request,render_template
from routes import register_blueprints
from config import SECRET_KEY
from token_services import get_email_from_token,token_control,get_user_type

app=Flask(__name__)
app.config['SECRET_KEY']=SECRET_KEY
register_blueprints(app)

@app.route('/')
def index():
    return render_template('index.html')

OUT_LIST= [
    "index", "login", "forgotten_password", "register",
    "login_validate", "logout", "static" , "access_token_validate","set_cookie","reset_password"]


@app.before_request
def before_request():
    if request.endpoint is None:
        return render_template('404.html')
    if request.path=="/":
        return None
    for item in OUT_LIST:
        if item in request.path:
            return None

    result=token_control()
    if result['valid']:
        user_type=get_user_type(get_email_from_token("Bearer "+result['token']))
        if (user_type=="user" and "admin" in request.path) or (user_type=="admin" and "admin" not in request.path):
            return render_template('403.html')
        return None

    return render_template('400.html')

if __name__ == '__main__':
    app.run(debug=True)