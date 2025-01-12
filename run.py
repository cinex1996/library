from app import create_app, db

app = create_app()

# Ensure 'index.html' is in /templates
with app.app_context():
    db.create_all()

def main():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()
