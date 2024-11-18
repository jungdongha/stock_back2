import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(code, period='1y'):
    """주식 데이터를 가져오는 함수"""
    try:
        # 한국 주식의 경우 '.KS' 접미사 추가
        ticker = f"{code}.KS"
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return None
        
        return df
    except Exception as e:
        print(f"Error fetching stock data for {code}: {e}")
        return None

def cal_increase(code, interval='monthly'):
    """주가 상승률을 계산하는 함수"""
    try:
        # 주식 데이터 가져오기
        df = get_stock_data(code)
        
        if df is None or df.empty:
            return None
            
        # 월별/주별 데이터로 리샘플링
        if interval == 'monthly':
            df_resampled = df.resample('M').last()
        else:  # weekly
            df_resampled = df.resample('W').last()
            
        # 가격 변화 계산
        df_resampled['Increase'] = df_resampled['Close'].diff()
        df_resampled['Increase_Rate'] = df_resampled['Close'].pct_change() * 100
        
        return df_resampled
    except Exception as e:
        print(f"Error calculating increase for {code}: {e}")
        return None

def cal_data(code):
    """주식 분석 데이터를 계산하는 함수"""
    try:
        # 기본 주식 데이터 가져오기
        df = get_stock_data(code)
        
        if df is None or df.empty:
            return {"error": "Failed to fetch stock data"}
            
        # 월별 데이터 계산
        df_monthly = cal_increase(code, interval='monthly')
        
        if df_monthly is None:
            return {"error": "Failed to calculate monthly data"}
            
        # 주별 데이터 계산
        df_weekly = cal_increase(code, interval='weekly')
        
        if df_weekly is None:
            return {"error": "Failed to calculate weekly data"}
            
        # 최근 데이터 추출
        latest_monthly = df_monthly.iloc[-1]
        latest_weekly = df_weekly.iloc[-1]
        
        return {
            "monthly": {
                "increase": float(latest_monthly['Increase']),
                "increase_rate": float(latest_monthly['Increase_Rate'])
            },
            "weekly": {
                "increase": float(latest_weekly['Increase']),
                "increase_rate": float(latest_weekly['Increase_Rate'])
            },
            "current_price": float(df['Close'].iloc[-1])
        }
    except Exception as e:
        print(f"Error in cal_data for {code}: {e}")
        return {"error": f"Analysis failed: {str(e)}"}

def predict_increase(code):
    """주가 상승 예측 함수"""
    try:
        df = get_stock_data(code)
        if df is None or df.empty:
            return {"error": "Failed to fetch stock data"}
            
        # 간단한 예측 로직 (예시)
        last_price = float(df['Close'].iloc[-1])
        avg_price = float(df['Close'].mean())
        
        return {
            "prediction": last_price > avg_price,
            "confidence": 0.6  # 임시 신뢰도
        }
    except Exception as e:
        print(f"Error predicting increase for {code}: {e}")
        return {"error": f"Prediction failed: {str(e)}"}

def get_stock_code(keyword):
    """주식 종목 코드 검색 함수"""
    # 실제 구현에서는 데이터베이스나 API를 통해 검색
    # 예시 데이터
    sample_stocks = {
        "삼성전자": "005930",
        "SK하이닉스": "000660",
        "NAVER": "035420"
    }
    
    results = {}
    for name, code in sample_stocks.items():
        if keyword.lower() in name.lower():
            results[name] = code
            
    return results
