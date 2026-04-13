@echo on
call venv\Scripts\activate
python -m uvicorn main:app --reload
pause