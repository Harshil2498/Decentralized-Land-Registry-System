@echo off
echo Setting up Land Registry System...

:: Verify Node.js (for Ganache)
node --version || (echo Install Node.js from nodejs.org && exit /b)

:: Activate virtual environment
call venv\Scripts\activate

:: Install Python dependencies
pip install streamlit web3 py-solc-x requests

:: Start Ganache with persistent state
start "Ganache" cmd /k ganache-cli --db ganache_data

:: Wait for services
timeout /t 10

:: Run Streamlit
streamlit run app.py