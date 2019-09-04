from flask import Flask, render_template
import creditscore

app = Flask(__name__)
@app.route('/', methods=["GET","POST"])
def indexing():
    return render_template ('homepage.html')          
if __name__ == "__main__":
    app.run(debug=True)
                
            
