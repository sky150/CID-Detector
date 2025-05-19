install:
	pip install -r requirements.txt

test:
	pytest tests/ 

run:
	uvicorn src.backend.api:app --reload & \
	streamlit run src/frontend/app.py

docker-build:
	docker build -t cid-detector .
	
docker-run:
	docker run -p 8000:8000 -p 8501:8501 --add-host=host.docker.internal:host-gateway cid-detector

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 