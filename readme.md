# Real-Time Market Data Engineering & Analytics Platform

This project is an end-to-end Data Engineering and BI platform for ingesting, processing, modeling, and visualizing stock market data.

## Architecture

Market Data APIs  
→ Python Batch and Streaming Ingestion  
→ Kafka / Redpanda  
→ AWS S3 Raw Zone  
→ Databricks Bronze, Silver, Gold Layers  
→ Snowflake Analytics Warehouse  
→ dbt Transformations  
→ Power BI Dashboard  

## Current Progress

### Day 1
- Created project repository structure
- Created Python virtual environment
- Installed ingestion dependencies
- Built historical stock price ingestion pipeline using yfinance
- Stored raw stock market data as CSV in the raw data zone