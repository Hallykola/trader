def close_order(mt5,position):
    # create a close request
    position_id=position.ticket
    price=mt5.symbol_info_tick(position.symbol).bid
    deviation=20
    if position.type == mt5.ORDER_TYPE_BUY:
        type = mt5.ORDER_TYPE_SELL
    else:
        type = mt5.ORDER_TYPE_BUY
    request={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": position.symbol,
        "volume": position.volume,
        "type": type,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK  
    }
    # send a trading request "magic": 234000, #mt5.ORDER_FILLING_RETURN,
    result=mt5.order_send(request)
    print(result)