# Camera-Traps-Wild-Life-Dashboard

**Main Application Repository**: [https://github.com/pietro-foini/agentic-chatbot](https://github.com/pietro-foini/camera-traps-wild-life).

Hello there! 😀

A dashboard for the Camera Traps Wildlife project, providing an interface to explore and monitor wildlife camera-trap data.

## Getting Started

You can run this project locally either using **Docker Compose** (for a quick containerized setup) or through a 
**Manual Setup** directly on your host machine.

### Manual Setup

This project requires Python 3.11 or 3.12 and relies on Poetry for dependency management.

```bash
poetry install
```

#### Running the Application

With **PostgreSQL** and **SeaweedFS** running in the background (running the main application project), start the 
application, running the `api.debug.py` file.

The Application will be available at http://localhost:8050.

### Docker Setup

If you prefer running the entire stack in containers, run the entire pipeline with a single command:

```bash
docker compose up --build
```

Note on defaults: your environment file must be named `.env` in the project root.

Once the containers are running:

- The Application will be available at http://localhost:8050.

> [!NOTE]
> Before launching the application you have to be launched the main application project with Docker as well.

## License

MIT

## Contacts

If you have any questions regarding the project, feel free to get in touch.

Email: pietro.foini1@gmail.com
