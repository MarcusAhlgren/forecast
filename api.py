from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/predict', methods = ["GET", "POST"])
def predict():
    model = joblib.load('models/sarima.pkl')
    
    params = {}
    if "steps" in request.args:
        params["steps"] = int(request.args.get("steps"))
    if "start" in request.args:
        params["start"] = str(request.args.get("start"))
    if "end" in request.args:
        params["end"] = str(request.args.get("end"))
    
    
    start_date = str(request.args.get("start"))
    end_date = str(request.args.get("end"))
    
    preds = np.round(model.pred(**params))
    predictions = dict(zip(preds.index.strftime('%Y-%m-%d'), preds.values))
    
    return predictions

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
#curl -X POST "http://127.0.0.1:5000/predict?start=2020-02-01&end=2020-05-01"