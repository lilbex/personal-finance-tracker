
import axios, { AxiosResponse, AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';


const client = axios.create({
    baseURL: 'https://api.github.com',
  });
  