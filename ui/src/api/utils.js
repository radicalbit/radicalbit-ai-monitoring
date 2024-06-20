import axios from 'axios';

export const customBaseQuery = () => async ({
  baseUrl, url, method, data, headers = {},
}) => {
  try {
    const result = await axios({
      url: `${baseUrl}${url}`,
      method,
      data,
      headers,
    });

    if (result.headers['x-total-count'] !== undefined) {
      return {
        data: {
          items: result.data,
          xTotalCount: +result.headers['x-total-count'],
        },
      };
    }

    return { data: result.data };
  } catch (axiosError) {
    const err = axiosError;

    return {
      error: { status: err.response?.status, data: err.response?.data },
    };
  }
};
