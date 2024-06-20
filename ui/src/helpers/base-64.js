import { Buffer } from 'buffer';

export const encode = (data) => Buffer.from(JSON.stringify(data), 'utf8').toString('base64');

export const decode = (data) => Buffer.from(data, 'base64').toString('utf8');
