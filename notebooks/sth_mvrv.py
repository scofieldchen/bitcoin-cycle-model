import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from pathlib import Path

    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    return Path, go, make_subplots, pd


@app.cell
def _(Path, pd):
    # 数据目录
    data_dir = Path("/Users/scofield/projects/bitcoin-cycle-model/data/strategy/")

    # 读取周期指标
    mvrv_file = data_dir / "sth_mvrv.csv"
    mvrv = pd.read_csv(mvrv_file, index_col="date", parse_dates=True)
    mvrv

    # 读取交易历史记录
    trades_file = data_dir / "lowpass_reverse_h1_v2_trd.csv"
    trades = pd.read_csv(trades_file)
    trades.head()
    return mvrv, trades


@app.cell
def _(trades):
    trades_btc = (
        trades.query("Asset == 'BTCUSDT'")
        .groupby(["Open"])
        .agg(
            {
                "Open": "last",
                "Close": "last",
                "Entry": "last",
                "Exit": "last",
                "Profit": "sum",
            }
        )
    )
    trades_btc
    return (trades_btc,)


@app.cell
def _(go, make_subplots, mvrv, pd, trades_btc):
    # 创建分层图表
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        subplot_titles=["BTC Price", "MVRV", "Momentum"],
        vertical_spacing=0.05,
    )

    # 第一行：btc 价格
    fig.add_trace(
        go.Scatter(x=mvrv.index, y=mvrv["btc"], mode="lines", name="BTC Price"),
        row=1,
        col=1,
    )

    # 第二行: MVRV
    fig.add_trace(
        go.Scatter(x=mvrv.index, y=mvrv["mvrv"], mode="lines", name="MVRV"),
        row=2,
        col=1,
    )
    fig.add_hline(
        y=1.2, row=2, col=1, line_color="grey", line_width=1, line_dash="dot"
    )
    fig.add_hline(
        y=1.0, row=2, col=1, line_color="grey", line_width=1, line_dash="dot"
    )
    fig.add_hline(
        y=0.9, row=2, col=1, line_color="grey", line_width=1, line_dash="dot"
    )

    # 第三行: MVRV 动量
    colors = ["green" if val > 0 else "red" for val in mvrv["momentum"]]
    fig.add_trace(
        go.Bar(
            x=mvrv.index,
            y=mvrv["momentum"],
            marker_color=colors,
            name="Momentum",
        ),
        row=3,
        col=1,
    )

    # 将历史交易添加到价格图表
    # 使用线条连接开盘和收盘价格的线条
    # 根据盈亏决定颜色：盈利绿色，亏损红色

    trades_btc["Open"] = pd.to_datetime(trades_btc["Open"])
    trades_btc["Close"] = pd.to_datetime(trades_btc["Close"])

    for index, trade in trades_btc.iterrows():
        color = "green" if trade["Profit"] > 0 else "red"
        fig.add_trace(
            go.Scatter(
                x=[trade["Open"], trade["Close"]],
                y=[trade["Entry"], trade["Exit"]],
                mode="lines",
                line=dict(color=color, width=2),
                showlegend=False,  # 隐藏个体图例
                hoverinfo="skip",  # 隐藏交易线条的悬停信息
            ),
            row=1,
            col=1,
        )

    # 更新图表样式
    fig.update_layout(
        title="BTC Price, MVRV, and Momentum with Trades",
        height=800,
        hovermode="x unified",
        showlegend=False,
    )

    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="BTC Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="MVRV", row=2, col=1)
    fig.update_yaxes(title_text="Momentum", row=3, col=1)

    fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
