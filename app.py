from config import app,server,db
from dash import Dash,html
from controllers.auth import auth
from controllers.transact import transact

server.register_blueprint(auth)
server.register_blueprint(transact)

if __name__== '__main__':
    with server.app_context():
        db.create_all()
    app.run_server(debug=True)