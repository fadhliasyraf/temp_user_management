from proj import intial_app
import os
app = intial_app(os.getenv('ENVIRONMENT', 'development'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)

