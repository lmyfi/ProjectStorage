import axios from 'axios';

export default axios.create({
    baseURL: 'https://f938-223-104-61-124.ngrok-free.app',
    headers: {"ngrok-skip-browser-warning": "true"}
});
