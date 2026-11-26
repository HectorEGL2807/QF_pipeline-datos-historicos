import matplotlib.pyplot as plt
import mplfinance as mpf
from pathlib import Path

def plot_chart(df, ticker, output_dir=None, show=True):
    """
    Grafica de la evolución del precio de una acción en el tiempo.
    """

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df.index, df['Adj Close'], linewidth=1.2)

    ax.set_title(f"{ticker} - Precio de Cierre Ajustado en el tiempo")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio (USD)")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_dir / f"{ticker}_chart.png", dpi=150)

    if show:
        plt.show()

    plt.close(fig)

def plot_candle(df, ticker, output_dir=None, show=True, ultimos_dias=251):
    """Grafica de velas japonesas de los ultimos N dias de una accion."""

    data = df.tail(ultimos_dias)  # recorte sin modificar el df original

    fig, axes = mpf.plot(
        data,
        type="candle",
        style="charles",
        title=f"{ticker} - Velas (últimos {len(data)} días)",
        ylabel="Precio (USD)",
        volume=True,
        mav=(3, 6, 9),
        figratio=(12, 6),
        tight_layout=True,
        returnfig=True,
    )

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_dir / f"{ticker}_candle.png", dpi=150)

    if show:
        plt.show()

    plt.close(fig)