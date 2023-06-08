import uvicorn


if __name__ == '__main__':
    # Start the backend server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        log_level='info',
        access_log=False,
        reload=True
    )
