.PHONY: run
run:
	cd src/ && brew services start redis && uvicorn main:app --reload