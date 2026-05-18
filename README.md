# Sentiment-Enhanced Algorithmic Trading

This repository contains the implementation for a thesis project on integrating financial news sentiment into algorithmic trading using transformer-based natural language processing.

## Implemented pipeline

1. Collect daily ticker-specific RSS news  
2. Run FinBERT sentiment inference  
3. Aggregate article sentiment into daily sentiment signals  
4. Collect recent OHLCV market data  
5. Merge sentiment signals with market data  
6. Run baseline SMA and sentiment-enhanced SMA experiments  
7. Export generated trade tables  
8. Compute performance metrics  
9. Build cross-sectional strategy summaries  

## Repository structure

- `src/` - source code  
- `config/` - configuration files  
- `requirements.txt` - dependencies  
- `.gitignore` - excludes generated data and local files  

## Generated Files

The following files are generated when running the pipeline and are **not included in the repository**:

- `data/` - raw RSS news, processed sentiment data, merged datasets, trade tables, and metrics  
- `outputs/` - optional figures, logs, and analysis outputs  
- `*.csv` - generated trade tables, metrics, and summary results  
- `*.png` - generated plots and visualizations  

## Notes

This repository focuses on a reproducible end-to-end pipeline. Generated trade tables, performance summaries, and figures are outputs of the pipeline and are excluded from version control.