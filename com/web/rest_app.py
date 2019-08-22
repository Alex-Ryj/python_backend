import connexion
from flask_cors import CORS

app = connexion.FlaskApp(__name__, specification_dir='python_backend/')
app.add_api('rest_api.yaml')
CORS(app.app)
app.run(port=8080)
