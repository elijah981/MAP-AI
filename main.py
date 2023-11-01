from flask import Flask
from routes.user_routes import user_blueprint
from routes.step1_routes import step1_blueprint
from routes.step2_routes import step2_blueprint
from routes.step3_routes import step3_blueprint
from routes.step4_routes import step4_blueprint
from routes.home_routes import home_blueprint

app = Flask(__name__)
app.secret_key = "thisisalongstatement4asecretkey"
app.register_blueprint(home_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(step1_blueprint)
app.register_blueprint(step2_blueprint)
app.register_blueprint(step3_blueprint)
app.register_blueprint(step4_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
