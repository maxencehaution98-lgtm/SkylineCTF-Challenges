from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESGI - Ping Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo {
            font-size: 14px;
            color: #667eea;
            font-weight: bold;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        
        h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #333;
            font-weight: 500;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result-box {
            background: #f5f5f5;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }
        
        .result-box h2 {
            color: #333;
            font-size: 18px;
            margin-bottom: 15px;
        }
        
        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 13px;
            line-height: 1.5;
        }
        
        .back-link {
            display: inline-block;
            margin-top: 15px;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .back-link:hover {
            color: #764ba2;
        }
        
        .hint {
            text-align: center;
            margin-top: 20px;
            padding: 10px;
            background: #fff3cd;
            border-radius: 5px;
            font-size: 12px;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">ESGI</div>
            <h1>🌐 Network Ping Tool</h1>
            <p class="subtitle">Diagnostic réseau - Challenge CTF</p>
        </div>
        
        {% if result %}
        <div class="result-box">
            <h2>📊 Résultat du Ping</h2>
            <pre>{{ result }}</pre>
            <a href="/" class="back-link">← Nouvelle requête</a>
        </div>
        {% else %}
        <form method="GET" action="/ping">
            <div class="form-group">
                <label for="ip">Adresse IP ou hostname :</label>
                <input type="text" name="ip" id="ip" placeholder="Ex: 8.8.8.8" required>
            </div>
            <button type="submit">🚀 Lancer le Ping</button>
        </form>
        <div class="hint">
            💡 Astuce : Cette application pourrait avoir des failles de sécurité...
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(TEMPLATE, result=None)

@app.route('/ping')
def ping():
    ip = request.args.get('ip', '')
    cmd = f"ping -c 1 {ip}"
    output = ""
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    
    return render_template_string(TEMPLATE, result=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

