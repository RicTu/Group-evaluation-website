from website import create_app
from flask_ngrok import run_with_ngrok

app = create_app()
# run_with_ngrok(app)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)
    # app.run()
