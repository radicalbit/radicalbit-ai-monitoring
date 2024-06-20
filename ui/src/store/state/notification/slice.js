import { createSlice } from '@reduxjs/toolkit';
import { NotificationEnum } from './constants';

const initialState = {
  showMessage: false,
  message: {
    type: NotificationEnum.INFO,
    title: '',
    content: '',
    duration: 0,
  },
  showBox: false,
  box: {
    type: null,
    key: null,
    message: '',
    description: '',
    placement: 'topRight',
    duration: 0,
  },
};

export const notificationSlice = createSlice({
  name: 'notification',
  initialState,
  reducers: {
    setNotificationMessage: (state, { payload }) => ({
      ...state,
      showMessage: true,
      message: payload,
    }),

    resetNotificationMessage: (state) => ({
      ...state,
      showMessage: false,
      message: initialState.message,
    }),

    setNotificationBox: (state, { payload }) => ({
      ...state,
      showBox: true,
      box: payload,
    }),

    resetNotificationBox: (state) => ({
      ...state,
      showMessage: false,
      box: initialState.box,
    }),
  },
});

export const { actions } = notificationSlice;

export default notificationSlice.reducer;
