from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Routes
@app.route('/')
def home():
    return render_template('index.html')  # main site

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    product = request.form.get('product')
    quantity = request.form.get('quantity')

    if name and phone and address and product and quantity:
        # Save to Excel
        filename = 'data/orders.xlsx'
        new_data = pd.DataFrame([{
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Name': name,
            'Phone': phone,
            'Address': address,
            'Product': product,
            'Quantity': quantity
        }])

        try:
            if os.path.exists(filename):
                old_data = pd.read_excel(filename)
                combined = pd.concat([old_data, new_data], ignore_index=True)
            else:
                combined = new_data

            combined.to_excel(filename, index=False)
            return redirect(url_for('success'))

        except Exception as e:
            return f"Failed to save order: {e}"

    return "Invalid form data", 400

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
