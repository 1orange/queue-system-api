
# queue-system-api

This repo is just API part of my bachelor thesis.

Simple API system for queue management.

Current version is suitable for retail, banks, doctors' offices, etc.
## Features

- Join queue
- Preview queue


## Documentation

Swagger is hosted on [http://localhost:5000/](http://localhost:5000/)


## Deployment

To deploy this project use docker container.

## API Reference

### Get queue order number

#### Endpoint
```http
  GET /client
```

#### Response
```json
{
  "id": "string",
  "order_number": 0,
  "timestamp": "string"
}
```

### Get queue status

#### Endpoint
```http
  GET /status
```

#### Response
```json
{
  "clients": [
    {
      "id": "string",
      "order_number": 0,
      "timestamp": "string"
    }
  ],
  "queue_size": 0
}
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@JeanDossaTsimbazafy](https://www.github.com/1orange)
