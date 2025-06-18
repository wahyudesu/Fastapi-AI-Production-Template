<h1 align="center">Fastapi AI Production Boilerplate</h1>

## FAQ

<details>
    <summary><strong>Why FastAPI?</strong></summary>
    <ul>
        <li>FastAPI is a modern, high-performance web framework for building APIs with Python. For AI apps, it serves as the interface between your AI models and the outside world, allowing external systems to send data to your models and receive predictions or processing results. What makes FastAPI particularly appealing is its simplicity and elegance—it provides everything you need without unnecessary complexity.</li>
    </ul>
</details>

<details>
    <summary><strong>What is Uvicorn?</strong></summary>
    <ul>
        <li>Uvicorn is a lightning-fast ASGI server implementation for Python, commonly used to run FastAPI applications in production. It enables asynchronous request handling and is well-suited for modern web frameworks.</li>
    </ul>
</details>

<details>
    <summary><strong>Is this boilerplate connected to a database?</strong></summary>
    <ul>
        <li>You can add a database such as PostgreSQL, MySQL, or SQLite depending on your use case. If you are only serving models, a database may not be necessary. This repository is designed to be as simple as possible so users can get started quickly.</li>
    </ul>
</details>

<details>
    <summary><strong>How about security?</strong></summary>
    <ul>
        <li>The project includes built-in security features such as API endpoint protection, authentication, and rate limiting. You can further enhance security by configuring environment variables and using HTTPS in production.</li>
    </ul>
</details>

<details>
    <summary><strong>What can I develop with this?</strong></summary>
    <ul>
        <li>It depends on your project use case. For serving AI or ML models, this boilerplate is more than sufficient. If you need more features, you can add observability and monitoring tools such as Opik, Comet, or MLflow.</li>
    </ul>
</details>
