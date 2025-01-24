from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://silverline.it-pin.ch/"}})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask API. Use /calculate-kpis to POST your data."})

@app.route('/calculate-kpis', methods=['POST'])
def calculate_kpis():
    try:
        data = request.json
        
        # Extract and convert values to numbers (using float to handle decimals)
        bank = float(data.get('bank', 0))
        depot = float(data.get('depot', 0))
        agh = float(data.get('agh', 0))
        s3a = float(data.get('sa3', 0))
        efh = float(data.get('efh', 0))
        loan = float(data.get('loan', 0))
        credit = float(data.get('credit', 0))
        mortgage = float(data.get('mortgage', 0))
        other_debt = float(data.get('otherDebt', 0))
        
        # Calculate Liquidität (Liquidity)
        liquidity = bank + depot + agh + s3a + efh
        
        # Calculate Schuldenquote (Debt Ratio)
        total_debt = loan + credit + mortgage + other_debt
        if liquidity == 0:
            debt_ratio = 0  # Prevent division by zero
        else:
            debt_ratio = total_debt / liquidity
        
        # Return the results
        return jsonify({
            'Liquidität': liquidity,
            'Schuldenquote': debt_ratio,
            'message': 'Deine Privatbilanz wurde erfolgreich analysiert!'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
