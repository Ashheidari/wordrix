# Wordrix Project

Wordrix is a project that integrates a neural network-based backend with a client interface. This repository contains two main directories: `server` and `client`.

## Folder Structure

- **server**
  - **model.py**  
    Responsible for building and desinging the neural networks and saving the model.
  - **model-notebook.ipynb**  
    An exact copy of `model.py`, provided for those who want to review the neural network codebase interactively.
  - **extract-dataset.ipynb**  
    Used for web scraping data necessary for the project.
  - **app**  
    Responsible for managing our api endpoints.
  - **utils.py**  
    Contains code to create and populate the database.
- **client**  
  Contains the client-side code and necessary configurations.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) must be installed on your machine.

### Running the Server

1. **Clone the Repository**  
   Clone the entire codebase to your local machine.
2. **Navigate to the Server Folder**  
   ```bash
   cd server
    ```
    - you need to create your environment variable here in .env file
3. **Start the Server Containers**
    ```bash
    docker compose up -d
    ```
4. **Access the API Container**
    ```bashe
    docker exec -it wordrix-api sh
    ```
5. **Initialize the Database**
    - Inside the container, run:
    ```bash
    python utils.py
    ```
### Running the Client
1. **Navigate to the Server Folder**  
   ```bash
   cd client
    ```
2. **Start the Server Containers**
    ```bash
    docker compose up -d
    ```

## Additional Information
- The model-notebook.ipynb file is provided as a convenience for those who prefer to work in a notebook environment.
- The extract-dataset.ipynb file is designed to automate the process of web scraping data for the project.
## Contributing
- Contributions are welcome! Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss your ideas.