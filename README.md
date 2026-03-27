# Sentiment-Enhanced Algorithmic Trading

This repository contains the implementation for a thesis project on integrating financial news sentiment into algorithmic trading using transformer-based natural language processing.

## Planned pipeline

1. Collect daily OHLCV market data
2. Collect ticker-specific RSS financial news
3. Filter and preprocess news articles
4. Run FinBERT sentiment inference
5. Aggregate article-level sentiment into daily signals
6. Merge sentiment signals with market data
7. Run baseline and sentiment-augmented backtests
8. Export trade tables
9. Compute performance metrics and plots
10. Run forward paper-trading validation

## Repository structure

- `src/` - source code
- `config/` - configuration files
- `data/` - raw and processed data
- `outputs/` - generated figures, tables, and logs
- `tests/` - tests
- `notebooks/` - exploratory notebooks