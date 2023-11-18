import streamlit as st

def is_hammer(open_price, high_price, low_price, close_price):
    # Define the criteria for a hammer
    # The lower shadow should be at least twice the real body
    # The real body is small
    real_body_threshold = (high_price - low_price) * 0.2
    real_body = abs(close_price - open_price)
    lower_shadow = open_price - low_price if close_price > open_price else close_price - low_price
    
    # The upper shadow should be very small or non-existent
    upper_shadow = high_price - close_price if close_price > open_price else high_price - open_price
    
    is_bullish_hammer = (lower_shadow >= 3 * real_body) and (real_body <= real_body_threshold) and (upper_shadow < lower_shadow * 0.25)
                        # and (upper_shadow <= real_body)   
    
    return is_bullish_hammer

def is_shooting_star(open_price, high_price, low_price, close_price):
    # Define the criteria for a shooting star
    # The upper shadow should be at least twice the real body
    # The real body is small
    real_body_threshold = (high_price - low_price) * 0.2
    real_body = abs(close_price - open_price)
    upper_shadow = high_price - (max(open_price, close_price))
    
    # The lower shadow should be very small or non-existent
    lower_shadow = (min(open_price, close_price)) - low_price
    
    st.write(upper_shadow, lower_shadow, real_body)
    is_shooting_star = (upper_shadow >= 3.0 * real_body) and (real_body <= real_body_threshold) and (lower_shadow < upper_shadow * 0.25)
                        # and (lower_shadow <= real_body)
    
    return is_shooting_star
