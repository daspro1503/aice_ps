from flask import Flask,jsonify
app =Flask(__name__)
@app.route('/api/v1/create_redflag')
