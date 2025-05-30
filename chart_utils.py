import plotly.graph_objects as go

def show_stock_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'],
                                 name='K線'))

    fig.add_trace(go.Scatter(x=df.index, y=df['SMA5'], line=dict(width=1), name='SMA5'))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], line=dict(width=1), name='SMA20'))

    fig.update_layout(title=f"{symbol} 技術圖", xaxis_rangeslider_visible=False)
    return fig
