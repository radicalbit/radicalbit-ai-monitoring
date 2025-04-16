import { notificationErrorJson, notificationSuccessJson } from '@Helpers/notificationUtils';
import { actions as notificationActions } from '@State/notification';
import { isFulfilled, isRejectedWithValue } from '@reduxjs/toolkit';

const { setNotificationMessage } = notificationActions;

const errorWhiteList = {
  inferSchema: 404,
  getTraceLatencies: true,
  getSessionLatencies: true,
  getSpanLatencies: true,
  addNewApiKey: true,
};

const successWhiteList = {};

export const rtkQueryErrorLogger = ({ dispatch }) => (next) => (action) => {
  if (!isRejectedWithValue(action)) {
    return next(action);
  }

  if (action?.payload?.data) {
    console.error(action?.payload?.data);
  }

  const endpointName = action?.meta?.arg?.endpointName;
  const status = action?.payload?.status;

  if (endpointName && status && (errorWhiteList[endpointName] || errorWhiteList[endpointName]?.[status])) {
    return next(action);
  }

  const showNotification = action?.payload && status;

  if (showNotification) {
    const error1 = action.payload?.data?.message;
    const error2 = action.payload?.data?.error?.message; // likes models-repo errors
    const error3 = action.payload?.data;
    const message = error1 || error2 || error3 || 'generic error';
    const notificationMessage = notificationErrorJson({ status, message });

    dispatch(setNotificationMessage(notificationMessage));
  }

  return next(action);
};

export const rtkQueryMutationSuccessLogger = ({ dispatch }) => (next) => (action) => {
  const endpointName = action?.meta?.arg?.endpointName;

  if (endpointName && successWhiteList[endpointName]) {
    return next(action);
  }

  const showNotification = isFulfilled(action)
    && action?.meta?.arg?.type === 'mutation'
    && action?.meta?.arg?.originalArgs
    && action.meta.arg.originalArgs.successMessage;

  if (showNotification) {
    const message = action.meta?.arg?.originalArgs?.successMessage;
    const notificationMessage = notificationSuccessJson(message);
    dispatch(setNotificationMessage(notificationMessage));
  }

  return next(action);
};
